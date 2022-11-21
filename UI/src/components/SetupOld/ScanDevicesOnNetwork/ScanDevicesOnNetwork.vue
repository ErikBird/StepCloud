<template>
  <v-card
      flat
      class="mb-12"
      min-height="200px"
  >
    <v-card-title>
      {{ $t('ScanDevicesOnNetwork.title') }}
    </v-card-title>
    <v-card-subtitle>
      {{ $t('ScanDevicesOnNetwork.explanation') }}
    </v-card-subtitle>
    <v-card-text>
      <v-tabs>
        <v-tab key="search">
          {{ $t('general.search') }}
        </v-tab>
        <v-tab-item key="search">
          <v-card flat>
            <DeviceSearch @continue="this.continue" @cancel="this.cancel"/>
          </v-card>
        </v-tab-item>
        <v-tab key="manual">
          {{ $t('ScanDevicesOnNetwork.manual') }}
        </v-tab>
        <v-tab-item key="manual">
          <v-card flat>
            <DeviceManual @continue="this.continue" @cancel="this.cancel"/>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-card-text>
  </v-card>
</template>

<script>

import DeviceSearch from "@/components/SetupOld/ScanDevicesOnNetwork/DeviceSearch";
import DeviceManual from "@/components/SetupOld/ScanDevicesOnNetwork/DeviceManual"

export default {
  name: 'ScanDevicesOnNetwork',
  components: {DeviceSearch, DeviceManual},
  data() {
    return {
      tab: null,
    };
  },
  methods: {
    continue(device) {
      this.$emit('continue', device);
    },
    cancel() {
      this.$emit('cancel');
    },
  },
  created() {
    this.$store.dispatch('actionGetDevices');
    this.$store.dispatch('actionGetMyDevices');
  },
};
</script>

<style scoped>

</style>
