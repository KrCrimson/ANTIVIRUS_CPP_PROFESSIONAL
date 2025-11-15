import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  // Permitir todas las rutas de API sin autenticación
  if (request.nextUrl.pathname.startsWith('/api/')) {
    // Agregar headers CORS
    const response = NextResponse.next()
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
      response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-api-key')
    
    return response
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/api/:path*']
}