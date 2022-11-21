<template>
  <div>
    <DeviceOverview></DeviceOverview>
    Devices: {{ devices }}

  </div>
</template>

<script>
import DeviceOverview from "@/views/DeviceOverview/DeviceOverview";
import {useCustomerDeviceStore} from '@/stores/customer-device'

export default {
  setup() {
    const customerDeviceStore = useCustomerDeviceStore()
    return {customerDeviceStore}
  },
  name: "Dashboard",
  components: {DeviceOverview},
  methods: {
    getDevices() {
      this.customerDeviceStore.actionGetCustomerDevices()
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
