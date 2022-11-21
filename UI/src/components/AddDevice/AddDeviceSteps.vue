<template>
  <v-stepper v-model="e1">
    <v-stepper-header>
      <v-stepper-step
          :complete="e1 > 1"
          step="1"
      >
        {{ $t('AddDeviceSteps.step_select') }}
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step
          :complete="e1 > 2"
          step="2"
      >
        {{ $t('AddDeviceSteps.step_configure') }}
      </v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-tabs
            v-model="tabs"
        >
          <v-tab
              key="key_automatic"
          >
            {{ $t('AddDeviceSteps.automatic') }}
          </v-tab>
          <v-tab
              key="key_manual"
          >
            {{ $t('AddDeviceSteps.manual') }}
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tabs">
          <v-tab-item
              key="key_automatic"
          >
            <AutomaticDiscovery @close="close" @select="to_step_two"></AutomaticDiscovery>
          </v-tab-item>
          <v-tab-item
              key="key_manual"
          >
            <ManualDiscovery @close="close" @select="to_step_two"></ManualDiscovery>
          </v-tab-item>
        </v-tabs-items>
      </v-stepper-content>
      <v-stepper-content step="2">
        <InterfaceConfiguration @close="close" @save="save"
                                :selected_interface="selected_interface"></InterfaceConfiguration>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script>

import AutomaticDiscovery from "@/components/AddDevice/AutomaticDiscovery";
import InterfaceConfiguration from "@/components/AddDevice/InterfaceConfiguration";
import ManualDiscovery from "@/components/AddDevice/ManualDiscovery";
import {useGatewayStore} from "@/stores/gateway";

export default {
  name: 'AddDeviceSteps',
  props: {
    open: Boolean
  },
  components: {ManualDiscovery, AutomaticDiscovery, InterfaceConfiguration},
  setup() {
    const gatewayStore = useGatewayStore()
    return {gatewayStore}
  },
  data() {
    return {
      e1: 1,
      tabs: null,
      selected_interface: null
    };
  },
  created() {
    this.interval = setInterval(function () {
      if (this.open) {
        this.gatewayStore.actionDiscoverInterfaces()
        this.gatewayStore.actionGetManualInterfaces()
      }
    }.bind(this), 5000);
  },
  beforeDestroy() {
    clearInterval(this.interval);
  },
  methods: {
    close() {
      this.e1 = 1
      this.$emit('close')
    },
    to_step_two(selected_interface) {
      this.selected_interface = selected_interface
      this.e1 = 2
    },
    save(configured_device) {
      console.log(configured_device)
      this.gatewayStore.actionConfigureDevice(configured_device)
      this.e1 = 1
      this.$emit('close')
    }
  },
};
</script>

<style scoped>

</style>
