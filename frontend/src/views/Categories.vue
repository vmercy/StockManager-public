<template>
  <v-card>
    <v-card-title>
      <strong>Catégories de composants</strong>
    </v-card-title>
    <v-card-text>
      <list-of-categories :categories="categories" />
    </v-card-text>
  </v-card>
</template>

<script>
import ListOfCategories from "../components/ListOfCategories.vue";
import axios from "axios";

export default {
  name: "Categories",
  data() {
    return {
      latestComponents: [],
      categories: [],
    };
  },
  components: {
    ListOfCategories,
  },
  mounted() {
    document.title = "Catégories";
    this.getCategories();
  },
  methods: {
    /**
     * Get list of component categories
     */
    getCategories() {
      axios
        .get("/api/v1/categories")
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.log(error);
          switch (error.response.status) {
            /* case 401:
              this.$router.push({ name: "Login" });
              break; */
          
            default:
              this.$router.push({ name: "ErrorAPI" });
              break;
          }
        });
    },
  },
};
</script>
