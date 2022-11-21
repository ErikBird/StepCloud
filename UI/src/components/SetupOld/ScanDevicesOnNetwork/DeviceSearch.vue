<template>
  <div>

    <v-card-subtitle v-if="active_search">
      {{ $t('ScanDevicesOnNetwork.search') }}
    </v-card-subtitle>
    <v-card-subtitle v-if="has_printer && !active_search">
      {{ $t('ScanDevicesOnNetwork.select') }}
    </v-card-subtitle>
    <v-card-subtitle v-if="no_printer_found && !active_search">
      {{ $t('ScanDevicesOnNetwork.not_found') }}
    </v-card-subtitle>
    <v-card-text v-if="active_search">
      {{ $t('ScanDevicesOnNetwork.wait') }}
      <v-progress-linear
          indeterminate
          color="primary"
          class="mb-0"
      ></v-progress-linear>
    </v-card-text>
    <v-data-table
        flat
        v-if="has_printer&& !active_search"
        v-model="selected"
        :headers="headers"
        :items="devices"
        item-key="ip"
        single-select
        show-select
        hide-default-footer
    >
    </v-data-table>
    <v-row>
      <v-spacer></v-spacer>
      <v-btn class="ma-5" color="primary">{{ $t('general.search') }}</v-btn>
      <v-spacer></v-spacer>
    </v-row>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text
             @click="this.cancel">
        {{ $t('general.cancel') }}
      </v-btn>
      <v-btn
          color="primary"
          :disabled="!selected.length>0"
          @click="this.continue"
      >
        {{ $t('general.continue') }}
      </v-btn>


    </v-card-actions>
  </div>
</template>

<script>
export default {
  name: 'DeviceSearch',
  data() {
    return {
      has_printer: false,
      active_search: false,
      no_printer_found: false,
      devices: [],
      headers: [
        {text: this.$t('ScanDevicesOnNetwork.hostname'), value: 'name'},
        {text: this.$t('ScanDevicesOnNetwork.IP'), value: 'ip'},
        {text: this.$t('ScanDevicesOnNetwork.model'), value: 'model'},
        {text: this.$t('ScanDevicesOnNetwork.serial_number'), value: 'serial_number'},
      ],
      selected: [],
    };
  },
  computed: {},
  methods: {
    continue() {
      this.$emit('continue', this.selected[0].ip);
      this.devices = [];
      this.selected = [];
      this.has_printer = false;
      this.no_printer_found = false;
    },

    cancel() {
      this.$emit('cancel');
      this.devices = [];
      this.selected = [];
      this.has_printer = false;
      this.no_printer_found = false;
    },
  },
};
</script>

<style scoped>

</style>
