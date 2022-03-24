<template>
  <v-container>
    <v-card>
      <v-card-title>
        <strong>Résultats de recherche</strong>
      </v-card-title>
      <v-card-subtitle>
        Recherche effectuée : "{{ searchTerm }}"
      </v-card-subtitle>
      <v-card-text>
        <list-of-components
          :components="components"
          :columnsEnabled="componentsListColumns"
          :nbComponentsPerPage="10"
        />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
import ListOfComponents from "../components/ListOfComponents.vue";
export default {
  name: "Components",
  data() {
    return {
      components: [],
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
      searchTerm: ''
    };
  },
  components: {
    ListOfComponents,
  },
  mounted() {
    document.title = 'Résultats de recherche'
    if(this.$store.state.searchTerm)
    {
      this.searchTerm = this.$store.state.searchTerm
      this.searchComponents();
    }
  },
  methods: {
    /**
     * Get all components matching search term
     */
    searchComponents() {
      axios
        .post(`/api/v1/components/search/`, {'query':this.searchTerm})
        .then((response) => {
          this.components = response.data;
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
