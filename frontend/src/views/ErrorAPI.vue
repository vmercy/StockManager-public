<template>
  <v-card>
    <v-card-title>
    Erreur API
    </v-card-title>
    <v-card-subtitle>
      Désolé, StockManager rencontre actuellement une erreur d'API. Veuillez réessayer plus tard.
    </v-card-subtitle>
  </v-card>
</template>
<script>
export default {
  mounted()
  {
    document.title = "Erreur API"
  }
}
</script>