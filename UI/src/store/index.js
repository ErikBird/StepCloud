import Vue from 'vue'
import Vuex from 'vuex'

import {utilModule} from './cloud/util';
import {deviceModule} from './cloud/device';
import {userModule} from "@/store/cloud/user";
import {customerDeviceModule} from "@/store/cloud/customerDevice";
import {deviceEventModule} from "@/store/cloud/sensorEvent";

//import devicesAvailable from "@/store/modules/devicesAvailable";
//import devicesOverview from "@/store/modules/devicesOverview";
//import engineStatus from "@/store/modules/engineStatus";

Vue.use(Vuex)


const storeOptions = {
    modules: {
        util: utilModule, //includes Login
        device: deviceModule,
        user: userModule,
        customerDevice: customerDeviceModule,
        deviceEvent: deviceEventModule,
        //devicesAvailable,
        //devicesOverview,
        //engineStatus,
    },
};

export const store = new Vuex.Store(storeOptions);

export default store;

