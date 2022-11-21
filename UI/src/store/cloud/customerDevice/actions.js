import {server_api} from '@/helpers/server_api';


export const actions = {
    async actionGetCustomerDevices(context) {
        try {
            console.log(context.getters)
            console.log(context.state.token)
            const response = await server_api.getCustomerDevicesMe(context.getters.token);
            if (response.data) {
                context.commit('setCustomerDevices', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionUpdateCustomerDevice(context, customer_device_id, payload) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            context.commit('addNotification', loadingNotification);
            await Promise.all([
                server_api.updateCustomerDevice(context.rootState.util.token, customer_device_id, payload),
                await new Promise((resolve) => setTimeout(() => resolve(), 500)),
            ])
            await context.dispatch('actionGetCustomerDevices')
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Customer Device successfully updated', color: 'success'});
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionCreateCustomerDevice(context, payload) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            context.commit('addNotification', loadingNotification);
            await Promise.all([
                server_api.createCustomerDeviceMe(context.rootState.util.token, payload),
                await new Promise((resolve) => setTimeout(() => resolve(), 500)),
            ]);
            await context.dispatch('actionGetCustomerDevices')
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Device Customer successfully created', color: 'success'});
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
};

