<template>
  <div>
    <nav class="flex items-center justify-between flex-wrap bg-teal-500 p-6">
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
          <div v-if="$auth.isAuthenticated">
            {{ $auth.user.displayName }}
            <n-link
              to="/upgrade"
              tag="button"
              class="bg-yellow-700 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded"
            >
              Upgrade
            </n-link>

            <button
              class="bg-teal-700 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              @click="logout"
            >
              Logout
            </button>
          </div>

          <div v-else>
            <button
              class="bg-teal-700 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              @click="googleLogin"
            >
              Login with Google
            </button>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
// Minimal Firebase package import

export default {
  methods: {
    async googleLogin(user) {
      var provider = new this.$fireModule.auth.GoogleAuthProvider();
      provider.addScope("profile");
      provider.addScope("email");

      try {
        await this.$fire.auth.signInWithPopup(provider);

        // Get the current user idToken
        await this.$store.dispatch("auth/fetchUser");
      } catch (e) {
        console.error(e);
      }

      await this.$axios.get("/get-or-create-user");

      this.$toast.success("Successfully authenticated");
      this.$router.go();
    },
    async logout() {
      this.$fire.auth.signOut();
      await this.$apolloHelpers.onLogout();
      this.$toast.success("Successfully logged out");
    },
  },
};
</script>
