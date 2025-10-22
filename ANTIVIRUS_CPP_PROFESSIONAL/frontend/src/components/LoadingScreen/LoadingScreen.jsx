import React from 'react';
import './LoadingScreen.css';

const LoadingScreen = () => {
    return (
        <div className="loading-screen">
            <div className="loading-content">
                <div className="antivirus-logo">
                    <div className="shield-icon">🛡️</div>
                    <h1>Antivirus C++</h1>
                    <p className="subtitle">Professional Protection</p>
                </div>
                
                <div className="loading-animation">
                    <div className="spinner-ring">
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                    </div>
                    <p className="loading-text">Initializing protection systems...</p>
                </div>
                
                <div className="loading-features">
                    <div className="feature-item">
                        <span className="feature-icon">⚡</span>
                        <span>High Performance Engine</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">🔍</span>
                        <span>Real-time Detection</span>
                    </div>
                    <div className="feature-item">
                        <span className="feature-icon">🛡️</span>
                        <span>Advanced Heuristics</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoadingScreen;