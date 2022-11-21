<template>
  <v-container fluid>
    <div class="text-h5 font-weight-light ma-5">{{ $t("welcome") }} {{ greetedUser() }}</div>
  </v-container>
</template>

<script lang="js">

export default {
  name: "Dashboard",
  methods: {
    greetedUser() {
      const userProfile = this.$store.getters.userProfile;
      if (userProfile) {
        if (userProfile.full_name) {
          return userProfile.full_name;
        } else {
          return userProfile.email;
        }
      }
    }
  }
}
</script>
