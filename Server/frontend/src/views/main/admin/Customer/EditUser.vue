<template>
  <v-container fluid>
    <v-card>
      <v-card-title primary-title>
        <div class="headline primary--text">Edit User</div>
      </v-card-title>
      <v-card-text>
        <div class="my-3">
          <div class="subheading secondary--text text--lighten-2">Username</div>
          <div
              class="title primary--text text--darken-2"
              v-if="user"
          >{{ user.email }}
          </div>
          <div
              class="title primary--text text--darken-2"
              v-else
          >-----
          </div>
        </div>
        <v-form
            v-model="valid"
            ref="form"
            lazy-validation
        >
          <v-text-field
              label="Full Name"
              v-model="fullName"
              required
          ></v-text-field>
          <v-text-field
              v-model="email"
              :rules="emailRules"
              label="E-mail"
              required
          ></v-text-field>
          <div class="subheading secondary--text text--lighten-2">User is superuser <span v-if="isSuperuser">(currently is a superuser)</span><span
              v-else>(currently is not a superuser)</span></div>
          <v-checkbox
              label="Is Superuser"
              v-model="isSuperuser"
          ></v-checkbox>
          <div class="subheading secondary--text text--lighten-2">User is active <span v-if="isActive">(currently active)</span><span
              v-else>(currently not active)</span></div>
          <v-checkbox
              label="Is Active"
              v-model="isActive"
          ></v-checkbox>
          <v-layout align-center>
            <v-flex shrink>
              <v-checkbox
                  v-model="setPassword"
                  class="mr-2"
              ></v-checkbox>
            </v-flex>
            <v-flex>
              <v-text-field
                  :disabled="!setPassword"
                  type="password"
                  ref="password"
                  label="Set Password"
                  data-vv-name="password"
                  data-vv-delay="100"
                  v-validate="{required: setPassword}"
                  v-model="password1"
              >
              </v-text-field>
              <v-text-field
                  v-show="setPassword"
                  type="password"
                  label="Confirm Password"
                  data-vv-name="password_confirmation"
                  data-vv-delay="100"
                  data-vv-as="password"
                  v-validate="{required: setPassword, confirmed: 'password'}"
                  v-model="password2"
              >
              </v-text-field>
            </v-flex>
          </v-layout>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn
            @click="submit"
            :disabled="!valid"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import {ValidationObserver, ValidationProvider} from 'vee-validate'

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    valid: true,
    fullName: '',
    email: '',
    isActive: true,
    isSuperuser: false,
    setPassword: false,
    select: null,
    password1: '',
    password2: '',
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ],
  }),

  methods: {
    async submit() {
      if (await this.$validator.validateAll()) {
        const updatedProfile = {};
        if (this.fullName) {
          updatedProfile.full_name = this.fullName;
        }
        if (this.email) {
          updatedProfile.email = this.email;
        }
        updatedProfile.is_active = this.isActive;
        updatedProfile.is_superuser = this.isSuperuser;
        if (this.setPassword) {
          updatedProfile.password = this.password1;
        }
        await this.$store.dispatch('actionUpdateUser', {id: this.user.id, user: updatedProfile});
        this.$router.push('/main/admin/users');
      }
    },
    reset() {
      this.setPassword = false;
      this.password1 = '';
      this.password2 = '';
      this.$validator.reset();
      if (this.user) {
        this.fullName = this.user.full_name;
        this.email = this.user.email;
        this.isActive = this.user.is_active;
        this.isSuperuser = this.user.is_superuser;
      }
    },
    async mounted() {
      await this.$store.dispatch('actionGetUsers');
      this.reset();
    },
    cancel() {
      this.$router.back();
    },
    user() {
      return this.$store.getters.adminOneUser(+this.$router.currentRoute.params.id);
    }
  }
};
</script>
