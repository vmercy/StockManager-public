<template>
  <v-app>
    <NavBar />
    <LeftMenu />
    <v-main id="main">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import LeftMenu from "./components/LeftMenu.vue";
import axios from "axios";
export default {
  name: "App",

  data: () => ({}),

  components: {
    NavBar,
    LeftMenu,
  },

  methods: {},
  beforeCreate() {
    /**
     * Restricting all routes to non-authenticated users except Login and Dashboard ones
     */
    this.$router.beforeEach((to, from, next) => {
      if (
        to.name !== "Login" &&
        to.name !== "Signup" &&
        to.name !== "ErrorAPI" &&
        to.name !== "Dashboard" &&
        !this.$store.state.isAuthenticated
      )
        next({ name: "Dashboard" }); //redirect to dashboard
      else next();
    });

    this.$store.commit("initializeStore");
    const token = this.$store.state.token;
  
    if (token) {
      axios.defaults.headers.common["Authorization"] = "Token " + token; //set API authorization token
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
  },
  created()
  {
    document.title = "Stock Manager"
  },
  mounted()
  {
    if(window.$cookies) //retrieve dark mode state from cookies
    {
      let darkModeState = window.$cookies.get('dark-mode')
      darkModeState = (darkModeState=="true" ? true : false) 
      this.$store.state.darkMode = darkModeState
      this.$vuetify.theme.dark = darkModeState
    }
  }
};
</script>

<style scoped>
#main {
  margin: 10px;
}
</style>