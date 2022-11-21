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
        sort-by="id"
        hide-default-footer
    >
      <template v-slot:header>
        <v-toolbar
        >
          <v-spacer></v-spacer>
          <v-btn class="ma-5" @click="showDialogue=true">Neues Gerät</v-btn>
        </v-toolbar>
      </template>
      <template v-slot:default="props">
        <v-row>
          <v-col
              v-for="device in props.items"
              :key="device.id"
              cols="12"
              sm="12"
              md="6"
              lg="4">
            <v-card>
              <v-list-item three-line class="ma-0 pa-0">
                <v-card
                    flat
                    tile
                >
                  <v-list-item-avatar
                      tile
                      size="120">
                    <DeviceImage
                        :device_type="device.device.name"></DeviceImage>
                  </v-list-item-avatar>
                </v-card>
                <v-list-item-content class="ma-0 pa-0">
                  <v-card
                      class="ma-0 pa-0 d-flex flex-column"
                      flat
                      tile
                      height='100%'
                  >
                    <v-app-bar
                        class="mb-5 pa-0"
                        color="white"
                        dense
                        flat
                    >
                      <v-spacer></v-spacer>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              color="green darken-3"
                              v-if="device.monitoring"
                              v-bind="attrs"
                              v-on="on"
                          >mdi-shield-check
                          </v-icon>
                        </template>
                        <span>{{ $t('DeviceOverview.monitoring_tooltip') }}</span>
                      </v-tooltip>

                      <MonitoringSwitch :daniel="device"
                                        :disabled="devices.some((d) => d.monitoring === true)"></MonitoringSwitch>

                    </v-app-bar>
                    <v-list-item-title class="font-weight-black">
                      {{ device.name }}
                    </v-list-item-title>
                    {{ device.network_ip }}
                    <v-list-item-content class="mr-5">
                      <DeviceProgress :device_ip="device.network_ip"></DeviceProgress>
                    </v-list-item-content>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <router-link :to="{name: 'DeviceDetails',params: {id:device.id}}"
                                   tag="button">
                        <v-btn small>
                          {{ $t("general.open") }}
                        </v-btn>
                      </router-link>
                      <router-link :to="{name: 'WebView',params: {ip:device.network_ip}}"
                                   tag="button">
                        <v-btn small>
                          <v-icon>
                            mdi-open-in-new
                          </v-icon>
                        </v-btn>
                      </router-link>
                    </v-card-actions>
                  </v-card>
                </v-list-item-content>
              </v-list-item>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
</template>

<script>

import MonitoringSwitch from "@/components/DeviceOverviewOld/MonitoringSwitch";
import AddDeviceSteps from "@/components/AddDevice/AddDeviceSteps";

export default {
  name: "DeviceOverview",
  data: () => ({
    showDialogue: false,
  }),
  components: {
    AddDeviceSteps,
    MonitoringSwitch,
    DeviceProgress: () => import('./DeviceProgress'),
    DeviceImage: () => import('../DeviceImage'),
  },
  methods: {
    openInNewTab(Address) {
      window.open('http://' + Address, "_blank");
    },
    openSetupDialoge() {
      this.$store.commit('setSetupDialogue', true);
    },
  },
  computed: {
    devices() {
      return this.$store.getters.myDevices;
    },
    status() {
      return this.$store.getters.getStatus
    },
    cannotAddDevices() {
      return !(Object.keys(this.$store.getters.getStatus).length === 0)
    }
  }
}
</script>

<style scoped>

</style>
