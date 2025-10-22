import React from 'react';

const Settings = ({ backendConnected, systemInfo }) => {
    return (
        <div style={{ padding: '40px', textAlign: 'center' }}>
            <h1>⚙️ Settings</h1>
            <p>This page is under construction.</p>
            <p>Status: {backendConnected ? 'Connected' : 'Disconnected'}</p>
        </div>
    );
};

export default Settings;