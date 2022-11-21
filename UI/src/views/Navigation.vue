<template>
  <v-app>
    <dashboard-core-app-bar/>
    <dashboard-core-drawer :user_menu="menu_entries"/>
    <DashboardCoreView/>
    <!--SetupSteps></SetupSteps-->
  </v-app>
</template>

<script lang="ts">
export default {
  name: "Navigation",
  components: {
    DashboardCoreAppBar: () => import('@/components/core/AppBar'),
    DashboardCoreDrawer: () => import('@/components/core/AppDrawer'),
    DashboardCoreView: () => import('@/components/core/View'),
    //SetupSteps: () => import("@/components/SetupOld/SetupSteps")
  },
  methods: {},
  data() {
    return {
      menu_entries: [
        {'to': '/production', 'icon': 'mdi-factory', 'name': 'nav.production', 'disabled': true},
        {'to': '/workflow', 'icon': 'mdi-chart-timeline-variant', 'name': 'nav.workflow', 'disabled': true},
        {'to': '/my-devices', 'icon': 'mdi-printer-3d', 'name': 'nav.devices', 'disabled': false},
        {'to': '/consume', 'icon': 'mdi-flask', 'name': 'nav.consume', 'disabled': true},
      ],
    }
  },
};
</script>
