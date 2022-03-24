<template>
  <signup-form />
</template>
<script>
import SignupForm from "../components/SignupForm.vue";
export default {
  name: "Signup",
  components: {
    SignupForm,
  },
  data() {
    return {};
  },
  mounted() {
    document.title = "Créer un compte";
  },
  methods: {},
};
</script>