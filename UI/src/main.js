import Vue from 'vue'
import App from './App.vue'

import {createPinia, PiniaVuePlugin} from 'pinia'

Vue.use(PiniaVuePlugin)
const pinia = createPinia()

import router from './router'
import vuetify from './plugins/vuetify';
import i18n from './i18n'
import VueApexCharts from 'vue-apexcharts'
import VueRouter from "vue-router";

Vue.use(VueRouter);
Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)


Vue.config.productionTip = false

new Vue({
    router,
    pinia,
    vuetify,
    i18n,
    render: h => h(App)
}).$mount('#app')

