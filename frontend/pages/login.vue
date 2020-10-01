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
    twitterLogin: function (user) {
      var provider = new firebase.auth.TwitterAuthProvider();
      this.$fireAuth.signInWithPopup(provider).then(function (result) {
        var token = result.credential.accessToken;
        var secret = result.credential.secret;
        // The signed-in user info.
        var user = result.user;
      });
    },
    googleLogin: function (user) {
      var provider = new firebase.auth.GoogleAuthProvider();
      provider.addScope("profile");
      provider.addScope("email");
      this.$fireAuth.signInWithPopup(provider).then(function (result) {
        // This gives you a Google Access Token.
        var token = result.credential.accessToken;
        // The signed-in user info.
        var user = result.user;
      });
    },
    logout: function () {
      this.$fireAuth.signOut()
    }
  },
};
</script>