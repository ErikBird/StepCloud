import {server_api} from '@/helpers/server_api';
import router from '@/router';
import {getLocalToken, removeLocalToken, saveLocalToken} from '@/utils';


export const actions = {
    async actionLogIn(context, payload) {
        try {
            const response = await server_api.logInGetToken(payload.username, payload.password);
            console.log(response.status)
            const token = response.data.access_token;
            if (token) {
                saveLocalToken(token);
                context.commit('setToken', token);
                context.commit('setLoggedIn', true);
                context.commit('setLogInError', false);
                context.commit('setNetworkError', false);
                await context.dispatch('actionGetUserProfile');
                await context.dispatch('actionRouteLoggedIn');
                context.commit('addNotification', {content: 'Logged in', color: 'success'});
            } else {
                await context.dispatch('actionLogOut');
            }
        } catch (err) {
            if (!!err.isAxiosError && !err.response) { // See https://github.com/axios/axios/issues/383
                context.commit('setNetworkError', true);
                console.log('There was a network error.');
            } else {
                console.log('Name', err.name)
                context.commit('setLogInError', true);
                await context.dispatch('actionLogOut');
            }
        }
    },
    async actionCheckLoggedIn(context) {
        if (!context.state.isLoggedIn) {
            let token = context.state.token;
            if (!token) {
                const localToken = getLocalToken();
                if (localToken) {
                    context.commit('setToken', localToken);
                    token = localToken;
                }
            }
            if (token) {
                try {
                    const response = await server_api.getMe(token);
                    context.commit('setLoggedIn', true);
                    context.commit('setUserProfile', response.data);
                } catch (error) {
                    await context.dispatch('actionRemoveLogIn')
                }
            } else {
                await context.dispatch('actionRemoveLogIn')
            }
        }
    },
    async actionRemoveLogIn(context) {
        removeLocalToken();
        context.commit('setToken', '');
        context.commit('setLoggedIn', false);
    },
    async actionLogOut(context) {
        await context.dispatch('actionRemoveLogIn');
        await context.dispatch('actionRouteLogOut');
    },
    async actionUserLogOut(context) {
        await context.dispatch('actionLogOut');
        context.commit('addNotification', {content: 'Logged out', color: 'success'});
    },
    actionRouteLogOut() {
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    },
    actionRouteLoggedIn() {
        if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
            router.push('/main');
        }
    },

    async actionPasswordRecovery(context, payload) {
        const loadingNotification = {content: 'Sending password recovery email', showProgress: true};
        try {
            context.commit('addNotification', loadingNotification);
            await Promise.all([
                server_api.passwordRecovery(payload.username),
                await new Promise((resolve) => setTimeout(() => resolve(), 500)),
            ]);
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Password recovery email sent', color: 'success'});
            await context.dispatch('actionLogOut');
        } catch (error) {
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {color: 'error', content: 'Incorrect username'});
        }
    },
    async actionResetPassword(context, payload) {
        const loadingNotification = {content: 'Resetting password', showProgress: true};
        try {
            context.commit('addNotification', loadingNotification);
            await Promise.all([
                server_api.resetPassword(payload.password, payload.token),
                await new Promise((resolve) => setTimeout(() => resolve(), 500)),
            ]);
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Password successfully reset', color: 'success'});
            await context.dispatch('actionLogOut');
        } catch (error) {
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {color: 'error', content: 'Error resetting password'});
        }
    },
};

