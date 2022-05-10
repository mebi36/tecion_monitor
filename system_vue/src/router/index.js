import { createWebHistory, createRouter } from "vue-router";

import Home from "@/views/Home.vue";
import About from "@/views/About.vue";
import LogIn from "@/views/LogIn.vue";
import PageNotFound from "@/views/PageNotFound.vue";
import Profile from "@/views/Profile.vue";
import MonitoredItems from "@/views/MonitoredItems.vue";
import Dashboard from "@/views/Dashboard.vue";

import store from "../store";


const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: "/profile",
        name: "Profile",
        component: Profile,

        meta: {
            requireLogin: true
        }
    },
    {
        path: "/log-in",
        name: "LogIn",
        component: LogIn,

        meta: {
            disableIfLoggedIn: true
        }
    },
    {
        path: "/about",
        name: "About",
        component: About,
    },
    {
        path: "/monitored-items",
        name: "MonitoredItems",
        component: MonitoredItems,

        meta: {
            requireLogin: true
        }  
    },
    {
        path: "/dashboard/:item_id",
        name: "Dashboard",
        component: Dashboard,

        meta: {
            requireLogin: true
        }
    },
    {
        path: "/:catchAll(.*)",
        name: "PageNotFound",
        component: PageNotFound,
        meta: {
            requiresAuth: false
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from , next) => {
    if(to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated){
        next({ name: 'LogIn', query: { to: to.path} });
    } else {
        next()
    }
})
export default router;
