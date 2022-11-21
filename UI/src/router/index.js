import VueRouter from 'vue-router';
import Login from '@/views/Login'
import Navigation from '@/views/Navigation'
import {useAuthStore} from '@/stores/auth'


const routes = [
    {
        path: '/login', component: Login, name: 'Login', meta: {onlyWhenLoggedOut: true},
    },
    {
        component: Navigation,
        meta: {requiresAuth: true},
        path: '/',
        children: [
            {
                path: '/',
                name: 'Production',
                meta: {requiresAuth: true},
                component: () => import(/* webpackChunkName: "production" */ '@/views/Production/Production'),
            },
            {
                path: '/workflow',
                name: 'Workflow',
                meta: {requiresAuth: true},
                component: () => import(/* webpackChunkName: "workflow" */ '@/views/Workflow/Workflow'),
            },

            {
                path: '/my-devices',
                name: 'MyDevices',
                meta: {requiresAuth: true},
                component: () => import(/* webpackChunkName: "my-devices" */ '@/views/MyDevices/MyDevices'),
            },
            {
                path: '/my-devices/:id',
                name: 'MyDevicesDetail',
                meta: {requiresAuth: true}, props: true,
                component: () => import(/* webpackChunkName: "my-devices" */ '@/views/MyDevices/DeviceDetail'),
            },
            {
                path: '/consume',
                name: 'Consume',
                meta: {requiresAuth: true},
                component: () => import(/* webpackChunkName: "my-devices" */ '@/views/Consume/Consume'),
            },
            {
                path: '/webview/:ip',
                name: 'WebView',
                meta: {requiresAuth: true},
                component: () => import(/* webpackChunkName: "web-view" */ '@/views/WebView'),
            },
            {
                path: '/device_details/:id',
                name: 'DeviceDetails',
                meta: {requiresAuth: true},
                component: () => import(/* webpackChunkName: "device-details" */ '@/views/DeviceDetails/DeviceDetails'),
            },
        ]
    },
    {path: '*', redirect: '/'},
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

router.beforeEach((to, from, next) => {
        const auth = useAuthStore()

        if (auth.isLoggedIn) {
            if (to.path === '/login') {
                router.push('/');
            } else {
                next();
            }
        } else {
            if (to.path === '/' || (to.path).startsWith('/main')) {
                router.push('/login');
            } else {
                next();
            }
        }
    }
)
export default router;
