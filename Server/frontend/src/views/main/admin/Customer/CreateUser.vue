<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
      >
        {{ $t('create_user') }}
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">User Profile</span>
      </v-card-title>
      <v-card-text>
        <ValidationObserver ref="observer" v-slot="{ invalid,validate, reset, handleSubmit }">
          <v-form>
            <ValidationProvider immediate v-slot="{ errors, validate, reset, valid }" name="Name"
                                rules="required|max:10">
              <v-text-field
                  v-model="fullName"
                  :counter="10"
                  :error-messages="errors"
                  :success="valid"
                  label="Name"
                  required
              ></v-text-field>
            </ValidationProvider>
            <ValidationProvider v-slot="{ errors, valid }" name="email" rules="required|email">
              <v-text-field
                  v-model="email"
                  :error-messages="errors"
                  label="E-mail"
                  required
              ></v-text-field>
            </ValidationProvider>
            <div class="subheading secondary--text text--lighten-2">User is superuser <span v-if="isSuperuser">(currently is a superuser)</span><span
                v-else>(currently is not a superuser)</span></div>
            <ValidationProvider v-slot="{ errors, valid }" rules="required" name="checkbox">
              <v-checkbox
                  v-model="isSuperuser"
                  :error-messages="errors"
                  value="1"
                  label="Is Superuser"
                  type="checkbox"
                  required
              ></v-checkbox>
            </ValidationProvider>
            <div class="subheading secondary--text text--lighten-2">User is active <span v-if="isActive">(currently active)</span><span
                v-else>(currently not active)</span></div>
            <ValidationProvider v-slot="{ errors, valid }" rules="required" name="checkbox">
              <v-checkbox
                  v-model="isActive"
                  :error-messages="errors"
                  value="1"
                  label="Is Active"
                  type="checkbox"
                  required
              ></v-checkbox>
            </ValidationProvider>
            <v-layout align-center>
              <v-flex>
                <v-text-field type="password" ref="password" label="Set Password" data-vv-name="password"
                              data-vv-delay="100" v-model="password1"
                >
                </v-text-field>
                <v-text-field type="password" label="Confirm Password" data-vv-name="password_confirmation"
                              data-vv-delay="100" data-vv-as="password"
                              v-model="password2"
                >
                </v-text-field>
              </v-flex>
            </v-layout>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="dialog = false">{{ $t('cancel') }}</v-btn>
              <v-btn color="blue darken-1" text :disabled="invalid" @click="submit">{{ $t('save') }}</v-btn>
            </v-card-actions>
          </v-form>
        </ValidationObserver>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="js">
import {ValidationObserver, ValidationProvider} from 'vee-validate'

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  props: ['cusomerID'],
  data: () => ({
    valid: false,
    fullName: '',
    email: '',
    dialog: false,
    isActive: true,
    isSuperuser: false,
    setPassword: false,
    password1: '',
    password2: '',
  }),

  methods: {
    cancel() {
      this.$router.back();
    },
    async mounted() {
      await this.$store.dispatch('actionGetUsers');
      this.reset();
    },
    async submit() {
      if (this.$refs.observer.validate()) {
        const updatedProfile = {
          vat_id: this.email,
          customer_id: this.cusomerID
        };
        if (this.fullName) {
          updatedProfile.full_name = this.fullName;
        }
        if (this.email) {
          updatedProfile.email = this.email;
        }
        updatedProfile.is_active = this.isActive;
        updatedProfile.is_superuser = this.isSuperuser;
        updatedProfile.password = this.password1;
        await this.$store.dispatch('actionCreateUser', updatedProfile);
        this.dialog = false;
      }
    }
  }
}
</script>
