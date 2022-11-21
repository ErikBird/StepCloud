<template>
  <v-app>
    <v-app-bar
        app
        dense
        flat
        color="white"
    >
      <v-toolbar-title class="title">
        <img src="../../assets/stepcloud_logo_long.svg" width="130px">
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>
      <LocaleSwitcher :color="['white',false]"/>
      <Login/>
    </v-app-bar>
    <v-main>

      <v-card class="pb-6"
              align="center"
              flat
              tile
              justify="center"
              color="blue-grey darken-4"
      >
        <v-card
            class="pt-8 pb-6 "
            dark
            max-width="1000px"
            flat tile
            color="blue-grey darken-4">
          <div class="text-h3 font-weight-black">Dokumentiere deinen Druckprozess</div>
          <v-img src="../../assets/LandingpageDatafolw.svg"></v-img>
        </v-card>
        <v-card
            class="rounded"
            max-width="600">
          <v-card-title class="text-h6">Qualitätsmanagement im 3D Druck war noch nie einfacher!</v-card-title>
          <v-card-text class="text-h6 font-weight-regular">Teste unser <b> kostenloses </b> BETA Programm:</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="mb-0 pb-0" color="primary" large>
              <v-icon left>mdi-login</v-icon>
              Testen
            </v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-card>
      <v-card align="center"
              justify="center"
              color="grey lighten-4"
              flat
      >
        <v-card
            class="pt-4"
            flat
            tile
            color="grey lighten-4"
            max-width="1000">
          <v-row>
            <v-col
                v-for="feature in features"
                :key="feature.title"
                cols="12"
                sm="6"
                md="4"
                lg="3"
            >
              <v-card width="500" height="200">
                <v-avatar size="40" color="black">
                  <v-icon dark>{{ feature.icon }}</v-icon>
                </v-avatar>
                <v-card-title class="text-sm-center">
                  {{ feature.title }}
                </v-card-title>
                <ul class="text-sm-left"
                    v-for="bullet in feature.bullets"
                    :key="bullet">
                  <li class="text-body-2">{{ bullet }}</li>
                </ul>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-card>
    </v-main>

  </v-app>
</template>

<script>
// https://www.nerves-project.org/
export default {
  name: 'UserManager',
  components: {
    LocaleSwitcher: () => import('@/components/core/LocaleSwitcher.vue'),
    Login: () => import('@/components/core/Login.vue'),
  },
  data() {
    return {
      features:
          [{
            title: 'Prozesskontrolle',
            bullets: ['Identifikation von Produkten', 'Überwachung der Prozesse'],
            icon: 'mdi-chart-gantt'
          },
            {
              title: 'Fehlerüberwachung',
              bullets: ['Proaktive Fehlererkennung', 'Ursachenbehebung von Fehldrucken'],
              icon: 'mdi-alert'
            },
            {
              title: 'Produktionsanalyse',
              bullets: ['Automatische Produktionsdokumentation', 'Lokalisierung von Ineffizienzen'],
              icon: 'mdi-google-analytics'
            },
            {
              title: 'Materialverwaltung',
              bullets: ['Bestandsverwaltung', 'Verbrauchsvorhersage'],
              icon: 'mdi-flask-empty-plus-outline'
            }],

    };
  },
};
</script>
<style scoped>
.v-application {
  background-color: #f5f5f5;
}
</style>
