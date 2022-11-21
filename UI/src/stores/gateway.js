// Pinia Store
import {defineStore} from 'pinia'
import {useAuthStore} from "@/stores/auth";
import {useCustomerDeviceStore} from "@/stores/customer-device";
import {server_api} from "@/helpers/server_api";
import {gateway_api} from "@/helpers/gateway_api";

export const useGatewayStore = defineStore('gateway', {
    // convert to a function
    state: () => ({
        online: false,
        loading: false,
        network_address: '',
        office_id: null,
        config: null,
        discovered_interfaces: [],
        error_log: [],
        manual_interfaces: []
    }),
    actions: {
        async actionSetupGateway() {
            await this.actionGetGatewayConfig()
            if (!this.config.authenticated) {
                await this.actionAuthenticate()
                this.online = true
                this.loading = false
            } else {
                this.online = true
                this.loading = false
            }
        },
        async actionGetErrorLog() {
            try {
                const response = await gateway_api.getErrorLog(this.network_address);
                if (response.data) {
                    this.error_log = response.data
                }
            } catch (error) {
                console.log(error)
            }
        },
        async actionGetGatewayConfig() {
            try {
                const response = await gateway_api.getGatewayConfig(this.network_address);
                if (response.data) {
                    this.config = response.data
                }
            } catch (error) {
                console.log(error)
            }
        },
        async actionConfigureDevice(payload) {
            try {
                const customerDevice = useCustomerDeviceStore()
                await gateway_api.postConfigureDevice(this.network_address, payload.gateway_id, payload.device_type)
                await customerDevice.actionGetCustomerDevices()
            } catch (error) {
                console.log(error)
            }
        },
        async actionGetManualInterfaces() {
            try {
                const response = await gateway_api.getManualInterfaces(this.network_address);
                if (response.data) {
                    this.manual_interfaces = response.data
                }
            } catch (error) {
                console.log(error)
            }
        },
        async actionDiscoverInterfaces() {
            try {
                const response = await gateway_api.getDiscoverInterfaces(this.network_address);
                if (response.data) {
                    this.discovered_interfaces = response.data
                }
            } catch (error) {
                console.log(error)
            }
        },
        async actionAuthenticate() {
            console.log('actionAuthenticate')
            const auth = useAuthStore()
            try {
                let gateway_payload = {
                    "uuid": this.config.uuid,
                    "customer_office_id": this.office_id,
                    "serial_number": this.config.serial_number,
                    "software_version": this.config.software_version,
                    "hardware_version": this.config.hardware_version
                }
                const response = await server_api.createGateway(auth.token, gateway_payload);
                if (response.data) {
                    let gateway_token = response.data
                    let gateway_response = await gateway_api.postAuthToken(this.network_address, gateway_token);
                    if (gateway_response.data) {
                        this.config = gateway_response.data
                    }
                }
            } catch (error) {
                console.log(error)
                //await context.dispatch('actionCheckApiError', error);
            }
        },
    }
})
