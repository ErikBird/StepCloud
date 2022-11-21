export const mutations = {
    setToken(state, payload) {
        state.token = payload;
    },
    setLoggedIn(state, payload) {
        state.isLoggedIn = payload;
    },
    setLogInError(state, payload) {
        state.logInError = payload;
    },
    setUserProfile(state, payload) {
        state.userProfile = payload;
    },
    setDashboardMiniDrawer(state, payload) {
        state.dashboardMiniDrawer = payload;
    },
    setDashboardShowDrawer(state, payload) {
        state.dashboardShowDrawer = payload;
    },
    addNotification(state, payload) {
        state.notifications.push(payload);
    },
    removeNotification(state, payload) {
        state.notifications = state.notifications.filter((notification) => notification !== payload);
    },
    setDevices(state, payload) {
        state.devices = payload;
    },
    setDeviceSupplier(state, payload) {
        state.deviceSupplier = payload;
    },
};

