<template>
  <div>
    <webview style="height: 100vh; max-height: 100%;" id="webview" :src="device_address"></webview>
  </div>
</template>

<script>
export default {
  name: "WebView",
  computed: {
    device_address() {
      return "http://" + this.$route.params.ip + '/'
    }
  }
}
</script>

<style scoped>

</style>
