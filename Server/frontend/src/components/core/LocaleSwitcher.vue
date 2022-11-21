<template>
  <v-menu offset-y
          close-on-click
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          x-small
          :dark="color[1]"
          depressed
          :color="color[0]"
          v-bind="attrs"
          v-on="on"
      >
        <v-icon left>mdi-chevron-down</v-icon>
        {{ $i18n.locale }}
      </v-btn>
    </template>
    <v-list>
      <v-list-item
          v-for="(lang, i) in langs"
          :key="`Lang${i}`"
          :value="lang.id"
          @click="setLocale(lang.id)"
      >
        <v-avatar class="mr-3" size="20">
          <v-img :src="getLocationPic(lang.id)"></v-img>
        </v-avatar>
        {{ lang.name }}
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  name: 'LocaleSwitcher',
  props: ['color'],
  data() {
    return {
      en: require('../../assets/flags/en.svg'),
      de: require('../../assets/flags/de.svg'),
      langs: [
        {id: 'de', name: 'Deutsch'},
        {id: 'en', name: 'Englisch'}],
    };
  },
  methods: {
    setLocale(locale) {
      this.$i18n.locale = locale;
    },
    getLocationPic(localeID) {
      if (localeID === 'en') {
        return this.en;
      } else if (localeID === 'de') {
        return this.de;
      }
    },
  },
};
</script>
