<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          class="ma-1"
          color="primary"
          v-bind="attrs"
          v-on="on"
      >
        <v-icon left>mdi-account-edit</v-icon>
        {{ $t("edit") }}
      </v-btn>
    </template>
    <v-flex>
      <v-card>
        <v-card-title primary-title>
          <div class="headline primary--text">Edit User Profile</div>
        </v-card-title>
        <v-card-text>
          <ValidationObserver ref="observer" v-slot="{ invalid, validate, reset, handleSubmit }">
            <v-form>
              <ValidationProvider immediate v-slot="{ errors, valid }" name="Name" rules="required|max:30">
                <v-text-field
                    v-model="fullName"
                    :counter="30"
                    :error-messages="errors"
                    :success="valid"
                    label="Full Name"
                    required
                ></v-text-field>
              </ValidationProvider>
              <ValidationProvider immediate v-slot="{ errors, valid }" name="email" rules="required|email">
                <v-text-field
                    v-model="email"
                    :error-messages="errors"
                    :success="valid"
                    label="E-mail"
                    required
                ></v-text-field>
              </ValidationProvider>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="dialog = false">Cancel</v-btn>
                <v-btn @click="reset">Reset</v-btn>
                <v-btn
                    color="success"
                    @click="submit"
                    :disabled="invalid"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-form>
          </ValidationObserver>
        </v-card-text>

      </v-card>
    </v-flex>
  </v-dialog>
</template>
<script>
import {extend, ValidationObserver, ValidationProvider, setInteractionMode} from 'vee-validate'
import {required, email, max} from 'vee-validate/dist/rules'

setInteractionMode('eager')

extend('required', {
  ...required,
  message: '{_field_} can not be empty',
})

extend('max', {
  ...max,
  message: '{_field_} may not be greater than {length} characters',
})

extend('email', {
  ...email,
  message: 'Email must be valid',
})
export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    valid: false,
    fullName: '',
    email: '',
    dialog: false,
  }),

  methods: {
    async submit() {
      if (this.$refs.observer.validate()) {
        const updatedProfile = {};
        if (this.fullName) {
          updatedProfile.full_name = this.fullName;
        }
        if (this.email) {
          updatedProfile.email = this.email;
        }
        this.dialog = false;
        await this.$store.dispatch('actionUpdateUserProfile', updatedProfile);
      }
    },
    async mounted() {
      await this.$store.dispatch('actionGetUsers');
      this.reset();
    },
    user() {
      return this.$store.getters.adminOneUser(+this.$router.currentRoute.params.id);
    },
    userProfile() {
      return this.$store.getters.userProfile;
    },
    reset() {
      const userProfile = this.$store.getters.userProfile;
      if (userProfile) {
        this.fullName = userProfile.full_name;
        this.email = userProfile.email;
      }
    },
  },
  created() {
    const userProfile = this.userProfile();
    if (userProfile) {
      this.fullName = userProfile.full_name;
      this.email = userProfile.email;
    }
  },
};
</script>
