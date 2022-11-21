export const mutations = {
    setDeviceEvents(state, payload) {
        state.events[payload.id] = payload.data;
    },
    setDeviceEventsLast(state, payload) {
        state.eventLast[payload.id] = payload.data;
    },
};

