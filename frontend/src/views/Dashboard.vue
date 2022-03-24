<template>
  <v-container>
    <v-card>
      <v-card-title>
        <strong>Bienvenue sur StockManager !</strong>
      </v-card-title>
      <v-card-subtitle>
        Votre gestionnaire de stock préféré. StockManager a été créé pour
        simplifier le stockage aléatoire de pièces dans des compartiments
        numérotés.
      </v-card-subtitle>
    </v-card>
    <div v-if="$store.state.isAuthenticated">
      <v-card>
        <v-card-title>
          <strong>Catégories de composants</strong>
        </v-card-title>
        <v-card-text>
          <list-of-categories :categories="categories" />
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title>
          <strong>Derniers composants mis à jour</strong>
        </v-card-title>
        <v-card-text>
          <list-of-components
            :components="latestComponents"
            :columnsEnabled="componentsListColumns"
            :nbComponentsPerPage="5"
          />
        </v-card-text>
      </v-card>
    </div>
    <div v-else>
      <v-row>
        <v-col cols="12" sm="6"> 
      <login-form />
        </v-col>
        <v-col cols="12" sm="6">
      <signup-form />
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import ListOfComponents from "../components/ListOfComponents.vue";
import ListOfCategories from "../components/ListOfCategories.vue";
import LoginForm from "../components/LoginForm.vue";
import SignupForm from "../components/SignupForm.vue";
import axios from "axios";

export default {
  name: "Dashboard",
  data() {
    return {
      latestComponents: [],
      categories: [],
      componentsListColumns: [
        "date_updated",
        "category_name",
        "get_image",
        "get_thumbnail",
        "title",
        "ref",
        "quantity",
        "compartment",
      ],
    };
  },
  components: {
    ListOfComponents,
    ListOfCategories,
    LoginForm,
    SignupForm,
  },
  mounted() {
    document.title = "Tableau de bord";
    if (this.$store.state.isAuthenticated) {
      this.getLatestComponents();
      this.getCategories();
    }
  },
  methods: {
    /**
     * Get list of 10 last updated components
     */
    getLatestComponents() {
      axios
        .get("/api/v1/latest-components")
        .then((response) => {
          this.latestComponents = response.data;
        })
        .catch((error) => {
          console.log(error);
          switch (error.response.status) {
            case 401:
              this.$router.push({ name: "Login" });
              break;

            default:
              this.$router.push({ name: "ErrorAPI" });
              break;
          }
        });
    },
    /**
     * Get all categories
     */
    getCategories() {
      axios
        .get("/api/v1/categories")
        .then((response) => {
          this.categories = response.data;
          /* this.categories = this.categories.slice(10) */
        })
        .catch((error) => {
          console.log(error);
          switch (error.response.status) {
            case 401:
              this.$router.push({ name: "Login" });
              break;

            default:
              this.$router.push({ name: "ErrorAPI" });
              break;
          }
        });
    },
  },
};
</script>
