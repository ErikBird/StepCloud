<template>
  <div v-if="!(total===0)">
    {{ current }} / {{ total }}
    <v-progress-linear
        v-if="!(total===0)"
        :value=progress
        rounded
    ></v-progress-linear>
  </div>
</template>

<script>
import {useGatewayStateStore} from "@/stores/gateway-state";

export default {
  setup() {
    const gatewayStateStore = useGatewayStateStore()
    return {gatewayStateStore}
  },
  name: "ProgressBar",
  props: ['gateway_id'],
  computed: {
    current() {
      if (this.gateway_id in this.gatewayStateStore.progress) {
        return this.gatewayStateStore.progress[this.gateway_id].current
      } else {
        return 0
      }
    },
    total() {
      if (this.gateway_id in this.gatewayStateStore.progress) {
        return this.gatewayStateStore.progress[this.gateway_id].total
      } else {
        return 0
      }
    },
    progress() {
      return this.current / this.total * 100
    }
  }
}
</script>

<style scoped>

</style>