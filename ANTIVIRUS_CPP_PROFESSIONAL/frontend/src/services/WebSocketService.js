/**
 * WebSocket Service - Real-time communication with backend
 */
class WebSocketService {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectInterval = 3000;
        this.eventHandlers = {
            threatDetected: [],
            systemUpdate: [],
            connectionStatus: []
        };
    }

    /**
     * Connect to WebSocket server
     */
    connect(url = 'ws://localhost:8080/ws') {
        try {
            console.log('Attempting WebSocket connection to:', url);
            
            // For now, we'll simulate WebSocket connection since backend might not have WebSocket yet
            this.simulateWebSocketConnection();
            
            /* 
            // Real WebSocket implementation (uncomment when backend supports it):
            this.socket = new WebSocket(url);
            
            this.socket.onopen = () => {
                console.log('WebSocket connected');
                this.reconnectAttempts = 0;
                this.notifyHandlers('connectionStatus', { connected: true });
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };

            this.socket.onclose = () => {
                console.log('WebSocket disconnected');
                this.notifyHandlers('connectionStatus', { connected: false });
                this.attemptReconnect();
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
            */

        } catch (error) {
            console.error('WebSocket connection failed:', error);
        }
    }

    /**
     * Simulate WebSocket connection for development
     */
    simulateWebSocketConnection() {
        console.log('Simulating WebSocket connection...');
        
        // Simulate connection established
        setTimeout(() => {
            this.notifyHandlers('connectionStatus', { connected: true });
        }, 1000);

        // Simulate periodic system updates
        setInterval(() => {
            this.simulateSystemUpdate();
        }, 10000); // Every 10 seconds

        // Simulate random threat detection
        setInterval(() => {
            if (Math.random() < 0.1) { // 10% chance every 30 seconds
                this.simulateThreatDetection();
            }
        }, 30000);
    }

    /**
     * Simulate system update message
     */
    simulateSystemUpdate() {
        const updateData = {
            type: 'systemUpdate',
            data: {
                cpuUsage: Math.random() * 2, // 0-2%
                memoryUsage: 20 + Math.random() * 10, // 20-30MB
                threatsDetected: Math.floor(Math.random() * 5),
                filesScanned: Math.floor(Math.random() * 1000) + 50000,
                timestamp: new Date().toISOString()
            }
        };

        this.notifyHandlers('systemUpdate', updateData.data);
    }

    /**
     * Simulate threat detection
     */
    simulateThreatDetection() {
        const threats = [
            'Trojan.Win32.GenKrypt',
            'Keylogger.Behavior.Detected',
            'Malware.Heuristic.Detection',
            'Ransomware.Suspicious.Activity',
            'Rootkit.System.Modification'
        ];

        const paths = [
            'C:\\Users\\Downloads\\suspicious_file.exe',
            'C:\\Windows\\Temp\\keylog.dll',
            'C:\\Program Files\\Unknown\\malware.bin',
            'C:\\Users\\Documents\\encrypted.dat',
            'C:\\System32\\suspicious.sys'
        ];

        const severities = ['low', 'medium', 'high', 'critical'];
        const statuses = ['detected', 'quarantined', 'blocked', 'cleaned'];

        const threatData = {
            type: 'threatDetected',
            data: {
                id: Date.now(),
                name: threats[Math.floor(Math.random() * threats.length)],
                severity: severities[Math.floor(Math.random() * severities.length)],
                path: paths[Math.floor(Math.random() * paths.length)],
                status: statuses[Math.floor(Math.random() * statuses.length)],
                detectedAt: new Date().toISOString(),
                description: 'Suspicious activity detected by heuristic engine'
            }
        };

        console.log('Simulated threat detection:', threatData.data);
        this.notifyHandlers('threatDetected', threatData.data);
    }

    /**
     * Handle incoming WebSocket messages
     */
    handleMessage(data) {
        switch (data.type) {
            case 'threatDetected':
                this.notifyHandlers('threatDetected', data.data);
                break;
            case 'systemUpdate':
                this.notifyHandlers('systemUpdate', data.data);
                break;
            case 'scanProgress':
                this.notifyHandlers('scanProgress', data.data);
                break;
            default:
                console.log('Unknown WebSocket message type:', data.type);
        }
    }

    /**
     * Register event handler
     */
    on(event, handler) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].push(handler);
        }
    }

    /**
     * Unregister event handler
     */
    off(event, handler) {
        if (this.eventHandlers[event]) {
            const index = this.eventHandlers[event].indexOf(handler);
            if (index > -1) {
                this.eventHandlers[event].splice(index, 1);
            }
        }
    }

    /**
     * Notify all handlers for an event
     */
    notifyHandlers(event, data) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error('Error in WebSocket event handler:', error);
                }
            });
        }
    }

    /**
     * Register threat detection handler
     */
    onThreatDetected(handler) {
        this.on('threatDetected', handler);
    }

    /**
     * Register system update handler
     */
    onSystemUpdate(handler) {
        this.on('systemUpdate', handler);
    }

    /**
     * Register connection status handler
     */
    onConnectionStatus(handler) {
        this.on('connectionStatus', handler);
    }

    /**
     * Send message to backend
     */
    send(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(message));
        } else {
            console.warn('WebSocket not connected, cannot send message:', message);
        }
    }

    /**
     * Attempt to reconnect
     */
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectInterval);
        } else {
            console.error('Max reconnection attempts reached');
        }
    }

    /**
     * Disconnect WebSocket
     */
    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }

    /**
     * Get connection status
     */
    isConnected() {
        return this.socket && this.socket.readyState === WebSocket.OPEN;
    }
}

// Export singleton instance
export const WebSocketService = new WebSocketService();