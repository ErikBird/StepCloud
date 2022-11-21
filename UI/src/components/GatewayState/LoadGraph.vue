<template>
  <div>
    <v-sparkline
        v-if="!(load === undefined)"
        :smooth="16"
        :gradient="['#f72047', '#ffd200', '#1feaea']"
        :line-width="3"
        :value="load"
        auto-draw
        stroke-linecap="round"
    ></v-sparkline>
  </div>
</template>

<script>

import {useGatewayStateStore} from "@/stores/gateway-state";

export default {
  setup() {
    const gatewayStateStore = useGatewayStateStore()
    return {gatewayStateStore}
  },
  name: "LoadGraph",
  props: ['gateway_id'],
  computed: {
    load() {
      return this.gatewayStateStore.load[this.gateway_id]
    },
  }
}
</script>
