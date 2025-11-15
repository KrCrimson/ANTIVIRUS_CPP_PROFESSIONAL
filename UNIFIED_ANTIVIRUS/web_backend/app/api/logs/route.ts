import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'
import Joi from 'joi'
import { requireAuth, CORS_HEADERS } from '../../../lib/auth'

const prisma = new PrismaClient()

// Esquema de validación para logs
const logSchema = Joi.object({
  clientId: Joi.string().required(),
  hostname: Joi.string().required(),
  version: Joi.string().required(),
  os: Joi.string().required(),
  logs: Joi.array().items(
    Joi.object({
      timestamp: Joi.string().isoDate().required(),
      level: Joi.string().valid('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').required(),
      logger: Joi.string().required(),
      message: Joi.string().required(),
      module: Joi.string().optional(),
      function: Joi.string().optional(),
      line: Joi.number().optional(),
      component: Joi.string().optional(),
      data: Joi.object().optional()
    })
  ).min(1).required()
})

// POST /api/logs - Recibir logs de antivirus
export const POST = requireAuth(async (request: NextRequest) => {
  try {
    const body = await request.json()
    
    // Validar estructura de datos
    const { error, value } = logSchema.validate(body)
    if (error) {
      return NextResponse.json(
        { error: 'Validation Error', details: error.details },
        { status: 400, headers: CORS_HEADERS }
      )
    }

    const { clientId, hostname, version, os, logs } = value
    
    // Crear o actualizar cliente
    const client = await prisma.antivirusClient.upsert({
      where: { clientId },
      update: {
        hostname,
        version,
        os,
        lastSeen: new Date(),
        isActive: true
      },
      create: {
        clientId,
        hostname,
        version,
        os,
        isActive: true,
        lastSeen: new Date()
      }
    })

    // Insertar logs en la base de datos
    const logEntries = await prisma.logEntry.createMany({
      data: logs.map((log: any) => ({
        clientId: client.clientId,
        timestamp: new Date(log.timestamp),
        level: log.level,
        logger: log.logger,
        message: log.message,
        module: log.module,
        function: log.function,
        line: log.line,
        component: log.component,
        data: log.data
      })),
      skipDuplicates: true
    })

    // Generar alertas para logs críticos
    const criticalLogs = logs.filter((log: any) => log.level === 'CRITICAL' || log.level === 'ERROR')
    for (const log of criticalLogs) {
      try {
        await prisma.alert.create({
          data: {
            severity: log.level === 'CRITICAL' ? 'CRITICAL' : 'HIGH',
            title: `${log.level}: ${log.component || log.logger}`,
            description: log.message,
            status: 'OPEN',
            log: {
              connect: {
                id: (await prisma.logEntry.findFirst({
                  where: {
                    clientId: client.clientId,
                    timestamp: new Date(log.timestamp),
                    message: log.message
                  }
                }))?.id
              }
            }
          }
        })
      } catch (alertError) {
        console.warn('Error creating alert:', alertError)
      }
    }

    return NextResponse.json({
      success: true,
      message: `${logs.length} logs processed successfully`,
      clientId,
      timestamp: new Date().toISOString()
    }, { headers: CORS_HEADERS })

  } catch (error) {
    console.error('Error processing logs:', error)
    return NextResponse.json(
      { error: 'Internal Server Error', message: 'Failed to process logs' },
      { status: 500, headers: CORS_HEADERS }
    )
  }
})

// GET /api/logs - Obtener logs (para dashboard)
export const GET = requireAuth(async (request: NextRequest) => {
  try {
    const { searchParams } = new URL(request.url)
    
    // Parámetros de paginación
    const page = parseInt(searchParams.get('page') || '1')
    const limit = Math.min(parseInt(searchParams.get('limit') || '100'), 1000)
    const skip = (page - 1) * limit
    
    // Filtros
    const level = searchParams.get('level')
    const clientId = searchParams.get('clientId')
    const component = searchParams.get('component')
    
    // Construir filtros WHERE
    const where: any = {}
    if (level) where.level = level
    if (clientId) where.clientId = clientId
    if (component) where.component = component
    
    // Obtener logs con paginación
    const [logs, totalCount] = await Promise.all([
      prisma.logEntry.findMany({
        where,
        include: {
          client: {
            select: {
              hostname: true,
              version: true,
              os: true
            }
          }
        },
        orderBy: { timestamp: 'desc' },
        skip,
        take: limit
      }),
      prisma.logEntry.count({ where })
    ])
    
    const totalPages = Math.ceil(totalCount / limit)
    
    return NextResponse.json({
      logs,
      pagination: {
        currentPage: page,
        totalPages,
        totalCount,
        limit,
        hasNextPage: page < totalPages,
        hasPrevPage: page > 1
      }
    }, { headers: CORS_HEADERS })
    
  } catch (error) {
    console.error('Error fetching logs:', error)
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
    headers: CORS_HEADERS
  })
}