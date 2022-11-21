<template>
  <div class="text-center">
    <v-dialog
        v-model="showDialogue"
        persistent
        width="800"
    >
      <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step
              :complete="e1 > 1"
              step="1"
          >
            {{ $t('setupSteps.welcome') }}
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step
              :complete="e1 > 2"
              step="2"
          >
            {{ $t('setupSteps.scanDevices') }}
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step
              :complete="e1 > 3"
              step="3"
          >
            {{ $t('setupSteps.final') }}
          </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1">
            <v-card
                flat
                class="mb-12"
                height="200px"
            >
              <v-card-title>
                {{ $t('setupSteps.welcomeTitle') }}
              </v-card-title>
              <v-card-text>
                {{ $t('setupSteps.welcomeText') }}
              </v-card-text>
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
                  color="primary"
                  @click="e1 = 2"
              >
                {{ $t('general.continue') }}
              </v-btn>
            </v-card-actions>

          </v-stepper-content>

          <v-stepper-content step="2">
            <ScanDevicesOnNetwork @continue="this.continue" @cancel="this.cancel"></ScanDevicesOnNetwork>
          </v-stepper-content>
          <v-stepper-content step="3">
            <v-card
                flat
                class="mb-12"
                height="200px"
            >
              <v-card-title>
                {{ $t('setupSteps.finalTitle') }}
              </v-card-title>
              <v-card-text>
                {{ $t('setupSteps.finalText') }}
              </v-card-text>
            </v-card>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  color="primary"
                  @click="close"
              >
                {{ $t('general.finish') }}
              </v-btn>
            </v-card-actions>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-dialog>
  </div>
</template>

<script>
import ScanDevicesOnNetwork from "@/components/SetupOld/ScanDevicesOnNetwork/ScanDevicesOnNetwork";

export default {
  name: 'SetupSteps',
  components: {ScanDevicesOnNetwork},
  data() {
    return {
      e1: 1,
    };
  },
  methods: {
    async continue() {
      this.e1 = 3
    },
    cancel() {
      this.e1 = 1
    },
    close() {
      this.$store.commit('setSetupDialogue', false);
      this.e1 = 2
    }
  },
  computed: {
    showDialogue() {
      return this.$store.getters.setupDialogue
    }
  },
};
</script>

<style scoped>

</style>
