<template>
  <div class="container mx-auto">
    <p class="font-sans text-gray-800 text-4xl font-semibold">Rooms</p>
    <div v-for="r in room" class="bg-gray-400 rounded-lg p-6">
      <div :key="r.id">
        <nuxt-link :to="'/chat/' + r.id" class="text-lg">{{r.name}}</nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
import gql from "graphql-tag";

export default {
  data() {
    return {
      room: [],
    };
  },
  apollo: {
    room: {
      query: gql`
        query room {
          room {
            description
            id
            name
          }
        }
      `,
    },
  },
};
</script>

<style>
/* Sample `apply` at-rules with Tailwind CSS
.container {
@apply min-h-screen flex justify-center items-center text-center mx-auto;
}
*/

.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
