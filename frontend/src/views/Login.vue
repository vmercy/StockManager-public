<template>
  <login-form/>
</template>
<script>
import LoginForm from "../components/LoginForm.vue";
export default {
  name: "Login",
  components: {
    LoginForm,
  },
  data() {
    return {};
  },
  mounted() {
    document.title = "Connexion";
  },
  methods: {},
};
</script>