<template>
  <div>
    <div v-if="step == 0">
      <div
        class="container flex flex-wrap pt-4 pb-10 m-auto mt-6 md:mt-15 lg:px-12 xl:px-16"
      >
        <div class="w-full px-0 lg:px-4">
          <h2
            class="px-12 text-base font-bold text-center md:text-2xl text-teal-700"
          >
            Choose your plan
          </h2>
          <p class="py-1 text-sm text-center text-teal-700 mb-10">
            It is a long established fact that a reader will be distracted by
            the readable content of a page when looking at its layout.
          </p>
          <div class="flex flex-wrap items-center justify-center py-4 pt-0">
            <div class="w-full p-4 md:w-1/2 lg:w-1/4 plan-card">
              <label
                class="flex flex-col rounded-lg shadow-lg group relative cursor-pointer hover:shadow-2xl"
              >
                <div class="w-full px-4 py-6 rounded-t-lg card-section-1">
                  <h3
                    class="mx-auto text-base font-semibold text-center underline text-teal-500 group-hover:text-white"
                  >
                    Standard
                  </h3>
                  <p
                    class="text-5xl font-bold text-center group-hover:text-white text-teal-500"
                  >
                    $25.<span class="text-3xl">95</span>
                  </p>
                  <p
                    class="text-xs text-center uppercase group-hover:text-white text-teal-500"
                  >
                    monthly
                  </p>
                </div>
                <div
                  class="flex flex-col items-center justify-center w-full h-full py-6 rounded-b-lg bg-teal-500"
                >
                  <p class="text-xl text-white">1 month</p>
                  <button
                    class="w-5/6 py-2 mt-2 font-semibold text-center uppercase bg-white border border-transparent rounded text-teal-500"
                    v-on:click="stepPay('Standard', 25.95)"
                  >
                    Get Started
                  </button>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="step == 1">
      <div
        class="container flex flex-wrap pt-4 pb-10 m-auto mt-6 md:mt-15 lg:px-12 xl:px-16"
      >
        <form
          class="w-full max-w-xl m-4 p-10 bg-white rounded shadow-xl"
          @submit.stop.prevent="handleSubmit"
        >
          <p class="mt-4 text-gray-800 font-semibold">Payment information</p>
          <div class="">
            <label class="block text-sm text-gray-600" for="cus_name"
              >Card</label
            >

            <card
              ref="card-stripe"
              stripe="pk_test_51HdoRrAWdm4F9r8C48eCqf3H5ggmnaNM8dLapbRdbgoJ9HpLyksUbGQPrLZF9KJ9gGPuVI2OBChNkteup4BNLRRC005OO5RElL"
              @change="complete = $event.complete"
            />
          </div>
          <div class="mt-4">
            <button
              class="px-4 py-1 text-white font-light tracking-wider bg-gray-900 rounded"
              type="submit"
            >
              Pay ${{ price }}
            </button>
            <button
              class="px-4 py-1 text-white font-light tracking-wider bg-red-900 rounded"
              v-on:click="stepBack"
            >
              Back
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { StripeElement, createPaymentMethod } from "vue-stripe-elements-plus";

export default {
  components: {
    StripeElement,
  },

  data() {
    return {
      step: 0,
      price: 0,
      plan: "",
      loading: false,
    };
  },
  methods: {
    stepPay: function (plan, price) {
      this.step = 1;
      this.price = price;
      this.plan = plan;
    },
    stepBack: function () {
      this.step = 0;
    },
    handleSubmit() {
      // Create Stripe PaymentMethod
      // Attach the PaymentMethod ID to the User in Stripe (by invoking API Server)

      this.loading = true;
      createPaymentMethod("card").then((result) => {
        console.log(result);
        this.loading = false;

        if (result.error) {
          console.log(result.error);
          this.$toast.error("Payment failed. Please try again");
          setTimeout(() => (this.error = ""), 3000);
        } else {
          this.$axios.post("/subscribe", {
            payment_method_id: result.paymentMethod.id,
            plan: this.plan,
          });
          this.$toast.success("Payment succeed");
          // payment succeeded! show a success message
          // there's always a chance your customer closes the browser after the payment process and before this code runs so
          // we will use the webhook in handle-payment-succeeded for any business-critical post-payment actions
          this.$router.push("/");
        }
      });
    },
  },
};
</script>