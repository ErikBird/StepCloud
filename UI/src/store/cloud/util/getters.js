export const getters = {
    hasAdminAccess: (state) => {
        return (
            state.userProfile &&
            state.userProfile.is_superuser && state.userProfile.is_active);
    },
    loginError: (state) => state.logInError,
    networkError: (state) => state.networkError,
    dashboardShowDrawer: (state) => state.dashboardShowDrawer,
    dashboardMiniDrawer: (state) => state.dashboardMiniDrawer,
    token: (state) => state.token,
    isLoggedIn: (state) => state.isLoggedIn,
    setupDialogue: (state) => state.setupDialogue,
    firstNotification: (state) => state.notifications.length > 0 && state.notifications[0],
};
