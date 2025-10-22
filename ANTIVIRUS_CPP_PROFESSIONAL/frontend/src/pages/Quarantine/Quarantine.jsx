import React from 'react';

const Quarantine = ({ backendConnected }) => {
    return (
        <div style={{ padding: '40px', textAlign: 'center' }}>
            <h1>🔒 Quarantine Manager</h1>
            <p>This page is under construction.</p>
            <p>Status: {backendConnected ? 'Connected' : 'Disconnected'}</p>
        </div>
    );
};

export default Quarantine;