<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          text
          x-small
          color="primary"
          v-bind="attrs"
          v-on="on"
      >
        {{ $t('forgot_password') }}
      </v-btn>
    </template>
    <v-flex>
      <v-card class="elevation-12">
        <v-toolbar dark color="primary">
          <v-toolbar-title>{{ appName }} - Password Recovery</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <p class="subheading">A password recovery email will be sent to the registered account</p>
          <ValidationObserver ref="observer" v-slot="{ validate, reset }">
            <form>
              <ValidationProvider v-slot="{ errors }" name="Name" rules="required">
                <v-text-field
                    v-model="username"
                    :counter="30"
                    :error-messages="errors"
                    label="Username"
                    prepend-icon="person"
                    required
                ></v-text-field>
              </ValidationProvider>
            </form>
          </ValidationObserver>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Cancel</v-btn>
          <v-btn @click.prevent="submit" :disabled="!valid">
            Recover Password
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-dialog>
</template>
<script>
import {appName} from '../../env';
import {required} from 'vee-validate/dist/rules'
import {extend, ValidationObserver, ValidationProvider, setInteractionMode} from 'vee-validate'

setInteractionMode('eager')

extend('required', {
  ...required,
  message: '{_field_} can not be empty',
})
export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    dialog: false,
    valid: true,
    username: '',
    appName: appName,
  }),

  methods: {
    submit() {
      this.dialog = false;
      this.$store.dispatch('passwordRecovery', {username: this.username})
    },
  },
}
</script>

<style>
</style>
