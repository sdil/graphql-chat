<template>
  <div>
    <div v-if="$auth.loading">Loadingg....</div>

    <div v-else>
      <div>
        <nav
          class="flex items-center justify-between flex-wrap bg-teal-500 p-6"
        >
          <div class="flex items-center flex-shrink-0 text-white mr-6">
            <nuxt-link to="/" class="font-semibold text-xl tracking-tight"
              >Chat App</nuxt-link
            >
          </div>
          <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
            <div class="text-sm lg:flex-grow">
              <a
                href="https://github.com/sdil/graphql-chat"
                class="block mt-4 lg:inline-block lg:mt-0 text-teal-100 hover:text-white mr-4 font-semibold"
                >What is this?</a
              >
            </div>
            <div>
              <div v-if="!$auth.isAuthenticated">
                <button
                  class="bg-teal-700 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  @click="googleLogin"
                >
                  Login with Google
                </button>
              </div>
              <div v-else>
                <nuxt-link to="/me" class="text-white font-bold">{{
                  $auth.user.displayName
                }}</nuxt-link>
                <button
                  class="bg-teal-700 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                  @click="logout"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </nav>
      </div>
      <Nuxt />
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
      } catch (e) {
        console.error(e);
      }

      this.$axios.get("http://localhost:8082/get-or-create-user");

      // Set the token in the browser cookie
      await this.$apolloHelpers.onLogin(token, undefined, { expires: 7 });

      this.$toast.success("Successfully authenticated");
    },
    async logout() {
      this.$fireAuth.signOut();
      await this.$apolloHelpers.onLogout();
      this.$router.push("/");
      this.$toast.success("Successfully logged out");
    },
  },
};
</script>

<style>
html {
  font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
}

.button--green {
  display: inline-block;
  border-radius: 4px;
  border: 1px solid #3b8070;
  color: #3b8070;
  text-decoration: none;
  padding: 10px 30px;
}

.button--green:hover {
  color: #fff;
  background-color: #3b8070;
}

.button--grey {
  display: inline-block;
  border-radius: 4px;
  border: 1px solid #35495e;
  color: #35495e;
  text-decoration: none;
  padding: 10px 30px;
  margin-left: 15px;
}

.button--grey:hover {
  color: #fff;
  background-color: #35495e;
}
</style>
