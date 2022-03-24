<template>
  <v-card>
    <v-card-title> Composant : {{ component.title }} </v-card-title>
    <v-card-subtitle> Référence: {{ component.ref }} </v-card-subtitle>
    <v-card-text>
      <v-row>
        <v-col cols="12" md="6" lg="4">
          <ul>
            <li>Catégorie : <router-link :to="`/category/${component.category_slug}`">{{ component.category_name }}</router-link></li>
            <li>Quantité en stock : {{ component.quantity }}</li>
            <li>Compartiment : <router-link :to="`/compartment/${component.compartment}`">#{{ component.compartment }}</router-link></li>
          </ul>
            <v-btn color="primary" v-if="component.datasheet_url" target="_blank" :href="component.datasheet_url">
              <v-icon left>
                mdi-file
              </v-icon>
              Ouvrir la datasheet
            </v-btn>
        </v-col>
        <v-col cols="12" md="6" lg="4">
          <span><i>
          {{component.desc}}
          </i>
          </span>
        </v-col>
        <v-col cols="12" md="6" lg="4">
          <v-img
            :src="component.get_image"
            height="200"
            contain
          ></v-img>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  name: "Component",
  data: () => ({
    category: {},
    component: {},
  }),
  mounted(){
    document.title = "Composant"
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
     * Get component details
     */
    getComponent() {
      axios
        .get(
          `/api/v1/component/${this.$route.params.component_id}`
        )
        .then((response) => {
          this.component = response.data;
          document.title = `Composant ${this.component.title}`
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
    this.getComponent();
    //this.getCategory();
  },
};
</script>