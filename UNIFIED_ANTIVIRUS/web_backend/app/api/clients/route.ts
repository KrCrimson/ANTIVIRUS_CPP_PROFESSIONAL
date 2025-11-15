import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'
import { requireAuth, CORS_HEADERS } from '../../../lib/auth'
import { rateLimit, logRequest } from '../../../lib/middleware'

const prisma = new PrismaClient()

// Función helper para convertir BigInt a string recursivamente
function serializeBigInt(obj: any): any {
  if (obj === null || obj === undefined) {
    return obj
  }
  
  if (typeof obj === 'bigint') {
    return obj.toString()
  }
  
  if (Array.isArray(obj)) {
    return obj.map(serializeBigInt)
  }
  
  if (typeof obj === 'object') {
    const serialized: any = {}
    for (const [key, value] of Object.entries(obj)) {
      serialized[key] = serializeBigInt(value)
    }
    return serialized
  }
  
  return obj
}

// GET /api/clients - Obtener estadísticas detalladas por cliente
export const GET = requireAuth(async (request: NextRequest) => {
  const startTime = Date.now()
  
  // Rate limiting
  const rateLimitResponse = rateLimit({ requests: 100, windowMs: 3600000 })(request)
  if (rateLimitResponse) {
    return rateLimitResponse
  }

  try {
    // Log request for monitoring
    logRequest(request, startTime)
    
    const { searchParams } = new URL(request.url)
    const timeframe = searchParams.get('timeframe') || '24h'
    const limit = parseInt(searchParams.get('limit') || '20')
    
    // Calcular rango de tiempo
    const now = new Date()
    let startDate: Date
    
    switch (timeframe) {
      case '1h':
        startDate = new Date(now.getTime() - (60 * 60 * 1000))
        break
      case '6h':
        startDate = new Date(now.getTime() - (6 * 60 * 60 * 1000))
        break
      case '24h':
        startDate = new Date(now.getTime() - (24 * 60 * 60 * 1000))
        break
      case '7d':
        startDate = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000))
        break
      case '30d':
        startDate = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000))
        break
      default:
        startDate = new Date(now.getTime() - (24 * 60 * 60 * 1000))
    }

    // Obtener estadísticas por cliente
    const clientStats = await prisma.logEntry.groupBy({
      by: ['clientId'],
      where: {
        timestamp: {
          gte: startDate,
          lte: now
        }
      },
      _count: {
        id: true
      },
      _min: {
        timestamp: true
      },
      _max: {
        timestamp: true
      },
      orderBy: {
        _count: {
          id: 'desc'
        }
      },
      take: limit
    })

    // Obtener información adicional de cada cliente
    const clientsWithDetails = await Promise.all(
      clientStats.map(async (stat: any) => {
        const [clientInfo, levelDistribution, componentDistribution, recentAlert] = await Promise.all([
          // Información del cliente
          prisma.antivirusClient.findUnique({
            where: { clientId: stat.clientId },
            select: {
              hostname: true,
              version: true,
              os: true,
              lastSeen: true,
              createdAt: true
            }
          }),
          
          // Distribución por nivel de logs
          prisma.logEntry.groupBy({
            by: ['level'],
            where: {
              clientId: stat.clientId,
              timestamp: {
                gte: startDate,
                lte: now
              }
            },
            _count: {
              id: true
            }
          }),

          // Distribución por componente
          prisma.logEntry.groupBy({
            by: ['component'],
            where: {
              clientId: stat.clientId,
              timestamp: {
                gte: startDate,
                lte: now
              },
              component: {
                not: null
              }
            },
            _count: {
              id: true
            },
            orderBy: {
              _count: {
                id: 'desc'
              }
            },
            take: 5
          }),

          // Alerta más reciente
          prisma.logEntry.findFirst({
            where: {
              clientId: stat.clientId,
              level: {
                in: ['ERROR', 'WARNING', 'CRITICAL']
              }
            },
            orderBy: {
              timestamp: 'desc'
            },
            select: {
              timestamp: true,
              level: true,
              message: true,
              component: true
            }
          })
        ])

        return {
          clientId: stat.clientId,
          totalLogs: Number(stat._count.id),
          firstSeen: stat._min.timestamp,
          lastSeen: stat._max.timestamp,
          client: clientInfo ? {
            hostname: clientInfo.hostname,
            version: clientInfo.version,
            os: clientInfo.os,
            registeredAt: clientInfo.createdAt
          } : null,
          logDistribution: {
            byLevel: levelDistribution.map((item: any) => ({
              level: item.level,
              count: Number(item._count.id)
            })),
            byComponent: componentDistribution.map((item: any) => ({
              component: item.component,
              count: Number(item._count.id)
            }))
          },
          recentAlert: recentAlert ? {
            timestamp: recentAlert.timestamp,
            level: recentAlert.level,
            message: recentAlert.message.length > 100 
              ? recentAlert.message.substring(0, 100) + '...' 
              : recentAlert.message,
            component: recentAlert.component
          } : null
        }
      })
    )

    // Estadísticas generales
    const [totalClients, activeClients, totalLogsInPeriod] = await Promise.all([
      prisma.antivirusClient.count(),
      prisma.logEntry.groupBy({
        by: ['clientId'],
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          }
        }
      }).then((clients: any) => clients.length),
      prisma.logEntry.count({
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          }
        }
      })
    ])

    const clientAnalytics = {
      summary: {
        totalClients: Number(totalClients),
        activeClients: Number(activeClients),
        totalLogsInPeriod: Number(totalLogsInPeriod),
        timeframe,
        lastUpdate: now.toISOString()
      },
      clients: clientsWithDetails
    }

    // Serializar para evitar problemas con BigInt
    const serializedData = serializeBigInt(clientAnalytics)
    
    // Crear respuesta con serialización manual de JSON para evitar BigInt errors
    const jsonString = JSON.stringify(serializedData, (key, value) => {
      if (typeof value === 'bigint') {
        return value.toString()
      }
      return value
    })
    
    return new NextResponse(jsonString, {
      status: 200,
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json'
      }
    })
    
  } catch (error) {
    console.error('Error fetching client analytics:', error)
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    
    const errorResponse = JSON.stringify({
      error: 'Internal Server Error',
      message: 'Failed to fetch client analytics',
      details: errorMessage
    })
    
    return new NextResponse(errorResponse, {
      status: 500,
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json'
      }
    })
  }
})

// OPTIONS handler para CORS preflight
export async function OPTIONS(request: NextRequest) {
  return new NextResponse(null, {
    status: 200,
    headers: CORS_HEADERS
  })
}