import {api} from '@/services/server_api';


export const actions = {
    async actionGetUsers(context) {
        try {
            const response = await api.getUsers(context.rootState.main.token);
            if (response) {
                context.commit('setUsers', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionUpdateUser(context, payload) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            context.commit('addNotification', loadingNotification);
            const response = (await Promise.all([
                api.updateUser(context.rootState.main.token, payload.id, payload.user),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('setUsers', response.data);
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'User successfully updated', color: 'success'});
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionCreateUser(context, payload) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            context.commit('addNotification', loadingNotification);
            const response = (await Promise.all([
                api.createUser(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('setUser', response.data);
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'User successfully created', color: 'success'});
            await context.dispatch('actionGetUsers');
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionGetCustomers(context) {
        try {
            const response = await api.getCustomers(context.rootState.main.token);
            if (response) {
                context.commit('setCustomers', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionGetDeviceCustomers(context, payload) {
        try {
            const response = await api.getDeviceCustomers(context.rootState.main.token, payload.customerId);
            if (response) {
                context.commit('setDevices', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionCreateCustomer(context, payload) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            context.commit('addNotification', loadingNotification);
            const response = (await Promise.all([
                api.createCustomers(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'User successfully created', color: 'success'});
            await context.dispatch('actionGetCustomers');
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
};
