import React from 'react';

const Reports = ({ backendConnected }) => {
    return (
        <div style={{ padding: '40px', textAlign: 'center' }}>
            <h1>📊 Security Reports</h1>
            <p>This page is under construction.</p>
            <p>Status: {backendConnected ? 'Connected' : 'Disconnected'}</p>
        </div>
    );
};

export default Reports;