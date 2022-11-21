<template>
  <div>
    <v-card
        class="mb-5 pt-5"
    >

      <v-row no-gutters>
        <v-col cols="3">
          <div class="ml-10">
            <div class="text-h6 text-left mb-10">
              {{ device.device.supplier.name }} {{ device.device.name }}
            </div>
            <p v-if="!(device.network_ip ==='')" class="text-left">
              <b>Network IP:</b> {{ device.network_ip }}
            </p>
            <p v-if="!(device.registration_code ==='')" class="text-left">
              <b>Registration Code:</b> {{ device.registration_code }}</p>
            <p v-if="!(device.serial_number ==='')" class="text-left">
              <b>Serial </b> {{ device.serial_number }}</p>
          </div>
        </v-col>
        <v-col cols="4">
          <v-img
              max-height="150"
              max-width="250"
              contain
              :src="imagePath"
          ></v-img>
        </v-col>
        <v-col cols="2">
          <StatusChip :gateway_id=device.gateway_id></StatusChip>
          <LoadGraph :gateway_id=device.gateway_id></LoadGraph>
          <ProgressBar :gateway_id=device.gateway_id></ProgressBar>
        </v-col>

      </v-row>
      <v-card-subtitle>
      </v-card-subtitle>
    </v-card>
    <v-row>
      <v-col
          cols="12"
          sm="12"
          md="12"
          lg="6">
        <v-card>
          <v-card-title>
            {{ $t('DeviceDetail.' + eventLast.event_type.label) }}
          </v-card-title>
          <v-card-subtitle>{{ $t('DeviceDetail.last_event') }}</v-card-subtitle>
          <v-card-text>
            <EventDataVisualization :event="eventLast"></EventDataVisualization>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col
          cols="12"
          sm="12"
          md="12"
          lg="6">

        <v-card>
          <v-card-title>
            {{ $t('DeviceDetail.event_history') }}
          </v-card-title>
          <v-timeline>
            <v-timeline-item
                v-for="event in events"
                :key="event.id"
            >
              <template v-slot:opposite>
        <span
            :class="`font-weight-bold `"
            v-text="new Date(event.time_recorded).toDateString()"
        ></span>
              </template>
              <v-card>
                <v-card-title>
                  {{ $t('DeviceDetail.' + event.event_type.label) }}
                </v-card-title>
                <v-card-text>
                  <v-dialog
                      v-model="dialog"
                      width="600"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                          color="primary"
                          outlined
                          v-bind="attrs"
                          v-on="on"
                          @click="getDeviceEventDetail(event.id)"
                      >
                        {{ $t('general.open') }}
                      </v-btn>
                    </template>

                    <v-card>
                      <v-card-text
                          v-if="events_detail">
                        <EventDataVisualization :event="events_detail[event.id]"></EventDataVisualization>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="primary"
                            @click="dialog = false"
                        >
                          {{ $t('general.close') }}
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-card-text>
              </v-card>
            </v-timeline-item>
          </v-timeline>
        </v-card>
      </v-col>
    </v-row>


  </div>

</template>

<script>
import {useCustomerDeviceStore} from '@/stores/customer-device'
import {useDeviceEventStore} from '@/stores/device-event'
import {useGatewayStateStore} from "@/stores/gateway-state";
import LoadGraph from '@/components/GatewayState/LoadGraph';
import StatusChip from '@/components/GatewayState/StatusChip';
import ProgressBar from '@/components/GatewayState/ProgressBar';
import EventDataVisualization from "@/components/DeviceEvent/EventDataVisualization";

export default {
  setup() {
    const customerDeviceStore = useCustomerDeviceStore()
    const deviceEventStore = useDeviceEventStore()
    const gatewayStateStore = useGatewayStateStore()
    return {customerDeviceStore, deviceEventStore, gatewayStateStore}
  },
  name: "DeviceDetail",
  components: {
    EventDataVisualization,
    LoadGraph,
    ProgressBar,
    StatusChip
  },
  data() {
    return {
      publicPath: process.env.BASE_URL,
      dialog: false,
    }
  },
  props: ['id'],
  methods: {
    getDeviceEvents() {
      this.deviceEventStore.actionGetDeviceEventLast(this.id)
      this.deviceEventStore.actionGetDeviceEvents(this.id)
    },
    getDeviceEventDetail(event_id) {
      this.deviceEventStore.actionGetDeviceEvent(this.id, event_id)
    }
  },
  computed: {

    device() {
      return this.customerDeviceStore.devices.filter(device => parseInt(device.id) === parseInt(this.id))[0]
    },
    events() {
      return this.deviceEventStore.events[this.id]
    },
    events_detail() {
      return this.deviceEventStore.events_detail[this.id]
    },
    eventLast() {
      if (Object.keys(this.deviceEventStore.eventLast).length === 0) {
        return []
      } else {
        return this.deviceEventStore.eventLast[this.id]
      }
    },
    imagePath() {
      return this.publicPath + "device_images/" + this.device.device.image_path
    },
  },
  mounted() {
    this.getDeviceEvents()
  },
}
</script>

<style scoped>
</style>