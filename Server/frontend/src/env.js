const env = process.env.VUE_APP_ENV;

let envServerUrl = '';

if (env === 'production') {
    envServerUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}`;
} else if (env === 'staging') {
    envServerUrl = `https://${process.env.VUE_APP_DOMAIN_STAG}`;
} else if (env === 'local') {
    envServerUrl = `https://${process.env.VUE_APP_DOMAIN_DEV}`;
} else {
    envServerUrl = `http://${process.env.VUE_APP_DOMAIN_DEV}`;
}

export const serverUrl = envServerUrl;
export const engineUrl = `http://127.0.0.1:7353`;
export const appName = process.env.VUE_APP_NAME;
