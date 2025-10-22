import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Components
import Sidebar from './components/Sidebar/Sidebar';
import Header from './components/Header/Header';
import LoadingScreen from './components/LoadingScreen/LoadingScreen';

// Pages
import Dashboard from './pages/Dashboard/Dashboard';
import RealTimeProtection from './pages/RealTimeProtection/RealTimeProtection';
import ThreatsList from './pages/ThreatsList/ThreatsList';
import Quarantine from './pages/Quarantine/Quarantine';
import Settings from './pages/Settings/Settings';
import Reports from './pages/Reports/Reports';

// Services
import { BackendService } from './services/BackendService';
import { WebSocketService } from './services/WebSocketService';

// Styles
import './styles/App.css';
import './styles/Variables.css';

function App() {
    const [isLoading, setIsLoading] = useState(true);
    const [backendConnected, setBackendConnected] = useState(false);
    const [systemInfo, setSystemInfo] = useState(null);
    const [currentPage, setCurrentPage] = useState('dashboard');

    useEffect(() => {
        initializeApp();
    }, []);

    const initializeApp = async () => {
        try {
            // Get system information
            const sysInfo = await window.electronAPI.getSystemInfo();
            setSystemInfo(sysInfo);

            // Initialize backend connection
            const backendStatus = await BackendService.checkConnection();
            setBackendConnected(backendStatus);

            // Initialize WebSocket connection for real-time updates
            if (backendStatus) {
                WebSocketService.connect('ws://localhost:8080/ws');
                WebSocketService.onThreatDetected((threat) => {
                    console.log('New threat detected:', threat);
                    // Handle real-time threat notification
                });
            }

            setIsLoading(false);
        } catch (error) {
            console.error('App initialization error:', error);
            setIsLoading(false);
        }
    };

    if (isLoading) {
        return <LoadingScreen />;
    }

    return (
        <Router>
            <div className="app">
                <Toaster
                    position="top-right"
                    toastOptions={{
                        duration: 4000,
                        style: {
                            background: '#1a1a1a',
                            color: '#fff',
                            border: '1px solid #333'
                        }
                    }}
                />
                
                <div className="app-layout">
                    <Sidebar 
                        currentPage={currentPage}
                        onPageChange={setCurrentPage}
                        backendConnected={backendConnected}
                    />
                    
                    <div className="main-content">
                        <Header 
                            systemInfo={systemInfo}
                            backendConnected={backendConnected}
                            currentPage={currentPage}
                        />
                        
                        <div className="page-content">
                            <Routes>
                                <Route 
                                    path="/" 
                                    element={
                                        <Dashboard 
                                            backendConnected={backendConnected}
                                            onPageChange={setCurrentPage}
                                        />
                                    } 
                                />
                                <Route 
                                    path="/protection" 
                                    element={
                                        <RealTimeProtection 
                                            backendConnected={backendConnected}
                                        />
                                    } 
                                />
                                <Route 
                                    path="/threats" 
                                    element={
                                        <ThreatsList 
                                            backendConnected={backendConnected}
                                        />
                                    } 
                                />
                                <Route 
                                    path="/quarantine" 
                                    element={
                                        <Quarantine 
                                            backendConnected={backendConnected}
                                        />
                                    } 
                                />
                                <Route 
                                    path="/reports" 
                                    element={
                                        <Reports 
                                            backendConnected={backendConnected}
                                        />
                                    } 
                                />
                                <Route 
                                    path="/settings" 
                                    element={
                                        <Settings 
                                            backendConnected={backendConnected}
                                            systemInfo={systemInfo}
                                        />
                                    } 
                                />
                            </Routes>
                        </div>
                    </div>
                </div>
            </div>
        </Router>
    );
}

export default App;