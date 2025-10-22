import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';

// Global styles reset
import './styles/global.css';

// Initialize React application
const container = document.getElementById('root');
const root = createRoot(container);

// Render App component
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);

// Hide loading screen once React is mounted
document.addEventListener('DOMContentLoaded', () => {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.style.display = 'none';
        }, 1500);
    }
});

// Development hot reloading
if (module.hot) {
    module.hot.accept('./App.jsx', () => {
        const NextApp = require('./App.jsx').default;
        root.render(
            <React.StrictMode>
                <NextApp />
            </React.StrictMode>
        );
    });
}

// Error boundary for the app
window.addEventListener('unhandledrejection', event => {
    console.error('Unhandled promise rejection:', event.reason);
});

console.log('🛡️ Antivirus Professional C++ - Frontend Initialized');
console.log('📊 Dashboard components loaded');
console.log('🔗 Backend API endpoint: http://localhost:8080/api');