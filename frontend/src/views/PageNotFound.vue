<template>
  <v-card>
    <v-card-title>
    Erreur 404 : Page introuvable
    </v-card-title>
    <v-card-subtitle>
      Désolé, la page à laquelle vous tentez d'accéder n'existe pas ou n'a pas pu être chargée.
    </v-card-subtitle>
  </v-card>
</template>
<script>
export default {
  mounted()
  {
    document.title = "Erreur 404"
  }
}
</script>