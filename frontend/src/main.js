import Vue from 'vue'
import Vuetify from 'vuetify'
import { colors } from 'vuetify/lib';
Vue.use(Vuetify);
import App from './App.vue'
import router from './router'
import store from './store'
import VueCookies from 'vue-cookies';
import axios from 'axios';

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL

new Vue({
    vuetify: new Vuetify({

        theme: {
            themes: {
                light: {
                    primary: colors.green,
                    secondary: colors.lightGreen,
                    text: '#FFFFFF'
                }
            }
        },
        options: {
            customProperties: true
        }
    }),
    router,
    axios,
    store,
    render: h => h(App)
}).$mount('#app')

Vue.use(VueCookies)
Vue.$cookies.config('7d')