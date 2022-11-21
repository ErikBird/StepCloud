/**
 * updater.js
 *
 * Please use manual update only when it is really required, otherwise please use recommended non-intrusive auto update.
 *
 * Import steps:
 * 1. create `updater.js` for the code snippet
 * 2. require `updater.js` for menu implementation, and set `checkForUpdates` callback from `updater` for the click property of `Check Updates...` MenuItem.
 */

const {dialog} = require('electron')
const {autoUpdater} = require('electron-updater')

autoUpdater.autoDownload = false
autoUpdater.setFeedURL({
    provider: "generic",
    url: "https://gitlab.com/api/v4/projects/20455729/jobs/artifacts/master/raw/electron-builder-output-dir?job=build"
});
autoUpdater.requestHeaders = {'PRIVATE-TOKEN': '9E8t6WXyRTxgqVRgDshd'}


autoUpdater.on('error', (error) => {
    dialog.showErrorBox('Error: ', error == null ? "unknown" : (error.stack || error).toString())
})

autoUpdater.on('update-available', () => {
    dialog.showMessageBox({
        type: 'info',
        title: 'Found Updates',
        message: 'Found updates, do you want update now?',
        buttons: ['Sure', 'No']
    }, (buttonIndex) => {
        if (buttonIndex === 0) {
            autoUpdater.downloadUpdate()
        }
    })
})

autoUpdater.on('update-not-available', () => {
    dialog.showMessageBox({
        title: 'No Updates',
        message: 'Current version is up-to-date.'
    })
})

autoUpdater.on('update-downloaded', () => {
    dialog.showMessageBox({
        title: 'Install Updates',
        message: 'Updates downloaded, application will be quit for update...'
    }, () => {
        setImmediate(() => autoUpdater.quitAndInstall())
    })
})

function checkForUpdates() {
    autoUpdater.checkForUpdates().then((info) => {
        if (autoUpdater.updateAvailable) {
            downloadUpdate(info.cancellationToken);
        } else {
            console.log.info('Update not available')
        }
    }).catch((error) => {
        if (isNetworkError(error)) {
            console.log.info('Network Error');
        } else {
            console.log.info('Unknown Error');
            console.log.info(error == null ? "unknown" : (error.stack || error).toString());
        }
    });
}

function downloadUpdate(cancellationToken) {
    autoUpdater.downloadUpdate(cancellationToken).then(() => {
        setImmediate(() => autoUpdater.quitAndInstall());
    }).catch((error) => {
        if (isNetworkError(error)) {
            console.log.info('Network Error');
        } else {
            console.log.info('Unknown Error');
            console.log.info(error == null ? "unknown" : (error.stack || error).toString());
        }
    });
}

function isNetworkError(errorObject) {
    return errorObject.message === "net::ERR_INTERNET_DISCONNECTED" ||
        errorObject.message === "net::ERR_PROXY_CONNECTION_FAILED" ||
        errorObject.message === "net::ERR_CONNECTION_RESET" ||
        errorObject.message === "net::ERR_CONNECTION_CLOSE" ||
        errorObject.message === "net::ERR_NAME_NOT_RESOLVED" ||
        errorObject.message === "net::ERR_CONNECTION_TIMED_OUT";
}

module.exports.checkForUpdates = checkForUpdates
