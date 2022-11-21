import {mutations} from './mutations';
import {getters} from './getters';
import {actions} from './actions';

const defaultState = {
    events: {},
    eventLast: {}
};

export const deviceEventModule = {
    namespaced: true,
    state: defaultState,
    mutations,
    actions,
    getters,
};
