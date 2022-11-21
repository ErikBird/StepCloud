// Pinia Store
import {defineStore} from 'pinia'
import {useAuthStore} from './auth'

export const useUtilStore = defineStore('util', {
    // convert to a function
    state: () => ({
        networkError: false,
        dashboardMiniDrawer: false,
        dashboardShowDrawer: true,
        notifications: [],
        error_message: ''
    }),
    actions: {
        async actionCheckApiError(payload) {
            console.log(payload)
            const auth = useAuthStore()
            if (payload.response.status === 401 || payload.response.status === 403) {
                await auth.actionLogOut()
            } else {
                this.error_message = payload.message
                setTimeout(() => {
                    this.error_message = '';
                }, 3000);
            }
        },

        addNotification(payload) {
            this.notifications.push(payload);
        },
        removeNotification(payload) {
            this.notifications = this.notifications.filter((notification) => notification !== payload);
        },
    }
})
