'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

interface LoginProps {
  onLogin: (apiKey: string) => void
}

export default function LoginPage() {
  const [apiKey, setApiKey] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const validApiKeys = [
    'antivirus-key-2024-prod-12345',
    'antivirus-dev-key-local-67890'
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      // Verificar API key
      if (!validApiKeys.includes(apiKey)) {
        throw new Error('API key inválida')
      }

      // Probar conexión con el backend
      const response = await fetch('/api/dashboard', {
        headers: {
          'x-api-key': apiKey
        }
      })

      if (!response.ok) {
        throw new Error('Error de conexión con el backend')
      }

      // Guardar API key en localStorage
      localStorage.setItem('antivirusApiKey', apiKey)
      
      // Redirigir al dashboard
      router.push('/dashboard')
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error de autenticación')
    } finally {
      setIsLoading(false)
    }
  }

  const copyApiKey = (key: string) => {
    navigator.clipboard.writeText(key)
    alert('API key copiada al portapapeles')
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            🛡️ Unified Antivirus
          </h1>
          <p className="text-gray-600">Acceso al Dashboard de Monitoreo</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Ingresa tu API key"
              required
            />
          </div>

          {error && (
            <div className="text-red-600 text-sm bg-red-50 p-2 rounded">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Verificando...' : 'Acceder al Dashboard'}
          </button>
        </form>

        <div className="mt-6 p-4 bg-gray-50 rounded-md">
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            📋 API Keys disponibles:
          </h3>
          <div className="space-y-2 text-xs">
            {validApiKeys.map((key, index) => (
              <div key={index} className="flex items-center justify-between bg-white p-2 rounded border">
                <span className="font-mono text-gray-600">
                  {key.substring(0, 20)}...
                </span>
                <button
                  type="button"
                  onClick={() => copyApiKey(key)}
                  className="text-blue-600 hover:text-blue-800 text-xs"
                >
                  Copiar
                </button>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-2">
            💡 En producción, las API keys se gestionarían de forma segura
          </p>
        </div>

        <div className="mt-4 text-center">
          <div className="text-xs text-gray-500">
            <div className="flex items-center justify-center space-x-4">
              <span>✅ Dashboard con gráficos en tiempo real</span>
            </div>
            <div className="flex items-center justify-center space-x-4 mt-1">
              <span>✅ Autenticación por API key</span>
            </div>
            <div className="flex items-center justify-center space-x-4 mt-1">
              <span>✅ Logs automáticos desde launcher</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}