<template>
<v-container>
  <v-data-table
    :headers="headers"
    :items="components"
    :items-per-page="nbComponentsPerPage"
    no-data-text="Aucun composant à afficher"
  >
    <template v-slot:[`item.get_thumbnail`]="{ item }">
      <img
        :src="item.get_thumbnail"
        style="width: 50px; height: 50px"
        v-if="item.get_thumbnail"
      />
    </template>
    <template v-slot:[`item.date_updated`]="{ item }">
      {{ new Date(item.date_updated).toLocaleDateString() }}
    </template>
    <template v-slot:[`item.title`]="{ item }">
      <router-link :to="'/component/' + item.id">
        {{ item.title }}
      </router-link>
    </template>
    <template v-slot:[`item.ref`]="{ item }">
      <router-link :to="'/component/' + item.id">
        {{ item.ref }}
      </router-link>
    </template>
    <template v-slot:[`item.compartment`]="{ item }">
      <router-link :to="'/compartment/' + item.compartment">
        #{{ item.compartment }}
      </router-link>
    </template>
    <template v-slot:[`item.category_name`]="{ item }">
      <router-link :to="'/category/' + item.category_slug">
        {{ item.category_name }}
      </router-link>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
        <v-icon @click="targetComponent = item; confirmDeletionDialog = true">mdi-delete</v-icon>
    </template>
  </v-data-table>
  <v-dialog v-model="confirmDeletionDialog" width="700">
      <v-card>
        <v-card-title> Confirmer la suppression</v-card-title>
        <v-card-text>
          Voulez-vous vraiment supprimer le composant "{{targetComponent.title}}" ?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteComponent()" color="primary"
            >Supprimer</v-btn
          >
          <v-btn @click="confirmDeletionDialog = false">Annuler</v-btn>
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
import axios from 'axios';
export default {
  name: "ListOfComponents",
  props: {
    components: Array,
    columnsEnabled: Array,
    nbComponentsPerPage: Number,
  },
  data: () => ({
    headersAvailable: [
      {
        text: "Dernière MàJ",
        value: "date_updated",
      },
      {
        text: "Titre",
        value: "title",
      },
      { text: "Réf.", value: "ref" },
      { text: "Catégorie", value: "category_name" },
      { text: "Image", value: "get_thumbnail", sortable: false },
      { text: "Quantité", value: "quantity" },
      { text: "Compartiment", value: "compartment" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    targetComponent: {},
    unauthorized: false,
    confirmDeletionDialog: false
  }),
  computed: {
    headers() {
      var test = this.headersAvailable.filter((header) =>
        this.columnsEnabled.includes(header.value)
      );
      return test;
    },
  },
  methods: {
    /**
     * Delete a component
     */
    deleteComponent(){
      axios
        .delete(
          `/api/v1/delete-component/${this.targetComponent.id}`
        )
        .then((response) => {
          this.confirmDeletionDialog = false
          this.$emit('componentsUpdated')
        })
        .catch((error) => {
          console.log(error);
          switch (error.response.status) {
            case 401:
              this.$router.push({ name: "Login" });
              break;
            case 403:
              this.confirmDeletionDialog = false
              this.unauthorized = true
              break;
            default:
              this.$router.push({ name: "ErrorAPI" });
              break;
          }
        });
    }
  },
};
</script>