<template>
  <v-card>
    <v-card-title>
      <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          :label="$t('general.search')"
          single-line
          hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
        :headers="headers"
        :items="log"
        :search="search"
        item-key="id"
        :expanded.sync="expanded"
        class="elevation-1"
        show-expand
    >
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <table cellpadding="5" cellspacing="5">
            <tr v-for="(it, key) in item" :key="key">
              <td><b>{{ key }}</b></td>
              <td>{{ it }}</td>
            </tr>
          </table>
        </td>
      </template>
      <template v-slot:item.status="{ item }">
        <v-chip
            :color="getColor(item.status)"
            dark
        >
          {{ item.status }}
        </v-chip>
      </template>
      <template v-slot:item.ended="{ item }">
        {{ formatDate(item.ended) }}
      </template>
      <template v-slot:item.elapsed_time="{ item }">
        {{ fancyTimeFormat(item.elapsed_time) }}
      </template>


    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: "BuildLogTable",
  props: ['log'],
  data() {
    return {
      search: '',
      expanded: [],
      headers: [
        {
          search: '',
          text: this.$t('BuildLogTable.name'),
          align: 'start',
          sortable: false,
          value: 'name',
        },
        {text: this.$t('BuildLogTable.status'), value: 'status'},
        {text: this.$t('BuildLogTable.elapsed_time'), value: 'elapsed_time'},
        {text: this.$t('BuildLogTable.total_slice_count'), value: 'total_slice_count'},
        {text: this.$t('BuildLogTable.ended'), value: 'ended'},
        {text: '', value: 'data-table-expand'},
      ],
    }
  },
  methods: {
    getColor(status) {
      if (status === 'OK') return 'green'
      else if (status === 'Canceled') return 'orange'
      else return 'red'
    },
    fancyTimeFormat(duration) {
      // Hours, minutes and seconds
      var hrs = ~~(duration / 3600);
      var mins = ~~((duration % 3600) / 60);
      var secs = ~~duration % 60;

      // Output like "1:01" or "4:03:59" or "123:03:59"
      var ret = "";

      if (hrs > 0) {
        ret += "" + hrs + ' h ' + (mins < 10 ? "0" : "");
      }

      ret += "" + mins + " min " + (secs < 10 ? "0" : "");
      ret += "" + secs + " sec";
      return ret;
    },
    formatDate(datestring) {
      const event = new Date(datestring)
      const options = {year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric'};
      return event.toLocaleDateString('de-DE', options);
    }
  }
}
</script>

<style scoped>

</style>
