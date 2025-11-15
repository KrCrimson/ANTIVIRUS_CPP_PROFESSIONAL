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

// GET /api/dashboard - Obtener datos del dashboard
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
    
    // Calcular rango de tiempo
    const now = new Date()
    let startDate: Date
    
    switch (timeframe) {
      case '1h':
        startDate = new Date(now.getTime() - (1 * 60 * 60 * 1000))
        break
      case '6h':
        startDate = new Date(now.getTime() - (6 * 60 * 60 * 1000))
        break
      case '24h':
      default:
        startDate = new Date(now.getTime() - (24 * 60 * 60 * 1000))
        break
      case '7d':
        startDate = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000))
        break
      case '30d':
        startDate = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000))
        break
    }

    // Obtener estadísticas del dashboard
    const [
      totalLogs,
      logsByLevel,
      logsByComponent,
      recentLogs,
      alertsCount,
      clientsCount,
      systemStats
    ] = await Promise.all([
      // Total de logs
      prisma.logEntry.count({
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          }
        }
      }),
      
      // Logs por nivel
      prisma.logEntry.groupBy({
        by: ['level'],
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          }
        },
        _count: {
          id: true
        }
      }),
      
      // Logs por componente
      prisma.logEntry.groupBy({
        by: ['component'],
        where: {
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
        take: 10
      }),
      
      // Logs recientes
      prisma.logEntry.findMany({
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          }
        },
        include: {
          client: {
            select: {
              hostname: true,
              version: true,
              os: true
            }
          }
        },
        orderBy: {
          timestamp: 'desc'
        },
        take: 50
      }),
      
      // Conteo de alertas
      prisma.alert.count({
        where: {
          createdAt: {
            gte: startDate,
            lte: now
          }
        }
      }),
      
      // Conteo de clientes únicos
      prisma.antivirusClient.count(),
      
      // Estadísticas del sistema
      Promise.all([
        prisma.logEntry.count(),
        prisma.alert.count(),
        prisma.antivirusClient.count()
      ])
    ])

    // Preparar datos del dashboard con conversión de BigInt
    const dashboardData = {
      summary: {
        totalLogs: Number(totalLogs),
        alertsCount: Number(alertsCount),
        clientsCount: Number(clientsCount),
        timeframe,
        lastUpdate: now.toISOString()
      },
      logDistribution: {
        byLevel: logsByLevel.map((item: any) => ({
          level: item.level,
          count: Number(item._count.id)
        })),
        byComponent: logsByComponent.map((item: any) => ({
          component: item.component,
          count: Number(item._count.id)
        }))
      },
      recentActivity: recentLogs.slice(0, 20).map((log: any) => ({
        id: log.id.toString(), // Convertir BigInt a string
        timestamp: log.timestamp,
        level: log.level,
        logger: log.logger,
        message: log.message.length > 100 ? log.message.substring(0, 100) + '...' : log.message,
        component: log.component,
        client: log.client ? {
          hostname: log.client.hostname,
          version: log.client.version,
          os: log.client.os
        } : null
      })),
      systemStats: {
        totalLogsAllTime: Number(systemStats[0]),
        totalAlertsAllTime: Number(systemStats[1]),
        totalClients: Number(systemStats[2])
      }
    }

    // Serializar para evitar problemas con BigInt
    const serializedData = serializeBigInt(dashboardData)
    
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
    console.error('Error generating dashboard data:', error)
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    
    const errorResponse = JSON.stringify({
      error: 'Internal Server Error',
      message: 'Failed to fetch dashboard data',
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