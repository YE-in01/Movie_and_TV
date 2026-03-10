<template>
  <!-- 整体布局容器：弹性布局，包裹侧边栏和主内容区 -->
  <div class="sidebar-layout">
    <!-- 左侧导航栏：固定定位，占满屏幕高度 -->
    <aside class="sidebar sci-fi-sidebar">
      <!-- Logo 区域：包含网站名称和动画效果 -->
      <div class="logo-container">
        <!-- 路由链接：跳转到首页，无刷新导航 -->
        <router-link to="/" class="logo">
          <span class="logo-text">影视天地</span>
          <div class="logo-glow"></div> <!-- Logo 扫描发光效果 -->
        </router-link>
      </div>

      <!-- 导航菜单主体：按功能分组 -->
      <nav class="nav-menu">
        <!-- 导航分组1：核心功能导航 -->
        <div class="nav-section">
          <h3 class="nav-section-title">导航</h3>
          <!-- 首页导航项：结合 Element Plus 图标，使用exact-active-class确保精确匹配时的样式 -->
          <router-link 
            to="/" 
            class="nav-item" 
            exact 
            active-class="nav-item-active"
            exact-active-class="nav-item-active"
          >
            <el-icon><House /></el-icon><!-- 首页图标,使用 Element Plus 的图标组件 <el-icon> 来包裹并渲染一个 “房子” 图标 <House>。 -->
            <span>首页</span>
          </router-link>
          <!-- 电影分类导航项 -->
          <router-link 
            to="/category/movie" 
            class="nav-item"
            active-class="nav-item-active"
            exact-active-class="nav-item-active"
          >
            <el-icon><VideoPlay /></el-icon>
            <span>电影</span>
          </router-link>
          <!-- 电视剧分类导航项 -->
          <router-link 
            to="/category/tv" 
            class="nav-item"
            active-class="nav-item-active"
            exact-active-class="nav-item-active"
          >
            <el-icon><Monitor /></el-icon>
            <span>电视剧</span>
          </router-link>
          <!-- 综艺分类导航项 -->
          <router-link 
            to="/category/variety" 
            class="nav-item"
            active-class="nav-item-active"
            exact-active-class="nav-item-active"
          >
            <el-icon><Microphone /></el-icon>
            <span>综艺</span>
          </router-link>
        </div>

        <!-- 导航分组2：数据分析相关 -->
        <div class="nav-section">
          <h3 class="nav-section-title">数据分析</h3>
          <!-- 电影数据分析页面 -->
          <router-link 
            to="/movie-analysis" 
            class="nav-item"
            active-class="nav-item-active"
            exact-active-class="nav-item-active"
          >
            <el-icon><DataAnalysis /></el-icon>
            <span>个人电影数据分析</span>
          </router-link>
        </div>

        <!-- 导航分组3：影评功能 -->
        <div class="nav-section">
          <h3 class="nav-section-title">影评</h3>
          <router-link 
            to="/reviews" 
            class="nav-item"
            active-class="nav-item-active"
            exact-active-class="nav-item-active"
          >
            <el-icon><ChatDotRound /></el-icon>
            <span>影评中心</span>
          </router-link>
        </div>


      </nav>
    </aside>

    <!-- 主内容区域：自适应剩余宽度，包含路由视图 -->
    <main class="main-content">
      <div class="content-area">
        <!-- 路由视图出口：渲染当前匹配的路由组件 -->
        <!-- Vue 3 正确的路由视图过渡动画实现 -->
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script>
// 导入 Vue3 核心 API：ref（响应式数据）、onMounted（生命周期钩子）
import { ref, onMounted } from 'vue'
// 导入 Vue Router 组合式 API：用于编程式导航
import { useRouter } from 'vue-router'
// 导入 Element Plus 图标组件（侧边栏导航图标）
import { House, VideoPlay, Monitor, Microphone, ChatDotRound, DataAnalysis } from '@element-plus/icons-vue'
import { userApi } from '@/api/api'

export default {
  name: 'SidebarLayout', // 组件名称（用于调试和组件注册）
  components: {
    // 注册导入的图标组件，供模板使用
    House,
    VideoPlay,
    Monitor,
    Microphone,
    ChatDotRound,
    DataAnalysis
  },
  // Vue3 组合式 API 入口：组织组件逻辑
  setup() {
    const router = useRouter() // 获取路由实例（用于编程式导航）
    const searchKeyword = ref('') // 响应式数据：存储搜索关键词
    const isLoggedIn = ref(false) // 响应式数据：标记用户是否登录
    const username = ref('用户') // 响应式数据：存储用户名
    
    // 获取用户信息
    const fetchUserInfo = async () => {
      try {
        const response = await userApi.getUserInfo()
        isLoggedIn.value = true
        username.value = response.data.username || '用户'
      } catch (error) {
        // 用户未登录或获取失败
        isLoggedIn.value = false
        username.value = '用户'
      }
    }
    
    // 退出登录
    const handleLogout = async () => {
      try {
        await userApi.logout()
        isLoggedIn.value = false
        username.value = '用户'
        router.push('/')
      } catch (error) {
        console.error('退出登录失败:', error)
      }
    }

    /**
     * 搜索处理函数
     * 功能：关键词非空时，跳转到搜索结果页并携带查询参数
     */
    const handleSearch = () => {
      if (searchKeyword.value.trim()) {
        router.push({
          name: 'Search', // 路由名称（需在路由配置中定义）
          query: { keyword: searchKeyword.value } // URL 查询参数：?keyword=xxx
        })
      }
    }

    /**
     * 用户下拉菜单命令处理函数
     * 功能：根据菜单选择执行对应操作（路由跳转/登出）
     * @param {string} command - 菜单命令标识
     */
    const handleCommand = async (command) => {
      switch (command) {
        case 'profile':
          await router.push('/profile') // 跳转到个人中心
          break
        case 'favorites':
          await router.push('/favorites') // 跳转到收藏页面
          break
        case 'logout':
          await handleLogout() // 调用后端API执行登出
          break
      }
    }

    /**
     * 生命周期钩子：组件挂载完成后执行
     * 功能：初始化操作，从后端API获取用户登录状态和信息
     */
    onMounted(() => {
      fetchUserInfo()
    })

    // 暴露响应式数据和方法到模板
    return {
      searchKeyword,
      isLoggedIn,
      username,
      handleSearch,
      handleCommand,
      handleLogout
    }
  }
}
</script>

