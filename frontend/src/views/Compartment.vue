<template>
  <v-card>
    <v-card-title> Compartiment : #{{ compartment.id }} </v-card-title>
    <v-card-subtitle>
      <v-row>
        <v-col cols="4">
          <span
            >{{ pluralize(compartment.get_nb_ref, "référence") }} /
            {{ pluralize(compartment.get_nb_units, "unité") }}</span
          >
        </v-col>
        <v-col cols="8">
          <v-progress-linear
            :value="compartment.get_filling_rate"
            width="2"
          ></v-progress-linear>
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-card-text>
      Composants dans ce compartiment :
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
  name: "Compartment",
  data: () => ({
    compartment: {},
    components: [],
    componentsListColumns: [
      "date_updated",
      "get_image",
      "get_thumbnail",
      "title",
      "category_name",
      "ref",
      "quantity",
    ],
  }),
  mounted()
  {
    document.title = "Compartiment"
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
     * Get list of compartments
     */
    getCompartment() {
      axios
        .get(
          `/api/v1/compartment/${this.$route.params.compartment_id}`
        )
        .then((response) => {
          this.compartment = response.data;
          document.title = `Compartiment #${this.compartment.id}`
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
     * Get list of components in compartment
     */
    getComponents() {
      axios
        .get(
          `/api/v1/components/compartment=${this.$route.params.compartment_id}`
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
    this.getCompartment();
    this.getComponents();
  },
};
</script>