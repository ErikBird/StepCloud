<template>
  <v-navigation-drawer
      floating
      app
      clipped
      permanent
      color="grey lighten-4"
  >
    <v-list
        class="ma-2"
        dense
        rounded>
      <v-list-item-group color="primary">
        <v-list-item v-for="(item, i) in user_menu" :key="i"
                     :to="item.to" :disabled="item.disabled">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t(item.name) }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <v-divider></v-divider>
    <v-list
        v-show="hasAdminAccess"
        class="ma-2"
        dense
        rounded>
      <v-subheader>Admin</v-subheader>
      <v-list-item-group color="primary">
        <v-list-item v-for="(item, i) in admin_menu" :key="i"
                     :to="item.to" :disabled="item.disabled">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t(item.name) }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>
<script>


export default {
  name: "AppDrawer",
  props: ['user_menu', 'admin_menu'],
  methods: {
    hasAdminAccess() {
      return this.$store.getters.hasAdminAccess
    }
  }
  /*data() {
            return {
                menu_entries: [
                    {'to': '/', 'icon':'mdi-factory', 'name':'drawer_production', 'disabled':false },
                    {'to': 'disabled', 'icon':'mdi-transit-connection-variant', 'name':'drawer_processes', 'disabled':true },
                    {'to': '/production', 'icon':'mdi-printer-3d', 'name':'drawer_machines', 'disabled':false },
                    {'to': '/disabled', 'icon':'mdi-flask', 'name':'resins', 'disabled':true },
                    {'to': '/user_manger', 'icon':'mdi-account-group', 'name':'drawer_user', 'disabled':false },
                ],
            }
        },*/
}
</script>
