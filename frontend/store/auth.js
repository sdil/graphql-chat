
export const state = () => ({
    loading: true,
    isAuthenticated: false,
    user: null
})

export const mutations = {
    RESET_STORE: (state) => {
        state.isAuthenticated = false
        state.user = null
        state.loading = false
    },

    SET_AUTH_USER: (state, { authUser }) => {
        state.user = {
            uid: authUser.uid,
            email: authUser.email,
            displayName: authUser.displayName
        }
        state.isAuthenticated = true
    },

    SET_LOADING: (state, isLoading) => {
        state.loading = isLoading
    }
}

export const actions = {
    async nuxtServerInit({ dispatch }, ctx) {
        commit('SET_LOADING', true)
        if (this.$fireAuth === null) {
            throw 'nuxtServerInit Example not working - this.$fireAuth cannot be accessed.'
        }

        if (ctx.$fireAuth === null) {
            throw 'nuxtServerInit Example not working - ctx.$fireAuth cannot be accessed.'
        }

        if (ctx.app.$fireAuth === null) {
            throw 'nuxtServerInit Example not working - ctx.$fireAuth cannot be accessed.'
        }

        // INFO -> Nuxt-fire Objects can be accessed in nuxtServerInit action via this.$fire___, ctx.$fire___ and ctx.app.$fire___'

        /** Get the VERIFIED authUser from the server */
        if (ctx.res && ctx.res.locals && ctx.res.locals.user) {
            const { allClaims: claims, ...authUser } = ctx.res.locals.user

            console.info(
                'Auth User verified on server-side. User: ',
                authUser,
                'Claims:',
                claims
            )

            await dispatch('onAuthStateChanged', {
                authUser,
                claims
            })

        }
        
        commit('SET_LOADING', false)

    },

    onAuthStateChanged({ commit }, { authUser }) {
        commit('SET_LOADING', false)
        if (!authUser) {
            commit('RESET_STORE')
            return
        }
        commit('SET_AUTH_USER', { authUser })
    },

    checkVuexStore(ctx) {
        if (this.$fireAuth === null) {
            throw 'Vuex Store example not working - this.$fireAuth cannot be accessed.'
        }

        alert(
            'Success. Nuxt-fire Objects can be accessed in store actions via this.$fire___'
        )
        return
    }
}
