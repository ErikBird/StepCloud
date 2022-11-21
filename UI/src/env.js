const env = process.env.NODE_ENV;//process.env.VUE_APP_ENV;
let envApiUrl = '';

if (env !== 'development') {
    envApiUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}`;
} else {
    envApiUrl = `http://${process.env.VUE_APP_DOMAIN_DEV}`;
}

export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;
export const engineUrl = 'http://0.0.0.0:7353'
