<template>
  <div>
    <div v-if="$apollo.loading">
      <div class="animate-pulse flex space-x-4">
        <div class="flex-1 space-y-4 py-1">
          <div class="h-4 bg-gray-400 rounded w-3/4"></div>
          <div class="h-4 bg-gray-400 rounded w-3/4"></div>
          <div class="h-4 bg-gray-400 rounded w-3/4"></div>
        </div>
      </div>
    </div>

    <div id="chat">
      <div class="scrolling-touch overflow-auto">
        <p v-for="m in message" :key="m.id">
          <span class="ml-2">{{ m.message }}</span>
          <span class="float-right font-semibold text-teal-700 text-opacity-50"
            >{{ m.messagePoster.name }} {{ $dayjs(m.sent_at).fromNow() }}
          </span>
        </p>
      </div>

      <form
        v-if="$auth.isAuthenticated"
        class="w-full absolute bottom-0"
        @submit.prevent="submitNewMessage"
      >
        <div class="flex items-center border-b py-2">
          <input
            class="shadow appearance-none block bg-transparent bg-gray-300 w-full text-gray-700 mr-3 py-1 px-2 leading-tight rounded focus:outline-none focus:bg-white"
            type="text"
            v-model="newMessage"
          />
          <input
            class="bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
            value="Send"
          />
        </div>
      </form>
      <div
        v-else
        class="w-full absolute bottom-0 font-semibold text-center mb-5"
      >
        Please Login to Chat
      </div>
    </div>
  </div>
</template>

<script>
import gql from "graphql-tag";
import unionBy from "lodash.unionby";

export default {
  data() {
    return {
      newMessage: "",
    };
  },
  methods: {
    submitNewMessage: function (message) {
      this.$apollo.mutate({
        mutation: gql`
          mutation AddNewMessage($newMessage: String!, $room: uuid!) {
            insert_message(objects: { message: $newMessage, room: $room }) {
              returning {
                message
                sent_at
                sent_by
              }
            }
          }
        `,
        // Parameters
        variables: {
          newMessage: this.newMessage,
          room: this.$route.params.id,
        },
      });
      this.newMessage = "";
    },
  },
  apollo: {
    message: {
      query: gql`
        query Messages($room: uuid!) {
          message(where: { room: { _eq: $room } }) {
            messagePoster {
              name
            }
            id
            sent_at
            message
          }
        }
      `,
      variables() {
        // This works just like regular queries
        // and will re-subscribe with the right variables
        // each time the values change
        return {
          room: this.$route.params.id,
        };
      },
      subscribeToMore: {
        document: gql`
          subscription MessageSubscription($room: uuid!) {
            message(where: { room: { _eq: $room } }) {
              messagePoster {
                name
              }
              id
              message
              sent_at
            }
          }
        `,
        variables() {
          // This works just like regular queries
          // and will re-subscribe with the right variables
          // each time the values change
          return {
            room: this.$route.params.id,
          };
        },

        updateQuery: (previousResult, { subscriptionData }) => {
          // Merge the previous result and new subscription data (from WS).
          // Hasura will send all data (not only new one) when establishing subscription.
          return { message: unionBy(previousResult.message, subscriptionData.data.message, 'message') };
        },
      },
    },
  },
  head: {
    title: "Messages",
  },
};
</script>