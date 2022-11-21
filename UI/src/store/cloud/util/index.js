import {mutations} from './mutations';
import {getters} from './getters';
import {actions} from './actions';

const defaultState = {
    isLoggedIn: null,
    setupDialogue: false,
    token: '',
    logInError: false,
    networkError: false,
    dashboardMiniDrawer: false,
    dashboardShowDrawer: true,
    notifications: [],
};

export const utilModule = {
    state: defaultState,
    mutations,
    actions,
    getters,
};
