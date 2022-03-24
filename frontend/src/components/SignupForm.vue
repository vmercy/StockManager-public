<template>
  <v-container>
    <v-card>
      <v-card-title> Créer un compte </v-card-title>
      <v-card-subtitle>
        Creéz un compte pour accéder à toutes les fonctionnalités de
        StockManager
      </v-card-subtitle>
      <v-card-text>
        <v-row justify="center">
          <v-col cols="8">
            <v-form v-model="valid" ref="signupform">
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
              >
              </v-text-field>
              <v-text-field
                v-model="password_conf"
                :rules="rules.password_conf"
                :type="password_conf_hidden ? 'password' : 'text'"
                label="Confirmer le mot de passe"
                :append-icon="password_conf_hidden ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="
                  () => (password_conf_hidden = !password_conf_hidden)
                "
                @keyup.enter="submitSignupForm()"
              >
              </v-text-field>
              <vue-recaptcha
                loadRecaptchaScript
                language="fr"
                ref="recaptcha"
                size="invisible"
                :sitekey="getRecapPublic()"
                @verify="onCaptchaVerified"
                @expired="onCaptchaExpired"
              >
              <v-btn
                :disabled="!valid"
                color="primary"
                >Créer un compte</v-btn
              >
              </vue-recaptcha>
              
            </v-form>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-dialog v-model="signupError" width="500">
      <v-card>
        <v-card-title>Des erreurs ont été détectées</v-card-title>
        <v-card-text>
          Voici les erreurs à corriger :
          <v-list>
            <v-list-item-title v-if="errors.username"
              >Identifiant</v-list-item-title
            >
            <v-list-item v-for="error in errors.username" :key="error">{{
              error
            }}</v-list-item>
            <v-list-item-title v-if="errors.password"
              >Mot de passe</v-list-item-title
            >
            <v-list-item v-for="error in errors.password" :key="error">{{
              error
            }}</v-list-item>
            <v-list-item-title v-if="errors.password2"
              >Confirmation du mot de passe</v-list-item-title
            >
            <v-list-item v-for="error in errors.recaptcha" :key="error">{{
              error
            }}</v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="signupError = false">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="signupSuccess" width="500">
      <v-card>
        <v-card-title> Compté créé avec succès </v-card-title>
        <v-card-text>
          Votre compte a été créé avec succès avec l'identifiant suivant :
          <b>{{ username }}</b>. Vous pouvez désormais vous connecter à StockManager en
          utilisant le nom d'utilisateur et le mot de passe saisis.
        </v-card-text>
        <v-card-actions>
          <v-btn
            @click="
              signupSuccess = false;
              $router.push({ name: 'Login' });
            "
            >Me connecter</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script>
import axios from "axios";
import { VueRecaptcha } from 'vue-recaptcha';
const passwordRegex =
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
export default {
  name: "SignupForm",
  components: {
      'vue-recaptcha': VueRecaptcha
    },
  data() {
    return {
      username: "",
      password: "",
      password_conf: "",
      errors: [],
      rules: {
        username: [(v) => !!v || "Le nom d'utilisateur est requis"],
        password: [
          (v) => !!v || "Le mot de passe est requis",
          (v) =>
            this.checkPasswordRegex(v) ||
            "Le mot de passe doit contenir au moins 8 caractères dont une lettre minuscule, une lettre majuscule, un chiffre et un caractère spécial.",
        ],
        password_conf: [
          (v) => !!v || "La confirmation du mot de passe est requise",
          (v) =>
            this.password == this.password_conf ||
            "Les mots de passe doivent être identiques",
        ],
      },
      valid: false,
      signupError: false,
      reCaptchaOK: false,
      reCaptchaToken: "",
      signupSuccess: false,
      password_hidden: true,
      password_conf_hidden: true,
    };
  },
  mounted() {
    document.title = "Créer un compte";
  },
  methods: {
    getRecapPublic() {
      return process.env.VUE_APP_RECAPTCHA_PUBLIC;
    },
    onCaptchaVerified(recaptchaToken) {
      this.reCaptchaOK = true;
      this.reCaptchaToken = recaptchaToken;
      this.$refs.recaptcha.reset();
      this.submitSignupForm()
    },
    onCaptchaExpired() {
      this.reCaptchaOK = false;
    },
    checkPasswordRegex(password) {
      return Boolean(password.match(passwordRegex));
    },
    /**
     * Submits the signup form and show error messages if necessary
     */
    async submitSignupForm() {
      if (this.valid) {
        let signupFormData = {
          username: this.username,
          password: this.password,
          password2: this.password_conf,
          recaptcha: this.reCaptchaToken
        };
        await axios
          .post("/api/v1/register", signupFormData)
          .then((response) => {
            this.$refs.signupform.reset();
            this.signupSuccess = true;
            this.username = response.data.username;
          })
          .catch((error) => {
            switch (error.response.status) {
              case 400:
                this.errors = error.response.data;
                this.signupError = true;
                break;
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
