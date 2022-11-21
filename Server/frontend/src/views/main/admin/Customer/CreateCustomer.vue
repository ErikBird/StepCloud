<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
      >
        {{ $t('create_customer') }}
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">User Profile</span>
      </v-card-title>
      <v-card-text>
        <ValidationObserver ref="observer" v-slot="{ validate, reset }">
          <form>
            <ValidationProvider v-slot="{ errors }" name="Name" rules="required|max:20">
              <v-text-field
                  v-model="name"
                  :counter="20"
                  :error-messages="errors"
                  label="Name"
                  required
              ></v-text-field>
            </ValidationProvider>
            <ValidationProvider v-slot="{ errors }" name="vat" rules="">
              <v-text-field
                  v-model="vat_id"
                  :error-messages="errors"
                  label="VAT ID"
                  required
              ></v-text-field>
            </ValidationProvider>
          </form>
        </ValidationObserver>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialog = false">{{ $t('cancel') }}</v-btn>
        <v-btn color="blue darken-1" text @click="submit">{{ $t('save') }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {required, max} from 'vee-validate/dist/rules'
import {extend, ValidationObserver, ValidationProvider, setInteractionMode} from 'vee-validate'

setInteractionMode('eager')

extend('required', {
  ...required,
  message: '{_field_} can not be empty',
})

extend('max', {
  ...max,
  message: '{_field_} may not be greater than {length} characters',
})

export default {
  name: "CreateCustomer",
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    dialog: false,
    name: '',
    vat_id: '',
  }),

  methods: {
    submit() {
      if (this.$refs.observer.validate()) {
        const newCustomer = {
          contract_level: 0,
          name: this.name
        }
        if (this.vat_id) {
          newCustomer.vat_id = this.vat_id;
        }

        this.$store.dispatch('actionCreateCustomer', newCustomer);
      }
      this.dialog = false;
    },
  },
}

</script>

<style scoped>

</style>
