<template>
  <router-view></router-view>
</template>

<script lang="js">

const routeGuardAdmin = async (to, from, next) => {
  if (!this.$store.getters.hasAdminAccess) {
    next('/main/dashboard');
  } else {
    next();
  }
};

export default {
  name: "Admin",
  methods: {
    beforeRouteEnter(to, from, next) {
      routeGuardAdmin(to, from, next);
    },
    beforeRouteUpdate(to, from, next) {
      routeGuardAdmin(to, from, next);
    }

  }
}
</script>
