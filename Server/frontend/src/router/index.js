import Vue from 'vue'
import VueRouter from 'vue-router'
import RouterComponent from "@/components/RouterComponent";
import {dispatchCheckLoggedIn} from "@/store/main/actions";
import {store} from "@/store";
import {readIsLoggedIn} from "@/store/main/getters";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: () => import(/* webpackChunkName: "start" */ '@/App.vue'),
        children: [
            {
                path: 'products',
                name: 'Products',
                component: () => import(/* webpackChunkName: "products" */ '@/views/landingPage/Products'),
            },
            {
                path: 'nav',
                component: () => import(/* webpackChunkName: "nav" */ '@/layouts/NavigationLayout'),
            },
            {
                path: 'reset-password',
                name: 'ResetPassword',
                component: () => import(/* webpackChunkName: "reset-password" */ '@/views/ResetPassword.vue'),
            },
            {
                path: 'main',
                component: () => import(/* webpackChunkName: "main" */ '@/views/main/Main.vue'),
                children: [
                    {
                        path: 'dashboard',
                        name: 'Dashboard',
                        component: () => import(/* webpackChunkName: "main-dashboard" */ '@/views/main/Dashboard.vue'),
                    },
                    {
                        path: 'profile',
                        component: RouterComponent,
                        redirect: 'profile/view',
                        children: [
                            {
                                path: 'view',
                                name: 'UserProfile',
                                component: () => import(
                                    /* webpackChunkName: "main-profile" */ '@/views/main/profile/UserProfile.vue'),
                            },
                        ],
                    },
                    {
                        path: 'admin',
                        component: () => import(/* webpackChunkName: "main-admin" */ '@/views/main/admin/Admin.vue'),
                        redirect: 'admin/users/all',
                        children: [
                            {
                                path: 'users',
                                redirect: 'users/all',
                            },
                            {
                                path: 'customer/:id/users',
                                name: 'AdminCustomerUsers',
                                component: () => import(
                                    /* webpackChunkName: "main-admin-users" */ '@/views/main/admin/Customer/AdminCustomerUsers.vue'),
                            },
                            {
                                path: 'customer/:id/devices',
                                name: 'AdminCustomerDevices',
                                component: () => import(
                                    /* webpackChunkName: "main-admin-users" */ '@/views/main/admin/Customer/AdminCustomerDevices.vue'),
                            },
                            {
                                path: 'customers/all',
                                name: 'AdminCustomer',
                                component: () => import(
                                    /* webpackChunkName: "main-admin-users" */ '@/views/main/admin/Customer/AdminCustomers.vue'),
                            },
                            {
                                path: 'devices/all',
                                name: 'AdminDevices',
                                component: () => import(
                                    /* webpackChunkName: "main-admin-users" */ '@/views/main/admin/Devices/AdminDevices.vue'),
                            },
                            {
                                path: 'users/edit/:id',
                                name: 'main-admin-users-edit',
                                component: () => import(
                                    /* webpackChunkName: "main-admin-users-edit" */ '@/views/main/admin/Customer/EditUser.vue'),
                            },
                            {
                                path: 'users/create',
                                name: 'main-admin-users-create',
                                component: () => import(
                                    /* webpackChunkName: "main-admin-users-create" */ '@/views/main/admin/Customer/CreateUser.vue'),
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        path: '/*', redirect: '/',
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: routes
})


router.beforeEach((to, from, next) => {
        store.dispatch('actionCheckLoggedIn').then((response) => {
            if (store.getters.isLoggedIn) {
                if (to.path === '/login' || to.path === '/') {
                    next('/main/dashboard');
                } else {
                    next();
                }
            } else if (store.getters.isLoggedIn === false) {
                if (to.path === '/' || (to.path).startsWith('/main')) {
                    next('/products');
                } else {
                    next();
                }
            }
        })
    }
)

export default router
