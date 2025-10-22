/**
 * Backend Service - Comunicación con el backend C++
 */
class BackendService {
    constructor() {
        this.baseURL = 'http://localhost:8080';
        this.timeout = 5000;
    }

    /**
     * Verifica conexión con el backend
     */
    async checkConnection() {
        try {
            const result = await window.electronAPI.backendRequest('/api/health');
            return result.success;
        } catch (error) {
            console.error('Backend connection check failed:', error);
            return false;
        }
    }

    /**
     * Obtiene estadísticas del sistema
     */
    async getSystemMetrics() {
        try {
            const result = await window.electronAPI.backendRequest('/api/metrics');
            return result.success ? result.data : null;
        } catch (error) {
            console.error('Failed to get system metrics:', error);
            return null;
        }
    }

    /**
     * Obtiene lista de amenazas detectadas
     */
    async getThreats(filters = {}) {
        try {
            const queryParams = new URLSearchParams(filters).toString();
            const endpoint = `/api/threats${queryParams ? '?' + queryParams : ''}`;
            
            const result = await window.electronAPI.backendRequest(endpoint);
            return result.success ? result.data : [];
        } catch (error) {
            console.error('Failed to get threats:', error);
            return [];
        }
    }

    /**
     * Obtiene detalle de una amenaza específica
     */
    async getThreatDetail(threatId) {
        try {
            const result = await window.electronAPI.backendRequest(`/api/threats/${threatId}`);
            return result.success ? result.data : null;
        } catch (error) {
            console.error('Failed to get threat detail:', error);
            return null;
        }
    }

    /**
     * Pone una amenaza en cuarentena
     */
    async quarantineThreat(threatId) {
        try {
            const result = await window.electronAPI.quarantineThreat(threatId);
            return result.success;
        } catch (error) {
            console.error('Failed to quarantine threat:', error);
            return false;
        }
    }

    /**
     * Obtiene configuración del motor de detección
     */
    async getDetectionConfig() {
        try {
            const result = await window.electronAPI.backendRequest('/api/config/detection');
            return result.success ? result.data : null;
        } catch (error) {
            console.error('Failed to get detection config:', error);
            return null;
        }
    }

    /**
     * Actualiza configuración del motor de detección
     */
    async updateDetectionConfig(config) {
        try {
            const result = await window.electronAPI.backendRequest('/api/config/detection', {
                method: 'PUT',
                data: config
            });
            return result.success;
        } catch (error) {
            console.error('Failed to update detection config:', error);
            return false;
        }
    }

    /**
     * Obtiene lista de detectores disponibles
     */
    async getDetectors() {
        try {
            const result = await window.electronAPI.backendRequest('/api/detectors');
            return result.success ? result.data : [];
        } catch (error) {
            console.error('Failed to get detectors:', error);
            return [];
        }
    }

    /**
     * Habilita/deshabilita un detector específico
     */
    async toggleDetector(detectorName, enabled) {
        try {
            const result = await window.electronAPI.backendRequest(`/api/detectors/${detectorName}`, {
                method: 'PATCH',
                data: { enabled }
            });
            return result.success;
        } catch (error) {
            console.error('Failed to toggle detector:', error);
            return false;
        }
    }

    /**
     * Inicia escaneo manual del sistema
     */
    async startSystemScan(options = {}) {
        try {
            const result = await window.electronAPI.backendRequest('/api/scan/start', {
                method: 'POST',
                data: options
            });
            return result.success ? result.data : null;
        } catch (error) {
            console.error('Failed to start system scan:', error);
            return null;
        }
    }

    /**
     * Obtiene estado del escaneo actual
     */
    async getScanStatus() {
        try {
            const result = await window.electronAPI.backendRequest('/api/scan/status');
            return result.success ? result.data : null;
        } catch (error) {
            console.error('Failed to get scan status:', error);
            return null;
        }
    }

    /**
     * Cancela escaneo en curso
     */
    async cancelScan() {
        try {
            const result = await window.electronAPI.backendRequest('/api/scan/cancel', {
                method: 'POST'
            });
            return result.success;
        } catch (error) {
            console.error('Failed to cancel scan:', error);
            return false;
        }
    }

    /**
     * Obtiene reportes de seguridad
     */
    async getSecurityReports(dateRange = {}) {
        try {
            const queryParams = new URLSearchParams(dateRange).toString();
            const endpoint = `/api/reports${queryParams ? '?' + queryParams : ''}`;
            
            const result = await window.electronAPI.backendRequest(endpoint);
            return result.success ? result.data : [];
        } catch (error) {
            console.error('Failed to get security reports:', error);
            return [];
        }
    }

    /**
     * Obtiene elementos en cuarentena
     */
    async getQuarantineItems() {
        try {
            const result = await window.electronAPI.backendRequest('/api/quarantine');
            return result.success ? result.data : [];
        } catch (error) {
            console.error('Failed to get quarantine items:', error);
            return [];
        }
    }

    /**
     * Restaura elemento de cuarentena
     */
    async restoreFromQuarantine(itemId) {
        try {
            const result = await window.electronAPI.backendRequest(`/api/quarantine/${itemId}/restore`, {
                method: 'POST'
            });
            return result.success;
        } catch (error) {
            console.error('Failed to restore from quarantine:', error);
            return false;
        }
    }

    /**
     * Elimina permanentemente elemento de cuarentena
     */
    async deleteFromQuarantine(itemId) {
        try {
            const result = await window.electronAPI.backendRequest(`/api/quarantine/${itemId}`, {
                method: 'DELETE'
            });
            return result.success;
        } catch (error) {
            console.error('Failed to delete from quarantine:', error);
            return false;
        }
    }

    /**
     * Obtiene estadísticas del modelo ML
     */
    async getMLStats() {
        try {
            const result = await window.electronAPI.backendRequest('/api/ml/stats');
            return result.success ? result.data : null;
        } catch (error) {
            console.error('Failed to get ML stats:', error);
            return null;
        }
    }

    /**
     * Actualiza modelo ML
     */
    async updateMLModel(modelPath) {
        try {
            const result = await window.electronAPI.backendRequest('/api/ml/update-model', {
                method: 'POST',
                data: { model_path: modelPath }
            });
            return result.success;
        } catch (error) {
            console.error('Failed to update ML model:', error);
            return false;
        }
    }
}

// Singleton instance
export const BackendService = new BackendService();