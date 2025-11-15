import { NextRequest } from 'next/server'
import { healthCheck } from '../../../lib/middleware'

// GET /api/health - Health check endpoint
export async function GET(request: NextRequest) {
  return healthCheck()
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