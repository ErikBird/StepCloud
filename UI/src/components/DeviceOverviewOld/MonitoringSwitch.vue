<template>
  <v-switch
      class="ma-0 pa-0"
      hide-details
      :disabled="disabled && !daniel.monitoring"
      :input-value="daniel.monitoring"
      @change="changeState"
  ></v-switch>
</template>

<script>
const ipc = require('electron').ipcRenderer;
export default {
  name: "MonitoringSwitch",
  props: ['daniel', 'disabled'],
  methods: {
    changeState() {
      console.log("Switch ", this.daniel.monitoring, this.daniel.network_ip);
      if (this.daniel.monitoring) {
        this.$store.commit('setStatusStop');
      } else {
        console.log('message-to-worker', this.daniel.network_ip);
        ipc.send('message-to-worker', {
          command: 'start_monitoring', payload: (' ' + this.daniel.network_ip).slice(1)
        });
      }
      this.$store.dispatch('actionGetMyDevices')
    },
  }
}
</script>

<style scoped>

</style>
