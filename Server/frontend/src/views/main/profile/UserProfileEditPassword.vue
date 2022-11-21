<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          class="ma-1"
          color="primary"
          v-bind="attrs"
          v-on="on"
      >
        <v-icon left>mdi-security</v-icon>
        {{ $t("change_password") }}
      </v-btn>
    </template>
    <v-flex>
      <v-card>
        <v-card-title primary-title>
          <div class="headline primary--text">Set Password</div>
        </v-card-title>
        <v-card-text>
          <div class="my-3">
            <div class="title primary--text text--darken-2" v-if="userProfile.full_name">{{
                userProfile.full_name
              }}
            </div>
            <div class="title primary--text text--darken-2" v-else>{{ userProfile.email }}</div>
          </div>
          <div class="password">
            <v-text-field :class='{valid:passwordValidation.valid}' :type="passwordVisible ? 'text' : 'password'"
                          v-model="password" label="Password"></v-text-field>
            <button class="visibility" tabindex='-1' @click='togglePasswordVisibility'
                    :arial-label='passwordVisible ? "Hide password" : "Show password"'>
              <v-icon class="material-icons">{{ passwordVisible ? "visibility" : "visibility_off" }}</v-icon>
            </button>
          </div>
          <v-text-field type="password" v-model.lazy='checkPassword' label="Confirm Password"></v-text-field>
          <transition name="hint" appear>
            <div v-if='passwordValidation.errors.length > 0 && !submitted' class='hints'>
              <h2>Hints</h2>
              <p v-for='error in passwordValidation.errors'>{{ error }}</p>
            </div>
          </transition>
          <div class="matches" v-if='notSamePasswords'>
            <p>Passwords don't match.</p>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Cancel</v-btn>
          <v-btn
              color="success"
              @click="resetPasswords"
              :disabled="!(passwordsFilled && !notSamePasswords && passwordValidation.valid)"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-dialog>
</template>
<script>

import {extend} from 'vee-validate'

extend('password', {
  params: ['target'],
  validate(value, {target}) {
    return value === target;
  },
  message: 'Password confirmation does not match'
});
export default {
  data: () => ({
    valid: true,
    password: '',
    checkPassword: '',
    rules: [
      {message: 'One lowercase letter required.', regex: /[a-z]+/},
      {message: "One uppercase letter required.", regex: /[A-Z]+/},
      {message: "8 characters minimum.", regex: /.{8,}/},
      {message: "One number required.", regex: /[0-9]+/}
    ],
    passwordVisible: false,
    submitted: false,
    dialog: false,
  }),
  methods: {
    async resetPasswords() {
      this.password = ''
      this.checkPassword = ''
      this.submitted = true
      const updatedProfile = {};
      updatedProfile.password = this.password1;
      await this.$store.dispatch('actionUpdateUserProfile', updatedProfile);
      this.$router.push('/main/profile');
      setTimeout(() => {
        this.submitted = false
      }, 2000)
    },

    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible
    }
  },
  computed: {
    notSamePasswords() {
      if (this.passwordsFilled) {
        return (this.password !== this.checkPassword)
      } else {
        return false
      }
    },
    passwordsFilled() {
      return (this.password !== '' && this.checkPassword !== '')
    },
    passwordValidation() {
      let errors = []
      for (let condition of this.rules) {
        if (!condition.regex.test(this.password)) {
          errors.push(condition.message)
        }
      }
      if (errors.length === 0) {
        return {valid: true, errors}
      } else {
        return {valid: false, errors}
      }
    },
    reset() {
      this.password1 = '';
      this.password2 = '';
    },
    userProfile() {
      return this.$store.getters.userProfile;
    },
  },
};
</script>
