import {mutations} from './mutations';
import {getters} from './getters';
import {actions} from './actions';

const defaultState = {
    userProfile: null,
};

export const userModule = {
    namespaced: true,
    state: defaultState,
    mutations,
    actions,
    getters,
};
