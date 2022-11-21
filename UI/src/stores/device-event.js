// Pinia Store
import {defineStore} from 'pinia'
import {server_api} from "@/helpers/server_api";
import {useAuthStore} from './auth'
import {useUtilStore} from './util'


export const useDeviceEventStore = defineStore('sensor-event', {
    // convert to a function
    state: () => ({
        events: {},
        events_detail: {},
        eventLast: {}
    }),
    actions: {
        async actionGetDeviceEvents(customer_device_id) {
            const auth = useAuthStore()
            const util = useUtilStore()
            try {
                const response = await server_api.getDeviceEvents(auth.token, customer_device_id);
                this.events = {
                    ...this.events,
                    [customer_device_id]: response.data
                }
            } catch (error) {
                util.actionCheckApiError(error)
            }
        },
        async actionGetDeviceEventLast(customer_device_id) {
            const auth = useAuthStore()
            const util = useUtilStore()
            try {
                const response = await server_api.getDeviceEventLast(auth.token, customer_device_id);

                if (response.data) {
                    // Update state like this to break any object references
                    // Otherwise the state does not update bc. it does not detect changes
                    this.eventLast = {
                        ...this.eventLast,
                        [customer_device_id]: response.data
                    }
                }
            } catch (error) {
                util.actionCheckApiError(error)
            }
        },
        async actionGetDeviceEvent(customer_device_id, event_id) {
            const auth = useAuthStore()
            const util = useUtilStore()
            try {
                console.log(event_id)
                const response = await server_api.getDeviceEvent(auth.token, customer_device_id, event_id);

                if (response.data) {
                    // Update state like this to break any object references
                    // Otherwise the state does not update bc. it does not detect changes
                    this.events_detail = {
                        ...this.events_detail,
                        [customer_device_id]: {
                            ...this.events_detail[customer_device_id],
                            [event_id]: response.data
                        }
                    }
                }
            } catch (error) {
                util.actionCheckApiError(error)
            }
        },
    }
})
