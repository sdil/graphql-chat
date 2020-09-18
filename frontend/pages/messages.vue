<template>
    <div>
        test
        {{ user[0].username }}
    </div>
</template>

<script>
import messages from "~/apollo/queries/fetchMessages"

export default {
    apollo: {
        user: {
            prefetch: true,
            query: messages
        }
    },
    head: {
    title: 'Messages'
  }
}
</script>