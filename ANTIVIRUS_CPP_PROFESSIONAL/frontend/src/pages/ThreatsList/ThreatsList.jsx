import React from 'react';

const ThreatsList = ({ backendConnected }) => {
    return (
        <div style={{ padding: '40px', textAlign: 'center' }}>
            <h1>🚨 Threats List</h1>
            <p>This page is under construction.</p>
            <p>Status: {backendConnected ? 'Connected' : 'Disconnected'}</p>
        </div>
    );
};

export default ThreatsList;