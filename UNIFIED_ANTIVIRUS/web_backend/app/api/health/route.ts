import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// GET /api/health - Health check endpoint
export async function GET(request: NextRequest) {
  try {
    // Verificar conexión a la base de datos
    await prisma.$queryRaw`SELECT 1`
    
    return NextResponse.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      database: 'connected'
    }, {
      status: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      }
    })
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    
    return NextResponse.json({
      status: 'error',
      timestamp: new Date().toISOString(),
      database: 'disconnected',
      error: errorMessage
    }, {
      status: 503,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      }
    })
  } finally {
    await prisma.$disconnect()
  }
}

// OPTIONS handler para CORS
export async function OPTIONS() {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  })
}