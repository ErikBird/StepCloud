<template>
  <div>
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

    </v-form>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text
             @click="this.cancel">
        {{ $t('general.cancel') }}
      </v-btn>
      <v-btn
          color="primary"
          :disabled="!valid"
      >
        {{ $t('general.continue') }}
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script>
export default {
  name: 'DeviceManual',
  data() {
    return {
      valid: false,
      ip_address: '',
      selected: [],
      IPRules: [
        v => !!v || 'IP is required',
        v => /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/.test(v) || 'IP not valid',
      ],
    };
  },
  computed: {},
  methods: {
    cancel() {
      this.$emit('cancel');
    },
  },
};
</script>

<style scoped>

</style>
