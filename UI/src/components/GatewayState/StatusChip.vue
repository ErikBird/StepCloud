<template>
  <div>
    <v-chip
        v-if="!(status === undefined)"
        class="ma-2"
        :color=color
        text-color="white"
    >{{ status }}
    </v-chip>
  </div>
</template>

<script>

import {useGatewayStateStore} from "@/stores/gateway-state";

export default {
  setup() {
    const gatewayStateStore = useGatewayStateStore()
    return {gatewayStateStore}
  },
  name: "StatusChip",
  props: ['gateway_id'],
  computed: {
    status() {
      return this.gatewayStateStore.status[this.gateway_id]
    },
    color() {
      if (this.status === 'online') {
        return 'green'
      } else if (this.status === 'offline') {
        return 'red'
      } else {
        return 'grey'
      }
    }
  }
}
</script>
