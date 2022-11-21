// Pinia Store
import {defineStore} from 'pinia'
import {server_api} from "@/helpers/server_api";
import {removeLocalToken, saveLocalToken} from "@/utils";
import router from "@/router";


export const useAuthStore = defineStore('auth', {
    // convert to a function
    state: () => ({
        isLoggedIn: null,
        token: '',
        logInError: false,
        networkError: false,
    }),
    actions: {
        async actionLogIn(payload) {
            try {
                const response = await server_api.logInGetToken(payload.username, payload.password);
                const token = response.data.access_token;
                if (token) {
                    saveLocalToken(token);
                    this.token = token
                    this.isLoggedIn = true
                    this.logInError = false
                    //await context.dispatch('actionGetUserProfile');
                    await this.actionRouteLoggedIn()
                    //context.commit('addNotification', { content: 'Logged in', color: 'success' });
                } else {
                    await this.actionLogOut();
                }
            } catch (err) {
                if (err.code === 'ERR_NETWORK') {
                    this.networkError = true
                } else {
                    this.logInError = true
                    await this.actionLogOut()
                }
            }
        },

        async actionLogOut() {
            await this.actionRemoveLogIn()
            await this.actionRouteLogOut()
        },

        async actionRemoveLogIn() {
            removeLocalToken();
            this.token = ''
            this.isLoggedIn = false
        },

        /*async actionUserLogOut() {
            await context.dispatch('actionLogOut');
            context.commit('addNotification', { content: 'Logged out', color: 'success' });
        },*/

        async actionRouteLoggedIn() {
            if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
                await router.push('/main');
            }
        },
        async actionRouteLogOut() {
            if (router.currentRoute.path !== '/login') {
                await router.push('/login');
            }
        },
    }
})
