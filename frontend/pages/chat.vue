<template>
  <div>
    messages:
    <ul>
      <li v-for="m in messages" :key="m.id">{{ m.message }} {{ m.sent_at }}</li>
    </ul>

    <input type="text" v-model="newMessage" />
    <input @click="submitNewMessage" type="submit" />
  </div>
</template>

<script>
import messages from "~/apollo/queries/fetchMessages";
import gql from "graphql-tag";

export default {
  data() {
    return {
      newMessage: "",
      messages: [],
    };
  },
  methods: {
    submitNewMessage: function (message) {
      console.log("message: " + this.newMessage);
      this.$apollo.mutate({
        mutation: gql`
          mutation AddNewMessage($newMessage: String!) {
            insert_message(objects: { message: $newMessage }) {
              returning {
                id
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
        },
      });
    },
  },
  apollo: {
    $subscribe: {
      messages: {
        query: gql`
          subscription MessageSubscription {
            message {
              id
              message
              sent_at
              sent_by
            }
          }
        `, result ({data}) {
            console.log(data)
            this.messages = data.message
        }
      },
    },
  },
  head: {
    title: "Messages",
  },
};
</script>