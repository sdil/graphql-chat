<template>
  <div>
    <h3 class="display-1 mb-5">Firebase Authentication</h3>
    <div class="links">
      <input type="text" v-model="formData.email" />
      <input type="text" v-model="formData.password" />
      <input @click="signInUser" type="submit" />
    </div>
    {{authUser}}
  </div>
</template>


<script>
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
    signInUser: function (user) {
      console.log(this.formData.email);
      console.log(this.formData.password);
      try {
        console.log(this.$fireAuth.signInWithEmailAndPassword(
          this.formData.email,
          this.formData.password)
        );
      } catch (e) {
        alert(e);
      }
    //   console.log(this.)
    },
  },
};
</script>