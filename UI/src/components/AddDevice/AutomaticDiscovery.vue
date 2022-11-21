<template>
  <div>
    <v-card
        flat
        tile
        :loading="loading"
    >
      <template v-if="ListAvailableInterfaces.length !== 0">
        <v-data-iterator
            class="mt-6"
            :items="ListAvailableInterfaces"
            hide-default-footer
        >
          <v-row>
            <v-col
                v-for="item in ListAvailableInterfaces"
                :key="item.gateway_id"
                cols="12"
                sm="12"
                md="6"
                lg="4"
            >
              <v-card
                  :color="background_color(item)"
                  @click="click(item)"
              >
                <v-card-title class="justify-center">
                  {{ item.label }}
                </v-card-title>
                <v-img
                    height="250"
                    contain
                    :src="getImagePath(item)"
                ></v-img>
                <v-list-item>
                  IP:{{ item.ip }}
                </v-list-item>
              </v-card>
            </v-col>
          </v-row>
        </v-data-iterator>
      </template>
      <template v-else>
        <div class="mt-5">{{ $t('AddDeviceSteps.no_device') }}</div>
      </template>
    </v-card>
    <v-card-actions>
      <v-btn
          text
          @click="close"
      >
        {{ $t('general.cancel') }}
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn
          :disabled="Object.keys(selected).length === 0"
          color="primary"
          @click="next_step"
      >
        {{ $t('general.continue') }}
      </v-btn>
    </v-card-actions>
  </div>
</template>


<script>
import {useGatewayStore} from "@/stores/gateway";

export default {
  setup() {
    const gatewayStore = useGatewayStore()
    return {gatewayStore}
  },
  name: "AutomaticDiscovery",
  data() {
    return {
      selected: {},
      interval: null,
      loading: true,
      is_open: true,
      publicPath: process.env.BASE_URL
    }
  },
  computed: {
    ListAvailableInterfaces() {
      return this.gatewayStore.discovered_interfaces
    },
  },
  methods: {
    click(item) {
      if (this.selected === item) {
        this.selected = {}
      } else {
        this.selected = item
      }
    },
    getImagePath(item) {
      return this.publicPath + "interface_images/" + item.interface_name + '.png'
    },
    background_color(item) {
      if (item === this.selected) {
        return 'blue'
      } else {
        return 'grey'
      }
    },
    close() {
      this.$emit('close')
    },
    next_step() {
      this.$emit('select', this.selected)
    }
  }
}
</script>

<style scoped>

</style>
