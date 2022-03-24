<template>
  <v-app-bar color="primary" dark app clipped-left>
    <router-link
      to="/"
      tag="div"
      class="v-toolbar__title"
      style="cursor: pointer"
    >
      {{ mobile ? "SM" : "StockManager" }}
    </router-link>
    <v-spacer></v-spacer>
    <v-col cols="4">
      <v-text-field
        v-if="$store.state.isAuthenticated"
        class="pt-5"
        placeholder="Chercher un composant..."
        v-model="searchTerm"
        @keyup.enter="search()"
      ></v-text-field>
    </v-col>
    <v-btn v-if="$store.state.isAuthenticated" text @click="search()">
      <v-icon> mdi-magnify </v-icon>
    </v-btn>
    <v-menu left bottom v-if="$store.state.isAuthenticated">
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" v-on="on">
          <v-avatar width="80">
            <span>{{ $store.state.username }}</span>
          </v-avatar>
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="toggleDarkMode()">
          <v-list-item-title
            >{{ $store.state.darkMode ? "Désactiver" : "Activer" }} le dark
            mode</v-list-item-title
          >
          <v-list-item-icon
            ><v-icon>mdi-moon-waning-crescent</v-icon></v-list-item-icon
          >
          <!-- TODO -->
        </v-list-item>
        <v-list-item @click="logOut()">
          <v-list-item-title>Déconnexion</v-list-item-title>
          <v-list-item-icon><v-icon>mdi-logout</v-icon></v-list-item-icon>
        </v-list-item>
      </v-list>
    </v-menu>
    <div v-else>
      <v-btn to="/signup"> Créer un compte </v-btn>
      <v-btn to="/login"> Connexion </v-btn>
    </div>
  </v-app-bar>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return { components: {}, searchTerm: "" };
  },
  computed: {
    mobile() {
      return this.$vuetify.breakpoint.xs;
    },
  },
  methods: {
    /**
     * Redirects to the search results page if a search term was typed
     */
    search() {
      if (this.searchTerm) {
        this.$store.state.searchTerm = this.searchTerm;
        this.$router.push({ name: "Search" });
      }
    },
    /**
     * Toggles dark mode
     */
    toggleDarkMode() {
      let newDarkModeState = !this.$store.state.darkMode;
      this.$store.state.darkMode = newDarkModeState;
      if (this.$cookies) this.$cookies.set("dark-mode", newDarkModeState);
      this.$vuetify.theme.dark = newDarkModeState;
    },
    /**
     * Log out user
     */
    logOut() {
      this.$store.commit("removeToken");
      this.$router.push({ name: "Dahsboard" });
      window.location.reload();
    },
  },
  mounted() {},
};
</script>
