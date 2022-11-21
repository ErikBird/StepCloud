<template>
  <v-progress-linear
      :value=value
      :stream=stream
      :buffer-value=value
      :striped=striped
      :color=color
      rounded
  ></v-progress-linear>
</template>

<script>
export default {
  name: "DeviceProgress",
  props: ['device_ip'],
  data() {
    return {
      dialogLocation: false,
    }
  },
  computed: {
    value() {
      if (Object.keys(this.$store.getters.getStatus).length === 0) {
        return 100;
      }
      switch (this.$store.getters.getStatus[this.device_ip].status) {
        case 'offline':
          return 100;
        case 'running':
          return this.$store.getters.getStatus[this.device_ip].progress;
        default:
          return 100;
      }
    },
    color() {
      if (Object.keys(this.$store.getters.getStatus).length === 0) {
        return 'grey';
      }
      switch (this.$store.getters.getStatus[this.device_ip].status) {
        case 'running':
          if (this.$store.getters.getStatus[this.device_ip].progress === 100) {
            return "green";
          } else {
            return "primary";
          }
        case 'offline':
          return 'grey';
        default:
          return "grey";
      }
    },
    striped() {
      return false
    },
    stream() {
      if (Object.keys(this.$store.getters.getStatus).length === 0) {
        return true;
      }
      switch (this.$store.getters.getStatus[this.device_ip].status) {
        case 'pause':
          return false;
        case 'offline':
          return false;
        default:
          return true;
      }
    }
  },
  /*
    methods: {
        UpdateDeviceStatus() {
                if(res.status==='Production'){
                    this.value= (res.log.current_progress/res.log.total_progress)*100
                    this.striped= false
                    if (this.value === 100){
                        this.color= "green"
                    }else{
                        this.color=
                        this.stream=true
                    }
                } else if(res.status==='Status'){
                    if (res.log.label=== 'offline'){
                        this.value=100
                        this.stream=false
                        this.color="grey"
                        this.striped= true
                    } else if (res.log.label=== 'pause'){
                        this.stream=false
                        this.color="primary"
                        this.striped= false
                    }
                }else if(res.status==='Error'){
                    this.striped= false
                    if (res.log.fatal=== 'False') {
                        this.color = "amber"
                    }else{
                        this.value = 100
                        this.stream = false
                        this.color = "red"
                    }
                }
        }
    },
    mounted: function () {
      window.setInterval(() => {
        this.UpdateDeviceStatus()
      }, 10000)
    },
    created() {
        this.UpdateDeviceStatus();
    },*/

}
</script>

<style scoped>

</style>
