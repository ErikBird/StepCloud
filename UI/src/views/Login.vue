<template>
  <v-app>
    <v-app-bar
        app
        dense
        flat
        color="white"
    >
      <v-toolbar-title class="title">
        <v-img contain src="@/assets/stepcloud_logo_long.svg" width="150px"/>
      </v-toolbar-title>
    </v-app-bar>
    <v-main>
      <v-layout align-center justify-center>
        <v-card class="elevation-12" width="500px">
          <v-toolbar dark color="primary">
            <v-toolbar-title>{{ appName }}</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form @keyup.enter="submit">
              <v-text-field @keyup.enter="submit" v-model="email" prepend-icon="mdi-account" name="login" label="Login"
                            type="text"></v-text-field>
              <v-text-field @keyup.enter="submit" v-model="password" prepend-icon="mdi-lock" name="password"
                            label="Password" id="password" type="password"></v-text-field>
              <v-checkbox
                  class="ma-0 pa-0"
                  v-model="store_password"
                  :label="$t('Login.save_password')"
              ></v-checkbox>
            </v-form>
            <div v-if="loginError">
              <v-alert transition="fade-transition" type="error">
                Incorrect email or password
              </v-alert>
            </div>
            <div v-if="networkError">
              <v-alert transition="fade-transition" type="error">
                You are offline
              </v-alert>
            </div>
            <v-flex class="caption text-xs-right">
              <RecoverPassword></RecoverPassword>
            </v-flex>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="dialog = false">Close</v-btn>
            <v-btn color="primary" @click.prevent="submit">Login</v-btn>
          </v-card-actions>
        </v-card>
      </v-layout>
    </v-main>

  </v-app>
</template>

<script>

const LocalStore = require('electron-store');
const localStore = new LocalStore();
import {appName} from "@/env";
import {useAuthStore} from '@/stores/auth'
import {useUserStore} from '@/stores/user'

export default {
  setup() {
    const authStore = useAuthStore()
    const userStore = useUserStore()
    return {authStore, userStore}
  },
  name: 'App',
  components: {
    RecoverPassword: () => import('@/components/core/PasswordRecovery'),
  },
  data() {
    return {
      appName: appName,
      store_password: false,
      password: '',
      email: '',
      dialog: true,
    };
  },
  computed: {
    loginError() {
      return this.authStore.logInError
    },
    networkError() {
      return this.authStore.networkError
    }
  },
  methods: {
    async submit() {
      if (this.store_password) {
        localStore.set('username', this.email);
        localStore.set('password', this.password);
      }
      this.dialog = false;
      this.authStore.actionLogIn({username: this.email, password: this.password}).then(() => {
        this.userStore.actionGetUserMe()
      })
    },
    retrieve_stored_credentials() {
      if (localStore.has('username')) {
        this.email = localStore.get('username')
      }
      if (localStore.has('password')) {
        this.password = localStore.get('password')
      }
    }
  },
  mounted() {
    this.retrieve_stored_credentials()
  },
};
</script>
