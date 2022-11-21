export const getters = {
    adminUsers: (state) => state.users,
    adminOneUser: (state) => (userId) => {
        const filteredUsers = state.users.filter((user) => user.id === userId);
        if (filteredUsers.length > 0) {
            return {...filteredUsers[0]};
        }
    },
    adminUsersByCustomer: (state) => (customerId) => {
        return state.users.filter((user) => user.customer.id === customerId);
    },
    adminDevicesByCustomer: (state) => (customerId) => {
        console.log(state.devices)
        return state.devices.filter((device) => device.customer.id === customerId);
    },
    adminCustomers: (state) => state.customers,
};

