import {api} from '@/services/server_api';
import router from '@/router';
import {getLocalToken, removeLocalToken, saveLocalToken} from '@/utils';


export const actions = {
    async actionLogIn(context, payload) {
        try {
            const response = await api.logInGetToken(payload.username, payload.password);
            const token = response.data.access_token;
            if (token) {
                saveLocalToken(token);
                context.commit('setToken', token);
                context.commit('setLoggedIn', true);
                context.commit('setLogInError', false);
                await context.dispatch('actionGetUserProfile');
                await context.dispatch('actionRouteLoggedIn');
                context.commit('addNotification', {content: 'Logged in', color: 'success'});
            } else {
                await context.dispatch('actionLogOut');
            }
        } catch (err) {
            context.commit('setLogInError', true);
            await context.dispatch('actionLogOut');
        }
    },
    async actionGetUserProfile(context) {
        try {
            const response = await api.getMe(context.state.token);
            if (response.data) {
                context.commit('setUserProfile', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionUpdateUserProfile(context, payload) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            context.commit('addNotification', loadingNotification);
            const response = (await Promise.all([
                api.updateMe(context.state.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('setUserProfile', response.data);
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Profile successfully updated', color: 'success'});
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
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
                    const response = await api.getMe(token);
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
    actionRouteLogOut(context) {
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    },
    async actionCheckApiError(context, payload) {
        if (payload.response.status === 401) {
            await context.dispatch('actionLogOut');
        }
    },
    actionRouteLoggedIn(context) {
        if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
            router.push('/main');
        }
    },
    async removeNotification(context, payload) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                context.commit('removeNotification', payload.notification);
                resolve(true);
            }, payload.timeout);
        });
    },
    async passwordRecovery(context, payload) {
        const loadingNotification = {content: 'Sending password recovery email', showProgress: true};
        try {
            context.commit('addNotification', loadingNotification);
            const response = (await Promise.all([
                api.passwordRecovery(payload.username),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Password recovery email sent', color: 'success'});
            await context.dispatch('actionLogOut');
        } catch (error) {
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {color: 'error', content: 'Incorrect username'});
        }
    },
    async resetPassword(context, payload) {
        const loadingNotification = {content: 'Resetting password', showProgress: true};
        try {
            context.commit('addNotification', loadingNotification);
            const response = (await Promise.all([
                api.resetPassword(payload.password, payload.token),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Password successfully reset', color: 'success'});
            await context.dispatch('actionLogOut');
        } catch (error) {
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {color: 'error', content: 'Error resetting password'});
        }
    },
    async actionGetDeviceSupplier(context) {
        try {
            const response = await api.getDeviceSupplier(context.rootState.main.token);
            if (response) {
                context.commit('setDeviceSupplier', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionCreateDeviceSupplier(context, payload) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            context.commit('addNotification', loadingNotification);
            const response = (await Promise.all([
                api.createDeviceSupplier(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Device Supplier successfully created', color: 'success'});
            await context.dispatch('actionGetDeviceSupplier');
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionGetDevices(context) {
        try {
            const response = await api.getDevices(context.rootState.main.token);
            if (response) {
                context.commit('setDevices', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionCreateDevice(context, payload) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            context.commit('addNotification', loadingNotification);
            const response = (await Promise.all([
                api.createDevices(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'User successfully created', color: 'success'});
            await context.dispatch('actionGetDevices');
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
};

