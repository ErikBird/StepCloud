<template>
  <div>
    <v-tooltip
        v-if="online"
        bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-icon
            small
            v-bind="attrs"
            v-on="on"
            color="green">
          mdi-access-point-network
        </v-icon>
      </template>
      <span>{{ $t('GatewayConnection.info_online') }}</span>
    </v-tooltip>
    <v-tooltip v-if="offline" bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-icon
            small
            v-bind="attrs"
            v-on="on"
            color="red">
          mdi-access-point-network-off
        </v-icon>
      </template>
      <span>{{ $t('GatewayConnection.info_offline') }}</span>
    </v-tooltip>
    <v-progress-circular
        :size="20"
        :width="3"
        v-if="loading"
        indeterminate
        color="primary"
    ></v-progress-circular>
    <v-dialog
        v-model="choose_office_dialog"
        width="500"
        persistent
    >
      <v-card>
        <v-card-title class="text-h6 grey lighten-2">
          {{ this.online }}
          {{ $t('GatewayConnection.select_office') }}
        </v-card-title>

        <v-list
            dense
            nav
        >
          <v-list-item
              v-for="office in this.offices"
              :key="office.id"
              @click="set_gateway_office_id(office.id)"
          >
            <v-list-item-content>
              <v-list-item-title>{{ office.name }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import {useGatewayStore} from "@/stores/gateway";
import {useUserStore} from "@/stores/user";
import {useGatewayStateStore} from "@/stores/gateway-state";

const NodeSSDPClient = require('node-ssdp').Client
const ssdpCliend = new NodeSSDPClient()


export default {
  setup() {
    const gatewayStore = useGatewayStore()
    const gatewayStateStore = useGatewayStateStore()
    const userStore = useUserStore()
    return {gatewayStore, userStore, gatewayStateStore}
  },
  name: "GatewayConnection",
  data() {
    return {
      choose_office_dialog: false,
    }
  },
  methods: {
    set_gateway_office_id(id) {
      this.gatewayStore.office_id = id
      this.choose_office_dialog = false
      this.gatewayStore.loading = false
      this.gatewayStore.online = true
      this.gatewayStore.actionSetupGateway()
    },
    discover_gateway() {
      ssdpCliend.on('response', async (headers,) => {
        // Dont use rinfo.address since the gateway has a differnt address in the developer mode
        this.gatewayStore.network_address = headers.LOCATION

        if (this.offices.length === 1) {
          this.gatewayStore.loading = true
          this.gatewayStore.office_id = this.offices[0].id
          await this.gatewayStore.actionSetupGateway()
          this.gateway_connection()
        } else {
          this.gatewayStore.loading = true
          this.open_choose_office_dialog()
        }
      });
      setInterval(() => {
        if (!(this.online || this.loading)) {
          console.log('discover_gateway')
          ssdpCliend.search('stepcloud:gateway');
        }
      }, 5000)
    },
    open_choose_office_dialog() {
      this.choose_office_dialog = true
    },
    gateway_connection() {
      const source = new EventSource("http://" + this.gatewayStore.network_address + "/api/v1/events/stream");
      // onerror version
      source.onerror = () => {
        this.gatewayStore.online = false
        source.close()
        console.log("An error occurred while attempting to connect.");
      };

      source.onmessage = (data) => {
        let message_data = JSON.parse(data.data)
        console.log(message_data)
        if (message_data.typ === 'status') {
          this.gatewayStateStore.actionAddStatus(message_data.gateway_id, message_data.data)
        } else if (message_data.typ === 'progress') {
          this.gatewayStateStore.actionAddProgress(message_data.gateway_id, message_data.data)
        } else if (message_data.typ === 'load') {
          this.gatewayStateStore.actionAddStatus(message_data.gateway_id, 'online')
          this.gatewayStateStore.actionAddLoad(message_data.gateway_id, message_data.data)
        }
      };
    }
  },

  mounted() {
    this.discover_gateway()
  },
  computed: {
    online() {
      return this.gatewayStore.online && !this.loading
    },
    offline() {
      return !this.gatewayStore.online && !this.loading
    },
    loading() {
      return this.gatewayStore.loading
    },
    offices() {
      if (this.userStore.user.customer === undefined) {
        return []
      } else {
        return this.userStore.user.customer.offices
      }

    }
  }
}
</script>
