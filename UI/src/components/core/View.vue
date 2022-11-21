<template>
  <v-main>
    <v-dialog
        hide-overlay
        persistent
        v-model="dialog"
        max-width="290"
    >
      <v-card>

        <v-alert
            text
            prominent
            type="error"
        >
          {{ this.utilStore.error_message }}
        </v-alert>
      </v-card>
    </v-dialog>
    <v-card
        flat
        height='100%'
        justify="center"
        color="grey lighten-4"
    >
      <router-view></router-view>
    </v-card>
  </v-main>
</template>

<script>
import {useUtilStore} from "@/stores/util"

export default {
  setup() {
    const utilStore = useUtilStore()
    return {utilStore}
  },
  name: 'CoreView',
  computed: {
    dialog() {
      return this.utilStore.error_message !== '';
    }
  }
};
</script>
