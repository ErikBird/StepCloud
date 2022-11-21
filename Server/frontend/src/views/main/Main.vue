<template>
  <v-app>
    <dashboard-core-drawer :user_menu="menu_entries" :admin_menu="admin_entries"/>
    <dashboard-core-app-bar/>
    <dashboard-core-view/>
  </v-app>
</template>

<script lang="js">

const routeGuardMain = async (to, from, next) => {
  if (to.path === '/main') {
    next('/main/dashboard');
  } else {
    next();
  }
};
export default {
  name: "Main",
  components: {
    DashboardCoreAppBar: () => import('@/components/core/AppBar'),
    DashboardCoreDrawer: () => import('@/components/core/AppDrawer'),
    DashboardCoreView: () => import('@/components/core/View'),
  },
  methods: {
    beforeRouteEnter(to, from, next) {
      routeGuardMain(to, from, next);
    }, beforeRouteUpdate(to, from, next) {
      routeGuardMain(to, from, next);
    },
    miniDrawer() {
      return this.$store.getters.dashboardMiniDrawer;
    },
    showDrawer() {
      return this.$store.dashboardShowDrawer;
    },
    switchShowDrawer() {
      this.$store.commit(
          'setDashboardShowDrawer',
          !this.$store.getters.dashboardShowDrawer
      );
    },
    switchMiniDrawer() {
      this.$store.commit(
          'setDashboardMiniDrawer',
          !this.$store.getters.dashboardMiniDrawer
      );
    },
    hasAdminAccess() {
      return this.$store.hasAdminAccess;
    },
    async logout() {
      await this.$store.dispatch('actionLogOut');
    }

  },
  data() {
    return {
      menu_entries: [
        {'to': '/main/dashboard', 'icon': 'web', 'name': 'dashboard', 'disabled': false},
        {'to': '/main/profile/view', 'icon': 'person', 'name': 'profile', 'disabled': false},
      ],
      admin_entries: [
        {'to': '/main/admin/customers/all', 'icon': 'group', 'name': 'manage_customers', 'disabled': false},
        {'to': '/main/admin/devices/all', 'icon': 'mdi-printer-3d', 'name': 'manage_devices', 'disabled': false},
      ],
    }
  }
}

</script>
