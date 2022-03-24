<template>
  <v-container>
    <v-card>
      <v-card-title>
        <strong>Tous les composants</strong>
      </v-card-title>
      <v-card-text>
        <v-btn color="primary" @click="openComponentDialog()">
          <v-icon left>mdi-plus</v-icon>
          Ajouter un composant
        </v-btn>
        <list-of-components
          :components="components"
          :columnsEnabled="componentsListColumns"
          :nbComponentsPerPage="10"
          @componentsUpdated="getComponents()"
        />
      </v-card-text>
    </v-card>
    <v-dialog v-model="addComponentDialog" width="700">
      <v-card>
        <v-card-title> Ajouter un composant </v-card-title>
        <v-card-text>
          <v-form v-model="valid" ref="form">
            <v-row>
              <v-col cols="6">
                <v-text-field
                  label="* Nom"
                  v-model="newComponent.title"
                  :rules="rules.title"
                ></v-text-field>
                <v-text-field
                  label="* Référence"
                  :rules="rules.ref"
                  v-model="newComponent.ref"
                ></v-text-field>
                <v-text-field
                  label="* Quantité"
                  type="number"
                  min="0"
                  max="2000"
                  v-model="newComponent.quantity"
                  :rules="rules.quantity"
                ></v-text-field>
                <v-select
                  label="* Catégorie"
                  :items="categories"
                  item-text="name"
                  item-value="id"
                  :rules="rules.category"
                  v-model="newComponent.category"
                >
                  <template slot="item" slot-scope="data">
                    <v-row align="center">
                      <v-col cols="2">
                        <v-img
                          :src="data.item.get_thumbnail"
                          height="50"
                          width="50"
                        ></v-img>
                      </v-col>
                      <v-col cols="10">
                        <span>{{ data.item.name }}</span>
                      </v-col>
                    </v-row>
                  </template>
                </v-select>
                <v-select
                  label="* Compartiment"
                  :items="compartments"
                  item-text="id"
                  item-value="id"
                  :rules="rules.compartment"
                  v-model="newComponent.compartment"
                >
                  <template slot="item" slot-scope="data">
                    <v-row>
                      <v-col cols="2">
                        <span>#{{ data.item.id }}</span>
                      </v-col>
                      <v-col cols="10">
                        <v-progress-linear
                          :value="data.item.get_filling_rate"
                        ></v-progress-linear>
                      </v-col>
                    </v-row>
                  </template>
                </v-select>
              </v-col>
              <v-col cols="6">
                <v-file-input
                  label="Image"
                  accept="image/*"
                  v-model="newComponent.image"
                ></v-file-input>
                <v-textarea
                  lang="fr"
                  label="Description"
                  :rules="rules.desc"
                  v-model="newComponent.desc"
                  max-length="200"
                  counter="2000"
                  no-resize
                  height="100"
                ></v-textarea>
                <v-text-field
                  label="URL du datasheet"
                  type="url"
                  :rules="rules.datasheet_url"
                  v-model="newComponent.datasheet_url"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn :disabled="!valid" @click="registerComponent()" color="primary"
            >Ajouter</v-btn
          >
          <v-btn @click="addComponentDialog = false">Annuler</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="unauthorized" width="500">
      <v-card>
        <v-card-title> Action non autorisée </v-card-title>
        <v-card-text>
          Désolé, vous ne disposez pas des permissions nécessaires pour ajouter ou supprimer des composants.
        </v-card-text>
        <v-card-actions>
          <v-btn @click="unauthorized = false">J'ai compris</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";
import ListOfComponents from "../components/ListOfComponents.vue";
const URLRegex =
  /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/;
export default {
  name: "Components",
  data() {
    return {
      components: [],
      newComponent: {
        title: "",
        ref: "",
        quantity: "",
        compartment: "",
        desc: "",
        category: "",
        datasheet_url: "",
        image: [],
      },
      componentsListColumns: [
        "date_updated",
        "category_name",
        "get_image",
        "get_thumbnail",
        "title",
        "ref",
        "quantity",
        "compartment",
        "actions"
      ],
      compartments: [],
      categories: [],
      valid: false,
      unauthorized: false,
      addComponentDialog: false,
      rules: {
        title: [
          (v) => !!v || "Le nom du composant est requis",
          (v) => (v && v.length < 255) || "Le nom du composant est trop long",
        ],
        ref: [
          (v) => !!v || "La référence du composant est requise",
          (v) =>
            (v && v.length < 255) ||
            "La référence du composant est trop longue",
        ],
        desc: [
          (v) => !v || v.length < 2000 || "La description est trop longue",
        ],
        quantity: [
          (v) => !!v || "La quantité est requise",
          (v) => v >= 0 || "La quantité ne peut pas être négative",
          (v) => v <= 2000 || "La quantité doit être inférieure à 2000",
        ],
        datasheet_url: [
          (v) => !v || this.isURLValid(v) || "Ceci n'est pas une URL valide",
        ],
        compartment: [(v) => !!v || "Le compartiment est requis"],
        category: [(v) => !!v || "La catégorie est requise"],
      },
    };
  },
  components: {
    ListOfComponents,
  },
  mounted() {
    document.title = "Composants"
    this.getComponents();
  },
  methods: {
    /**
     * Get list of components
     */
    getComponents() {
      axios
        .get("/api/v1/components")
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
    /**
     * Get list of available compartments
     */
    getCompartments() {
      axios
        .get("/api/v1/compartments")
        .then((response) => {
          this.compartments = response.data;
          this.compartments.sort(
            (a, b) => a.get_filling_rate - b.get_filling_rate
          );
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
     * Get list of available categories
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
     * Register new component
     */
    registerComponent() {
      let formData = new FormData();
      for (const property in this.newComponent) {
        formData.append(property, this.newComponent[property]);
      }
      axios
        .post("/api/v1/component", formData)
        .then((response) => {
          this.$refs.form.reset();
          this.addComponentDialog = false;
          this.getComponents();
        })
        .catch((error) => {
          console.log(error);
          switch (error.response.status) {
            case 401:
              this.$router.push({ name: "Login" });
              break;

            case 403:
              this.addComponentDialog = false
              this.unauthorized = true
              break;
          
            default:
              this.$router.push({ name: "ErrorAPI" });
              break;
          }
        });
    },
    /**
     * Checks if a URL has correct format
     * @param string inputURL The URL to be checked
     * @return bool check result
     */
    isURLValid(inputURL) {
      if (!inputURL) return false;
      return inputURL.match(URLRegex);
    },
    /**
     * Opens the component add dialog
     */
    openComponentDialog() {
      this.getCompartments();
      this.getCategories(), (this.addComponentDialog = true);
    },
  },
};
</script>
