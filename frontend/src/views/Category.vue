<template>
  <v-card>
    <v-card-title> Catégorie : {{ category.name }} </v-card-title>
      <v-card-subtitle
        >{{ pluralize(category.get_nb_ref, "référence") }} /
        {{ pluralize(category.get_nb_units, "unité") }}</v-card-subtitle
      >
    <v-img
      :src="category.get_thumbnail"
      height="200"
      width="200"
      style="margin: auto"
    ></v-img>
    <v-card-text>
      Composants de la catégorie :
      <list-of-components
        :columnsEnabled="componentsListColumns"
        :components="components"
        :nbComponentsPerPage="10"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios";
import ListOfComponents from "../components/ListOfComponents.vue";
export default {
  components: { ListOfComponents },
  name: "Category",
  data: () => ({
    category: {},
    components: [],
    componentsListColumns: [
      "date_updated",
      "get_image",
      "get_thumbnail",
      "title",
      "ref",
      "quantity",
      "compartment",
    ],
  }),
  mounted()
  {
    document.title = "Catégorie"
  },
  methods: {
    /**
     * Add an 's' to the end of a work if necessay
     * 
     * @param int count The quantity indicator. If >1 the 's' will be added
     * @param string word The input word
     * @return string The maybe pluralized string
     */
    pluralize(count, word) {
      return `${count} ${word}${count > 1 ? "s" : ""}`;
    },
    /**
     * Get category details
     */
    getCategory() {
      axios
        .get(
          `/api/v1/category/${this.$route.params.category_slug}`
        )
        .then((response) => {
          this.category = response.data;
          document.title = `Catégorie : ${this.category.name}`;
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
    getComponents() {
      axios
        .get(
          `/api/v1/components/${this.$route.params.category_slug}`
        )
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
  mounted() {
    this.getCategory();
    this.getComponents();
  },
};
</script>