export const mutations = {
    setToken(state, payload) {
        state.token = payload;
    },
    setLoggedIn(state, payload) {
        state.isLoggedIn = payload;
    },
    setSetupDialogue(state, payload) {
        state.setupDialogue = payload;
    },
    setLogInError(state, payload) {
        state.logInError = payload;
    },
    setNetworkError(state, payload) {
        state.networkError = payload;
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
};

