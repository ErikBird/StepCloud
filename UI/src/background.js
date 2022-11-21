'use strict'

import {app, BrowserWindow, protocol} from 'electron'
import {createProtocol} from 'vue-cli-plugin-electron-builder/lib'
import installExtension, {VUEJS_DEVTOOLS} from 'electron-devtools-installer'

const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
    {scheme: 'app', privileges: {secure: true, standard: true}}
])

function changeCORSHeader(session) {
    const filter = {
        urls: ['https://amira3d.io/*', "https://localhost/*", "http://localhost/*", "http://dev.lithohub.com/*", "https://stag.lithohub.com/*"]
    };
    session.webRequest.onBeforeSendHeaders(
        filter,
        (details, callback) => {
            console.log(details);
            details.requestHeaders['Origin'] = 'https://localhost';
            callback({requestHeaders: details.requestHeaders});
        }
    );
    session.webRequest.onHeadersReceived(
        filter,
        (details, callback) => {
            console.log(details);
            details.responseHeaders['access-control-allow-origin'] = [
                'app://.'
            ];
            callback({responseHeaders: details.responseHeaders});
        }
    );
}


async function createWindow() {
    // Create the browser window.
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            // Use pluginOptions.nodeIntegration, leave this alone
            // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
            nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
            contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION
        }
    })
    if (process.env.WEBPACK_DEV_SERVER_URL) {
        // Load the url of the dev server if in development mode
        await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
        //if (!process.env.IS_TEST)
        win.webContents.openDevTools()
    } else {
        createProtocol('app')
        // Load the index.html when not in development
        win.loadURL('app://./index.html')
        // We have to manually change the header of our http requests in order to comply with the CORS Standard
        // This is because we can only explicitly allow real http/https origins in FastAPI.
        // Our electron app has the http header origin value of 'app://.' and cant be changed otherwise.
        // https://github.com/tiangolo/fastapi/issues/133#
        var session = win.webContents.session;
        changeCORSHeader(session);
    }
}


// Quit when all windows are closed.
app.on('window-all-closed', async () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
    if (process.platform === 'win32') {
        process.on('message', (data) => {
            if (data === 'graceful-exit') {
                app.quit()
            }
        })
    } else {
        process.on('SIGTERM', () => {
            app.quit()
        })
    }
}


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
    if (isDevelopment && !process.env.IS_TEST) {
        // Install Vue Devtools
        try {
            await installExtension(VUEJS_DEVTOOLS)
        } catch (e) {
            console.error('Vue Devtools failed to install:', e.toString())
        }
    }
    createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
    if (process.platform === 'win32') {
        process.on('message', (data) => {
            if (data === 'graceful-exit') {
                app.quit()
            }
        })
    } else {
        process.on('SIGTERM', () => {
            app.quit()
        })
    }
}


