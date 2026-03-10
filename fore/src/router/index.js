import { createRouter, createWebHistory } from 'vue-router'

// 导入布局组件
import SidebarLayout from '../components/SidebarLayout.vue'

const routes = [
  {
    path: '/',
    component: SidebarLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/HomeView.vue')
      },
      {
        path: 'reviews',
        name: 'Reviews',
        component: () => import('../views/ReviewsView.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/MyProfileView.vue')
      },
      {
        path: 'search',
        name: 'Search',
        component: () => import('../views/SearchView.vue')
      },
      {
        path: 'category/:type',
        name: 'Category',
        component: () => import('../views/CategoryView.vue')
      },
      {
        path: 'favorites',
        name: 'Favorites',
        component: () => import('../views/MyProfileView.vue')
      },
      {
        path: 'movie/:id',
        name: 'MovieDetail',
        component: () => import('../views/MovieDetail.vue')
      },
      {
        path: 'movie-analysis',
        name: 'MovieAnalysis',
        component: () => import('../views/MovieAnalysisView.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue')
  },
   {
    path: '/verify-email',
    name: 'VerifyEmail',
    component: () => import('../views/VerifyEmailView.vue')
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  // 添加滚动行为配置，确保路由切换时页面滚动到顶部
  scrollBehavior() {
    // 总是滚动到顶部
    return { top: 0 }
  }
})

// 路由守卫
// router.beforeEach((to, from, next) => {
//   const requireAuthPaths = ['/movie-analysis', '/favorites', '/profile']
//   const isLogin = !!localStorage.getItem('accessToken') // 判断是否登录
//   if (requireAuthPaths.includes(to.path) && !isLogin) {
//     next('/login') // 未登录则跳转登录页
//   } else {
//     next()
//   }
// })

export default router
