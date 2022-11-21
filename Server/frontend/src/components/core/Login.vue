<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          color="blue-grey darken-4"
          small
          text
          dark
          v-bind="attrs"
          v-on="on"
      >
        Login
      </v-btn>
    </template>
    <v-flex>
      <v-card class="elevation-12">
        <v-toolbar dark color="primary">
          <v-toolbar-title>{{ appName }}</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text>
          <v-form @keyup.enter="submit">
            <v-text-field @keyup.enter="submit" v-model="email" prepend-icon="person" name="login" label="Login"
                          type="text"></v-text-field>
            <v-text-field @keyup.enter="submit" v-model="password" prepend-icon="lock" name="password" label="Password"
                          id="password" type="password"></v-text-field>
          </v-form>
          <div v-if="loginError">
            <v-alert :value="loginError" transition="fade-transition" type="error">
              Incorrect email or password
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
    </v-flex>
  </v-dialog>
</template>

<script>
import {appName} from '../../env.js';
import store from '../../store';
import router from "@/router";


export default {
  name: "Login",
  components: {
    RecoverPassword: () => import('./PasswordRecovery'),
  },
  data: () => ({
    appName: appName,
    password: '',
    email: '',
    dialog: false,
    login_error: false,
  }),
  computed: {
    loginError() {
      return this.$store.state.logInError
    }
  },
  methods: {
    async submit() {
      this.dialog = false;
      console.log('submit')
      this.$store.dispatch('actionLogIn',
          {username: this.email, password: this.password}).then((response) => {
        router.push({name: 'Dashboard'});
      })
    }
  },
};
</script>

<style>
</style>
