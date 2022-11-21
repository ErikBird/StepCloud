<template>
  <div>
    <div v-if="event.sensor_data.length>0" class="text-left font-weight-bold text-subtitle-1 ml-5">
      {{ $t('DeviceDetail.sensor_data') }}:
    </div>
    <v-card
        v-for="item in event.sensor_data"
        :key="item.id"
        flat>
      <SensorDataVisualization :data=item></SensorDataVisualization>
    </v-card>
    <div v-if="event.log_data.length>0" class="text-left font-weight-bold text-subtitle-1 ml-5">
      {{ $t('DeviceDetail.log_data') }}:
    </div>
    <v-expansion-panels>
      <v-expansion-panel
          v-for="item in event.log_data"
          :key="item.label"
      >
        <v-expansion-panel-header>
          {{ item.label }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-divider></v-divider>
          <p v-html="toParagraph(item.data.content)"></p>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>
<script>

import SensorDataVisualization from '@/views/MyDevices/SensorDataVisualization';

export default {
  name: "EventDataVisualization",
  props: {
    event: {}
  },
  components: {
    SensorDataVisualization,
  },
  data() {
    return {
      logTableHeaders: [{text: 'Name', value: 'label'}],
    }
  },
  methods: {
    toParagraph(string_list) {
      return string_list.join("</p><p>")
    }
  },
}
</script>

<style scoped>

</style>