<style scoped>
/* 整体布局：弹性布局，背景渐变，占满屏幕高度 */
.sidebar-layout {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f172a 100%);
  color: #ffffff;
}

/* 左侧导航栏：固定定位，宽度260px，科幻风格背景 */
.sidebar {
  width: 260px;
  background-color: rgba(10, 14, 39, 0.9);
  /* 简化毛玻璃效果，增加兼容性 */
  background-color: #0a0e27; /* 回退背景色 */
  background-image: linear-gradient(rgba(10, 14, 39, 0.9), rgba(10, 14, 39, 0.9));
  
  /* 优化阴影效果，增加兼容性 */
  box-shadow: 2px 0 10px rgba(0, 153, 255, 0.15); /* 降低透明度增加兼容性 */
  
  /* 优化边框效果 */
  border-right: 1px solid rgba(100, 200, 255, 0.3); /* 增加不透明度使边框更清晰 */
  
  display: flex;
  flex-direction: column;
  position: fixed; /* 固定在左侧*/
  height: 100vh; /* 占满屏幕高度*/
  overflow-y: auto; /* 内容溢出时可滚动*/
  z-index: 100; /* 保证在最上层，不被遮挡*/
  
  /* 增加硬件加速 */
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
}

/* Logo 容器：底部边框分隔，内边距 */
.logo-container {
  padding: 20px;
  border-bottom: 1px solid rgba(100, 200, 255, 0.1);
}

/* Logo 链接：块级元素，移除下划线 */
.logo {
  display: block;
  text-decoration: none;
  position: relative;
}

/* Logo 文字：居中，发光文字效果 */
.logo-text {
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
  text-shadow: 0 0 10px rgba(100, 200, 255, 0.8); /* 文字发光*/
  display: block;
  text-align: center;
}

/* Logo 扫描发光效果：绝对定位，渐变背景，动画 */
.logo-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(100, 200, 255, 0.3), transparent);
  animation: scan 3s infinite; /* 扫描动画,3秒循环*/
  border-radius: 4px;
}

/* 扫描动画关键帧：从左到右平移 */
@keyframes scan {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* 导航菜单：弹性占满剩余空间，内边距 */
.nav-menu {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

/* 导航分组：底部间距 */
.nav-section {
  margin-bottom: 30px;
}

/* 导航分组标题：大写字母，浅色，内边距 */
.nav-section-title {
  padding: 0 20px 10px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase; /* 文字大写*/
  letter-spacing: 1px; /* 字间距 */
}

/* 导航项：弹性布局，对齐图标和文字，内边距 */
.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s; /* 过渡动画*/
  position: relative;
}

/* 导航项 hover 效果：背景变色，文字变亮 */
.nav-item:hover {
  background-color: rgba(100, 200, 255, 0.1);
  color: #00ccff;
}

/* 导航项激活态（当前路由完全匹配）：特殊背景和文字颜色 */
.nav-item.router-link-exact-active,
.nav-item.router-link-active,
.nav-item.nav-item-active {
  background-color: rgba(0, 153, 255, 0.3);
  color: #ffffff !important;
  text-shadow: 0 0 10px rgba(0, 204, 255, 0.8);
}

/* 激活态左侧竖线：渐变颜色，绝对定位 */
.nav-item.router-link-exact-active::before,
.nav-item.router-link-active::before,
.nav-item.nav-item-active::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(to bottom, #00ccff, #0099ff);
  box-shadow: 0 0 10px rgba(0, 204, 255, 0.8);
}



/* 导航项图标：右边距，字体大小 */
.nav-item .el-icon {
  margin-right: 12px;
  font-size: 18px;
}

/* 主内容区域：自适应剩余宽度，左边距等于侧边栏宽度 */
.main-content {
  flex: 1;
  margin-left: 260px; /* 避开左侧固定侧边栏*/
  display: flex;
  flex-direction: column;
}

/* 内容区域：内边距，相对定位 */
.content-area {
  flex: 1;
  padding: 30px;
  position: relative;
  z-index: 1;
}

/* 响应式调整：屏幕宽度 ≤768px 时（移动端） */
@media (max-width: 768px) {
  .sidebar {
    width: 70px; /* 侧边栏缩窄*/
  }

  .logo-text {
    display: none; /* 隐藏 Logo 文字*/
  }

  .nav-section-title {
    display: none; /* 隐藏分组标题*/
  }

  .nav-item span {
    display: none; /* 隐藏导航文字*/
  }

  .nav-item {
    justify-content: center; /* 图标居中*/
    padding: 15px;
  }

  .nav-item .el-icon {
    margin-right: 0; /* 移除图标右边距*/
    font-size: 20px; /* 图标放大*/
  }

  .main-content {
    margin-left: 70px; /* 主内容区左边距同步缩窄*/
  }
}

/* 过渡动画样式：淡入淡出 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease; /* 透明度过渡，0.3秒*/
}

/* 进入开始状态 + 离开结束状态：透明度0 */
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>