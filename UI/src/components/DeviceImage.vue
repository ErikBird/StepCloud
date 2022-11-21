<template>
  <v-img
      contain
      :src="image_src"
  ></v-img>
</template>

<script>
export default {
  name: "DeviceImage",
  props: ['device_type'],
  data() {
    return {
      //This is mandatory to preload all assets
      max_image: require("@/assets/deviceImages/MAX.png"),
      pro_image: require("@/assets/deviceImages/PRO_small.png"),
      shelly_plug_s_image: require("@/assets/deviceImages/SHPLG-S.png"),
      image_src: ''
    }
  },
  methods: {
    setImageSource() {
      if (this.device_type === "SHPLG-S") {
        this.image_src = this.shelly_plug_s_image
      } else if (this.device_type.includes("MAX")) {
        this.image_src = this.max_image
      } else {
        this.image_src = this.pro_image
      }
    },
  },
  created() {
    this.setImageSource();
  },
}
</script>
