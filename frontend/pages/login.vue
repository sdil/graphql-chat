<template>
  <div>
    <h3 class="display-1 mb-5">Firebase Authentication</h3>
    Login
    <div class="links">
      <input type="text" v-model="formData.email" />
      <input type="text" v-model="formData.password" />
      <input @click="signInUser" type="submit" />
    </div>
    Register
    <div class="links">
      <input type="text" v-model="formData.email" />
      <input type="text" v-model="formData.password" />
      <input @click="signInUser" type="submit" />
    </div>

    <input @click="googleLogin" type="submit" />
  </div>
</template>


<script>
import firebase from "firebase"

export default {
  data() {
    return {
      formData: {
        email: "",
        password: "",
      },
    };
  },
  methods: {
    googleLogin: function (user) {
      var provider = new firebase.auth.GoogleAuthProvider();
      provider.addScope("profile");
      provider.addScope("email");
      this.$fireAuth.signInWithPopup(provider).then(function (result) {
        // This gives you a Google Access Token.
        var token = result.credential.accessToken;
        // The signed-in user info.
        var user = result.user;
        console.log(token)
        console.log(user)
      });
    },
    signInUser: function (user) {
      console.log(this.formData.email);
      console.log(this.formData.password);
      try {
        console.log(
          this.$fireAuth.signInWithEmailAndPassword(
            this.formData.email,
            this.formData.password
          )
        );
      } catch (e) {
        alert(e);
      }
      //   console.log(this.)
    },
  },
};
</script>