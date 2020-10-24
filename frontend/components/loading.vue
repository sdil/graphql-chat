<template>
  <div v-if="loading" class="loading-page">
    <div id="bm"></div>
  </div>
</template>

<script>
export default {
  data: () => ({
    loading: false,
  }),
  methods: {
    start() {
      this.loading = true;
    },
    finish() {
      this.loading = false;
    },
  },
  mounted() {
    var animation = bodymovin.loadAnimation({
      container: document.getElementById("bm"), // Required
      path: "/loader-lottie.json", // Required
      renderer: "svg",
      name: "Hello World", // Name for future reference. Optional.
    });
  },
};
</script>

<style>
#bm {
  width: 100vh;
  height: 100vh;
}
</style>