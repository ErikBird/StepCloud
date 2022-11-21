<template>
  <v-container fluid>
    <v-card>
      <v-card-title primary-title>
        <div class="headline primary--text">User Profile</div>
      </v-card-title>
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Full Name</div>
          <div class="title primary--text text--darken-2" v-if="userProfile() && userProfile().full_name">
            {{ userProfile().full_name }}
          </div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
        <div class="my-3">
          <div class="subheading secondary--text text--lighten-3">Email</div>
          <div class="title primary--text text--darken-2" v-if="userProfile() && userProfile().email">
            {{ userProfile().email }}
          </div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
      </v-card-text>
      <v-card-actions>
        <Edit/>
        <Password/>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>

export default {
  name: 'UserProfile',
  components: {
    Edit: () => import('./UserProfileEdit.vue'),
    Password: () => import('./UserProfileEditPassword.vue'),
  },
  methods: {
    userProfile() {
      return this.$store.getters.userProfile;
    },
    goToEdit() {
      this.$router.push('/main/profile/edit');
    },
    goToPassword() {
      this.$router.push('/main/profile/password');
    }
  }
};
</script>
