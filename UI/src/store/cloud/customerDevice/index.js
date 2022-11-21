import {mutations} from './mutations';
import {getters} from './getters';
import {actions} from './actions';

const defaultState = {
    devices: null,
};

export const customerDeviceModule = {
    namespaced: true,
    state: defaultState,
    mutations,
    actions,
    getters,
};
