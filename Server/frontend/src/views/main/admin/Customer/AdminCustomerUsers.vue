<template>
  <v-container fluid>
    <v-toolbar light>
      <v-toolbar-title>
        {{ $route.params.name }} - {{ $t('drawer_user') }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <CreateUser :cusomerID="this.$route.params.id"></CreateUser>
    </v-toolbar>
    <v-data-table :headers="headers" :items="users">
    </v-data-table>
  </v-container>
</template>

<script lang="js">
import CreateUser from "@/views/main/admin/Customer/CreateUser";
import {extend} from 'vee-validate'

extend('password', {
  params: ['target'],
  validate(value, {target}) {
    return value === target;
  },
  message: 'Password confirmation does not match'
});

export default {
  name: "AdminCustomerUsers",
  components: {CreateUser},
  data() {
    return {

      headers: [
        {
          text: 'System ID',
          value: 'id',
          align: 'left'
        },
        {
          text: 'Full Name',
          sortable: true,
          value: 'full_name',
          align: 'left',
        },
        {
          text: 'Email',
          sortable: true,
          value: 'email',
          align: 'left',
        },
        {
          text: 'Is Active',
          sortable: true,
          value: 'isActive',
          align: 'left',
        },
        {
          text: 'Is Superuser',
          sortable: true,
          value: 'isSuperuser',
          align: 'left',
        },
      ],
    }
  },
  computed: {
    users() {
      return this.$store.getters.adminUsersByCustomer(this.$route.params.id);
    },
  },
  methods: {},
  mounted() {
    this.$store.dispatch('actionGetUsers');
  }

}
</script>
