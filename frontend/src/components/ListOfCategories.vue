<template>
  <v-container class="">
    <v-row>
      <v-col v-for="category in categories" :key="category.slug" cols="12" sm="6" md="3">
        <router-link :to="`category/${category.slug}`" style="text-decoration: none; color: inherit;">
      <v-card>
        <v-img style="margin: auto" :src="category.get_thumbnail" height="150" width="150"> </v-img>
        <v-card-title>
          {{ category.name }}
        </v-card-title>
        <v-card-subtitle>{{pluralize(category.get_nb_ref, 'référence')}} / {{ pluralize(category.get_nb_units, 'unité') }}</v-card-subtitle>
      </v-card>
        </router-link>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "ListOfCategories",
  props: {
    categories: Array,
  },
  data: () => ({}),
  computed: {},
  methods: {
    /**
     * Add an 's' to the end of a work if necessay
     * 
     * @param int count The quantity indicator. If >1 the 's' will be added
     * @param string word The input word
     * @return string The maybe pluralized string
     */
    pluralize(count, word)
    {
      return `${count} ${word}${count>1 ? 's':''}`
    }
  },
};
</script>