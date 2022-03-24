<template>
  <v-card>
    <v-card-title>
      <strong>Tous les compartiments</strong>
    </v-card-title>
    <v-card-subtitle>
      <v-switch
        label="Masquer les compartiments vides"
        v-model="hideEmpty"
        @change="hideEmptyCompartments()"
      ></v-switch>
    </v-card-subtitle>
    <v-card-text>
      <list-of-compartments
        :compartments="compartments"
        :componentsColumnsEnabled="componentsListColumns"
        :nbComponentsPerPage="10"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios";
import ListOfCompartments from "../components/ListOfCompartments.vue";

export default {
  name: "Compartments",
  data() {
    return {
      compartments: [],
      componentsListColumns: [
        "date_updated",
        "category_name",
        "get_image",
        "get_thumbnail",
        "title",
        "ref",
        "quantity",
      ],
      hideEmpty: false,
    };
  },
  components: {
    ListOfCompartments,
  },
  mounted() {
    document.title = "Compartiments"
    this.getCompartments();
  },
  methods: {
    /**
     * Get all compartments
     */
    getCompartments() {
      axios
        .get("/api/v1/compartments")
        .then((response) => {
          this.compartments = response.data;
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
     * Hide empty compartments from list of compartments
     */
    hideEmptyCompartments() {
      if (this.hideEmpty) {
        this.compartments = this.compartments.filter(
          (compartment) => compartment.get_nb_units > 0
        );
      } else {
        this.getCompartments();
      }
    },
  },
};
</script>
