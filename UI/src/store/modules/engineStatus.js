const state = () => ({
    online: true,
})

const getters = {
    online: (state) => state.online,
}

const mutations = {
    updateOnline(state, status) {
        state.online = status
    },
}

export default {
    namespaced: true,
    state,
    getters,
    mutations
}
