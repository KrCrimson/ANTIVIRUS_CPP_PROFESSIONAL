import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'
import { requireAuth, CORS_HEADERS } from '../../../lib/auth'

const prisma = new PrismaClient()

// GET /api/dashboard - Obtener estadísticas del dashboard
export const GET = requireAuth(async (request: NextRequest) => {

  try {
    const { searchParams } = new URL(request.url)
    const timeRange = searchParams.get('timeRange') || '24h'
    
    // Calcular fecha de inicio según el rango
    const now = new Date()
    let startDate = new Date()
    
    switch (timeRange) {
      case '1h':
        startDate.setHours(now.getHours() - 1)
        break
      case '24h':
        startDate.setDate(now.getDate() - 1)
        break
      case '7d':
        startDate.setDate(now.getDate() - 7)
        break
      case '30d':
        startDate.setDate(now.getDate() - 30)
        break
      default:
        startDate.setDate(now.getDate() - 1)
    }

    // Estadísticas generales
    const totalClients = await prisma.antivirusClient.count({
      where: { isActive: true }
    })

    const activeClients = await prisma.antivirusClient.count({
      where: {
        isActive: true,
        lastSeen: { gte: new Date(Date.now() - 5 * 60 * 1000) } // Activos en últimos 5 min
      }
    })

    const totalLogs = await prisma.logEntry.count({
      where: {
        timestamp: { gte: startDate }
      }
    })

    const criticalAlerts = await prisma.alert.count({
      where: {
        severity: 'CRITICAL',
        resolved: false,
        createdAt: { gte: startDate }
      }
    })

    const highAlerts = await prisma.alert.count({
      where: {
        severity: 'HIGH',
        resolved: false,
        createdAt: { gte: startDate }
      }
    })

    // Distribución de logs por nivel
    const logsByLevel = await prisma.logEntry.groupBy({
      by: ['level'],
      where: {
        timestamp: { gte: startDate }
      },
      _count: {
        level: true
      }
    })

    // Distribución de logs por componente
    const logsByComponent = await prisma.logEntry.groupBy({
      by: ['component'],
      where: {
        timestamp: { gte: startDate },
        component: { not: null }
      },
      _count: {
        component: true
      },
      orderBy: {
        _count: {
          component: 'desc'
        }
      },
      take: 10
    })

    // Actividad por hora (últimas 24 horas)
    const hourlyActivity = await prisma.$queryRaw`
      SELECT 
        DATE_TRUNC('hour', timestamp) as hour,
        COUNT(*) as count,
        COUNT(CASE WHEN level = 'ERROR' THEN 1 END) as errors,
        COUNT(CASE WHEN level = 'CRITICAL' THEN 1 END) as critical
      FROM log_entries 
      WHERE timestamp >= ${startDate}
      GROUP BY DATE_TRUNC('hour', timestamp)
      ORDER BY hour DESC
      LIMIT 24
    `

    // Top clientes por actividad
    const topClients = await prisma.logEntry.groupBy({
      by: ['clientId'],
      where: {
        timestamp: { gte: startDate }
      },
      _count: {
        clientId: true
      },
      orderBy: {
        _count: {
          clientId: 'desc'
        }
      },
      take: 5
    })

    // Obtener información adicional de los top clientes
    const topClientsWithInfo = await Promise.all(
      topClients.map(async (item: any) => {
        const client = await prisma.antivirusClient.findUnique({
          where: { clientId: item.clientId },
          select: {
            hostname: true,
            version: true,
            os: true,
            lastSeen: true
          }
        })
        return {
          ...item,
          client
        }
      })
    )

    // Alertas recientes
    const recentAlerts = await prisma.alert.findMany({
      where: {
        createdAt: { gte: startDate }
      },
      include: {
        log: {
          include: {
            client: {
              select: {
                hostname: true,
                clientId: true
              }
            }
          }
        }
      },
      orderBy: { createdAt: 'desc' },
      take: 10
    })

    // Tendencias (comparación con período anterior)
    const previousStartDate = new Date(startDate.getTime() - (now.getTime() - startDate.getTime()))
    
    const previousLogs = await prisma.logEntry.count({
      where: {
        timestamp: { gte: previousStartDate, lt: startDate }
      }
    })

    const logsTrend = previousLogs === 0 ? 0 : ((totalLogs - previousLogs) / previousLogs) * 100

    return NextResponse.json({
      overview: {
        totalClients,
        activeClients,
        totalLogs,
        criticalAlerts,
        highAlerts,
        trends: {
          logsTrend: Math.round(logsTrend * 100) / 100
        }
      },
      charts: {
        logsByLevel: logsByLevel.map((item: any) => ({
          level: item.level,
          count: item._count.level
        })),
        logsByComponent: logsByComponent.map((item: any) => ({
          component: item.component || 'Unknown',
          count: item._count.component
        })),
        hourlyActivity,
        topClients: topClientsWithInfo
      },
      recentAlerts,
      timeRange,
      generatedAt: new Date().toISOString()
    }, { headers: CORS_HEADERS })

  } catch (error) {
    console.error('Error generating dashboard data:', error)
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500, headers: CORS_HEADERS }
    )
  }
})

// OPTIONS handler para CORS preflight
export async function OPTIONS(request: NextRequest) {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}