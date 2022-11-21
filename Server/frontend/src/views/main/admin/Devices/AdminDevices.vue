<template>
  <v-container fluid>
    <v-data-iterator
        :items="devices"
        :items-per-page.sync="itemsPerPage"
        :search="search"
        hide-default-footer
    >
      <template v-slot:header>
        <v-toolbar
            class="mb-1 rounded"
        >
          <v-text-field
              v-model="search"
              clearable
              flat
              solo-inverted
              hide-details
              prepend-inner-icon="search"
              label="Search"
              class="mr-5"
          ></v-text-field>
          <CreateDevice/>
        </v-toolbar>
      </template>

      <template>
        <v-row>
          <v-col
              v-for="device in devices"
              :key="device.id"
              cols="12"
              sm="6"
              md="4"
              lg="4"
          >
            <v-card>
              <v-card-title class="subheading">
                <v-icon class="mr-2">mdi-printer-3d</v-icon>
                <b>{{ device.supplier.name }}- </b>{{ device.name }}
              </v-card-title>
              <v-card-subtitle class="text-left">
                <b>{{ $t('identifier') }}:</b>
                <li class="ml-5" v-for="idf in device.identifier">
                  {{ idf }}
                </li>
              </v-card-subtitle>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    text
                    color="primary"
                    :to="{name: 'AdminCustomerUsers', params: {id: device.id, name: device.name}}"
                >
                  {{ $t('open') }}
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
import {mapGetters, mapState} from "vuex";

export default {
  name: "Device",
  components: {
    CreateDevice: () => import('./CreateDevice.vue'),
  },
  data() {
    return {
      itemsPerPageArray: [8, 12, 16],
      search: '',
      page: 1,
      itemsPerPage: 8,
    }
  },
  async created() {
    await this.$store.dispatch('actionGetDevices');
    await this.$store.dispatch('actionGetDeviceSupplier');
  },
  computed: {
    devices() {
      return this.$store.getters.devices;
    }
  }
}
</script>

<style scoped>

</style>
