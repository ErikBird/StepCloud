<template>

  <v-card
      class="fill-height">
    <v-card-text>
      <v-sheet height="64">
        <v-toolbar
            flat
        >
          <v-btn
              outlined
              class="mr-4"
              color="grey darken-2"
              @click="setToday"
          >
            Today
          </v-btn>
          <v-btn
              fab
              text
              small
              color="grey darken-2"
              @click="prev"
          >
            <v-icon small>
              mdi-chevron-left
            </v-icon>
          </v-btn>
          <v-btn
              fab
              text
              small
              color="grey darken-2"
              @click="next"
          >
            <v-icon small>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-menu
              bottom
              right
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                  outlined
                  color="grey darken-2"
                  v-bind="attrs"
                  v-on="on"
              >
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right>
                  mdi-menu-down
                </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>Day</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'week'">
                <v-list-item-title>Week</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'month'">
                <v-list-item-title>Month</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = '4day'">
                <v-list-item-title>4 days</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-sheet>
      <v-sheet height="600">
        <v-calendar
            ref="calendar"
            v-model="focus"
            color="primary"
            :event-color="getEventColor"
            :events="events"
            :event-start="started"
            :event-end="ended"
            :type="type"
            @click:event="showEvent"
            @click:more="viewDay"
            @click:date="viewDay"
        ></v-calendar>
        <v-menu
            v-model="selectedOpen"
            :close-on-content-click="false"
            :activator="selectedElement"
            offset-x
        >
          <v-card
              color="grey lighten-4"
              min-width="350px"
              flat
          >
            <v-toolbar
                :color="getEventColor(selectedEvent)"
                dark
            >
              <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <table cellpadding="5" cellspacing="5">
                <tr v-for="(it, key) in selectedEvent" :key="key">
                  <td><b>{{ key }}</b></td>
                  <td>{{ it }}</td>
                </tr>
              </table>
            </v-card-text>
            <v-card-actions>
              <v-btn
                  text
                  color="secondary"
                  @click="selectedOpen = false"
              >
                Cancel
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-card-text>

  </v-card>
</template>

<script>
export default {
  name: "DeviceCalendar.vue",
  props: ['events'],
  data: () => ({
    focus: '',
    type: 'month',
    typeToLabel: {
      month: 'Month',
      week: 'Week',
      day: 'Day',
      '4day': '4 Days',
    },
    started: 'started',
    ended: 'ended',
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    today: Date.now(),
  }),
  methods: {
    viewDay({date}) {
      this.focus = date
      this.type = 'day'
    },
    getEventColor(event) {
      if (event.status === 'OK') return 'green'
      else if (event.status === 'Canceled') return 'orange'
      else return 'red'
    },
    setToday() {
      this.focus = ''
    },
    prev() {
      this.$refs.calendar.prev()
    },
    next() {
      this.$refs.calendar.next()
    },
    showEvent({nativeEvent, event}) {
      const open = () => {
        this.selectedEvent = event
        this.selectedElement = nativeEvent.target
        setTimeout(() => {
          this.selectedOpen = true
        }, 10)
      }

      if (this.selectedOpen) {
        this.selectedOpen = false
        setTimeout(open, 10)
      } else {
        open()
      }

      nativeEvent.stopPropagation()
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
  },
}
</script>
