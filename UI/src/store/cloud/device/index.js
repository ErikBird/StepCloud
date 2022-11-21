import {mutations} from './mutations';
import {getters} from './getters';
import {actions} from './actions';

const defaultState = {
    devices: [],
};

export const deviceModule = {
    namespaced: true,
    state: defaultState,
    mutations,
    actions,
    getters,
};
