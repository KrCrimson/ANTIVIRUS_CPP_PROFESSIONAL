import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// GET /api/clients - Obtener lista de clientes de antivirus
export async function GET(request: NextRequest) {
  // Headers CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Content-Type': 'application/json'
  }

  try {
    const { searchParams } = new URL(request.url)
    const includeInactive = searchParams.get('includeInactive') === 'true'

    const clients = await prisma.antivirusClient.findMany({
      where: includeInactive ? {} : { isActive: true },
      include: {
        _count: {
          select: {
            logs: true
          }
        }
      },
      orderBy: { lastSeen: 'desc' }
    })

    // Calcular estadísticas de cada cliente
    const clientsWithStats = await Promise.all(
      clients.map(async (client: any) => {
        const last24h = new Date(Date.now() - 24 * 60 * 60 * 1000)
        
        const recentLogs = await prisma.logEntry.count({
          where: {
            clientId: client.clientId,
            timestamp: { gte: last24h }
          }
        })

        const criticalLogs = await prisma.logEntry.count({
          where: {
            clientId: client.clientId,
            level: 'CRITICAL',
            timestamp: { gte: last24h }
          }
        })

        const errorLogs = await prisma.logEntry.count({
          where: {
            clientId: client.clientId,
            level: 'ERROR',
            timestamp: { gte: last24h }
          }
        })

        return {
          ...client,
          stats: {
            totalLogs: client._count.logs,
            recentLogs,
            criticalLogs,
            errorLogs,
            status: Date.now() - client.lastSeen.getTime() < 5 * 60 * 1000 ? 'online' : 'offline'
          }
        }
      })
    )

    return NextResponse.json({
      clients: clientsWithStats,
      total: clients.length
    }, { headers })

  } catch (error) {
    console.error('Error fetching clients:', error)
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500, headers }
    )
  }
}

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

