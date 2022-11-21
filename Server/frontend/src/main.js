import '@babel/polyfill';
// Import Component hooks before component definitions
import '@/component-hooks';
import Vue from 'vue';
import '@/plugins/vee-validate';
import App from '@/App.vue';
import router from '@/router';
import store from './store';
import './registerServiceWorker';
import i18n from '@/i18n';
import vuetify from '@/plugins/vuetify';
import * as Sentry from "@sentry/browser";
import {Vue as VueIntegration} from "@sentry/integrations";
import {Integrations} from "@sentry/tracing";

Sentry.init({
    dsn: "https://a1d6097ab5c947c0879cdf9325bdd331@o479962.ingest.sentry.io/5525848",
    integrations: [
        new VueIntegration({
            Vue,
            tracing: true,
        }),
        new Integrations.BrowserTracing(),
    ],

    // We recommend adjusting this value in production, or using tracesSampler
    // for finer control
    tracesSampleRate: 1.0,
});


Vue.config.productionTip = false;

new Vue({
    store,
    router,
    i18n,
    vuetify,
    render: (h) => h(App)
}).$mount('#app');
