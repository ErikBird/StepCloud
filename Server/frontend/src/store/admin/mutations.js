export const mutations = {
    setUsers(state, payload) {
        state.users = payload;
    },
    setUser(state, payload) {
        const users = state.users.filter((user) => user.id !== payload.id);
        users.push(payload);
        state.users = users;
    },
    setDevices(state, payload) {
        console.log('should be array')
        console.log(payload)
        state.devices = payload;
    },
    setCustomers(state, payload) {
        state.customers = payload;
    },
};
