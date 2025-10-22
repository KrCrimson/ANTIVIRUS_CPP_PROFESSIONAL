import React from 'react';

const RealTimeProtection = ({ backendConnected }) => {
    return (
        <div style={{ padding: '40px', textAlign: 'center' }}>
            <h1>🛡️ Real-time Protection</h1>
            <p>This page is under construction.</p>
            <p>Status: {backendConnected ? 'Connected' : 'Disconnected'}</p>
        </div>
    );
};

export default RealTimeProtection;