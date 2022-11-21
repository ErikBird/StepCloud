<template>
  <v-app-bar
      app
      clipped-left
      dense
      dark
      color="blue-grey darken-4"
  >
    <v-toolbar-title class="title">
      <img src="../../assets/stepcloud_logo_long_dark.svg" width="130px" alt="">
    </v-toolbar-title>
    <v-chip
        class="ma-5"
        small
        outlined
    >
      Version: {{ currentAppVersion }}
    </v-chip>

    <v-spacer></v-spacer>
    <EngineConnectionIndicator></EngineConnectionIndicator>
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
            <v-icon color="white">mdi-account-circle</v-icon>
          </v-avatar>
        </v-btn>
      </template>
      <v-list>
        <v-list-item>{{ userProfile.email }}</v-list-item>
        <v-list-item @click="logout()">
          <v-icon left>mdi-logout</v-icon>
          <v-list-item-title>{{ $t("nav.logout") }}</v-list-item-title>
        </v-list-item>
        <v-list-item @click="check_updates()">
          <v-icon left>mdi-logout</v-icon>
          <v-list-item-title>Check for Updates</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

  </v-app-bar>
</template>
<script>
import LocaleSwitcher from './LocaleSwitcher';
import EngineConnectionIndicator from './GatewayConnection';
//const { ipcRenderer } = require('electron');
import {remote} from 'electron'
import {useAuthStore} from '@/stores/auth'
import {useUserStore} from '@/stores/user'

export default {
  components: {
    LocaleSwitcher,
    EngineConnectionIndicator
  },
  setup() {
    const authStore = useAuthStore()
    const userStore = useUserStore()
    return {authStore, userStore}
  },

  data() {
    return {
      //currentAppVersion: remote.app.getVersion(),
      latestAppVersion: 'Not yet Developed'
    }
  },
  methods: {
    async logout() {
      //await this.$store.commit('setStatusStop');
      await this.authStore.actionLogOut()
    },
    check_updates() {
      //ipcRenderer.send('checkForUpdates');
    },
  },
  computed: {
    currentAppVersion() {
      try {
        return remote.app.getVersion()
      } catch (error) {
        return 'development'
      }
    },
    userProfile() {
      return this.userStore.user
    }

  }
};
</script>
