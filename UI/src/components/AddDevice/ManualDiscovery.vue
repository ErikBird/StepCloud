<template>
  <div>
    <v-card
        flat
        tile
    >
      <v-form
          v-model="valid"
          ref="form"
          lazy-validation
      >
        <v-text-field
            v-model="ip_address"
            :rules="IPRules"
            label="IP Address"
            required
        ></v-text-field>
        <v-select
            v-model="select"
            :items="interfaceList"
            item-text="interface_name"
            item-value="interface_name"
            :rules="TypeRules"
            label="Interface"
            required
        ></v-select>
      </v-form>
      <v-alert
          v-if="show_error"
          dense
          outlined
          type="error"
      >
        {{ $t('DeviceManual.error') }}
      </v-alert>
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
          :disabled="!valid"
          color="primary"
          @click="register"
      >
        {{ $t('general.continue') }}
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script>
import {gateway_api} from "@/helpers/gateway_api";
import {useGatewayStore} from "@/stores/gateway";

export default {
  setup() {
    const gatewayStore = useGatewayStore()
    return {gatewayStore}
  },
  name: "ManualDiscovery",
  data() {
    return {
      valid: false,
      select: null,
      ip_address: '',
      show_error: false,
      IPRules: [
        v => !!v || this.$t('DeviceManual.ip_required'),
        v => /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/.test(v) || this.$t('DeviceManual.ip_wrong'),
      ],
      TypeRules: [v => !!v || this.$t('DeviceManual.type_required')]
    }
  },
  computed: {
    interfaceList() {
      return this.gatewayStore.manual_interfaces
    },
  },
  methods: {
    close() {
      this.$emit('close')
    },
    async register() {
      try {
        const response = await gateway_api.introductInterfaceByIP(this.gatewayStore.network_address, this.select, this.ip_address)
        if (response) {
          let data = response.data;
          this.$emit('select', data)
        }
      } catch (error) {
        this.show_error = true;
        this.valid = false;
        this.select = null;
        this.ip_address = '';
        setTimeout(() => {
          this.show_error = false;
        }, 5000);
      }
    }
  }
}
</script>

<style scoped>

</style>
