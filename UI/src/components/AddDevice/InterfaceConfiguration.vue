<template>
  <div>
    <p class="text-h5 text-center">Interface: <b>{{ selected_interface.label }}</b>
      ({{ selected_interface.interface_name }}) </p>
    <v-img
        height="150"
        contain
        :src="getImagePath(selected_interface)"
    ></v-img>
    <v-container v-if="selected_interface.supported_devices.length>1">
      <p class="mt-10 text-h5 text-center">
        {{ $t('AddDeviceSteps.use_interface_for_multi') }}
      </p>
      <v-row
          justify="center"
      >
        <v-col
            md="6"
        >
          <v-select
              v-model="select"
              :items="selected_interface.supported_devices"
              :label="$t('AddDeviceSteps.select_device')"
          ></v-select>
        </v-col>
      </v-row>
    </v-container>
    <v-container
        v-if="selected_interface.supported_devices.length===1"
    >
      <p class="mt-10 text-h5 text-center">
        {{ $t('AddDeviceSteps.use_interface_for_single') }}
      </p>
      <p class="mt-10 text-h5 text-center">
        <b>{{ selected_interface.supported_devices[0] }}</b>
      </p>
    </v-container>
    <v-card-actions>
      <v-btn
          text
          @click="close"
      >
        {{ $t('general.cancel') }}
      </v-btn>
      <v-spacer></v-spacer>

      <v-btn
          :disabled="!(selected_interface.supported_devices.length===1)&&this.select===''"
          color="primary"
          @click="save"
      >
        {{ $t('general.save') }}
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script>
export default {
  name: "InterfaceConfiguration",
  data() {
    return {
      select: ''
    };
  },
  props: {
    selected_interface: {}
  },
  methods: {
    getImagePath(item) {
      return process.env.BASE_URL + "interface_images/" + item.interface_name + '.png'
    },
    close() {
      this.$emit('close')
    },
    save() {
      this.$emit('save', this.device_info)
    }
  },
  computed: {
    configured_device() {
      if (this.selected_interface.supported_devices.length === 1) {
        return this.selected_interface.supported_devices[0]
      } else {
        return this.select
      }
    },
    device_info() {
      return {
        gateway_id: this.selected_interface.gateway_id,
        label: this.selected_interface.label,
        interface_name: this.selected_interface.interface_name,
        ip: this.selected_interface.ip,
        device_type: this.configured_device
      }
    }

  }
}
</script>

<style scoped>

</style>