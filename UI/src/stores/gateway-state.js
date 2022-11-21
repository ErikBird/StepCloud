// Pinia Store
import {defineStore} from 'pinia'

export const useGatewayStateStore = defineStore('gateway-state', {
    // convert to a function
    state: () => ({
        status: {},
        progress: {},
        load: {},
    }),
    actions: {
        async actionAddStatus(gateway_id, status) {
            this.status[gateway_id] = status
            this.status = {...this.status}// break any object references, so pinia update
        },
        async actionAddProgress(gateway_id, progress) {
            this.progress[gateway_id] = progress
            this.progress = {...this.progress}// break any object references, so pinia update
        },
        async actionAddLoad(gateway_id, load) {
            if (Object.prototype.hasOwnProperty.call(this.load, gateway_id)) {
                this.load[gateway_id].push(load)
                this.load[gateway_id] = this.load[gateway_id].slice(-20); //Keep only the last 20 Values to avoid to much data
                this.load = {...this.load}// break any object references, so pinia update
            } else {
                this.load[gateway_id] = [load]
            }
        },
    }
})
