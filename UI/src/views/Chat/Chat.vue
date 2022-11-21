<template>
  <div>
    <v-container class="fluid d-flex align-top">
      <v-row align="end">
        <v-col>
          <div v-for="(item, index) in chat" :key="index"
               :class="['d-flex flex-row align-center my-2', item.from == 'user' ? 'justify-end': null]">
            <span v-if="item.from == 'user'" class="mr-3">{{ item.msg }}</span>
            <v-avatar :color="item.from == 'user' ? 'primary': 'blue-grey darken-4'" size="36">
              <v-icon dark>{{ item.from == 'user' ? 'mdi-account' : 'mdi-face-agent' }}</v-icon>
            </v-avatar>
            <span v-if="item.from != 'user'" class="ml-3">{{ item.msg }}</span>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-footer absolute>
      <v-container class="ma-0 pa-0">
        <v-card>
          <v-card-text>
            <v-row no-gutters>
              <v-col>
                <div class="d-flex">
                  <v-text-field
                      v-model="msg"
                      placeholder="Type Something"
                      @keypress.enter="send"></v-text-field>
                  <v-btn icon class="ml-4" @click="send">
                    <v-icon>mdi-send</v-icon>
                  </v-btn>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-container>
    </v-footer>
  </div>
</template>

<script>
export default {
  name: "Chat",
  data() {
    return {
      chat: [],
      msg: null,
    }
  },
  methods: {
    send: function () {
      this.chat.push(
          {
            from: "user",
            msg: this.msg
          })
      this.msg = null
      this.addReply()
    },
    addReply() {
      this.chat.push({
        from: "lithohub",
        msg: this.$t('Chat.reply')
      })
    }
  }
}
</script>

<style scoped>

</style>
