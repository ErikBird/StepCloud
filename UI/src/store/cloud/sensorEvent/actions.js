import {server_api} from '@/helpers/server_api';


export const actions = {
    async actionGetDeviceEvents(context, customer_device_id) {
        try {
            const response = await server_api.getDeviceEvents(context.state.token, customer_device_id);
            if (response.data) {
                context.commit('setDeviceEvents', {id: customer_device_id, data: response.data});
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
    async actionGetDeviceEventLast(context, customer_device_id) {
        try {
            const response = await server_api.getDeviceEventLast(context.state.token, customer_device_id);
            if (response.data) {
                context.commit('setDeviceEventsLast', {id: customer_device_id, data: response.data});
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
};

