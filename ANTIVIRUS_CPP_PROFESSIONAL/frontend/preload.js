const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    // System information
    getSystemInfo: () => ipcRenderer.invoke('get-system-info'),
    
    // Backend communication
    backendRequest: (endpoint, options) => ipcRenderer.invoke('backend-request', endpoint, options),
    
    // Threat management
    quarantineThreat: (threatId) => ipcRenderer.invoke('quarantine-threat', threatId),
    
    // File operations
    openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
    
    // Notifications
    showNotification: (options) => ipcRenderer.invoke('show-notification', options),
    
    // Navigation
    onNavigateTo: (callback) => ipcRenderer.on('navigate-to', callback),
    removeNavigationListeners: () => ipcRenderer.removeAllListeners('navigate-to'),
    
    // About dialog
    onShowAbout: (callback) => ipcRenderer.on('show-about', callback),
    removeAboutListeners: () => ipcRenderer.removeAllListeners('show-about'),
    
    // Window controls
    minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
    maximizeWindow: () => ipcRenderer.invoke('maximize-window'),
    closeWindow: () => ipcRenderer.invoke('close-window'),
    
    // App info
    getAppVersion: () => ipcRenderer.invoke('get-app-version'),
    
    // Settings
    getSetting: (key) => ipcRenderer.invoke('get-setting', key),
    setSetting: (key, value) => ipcRenderer.invoke('set-setting', key, value),
    
    // Logging
    logInfo: (message) => ipcRenderer.invoke('log-info', message),
    logError: (message) => ipcRenderer.invoke('log-error', message),
    logDebug: (message) => ipcRenderer.invoke('log-debug', message)
});