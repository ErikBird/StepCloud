import {server_api} from '@/helpers/server_api';


export const actions = {
    async actionGetUserProfile(context) {
        try {
            const response = await server_api.getMe(context.state.token);
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
                server_api.updateMe(context.state.token, payload),
                await new Promise((resolve) => setTimeout(() => resolve(), 500)),
            ]))[0];
            context.commit('setUserProfile', response.data);
            context.commit('removeNotification', loadingNotification);
            context.commit('addNotification', {content: 'Profile successfully updated', color: 'success'});
        } catch (error) {
            await context.dispatch('actionCheckApiError', error);
        }
    },
};

