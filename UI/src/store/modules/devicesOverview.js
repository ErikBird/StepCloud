import {gateway_api} from "@/helpers/gateway_api";

// shape: [{ id, quantity }]
const state = () => ({
    devices: [],
})

const getters = {
    devices: (state) => state.devices,
}

const actions = {
    async actionGetDevices(context) {
        try {
            const response = await gateway_api.getMyDevices();
            if (response.data) {
                context.commit('setDevices', response.data);
            }
        } catch (error) {
            await context.dispatch('actionCheckEngineApiError', error);
        }
    },
}

const mutations = {
    addDevice(state, device_name) {
        state.devices.push({'name': device_name, 'status': []})
    },
    addStatus(state, payload) {
        //should only be one since name should be unique
        let devices_with_name = state.devices.filter(function (el) {
            return el.name === payload.name;
        });
        if (devices_with_name.length > 0) {
            devices_with_name[0].status.push(payload.message)
        }
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
