// Pinia Store
import {defineStore} from 'pinia'
import {server_api} from "@/helpers/server_api";
import {useAuthStore} from './auth'
import {useUtilStore} from './util'


export const useUserStore = defineStore('user', {
    // convert to a function
    state: () => ({
        user: {},
    }),
    actions: {
        async actionGetUserMe() {
            const auth = useAuthStore()
            const util = useUtilStore()
            try {
                const response = await server_api.getMe(auth.token);
                if (response.data) {
                    this.user = response.data
                }
            } catch (error) {
                util.actionCheckApiError(error)
                //await context.dispatch('actionCheckApiError', error);
            }
        },
        async actionUpdateUserMe(payload) {
            const auth = useAuthStore()
            const util = useUtilStore()
            try {
                //const loadingNotification = { content: 'saving', showProgress: true };
                //context.commit('addNotification', loadingNotification);
                await Promise.all([
                    server_api.updateMe(auth.state.token, payload),
                    await new Promise((resolve) => setTimeout(() => resolve(), 500)),
                ])
                await this.actionGetCustomerDevices()
                //context.commit('removeNotification', loadingNotification);
                //context.commit('addNotification', { content: 'Customer Device successfully updated', color: 'success' });
            } catch (error) {
                util.actionCheckApiError(error)
                //await context.dispatch('actionCheckApiError', error);
            }
        },
    }
})
