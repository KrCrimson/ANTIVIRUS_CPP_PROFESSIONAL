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

// GET /api/threats - Obtener análisis de amenazas
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

    // Análisis de patrones de amenazas
    const [
      threatsByLevel,
      threatsByComponent,
      threatPatterns,
      criticalAlerts,
      timelineData,
      topThreats
    ] = await Promise.all([
      // Amenazas por nivel de severidad
      prisma.logEntry.groupBy({
        by: ['level'],
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          },
          level: {
            in: ['ERROR', 'WARNING', 'CRITICAL']
          }
        },
        _count: {
          id: true
        },
        orderBy: {
          _count: {
            id: 'desc'
          }
        }
      }),

      // Amenazas por componente/detector
      prisma.logEntry.groupBy({
        by: ['component'],
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          },
          level: {
            in: ['ERROR', 'WARNING', 'CRITICAL']
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

      // Patrones de amenazas (análisis de texto de mensajes)
      prisma.logEntry.findMany({
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          },
          level: {
            in: ['ERROR', 'WARNING', 'CRITICAL']
          }
        },
        select: {
          message: true,
          level: true,
          component: true
        }
      }),

      // Alertas críticas recientes
      prisma.logEntry.findMany({
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          },
          level: 'CRITICAL'
        },
        include: {
          client: {
            select: {
              hostname: true,
              clientId: true
            }
          }
        },
        orderBy: {
          timestamp: 'desc'
        },
        take: 20
      }),

      // Datos de timeline por horas
      prisma.logEntry.findMany({
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          },
          level: {
            in: ['ERROR', 'WARNING', 'CRITICAL']
          }
        },
        select: {
          timestamp: true,
          level: true
        },
        orderBy: {
          timestamp: 'asc'
        }
      }),

      // Top amenazas por keywords
      prisma.logEntry.findMany({
        where: {
          timestamp: {
            gte: startDate,
            lte: now
          },
          OR: [
            { message: { contains: 'malware' } },
            { message: { contains: 'virus' } },
            { message: { contains: 'keylogger' } },
            { message: { contains: 'suspicious' } },
            { message: { contains: 'blocked' } },
            { message: { contains: 'threat' } },
            { message: { contains: 'detected' } }
          ]
        },
        select: {
          message: true,
          level: true,
          component: true,
          timestamp: true,
          clientId: true
        }
      })
    ])

    // Procesar patrones de amenazas
    const threatKeywords = ['malware', 'virus', 'keylogger', 'suspicious', 'blocked', 'threat', 'detected', 'ransomware', 'trojan', 'spyware']
    const threatPatternCounts = threatKeywords.map(keyword => {
      const count = threatPatterns.filter((threat: any) => 
        threat.message.toLowerCase().includes(keyword.toLowerCase())
      ).length
      return { keyword, count }
    }).filter(pattern => pattern.count > 0)
    .sort((a: any, b: any) => b.count - a.count)

    // Crear timeline por horas
    const timelineByHour: { [hour: string]: { ERROR: number, WARNING: number, CRITICAL: number } } = {}
    timelineData.forEach((log: any) => {
      const hour = new Date(log.timestamp).toISOString().substring(0, 13) + ':00:00.000Z'
      if (!timelineByHour[hour]) {
        timelineByHour[hour] = { ERROR: 0, WARNING: 0, CRITICAL: 0 }
      }
      timelineByHour[hour][log.level as 'ERROR' | 'WARNING' | 'CRITICAL']++
    })

    const timelineSorted = Object.entries(timelineByHour)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([hour, counts]) => ({
        timestamp: hour,
        ...counts,
        total: counts.ERROR + counts.WARNING + counts.CRITICAL
      }))

    const threatAnalytics = {
      summary: {
        totalThreats: Number(threatsByLevel.reduce((sum: any, item: any) => sum + item._count.id, 0)),
        criticalThreats: Number(criticalAlerts.length),
        timeframe,
        lastUpdate: now.toISOString()
      },
      distribution: {
        byLevel: threatsByLevel.map((item: any) => ({
          level: item.level,
          count: Number(item._count.id)
        })),
        byComponent: threatsByComponent.map((item: any) => ({
          component: item.component,
          count: Number(item._count.id)
        }))
      },
      patterns: {
        keywords: threatPatternCounts,
        topThreats: topThreats.slice(0, 10).map((threat: any) => ({
          message: threat.message.length > 150 
            ? threat.message.substring(0, 150) + '...' 
            : threat.message,
          level: threat.level,
          component: threat.component,
          timestamp: threat.timestamp,
          clientId: threat.clientId
        }))
      },
      criticalAlerts: criticalAlerts.map((alert: any) => ({
        id: alert.id.toString(),
        timestamp: alert.timestamp,
        message: alert.message.length > 200 
          ? alert.message.substring(0, 200) + '...' 
          : alert.message,
        component: alert.component,
        client: alert.client ? {
          hostname: alert.client.hostname,
          clientId: alert.client.clientId
        } : null
      })),
      timeline: timelineSorted
    }

    // Serializar para evitar problemas con BigInt
    const serializedData = serializeBigInt(threatAnalytics)
    
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
    console.error('Error fetching threat analytics:', error)
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    
    const errorResponse = JSON.stringify({
      error: 'Internal Server Error',
      message: 'Failed to fetch threat analytics',
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