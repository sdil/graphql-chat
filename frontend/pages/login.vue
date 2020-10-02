<template>
  <div>
    <button @click="googleLogin">Login with Google</button>
    <div v-if="$auth.isAuthenticated">
      {{ $auth.user }}
      <button @click="logout">Logout</button>
      <nuxt-link to="/messages">Messages</nuxt-link>
    </div>
  </div>
</template>


<script>
import firebase from "firebase";

export default {
  methods: {
    async googleLogin(user) {
      var provider = new firebase.auth.GoogleAuthProvider();
      provider.addScope("profile");
      provider.addScope("email");
      try {
        var token
        await this.$fireAuth.signInWithPopup(provider).then(function (result) {
          var user = result.user;
          token = user.xa
          console.log(user);
        });
        await this.$apolloHelpers.onLogin(token, undefined, { expires: 7 });
      } catch (e) {
        console.error(e);
      }
    },
    async logout() {
      this.$fireAuth.signOut();
      await this.$apolloHelpers.onLogout();
    },
  },
};
</script>