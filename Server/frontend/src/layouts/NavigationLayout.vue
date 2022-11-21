<template>
  <v-app>
    <dashboard-core-drawer :user_menu="menu_entries" :admin_menu="admin_entries"/>
    <dashboard-core-app-bar/>
    <dashboard-core-view/>
  </v-app>
</template>

<script>
export default {
  name: 'NavigationLayout',
  components: {
    DashboardCoreAppBar: () => import('../components/core/AppBar'),
    DashboardCoreDrawer: () => import('../components/core/AppDrawer'),
    DashboardCoreView: () => import('../components/core/View'),
  },
  data() {
    return {
      menu_entries: [
        {'to': '/', 'icon': 'mdi-factory', 'name': 'drawer_production', 'disabled': false},
        {'to': 'disabled', 'icon': 'mdi-transit-connection-variant', 'name': 'drawer_processes', 'disabled': true},
        {'to': '/production', 'icon': 'mdi-printer-3d', 'name': 'drawer_machines', 'disabled': false},
        {'to': '/disabled', 'icon': 'mdi-flask', 'name': 'resins', 'disabled': true},
      ],
      admin_entries: [
        {'to': '/user_manger', 'icon': 'mdi-account-group', 'name': 'drawer_user', 'disabled': false},
      ],
    }
  }
};
</script>
