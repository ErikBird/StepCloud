<template>
  <v-container fluid>
    Hello
    <!--
    <v-data-iterator
        :items="logs"
        hide-default-footer
    >
      <template v-slot:default="props">
        <v-row>
          <v-col
              v-for="item in props.items"
              :key="item.id"
              cols="12"
              sm="12"
              md="12"
              lg="12"
          >
            <v-card>
              <v-card-title class="subheading font-weight-bold">
                {{ item.name }}
              </v-card-title>
              <v-divider></v-divider>
              <v-stepper>
                <v-stepper-header>
                  <v-stepper-step
                      complete-icon="mdi-printer-3d"
                      edit-icon="mdi-printer-3d"
                      color="green darken-3"
                      complete
                      editable
                      step="1"
                  >
                   Print
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                      complete-icon="mdi-water"
                      edit-icon="mdi-water"
                      color="green darken-3"
                      complete
                      editable
                      step="2"
                  >
                    Clean
                  </v-stepper-step>

                  <v-divider></v-divider>

                  <v-stepper-step
                      complete-icon="mdi-lightbulb-on"
                      edit-icon="mdi-lightbulb-on"
                      color="green darken-3"
                      step="3"
                      editable
                      complete
                  >
                    Curing
                  </v-stepper-step>
                </v-stepper-header>
              </v-stepper>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>-->
  </v-container>
</template>

<script>
export default {
  name: "Production",
  data() {
    return {
      build_log: []
    };
  },
  methods: {
    async getLogs() {
      this.devices.forEach((device) => {
        this.$store.dispatch('actionGetBuildLog', device.id);
        console.log(device.id)
      })
      this.build_log = this.$store.getters.getBuildLog;
    }
  },
  computed: {
    logs() {
      return [].concat.apply([], Object.values(this.$store.getters.getBuildLog));
    },
    devices() {
      return this.$store.getters.myDevices;
    },
  },
  /*
  created() {
    this.getLogs();
  },*/
}
</script>

<style scoped>

</style>
