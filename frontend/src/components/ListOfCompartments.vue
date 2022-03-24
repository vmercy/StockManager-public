<template>
  <v-expansion-panels>
    <v-expansion-panel
      v-for="compartment in compartments"
      :key="compartment.id"
      @click="
        expandedCompartmentId = compartment.id;
        getComponentsInExpandedCompartment();
      "
    >
      <v-expansion-panel-header>
        <v-row>
          <v-col cols="2"
            ><router-link :to="`/compartment/${compartment.id}`">
              #{{ compartment.id }}</router-link
            ></v-col
          >
          <v-col cols="6"
            ><v-progress-linear
              :value="compartment.get_filling_rate"
              width="2"
            ></v-progress-linear
          ></v-col>
          <!-- TODO -->
          <v-col cols="4"
            ><span
              >({{ pluralize(compartment.get_nb_ref, "référence") }} /
              {{ pluralize(compartment.get_nb_units, "unité") }})</span
            ></v-col
          >
        </v-row>
      </v-expansion-panel-header>
      <v-expansion-panel-content v-if="componentsInExpandedCompartment.length">
        <list-of-components
          :columnsEnabled="componentsListColumns"
          :components="componentsInExpandedCompartment"
          :nbComponentsPerPage="nbComponentsPerPage"
        />
      </v-expansion-panel-content>
      <v-expansion-panel-content v-else>
        Aucun composant n'est rangé dans ce compartiment
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import ListOfComponents from "../components/ListOfComponents.vue";
import axios from "axios";
export default {
  name: "ListOfCompartments",
  components: {
    ListOfComponents,
  },
  props: {
    compartments: Array,
    componentsColumnsEnabled: Array,
    nbComponentsPerPage: Number,
  },
  data: () => ({
    componentsListColumns: [
      "date_updated",
      "category_name",
      "get_image",
      "get_thumbnail",
      "title",
      "ref",
      "quantity",
    ],
    expandedCompartmentId: 1,
    componentsInExpandedCompartment: [],
  }),
  computed: {},
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
     * Get the component of compartment which expansion panel is expanded
     */
    getComponentsInExpandedCompartment() {
      axios
        .get(
          `/api/v1/components/compartment=${this.expandedCompartmentId}`
        )
        .then((response) => {
          this.componentsInExpandedCompartment = response.data;
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
    this.getComponentsInExpandedCompartment();
  },
};
</script>