<template>
  <v-container fluid>
    <v-dialog
        v-model="showDialogue"
        persistent
        width="800"
    >
      <AddDeviceSteps @close="showDialogue = false"></AddDeviceSteps>
    </v-dialog>
    <v-data-iterator
        :items="devices"
        hide-default-footer
    >
      <template v-slot:header>
        <v-toolbar
            class="mb-2"
        >
          <v-spacer></v-spacer>
          <v-btn class="ma-5" @click="openSetupDialoge">{{ $t('DeviceOverview.add_device') }}</v-btn>
        </v-toolbar>
      </template>

      <template v-slot:item="props">
        <v-flex
            xs12
            sm6
            md4
            lg3
        >
          <v-card>
            <v-card-title>{{ props.item.name }}</v-card-title>
            <apexchart height="100" type="line" :options="options" :series="Theseries(props.item.status)"></apexchart>
          </v-card>
        </v-flex>
      </template>

    </v-data-iterator>
  </v-container>
</template>

<script>

import AddDeviceSteps from "@/components/AddDevice/AddDeviceSteps";

export default {
  name: "DeviceOverview2",
  data: () => ({
    showDialogue: false,
    options: {
      chart: {
        type: 'line',
        sparkline: {
          enabled: true
        }
      },
      stroke: {
        width: 1,
        curve: "stepline",
      },
      tooltip: {
        enabled: false,
      }
    },
  }),

  components: {
    AddDeviceSteps,
  },
  methods: {
    openInNewTab(Address) {
      window.open('http://' + Address, "_blank");
    },
    openSetupDialoge() {
      this.showDialogue = true;
      this.$store.dispatch('devicesAvailable/actionGetDevices');
    },
    Theseries(data) {
      return [{
        name: 'sensordata',
        data: data.filter(function (item) {
          return item[0] > (new Date().getTime() / 1000) - (200)
        }) // only the last 2 minute data
      }]
    }
  },
  computed: {
    devices() {
      return this.$store.getters['devicesOverview/device'];
    },
  }
}
</script>

<style scoped>

</style>
