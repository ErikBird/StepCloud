<template>
  <div>
    <apexchart width="100%" type="line" :options="options" :series="this.series"></apexchart>
  </div>
</template>

<script>
export default {
  name: "SensorDataVisualization",
  props: ['data'],
  data: () => ({
    options: {
      chart: {
        id: 'vuechart-example'
      },
      xaxis: {
        type: 'datetime'
      },
      legend: {
        show: true,
        showForSingleSeries: true
      },
    },
  }),
  computed: {
    series() {
      return [{
        name: this.data.label,
        data: this.data.data.values.map((e, i) => {
          return [new Date(this.data.data.time[i]).getTime(), e];
        })
      }]
    }
  }
}
</script>

<style scoped>

</style>