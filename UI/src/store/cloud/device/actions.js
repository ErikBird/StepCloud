import {server_api} from '@/helpers/server_api';

export const actions = {
    async actionGetDevices(context) {
        try {
            const response = await server_api.getDevices(context.rootState.util.token);
            if (response.data) {
                context.commit('setDevices', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
};

