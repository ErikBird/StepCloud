// Pinia Store
import {defineStore} from 'pinia'
import {server_api} from "@/helpers/server_api";
import {useAuthStore} from './auth'
import {useUtilStore} from './util'


export const useCustomerDeviceStore = defineStore('customer-device', {
    // convert to a function
    state: () => ({
        devices: [],
    }),
    actions: {
        async actionGetCustomerDevices() {
            const auth = useAuthStore()
            const util = useUtilStore()
            try {
                const response = await server_api.getCustomerDevicesMe(auth.token);
                if (response.data) {
                    this.devices = response.data
                }
            } catch (error) {
                util.actionCheckApiError(error)
                //await context.dispatch('actionCheckApiError', error);
            }
        },
        async actionUpdateCustomerDevice(customer_device_id, payload) {
            const auth = useAuthStore()
            const util = useUtilStore()
            try {
                //const loadingNotification = { content: 'saving', showProgress: true };
                //context.commit('addNotification', loadingNotification);
                await Promise.all([
                    server_api.updateCustomerDevice(auth.state.token, customer_device_id, payload),
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
        async actionCreateCustomerDevice(payload) {
            const auth = useAuthStore()
            const util = useUtilStore()
            try {
                //const loadingNotification = { content: 'saving', showProgress: true };
                //context.commit('addNotification', loadingNotification);
                await Promise.all([
                    server_api.createCustomerDeviceMe(auth.state.token, payload),
                    await new Promise((resolve) => setTimeout(() => resolve(), 500)),
                ]);
                await this.actionGetCustomerDevices()
                //context.commit('removeNotification', loadingNotification);
                //context.commit('addNotification', { content: 'Device Customer successfully created', color: 'success' });
            } catch (error) {
                util.actionCheckApiError(error)
                //await context.dispatch('actionCheckApiError', error);
            }
        },
    }
})
