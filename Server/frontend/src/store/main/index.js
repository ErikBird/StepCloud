import {mutations} from './mutations';
import {getters} from './getters';
import {actions} from './actions';

const defaultState = {
    isLoggedIn: null,
    token: '',
    logInError: false,
    userProfile: null,
    dashboardMiniDrawer: false,
    dashboardShowDrawer: true,
    notifications: [],
    devices: [],
    deviceSupplier: [],
};

export const mainModule = {
    state: defaultState,
    mutations,
    actions,
    getters,
};
