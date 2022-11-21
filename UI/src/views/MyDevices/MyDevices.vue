<template>
  <v-container fluid>
    <v-data-iterator
        :items="devices"
        hide-default-footer
    >
      <template v-slot:header>
        <v-toolbar
            rounded
            dense
            class="mb-2"
        >
          <v-spacer></v-spacer>
          <v-btn
              class="ma-5"
              @click="openSetupDialoge"
          >
            {{ $t('DeviceOverview.add_device') }}
          </v-btn>
          <v-dialog
              v-model="showDialogue"
              width="800"
          >
            <AddDeviceSteps :open=showDialogue @close="showDialogue = false"></AddDeviceSteps>
          </v-dialog>
        </v-toolbar>
      </template>

      <template v-slot:default="props">

        <v-row>
          <v-col
              v-for="item in props.items"
              :key="item.gateway_id"
              cols="12"
              sm="6"
              md="4"
              lg="3"
          >
            <v-card>
              <v-card-title>{{ item.label }}</v-card-title>
              <v-img
                  max-height="150"
                  max-width="250"
                  contain
                  :src="getImagePath(item)"
              ></v-img>
              <v-card-text>
                {{ item.device.supplier.name }} {{ item.device.name }}
              </v-card-text>
              <ProgressBar :gateway_id="item.gateway_id"></ProgressBar>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="primary"
                    text
                    :to="/my-devices/+item.id"
                >
                  Open
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
</template>

<script>
import {useCustomerDeviceStore} from '@/stores/customer-device'
import AddDeviceSteps from "@/components/AddDevice/AddDeviceSteps";
import ProgressBar from '@/components/GatewayState/ProgressBar';

export default {
  setup() {
    const customerDeviceStore = useCustomerDeviceStore()
    return {customerDeviceStore}
  },
  components: {
    AddDeviceSteps,
    ProgressBar,
  },
  name: "Dashboard",
  data() {
    return {
      publicPath: process.env.BASE_URL,
      showDialogue: false,
    }
  },

  methods: {
    getDevices() {
      this.customerDeviceStore.actionGetCustomerDevices()
    },
    getImagePath(item) {
      return this.publicPath + "device_images/" + item.device.image_path
    },
    openSetupDialoge() {
      this.showDialogue = true;
    },
  },
  mounted() {
    this.getDevices()
  },
  computed: {
    devices() {
      return this.customerDeviceStore.devices
    },
  }
}
</script>

<style scoped>

</style>