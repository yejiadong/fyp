import { createRouter, createWebHashHistory } from 'vue-router'
import AdminDashboard from "../views/AdminDashboard.vue";
import Annotate from "../views/Annotate.vue";
import Unauthorised from "../views/UnauthorisedAccess.vue";
import Home from "../views/Home.vue";
import { useUserStore } from "../stores/user";

const routes = [
  { path: '/', name: 'homepage', component: Home },
  { path: '/dashboard', name: 'dashboard', component: AdminDashboard,
    meta: {
      requiresAuth: true
    }
  },
  { path: '/annotate', name: 'annotate', component: Annotate },
  { path: '/unauthorised', name: 'unauthorised', component: Unauthorised },
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    const store = useUserStore()
    await store;
    if (!store.isAuthenticated) {
      next({ name: 'homepage' })
    } else {
      next() // go to wherever I'm going
    }
  } else {
    next() // does not require auth, make sure to always call next()!
  }
})

export default router
