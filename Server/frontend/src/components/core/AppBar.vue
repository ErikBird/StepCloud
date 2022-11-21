<template>
  <v-app-bar
      app
      clipped-left
      dense
      color="blue-grey darken-4"
  >
    <v-toolbar-title class="title">
      <img src="../../assets/stepcloud_logo_long_dark.svg" width="130px">
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <LocaleSwitcher :color="['blue-grey darken-4', true]"/>
    <v-menu
        bottom
        open-on-hover
        left
        offset-y>
      <template v-slot:activator="{ on }">
        <v-btn
            icon
            v-on="on"
        >
          <v-avatar>
            <v-icon color="white">account_circle</v-icon>
          </v-avatar>
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="logout()">
          <v-icon left>mdi-logout</v-icon>
          <v-list-item-title>{{ $t("logout") }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>
<script>
import LocaleSwitcher from './LocaleSwitcher';
import {dispatchUserLogOut} from '../../store/main/actions';

export default {
  components: {LocaleSwitcher},
  methods: {
    async logout() {
      await this.$store.dispatch('actionUserLogOut');
      this.$router.push({name: 'Products'});
    },
  },
};
</script>
