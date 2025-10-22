const { app, BrowserWindow, ipcMain, Menu, shell } = require('electron');
const path = require('path');
const isDev = process.env.NODE_ENV === 'development';

class AntivirusApp {
    constructor() {
        this.mainWindow = null;
        this.setupApp();
    }

    setupApp() {
        // App event handlers
        app.whenReady().then(() => {
            this.createMainWindow();
            this.setupMenu();
            this.setupIPC();
            
            app.on('activate', () => {
                if (BrowserWindow.getAllWindows().length === 0) {
                    this.createMainWindow();
                }
            });
        });

        app.on('window-all-closed', () => {
            if (process.platform !== 'darwin') {
                app.quit();
            }
        });

        // Security: Prevent new window creation
        app.on('web-contents-created', (event, contents) => {
            contents.on('new-window', (navigationEvent, url) => {
                navigationEvent.preventDefault();
                shell.openExternal(url);
            });
        });
    }

    createMainWindow() {
        this.mainWindow = new BrowserWindow({
            width: 1400,
            height: 900,
            minWidth: 1200,
            minHeight: 800,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                enableRemoteModule: false,
                preload: path.join(__dirname, 'preload.js')
            },
            icon: path.join(__dirname, 'assets', 'icon.png'),
            titleBarStyle: 'default',
            show: false // Don't show until ready
        });

        // Load the app
        if (isDev) {
            this.mainWindow.loadURL('http://localhost:3000');
            this.mainWindow.webContents.openDevTools();
        } else {
            this.mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));
        }

        // Show window when ready
        this.mainWindow.once('ready-to-show', () => {
            this.mainWindow.show();
            
            if (isDev) {
                this.mainWindow.webContents.openDevTools();
            }
        });

        // Handle window closed
        this.mainWindow.on('closed', () => {
            this.mainWindow = null;
        });

        // Prevent external navigation
        this.mainWindow.webContents.on('will-navigate', (event, url) => {
            if (url !== this.mainWindow.webContents.getURL()) {
                event.preventDefault();
                shell.openExternal(url);
            }
        });
    }

    setupMenu() {
        const template = [
            {
                label: 'File',
                submenu: [
                    {
                        label: 'Settings',
                        accelerator: 'CmdOrCtrl+,',
                        click: () => {
                            this.mainWindow.webContents.send('navigate-to', '/settings');
                        }
                    },
                    { type: 'separator' },
                    {
                        label: 'Exit',
                        accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
                        click: () => {
                            app.quit();
                        }
                    }
                ]
            },
            {
                label: 'View',
                submenu: [
                    { role: 'reload' },
                    { role: 'forceReload' },
                    { role: 'toggleDevTools' },
                    { type: 'separator' },
                    { role: 'resetZoom' },
                    { role: 'zoomIn' },
                    { role: 'zoomOut' },
                    { type: 'separator' },
                    { role: 'togglefullscreen' }
                ]
            },
            {
                label: 'Window',
                submenu: [
                    { role: 'minimize' },
                    { role: 'close' }
                ]
            },
            {
                label: 'Help',
                submenu: [
                    {
                        label: 'About',
                        click: () => {
                            this.mainWindow.webContents.send('show-about');
                        }
                    },
                    {
                        label: 'Documentation',
                        click: () => {
                            shell.openExternal('https://github.com/KrCrimson/antivirus-docs');
                        }
                    }
                ]
            }
        ];

        const menu = Menu.buildFromTemplate(template);
        Menu.setApplicationMenu(menu);
    }

    setupIPC() {
        // System information requests
        ipcMain.handle('get-system-info', async () => {
            const os = require('os');
            return {
                platform: process.platform,
                arch: process.arch,
                cpus: os.cpus().length,
                totalMemory: os.totalmem(),
                freeMemory: os.freemem(),
                uptime: os.uptime()
            };
        });

        // Backend API communication
        ipcMain.handle('backend-request', async (event, endpoint, options = {}) => {
            try {
                const axios = require('axios');
                const baseURL = 'http://localhost:8080'; // C++ backend port
                
                const response = await axios({
                    url: `${baseURL}${endpoint}`,
                    method: options.method || 'GET',
                    data: options.data || {},
                    timeout: options.timeout || 5000
                });
                
                return { success: true, data: response.data };
            } catch (error) {
                console.error('Backend request error:', error);
                return { 
                    success: false, 
                    error: error.message,
                    code: error.code
                };
            }
        });

        // Quarantine actions
        ipcMain.handle('quarantine-threat', async (event, threatId) => {
            try {
                // Call C++ backend quarantine API
                const axios = require('axios');
                const response = await axios.post(`http://localhost:8080/api/quarantine/${threatId}`);
                return { success: true, data: response.data };
            } catch (error) {
                return { success: false, error: error.message };
            }
        });

        // File operations
        ipcMain.handle('open-file-dialog', async () => {
            const { dialog } = require('electron');
            const result = await dialog.showOpenDialog(this.mainWindow, {
                properties: ['openFile'],
                filters: [
                    { name: 'All Files', extensions: ['*'] },
                    { name: 'Executables', extensions: ['exe', 'dll', 'sys'] }
                ]
            });
            return result;
        });

        // Notifications
        ipcMain.handle('show-notification', async (event, options) => {
            const { Notification } = require('electron');
            
            if (Notification.isSupported()) {
                const notification = new Notification({
                    title: options.title || 'Antivirus Alert',
                    body: options.body || '',
                    icon: path.join(__dirname, 'assets', 'icon.png'),
                    urgency: options.urgency || 'normal'
                });
                
                notification.show();
                return { success: true };
            }
            
            return { success: false, error: 'Notifications not supported' };
        });
    }
}

// Create app instance
new AntivirusApp();