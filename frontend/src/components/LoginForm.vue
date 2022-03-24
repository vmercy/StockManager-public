<template>
  <v-container>
    <v-card>
      <v-card-title> Connexion </v-card-title>
      <v-card-subtitle>
        Connectez-vous pour accéder à toutes les fonctionnalités de StockManager
      </v-card-subtitle>
      <v-card-text>
        <v-row justify="center">
          <v-col cols="8">
            <v-form v-model="valid" ref="loginform">
              <v-text-field
                v-model="username"
                :rules="rules.username"
                label="Nom d'utilisateur"
              ></v-text-field>
              <v-text-field
                v-model="password"
                :rules="rules.password"
                :type="password_hidden ? 'password' : 'text'"
                label="Mot de passe"
                :append-icon="password_hidden ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="() => (password_hidden = !password_hidden)"
                @keyup.enter="submitLoginForm()"
              >
              </v-text-field>
              <v-btn
                :disabled="!valid"
                @click="submitLoginForm()"
                color="primary"
                >Connexion</v-btn
              >
            </v-form>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-dialog v-model="wrongId" width="500">
      <v-card>
        <v-card-title> Identifiants erronés </v-card-title>
        <v-card-text>
          Désolé, les identifiants saisis n'ont pas permis de vous connecter.
          Veuillez réessayer.
        </v-card-text>
        <v-card-actions>
          <v-btn @click="wrongId = false">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script>
import axios from "axios";
export default {
  name: "LoginForm",
  data() {
    return {
      username: "",
      password: "",
      errors: [],
      rules: {
        username: [(v) => !!v || "Le nom d'utilisateur est requis"],
        password: [(v) => !!v || "Le mot de passe est requis"],
      },
      valid: false,
      wrongId: false,
      password_hidden: true,
    };
  },
  mounted() {
    document.title = "Connexion";
  },
  methods: {
    /**
     * Submits the login form and connects the user if credentiels are recognized
     */
    async submitLoginForm() {
      if (this.valid) {
        axios.defaults.headers.common["Authorization"] = "";
        localStorage.removeItem("token");
        const loginFormData = {
          username: this.username,
          password: this.password,
        };
        await axios
          .post("/api/v1/token/login/", loginFormData)
          .then((response) => {
            const token = response.data.auth_token;
            this.$store.commit("setToken", token);

            axios.defaults.headers.common["Authorization"] = "Token " + token;
            localStorage.setItem("token", token);
            localStorage.setItem("username", this.username);
            this.$store.state.username = this.username;
            this.$refs.loginform.reset();
            this.$router.push({ name: "Dashboard" });
            //window.location.reload();
          })
          .catch((error) => {
            switch (error.response.status) {
              case 400:
                this.wrongId = true;
              case 401:
                this.$router.push({ name: "Login" });
                break;
              default:
                this.$router.push({ name: "ErrorAPI" });
                break;
            }
          });
      }
    },
  },
};
</script>