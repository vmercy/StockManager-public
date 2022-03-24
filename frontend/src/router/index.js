import Vue from "vue";
import VueRouter from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import Category from "../views/Category.vue";
import Categories from "../views/Categories.vue";
import Components from "../views/Components.vue";
import Component from "../views/Component.vue";
import SearchResults from "../views/SearchResults.vue";
import Compartments from "../views/Compartments.vue";
import Compartment from "../views/Compartment.vue";
import ErrorAPI from "../views/ErrorAPI.vue";
import PageNotFound from "../views/PageNotFound.vue";

Vue.use(VueRouter);

const routes = [{
        path: "/",
        name: "Dashboard",
        component: Dashboard,
    },
    {
        path: "/login",
        name: "Login",
        component: Login,
    },
    {
        path: "/signup",
        name: "Signup",
        component: Signup,
    },
    {
        path: "/categories",
        name: "Categories",
        component: Categories,
    },
    {
        path: "/components",
        name: "Components",
        component: Components,
    },
    {
        path: "/component/:component_id",
        name: "Component",
        component: Component,
    },
    {
        path: "/components/search/",
        name: "Search",
        component: SearchResults,
    },
    {
        path: "/compartments",
        name: "Compartiments",
        component: Compartments,
    },
    {
        path: "/compartment/:compartment_id",
        name: "Compartiment",
        component: Compartment,
    },
    {
        path: "/category/:category_slug",
        name: "Category",
        component: Category,
    },
    {
        path: "*",
        name: "404",
        component: PageNotFound,
    },
    {
        path: "/",
        name: "ErrorAPI",
        component: ErrorAPI,
    },
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});


export default router;