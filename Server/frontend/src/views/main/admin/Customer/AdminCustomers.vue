<template>
  <v-container fluid>
    <v-data-iterator
        :items="customers"
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
          <CreateCustomer/>
        </v-toolbar>
      </template>

      <template>
        <v-row>
          <v-col
              v-for="customer in customers"
              :key="customer.id"
              cols="12"
              sm="6"
              md="4"
              lg="4"
          >
            <v-card>
              <v-card-title class="subheading font-weight-bold">
                <v-icon class="mr-2">mdi-account</v-icon>
                {{ customer.name }}
              </v-card-title>
              <v-card-subtitle class="text-left">
                <b>{{ $t('vat_id') }}:</b> {{ customer.vat_id }}
              </v-card-subtitle>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    text
                    color="primary"
                    :to="{name: 'AdminCustomerUsers', params: {id: customer.id, name: customer.name}}"
                >
                  {{ $t('drawer_user') }}
                </v-btn>
                <v-btn
                    text
                    color="primary"
                    :to="{name: 'AdminCustomerDevices', params: {id: customer.id, name: customer.name}}"
                >
                  {{ $t('drawer_devices') }}
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
import {mapState, mapGetters} from 'vuex';

export default {
  name: "AdminCustomer",
  components: {
    CreateCustomer: () => import('./CreateCustomer.vue'),
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
    await this.$store.dispatch('actionGetCustomers');
  },
  computed: {
    ...mapState([
      'customers',
    ]),
    ...mapGetters([
      'adminCustomers',
    ]),
    customers() {
      return this.$store.getters.adminCustomers;
    }
  }
}
</script>

<style scoped>

</style>
