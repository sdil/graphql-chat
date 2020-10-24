<template>
  <div v-if="loading" class="loading-page">
    Loading...
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
};
</script>

<style>
#bm {
  width: 100vh;
  height: 100vh;
}
</style>