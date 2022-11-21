<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          class="mx-2"
          v-bind="attrs"
          v-on="on"
          fab
          outlined
          x-small
      >
        <v-icon dark>
          mdi-plus
        </v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">{{ $t('create_deviceSupplier') }}</span>
      </v-card-title>
      <v-card-text>
        <ValidationObserver ref="observer" v-slot="{ invalid,validate, reset, handleSubmit }">
          <v-form>
            <ValidationProvider immediate v-slot="{ errors, validate, reset, valid }" name="Name"
                                rules="required|max:30">
              <v-text-field
                  v-model="Name"
                  :counter="30"
                  :error-messages="errors"
                  :success="valid"
                  label="Name"
                  required
              ></v-text-field>
            </ValidationProvider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="dialog = false">{{ $t('cancel') }}</v-btn>
              <v-btn color="blue darken-1" text :disabled="invalid" @click="submit">{{ $t('save') }}</v-btn>
            </v-card-actions>
          </v-form>
        </ValidationObserver>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="js">
import {ValidationObserver, ValidationProvider} from 'vee-validate'
import {mapGetters, mapState} from "vuex";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  props: ['customerID'],
  data: () => ({
    valid: false,
    Name: '',
    dialog: false,
  }),

  methods: {
    cancel() {
      this.$router.back();
    },
    async created() {
      this.reset();
    },
    async submit() {
      if (this.$refs.observer.validate()) {
        const updatedSupplier = {
          name: this.Name,
        };
        await this.$store.dispatch('actionCreateDeviceSupplier', updatedSupplier);
        await this.$store.dispatch('actionGetDeviceSupplier');
        this.dialog = false;
      }
    }
  },
}
</script>
