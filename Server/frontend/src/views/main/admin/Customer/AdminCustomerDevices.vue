<template>
  <v-container fluid>
    <v-toolbar light>
      <v-toolbar-title>
        {{ $route.params.name }} - {{ $t('drawer_devices') }}
      </v-toolbar-title>
    </v-toolbar>
    <v-data-table :headers="headers" :items="devices">
    </v-data-table>
  </v-container>
</template>

<script lang="js">
export default {
  name: "AdminCustomerDevices",
  components: {},
  data() {
    return {
      headers: [
        {
          text: 'Name',
          sortable: true,
          value: 'name',
          align: 'left',
        },
        {
          text: 'Device Name',
          sortable: true,
          value: 'device.name',
          align: 'left',
        },
        {
          text: 'Device Supplier',
          sortable: true,
          value: 'device.supplier.name',
          align: 'left',
        },
        {
          text: 'Network IP',
          sortable: false,
          value: 'network_ip',
          align: 'left',
        },
        {
          text: 'Monitoring',
          sortable: true,
          value: 'monitoring',
          align: 'left',
        },
      ],
    }
  },
  computed: {
    devices() {
      return this.$store.getters.adminDevicesByCustomer(this.$route.params.id);
    },
  },
  methods: {},
  mounted() {
    this.$store.dispatch('actionGetDeviceCustomers', {customerId: this.$route.params.id});
  }


}
</script>
