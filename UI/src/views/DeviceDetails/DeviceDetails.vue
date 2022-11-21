<template>
  <v-card
      flat
      tile
      color="grey lighten-4"
      max-width="1600px"
  >
    <v-container fluid>
      <v-row dense>
        <v-col
            cols="12"
            sm="12"
            md="12"
            lg="6">
          <BuildLogTable v-bind:log="build_log"></BuildLogTable>
        </v-col>
        <v-col
            cols="12"
            sm="12"
            md="12"
            lg="6">

          <DeviceCalendar v-bind:events="build_log"></DeviceCalendar>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
// started - ended
export default {
  name: 'DeviceDetails.vue',
  components: {
    BuildLogTable: () => import('./BuildLogTable'),
    DeviceCalendar: () => import('./DeviceCalendar')
  },
  data() {
    return {
      build_log: []
    };
  },
  methods: {
    async getLogs() {
      await this.$store.dispatch('actionGetBuildLog', this.$route.params.id);
      this.build_log = this.$store.getters.getBuildLog[this.$route.params.id];
    }
  },
  computed: {
    logs() {
      return this.$store.getters.getBuildLog;
    }
  },
  created() {
    this.getLogs();
  },
};
</script>

<style scoped>

</style>
