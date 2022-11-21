import {mutations} from './mutations';
import {getters} from './getters';
import {actions} from './actions';

const defaultState = {
    users: [],
    devices: [],
    customers: [],
};

export const adminModule = {
    state: defaultState,
    mutations,
    actions,
    getters,
};
