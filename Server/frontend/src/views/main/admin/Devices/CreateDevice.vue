<template>
  <v-dialog v-model="dialog" persistent max-width="800px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
      >
        {{ $t('create_device') }}
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">{{ $t('create_device') }}</span>
        deviceSupplier
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
            <v-row class="mt-5 ml-5">
              <div class="text-h6">{{ $t('identifier') }}</div>
              <v-btn
                  class="mx-2"
                  fab
                  outlined
                  x-small
                  @click="identifier.push({text:''})"
              >
                <v-icon dark>
                  mdi-plus
                </v-icon>
              </v-btn>
              <v-spacer></v-spacer>
            </v-row>
            <ValidationProvider v-for="(item, index) in identifier" immediate v-slot="{ validate, reset, valid }"
                                name="Identifier">
              <v-text-field
                  class="ml-5"
                  v-model="item.text"
                  :counter="30"
                  :success="valid"
                  clearable
              ></v-text-field>
            </ValidationProvider>
            <v-row class="mt-5 ml-5">
              <div class="text-h6">
                {{ $t('supplier') }}
              </div>
              <CreateDeviceSupplier></CreateDeviceSupplier>
            </v-row>
            <v-row class="ml-7">
              <validation-provider
                  class="flex-grow-1"
                  v-slot="{ errors, validate }"
                  name="select"
                  rules="required"
              >
                <v-select
                    v-model="supplier"
                    :items="deviceSupplier"
                    :error-messages="errors"
                    item-text="name"
                    item-value="id"
                    :label="$t('supplier')"
                    data-vv-name="select"
                    required
                ></v-select>
              </validation-provider>
            </v-row>
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
import CreateDeviceSupplier from "@/views/main/admin/Devices/CreateDeviceSupplier";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    CreateDeviceSupplier,
  },
  props: ['customerID'],
  data: () => ({
    valid: false,
    Name: '',
    supplier: NaN,
    dialog: false,
    identifier: [{text: 'hans'}],
  }),

  methods: {
    cancel() {
      this.$router.back();
    },
    async mounted() {
      this.reset();
    },
    async submit() {
      if (this.$refs.observer.validate()) {
        const updatedDevice = {
          name: this.Name,
          supplier_id: this.supplier,
          identifier: this.identifier.map(a => a.text).filter(text => text !== ''),
        };
        /*
        if (this.Name) {
          updatedProfile.Name = this.fullName;
        }*/
        await this.$store.dispatch('actionCreateDevice', updatedDevice);
        this.dialog = false;
      }
    }
  },
  computed: {
    deviceSupplier() {
      return this.$store.getters.deviceSupplier;
    }
  }
}
</script>
