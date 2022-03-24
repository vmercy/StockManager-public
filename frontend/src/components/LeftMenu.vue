<template>
  <v-navigation-drawer
    clipped
    expand-on-hover
    mini-variant
    absolute
    app
    color="primary"
    permanent
  >
    <v-list dense nav>
      <v-list-item v-for="item in items" :key="item.title" link :to="item.route">
        <v-list-item-icon>
          <v-icon color="text">{{ item.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title :style="itemTitleStyle" class="itemTitle">{{
            item.title
          }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  data: () => ({
    items: [
      { title: "Accueil", icon: "mdi-home", route: "/" },
      { title: "Catégories", icon: "mdi-shape", route: "/categories" },
      { title: "Composants", icon: "mdi-puzzle", route: "/components"  },
      { title: "Compartiments", icon: "mdi-archive", route: "/compartments"  },
    ],
    right: null,
    expanded: false,
  }),
  computed: {
    itemTitleStyle() {
      return "--text-color:" + this.$vuetify.theme.currentTheme.text + ";";
    },
  },
  methods: {
    
  },
};
</script>

<style scoped>
.itemTitle {
  color: var(--text-color, white);
}
</style>
