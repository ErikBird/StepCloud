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
  </v-navigation-drawer>
</template>
<script>

export default {
  name: "AppDrawer",
  props: ['user_menu'],
}
</script>
