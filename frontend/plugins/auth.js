import Vue from 'vue';

class AuthService {
    constructor(store) {
        this.$store = store;
    }

    get isAuthenticated() {
        return this.$store.state.auth.isAuthenticated;
    }

    get user() {
        return this.$store.state.auth.user;
    }

    get email() {
        if (!this.user) return;
        return this.user.email;
    }

    get loading() {
        return this.$store.state.auth.loading;
    }
}

export default async ({ store }) => {
    const authService = new AuthService(store);
    Vue.prototype.$auth = authService;
    Vue.$auth = authService;
}