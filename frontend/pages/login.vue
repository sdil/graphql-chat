<template>
  <div>
    <div v-if="!$auth.isAuthenticated">
      <button @click="googleLogin">Login with Google</button>
    </div>
    <div v-else>
      {{ $auth.user }}
      <button @click="logout">Logout</button>
      <nuxt-link to="/messages">Messages</nuxt-link>
    </div>
  </div>
</template>


<script>
// Minimal Firebase package import
import firebase from "firebase/app";

export default {
  methods: {
    async googleLogin(user) {
      var provider = new firebase.auth.GoogleAuthProvider();
      provider.addScope("profile");
      provider.addScope("email");
      try {
        var token;

        await this.$fireAuth.signInWithPopup(provider);

        // Get the current user idToken
        await this.$fireAuth.currentUser
          .getIdToken(true)
          .then(function (idToken) {
            token = idToken;
          })
          .catch(function (error) {
            console.error("Failed to get firebase idToken" + error);
          });

        // Set the token in the browser cookie
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