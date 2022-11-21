<template>
  <v-main>
    <v-card align="center"
            height='100%'
            justify="center"
            color="grey lighten-4"
    >
      <router-view></router-view>
    </v-card>
  </v-main>
</template>

<script>
export default {
  name: 'CoreView',
};
</script>
