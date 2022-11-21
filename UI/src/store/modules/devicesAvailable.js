import {gateway_api} from "@/helpers/gateway_api";

// shape: [{ id, quantity }]
const state = () => ({
    devices: [],
    loading: false
})

const getters = {
    devices: (state) => state.devices,
}

const actions = {
    async actionGetDevices(context) {
        try {
            context.commit('setLoading', true);
            const response = await gateway_api.getMyDevices();
            context.commit('setLoading', false);
            if (response.data) {
                context.commit('setDevices', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckEngineApiError', error);
        }
    },
    async activateDevice(context, device_name) {
        try {
            await gateway_api.activateDevice(device_name);
            context.commit('devicesOverview/addDevice', device_name, {root: true})
        } catch (error) {
            await context.dispatch('actionCheckEngineApiError', error);
        }
    }
}

const mutations = {
    setDevices(state, payload) {
        state.devices = payload;
    },
    setLoading(state, payload) {
        state.loading = payload
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
