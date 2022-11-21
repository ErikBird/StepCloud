<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              LithoHub - Reset Password
            </v-card-title>
            <v-card-text>
              <p class="subheading">Enter your new password below</p>
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
              <v-btn @click="cancel">Cancel</v-btn>
              <v-btn @click="reset">Clear</v-btn>
              <v-btn
                  color="success"
                  @click="submit"
                  :disabled="!(passwordsFilled && !notSamePasswords && passwordValidation.valid)"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="js">
import {extend, setInteractionMode, ValidationObserver, ValidationProvider} from "vee-validate";


setInteractionMode('eager')

extend('password', {
  params: ['target'],
  validate(value, {target}) {
    return value === target;
  },
  message: 'Password confirmation does not match'
});
export default {
  name: "UserProfileEdit",
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
    mounted() {
      this.checkToken();
    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible
    },
    reset() {
      this.password1 = '';
      this.password2 = '';
      this.$validator.reset();
    },
    cancel() {
      this.$router.push('/');
    },
    checkToken() {
      const token = (this.$router.currentRoute.query.token);
      if (!token) {
        this.$store.commit('addNotification',
            {
              content: 'No token provided in the URL, start a new password recovery',
              color: 'error',
            }
        );
        this.$router.push('/recover-password');
      } else {
        return token;
      }
    },
    async submit() {
      if (await this.$validator.validateAll()) {
        const token = this.checkToken();
        if (token) {
          await this.$store.dispatch('resetPassword', {token, password: this.password1});
          this.$router.push('/');
        }
      }
    }
  }, computed: {
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
  },
}
</script>
