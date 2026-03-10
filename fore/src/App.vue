<template>
  <div id="app">
    <!-- 顶部导航栏区域：固定在页面顶部，包含登录/注册入口 -->
    <header class="app-header">
      <!-- 导航栏右侧容器：用于包裹登录注册按钮或个人中心 -->
      <div class="header-right">
        <!-- 根据登录状态显示不同按钮 -->
        <template v-if="isLoggedIn">
          <!-- 已登录：显示个人中心按钮 -->
          <el-dropdown @command="handleCommand" class="user-dropdown">
            <span class="header-button user-button">
              <el-icon><User /></el-icon>
              {{ username }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                  <el-dropdown-item command="favorites">我的收藏</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <!-- 未登录：显示登录和注册按钮 -->
          <router-link to="/login" class="header-button">登录</router-link>
          <router-link to="/register" class="header-button">注册</router-link>
        </template>
      </div>
    </header>
    
    <!-- 主要内容显示区域：路由视图出口，所有路由对应的组件都会在这里渲染 -->
    <router-view />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 导出Vue根组件，作为整个应用的入口组件
export default {
  name: 'App', // 组件名称，用于调试和组件递归引用
  components: {
    User,
    ArrowDown
  },
  setup() {
    const router = useRouter()
    const isLoggedIn = ref(false) // 响应式数据：标记用户是否登录
    const username = ref('用户') // 响应式数据：存储用户名
    
    // 处理下拉菜单命令
    const handleCommand = (command) => {
      switch (command) {
        case 'profile':
          router.push('/profile')
          break
        case 'favorites':
          router.push('/favorites')
          break
        case 'logout':
          isLoggedIn.value = false
          // 清除本地存储的登录状态
          localStorage.removeItem('isLoggedIn')
          localStorage.removeItem('username')
          localStorage.removeItem('rememberMe')
          ElMessage.success('已退出登录')
          router.push('/')
          break
      }
    }
    
    // 检查登录状态的函数
    const checkLoginStatus = () => {
      const savedLoginStatus = localStorage.getItem('isLoggedIn')
      const savedUsername = localStorage.getItem('username')
      
      if (savedLoginStatus === 'true' && savedUsername) {
        isLoggedIn.value = true
        username.value = savedUsername
      } else {
        isLoggedIn.value = false
        username.value = '用户'
      }
    }
    
    // 组件挂载时检查登录状态
    onMounted(() => {
      // 初始检查登录状态
      checkLoginStatus()
      
      // 监听storage变化，当其他标签页修改localStorage时也能更新状态
      const handleStorageChange = (e) => {
        if (e.key === 'isLoggedIn' || e.key === 'username') {
          checkLoginStatus()
        }
      }
      
      // 添加storage事件监听
      window.addEventListener('storage', handleStorageChange)
      
      // 监听自定义登录状态变化事件
      const handleLoginStatusChange = (e) => {
        isLoggedIn.value = e.detail.isLoggedIn
        username.value = e.detail.username
      }
      window.addEventListener('loginStatusChanged', handleLoginStatusChange)
      
      // 在组件卸载时移除事件监听
      return () => {
        window.removeEventListener('storage', handleStorageChange)
        window.removeEventListener('loginStatusChanged', handleLoginStatusChange)
      }
    })
    
    return {
      isLoggedIn,
      username,
      handleCommand
    }
  }
}
</script>

<style>
/* 全局样式重置：清除所有元素的默认内外边距，统一盒模型为border-box */
/* box-sizing: border-box：元素的padding和border不会增加其总宽度/高度，布局更可控 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 全局body样式：设置默认字体、页面背景色和文本颜色 */
body {
  /* 跨平台兼容字体栈：优先使用系统默认无衬线字体，确保在不同设备上显示一致 */
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  font-size: 20px; /* 增大全局字体大小 */
  background-color: #0f172a; /* 深色背景色，现代UI风格 */
  color: #e2e8f0; /* 更亮的文本颜色，增强可读性 */
  line-height: 1.6; /* 增加行高，提高文本可读性 */
  letter-spacing: 0.5px; /* 增加字间距，使文本更加清晰 */
}

/* 根组件容器样式：设置最小高度为视口高度，确保内容不足时也占满屏幕 */
#app {
  min-height: 100vh; /* 100vh = 视口高度，保证页面至少占满屏幕 */
  position: relative; /* 为绝对定位的子元素（如固定导航栏）提供定位上下文 */
  padding: 15px; /* 添加内边距，减少空白区域 */
  box-sizing: border-box; /* 确保内边距不会增加总宽度 */
}

/* 顶部导航栏样式 */
.app-header {
  position: fixed; /* 固定定位：导航栏始终停留在页面顶部，不随滚动移动 */
  border-radius: 16px; /* 圆角：8px，柔和不尖锐 */
  top: 0; /* 距离页面顶部0px */
  right: 0; /* 距离页面右侧0px */
  z-index: 1000; /* 层级优先级：确保导航栏在其他元素之上，不被遮挡 */
  padding: 15px 25px; /* 减小内边距，使按钮更紧凑 */
  background: rgba(15, 23, 42, 0.9); /* 添加半透明背景，增强视觉层次 */
  backdrop-filter: blur(10px); /* 添加毛玻璃效果，增强视觉层次 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 添加阴影，增强立体感 */
}

/* 导航栏右侧按钮容器：使用flex布局排列按钮 */
.header-right {
  display: flex; /* 弹性布局：让子元素（登录/注册按钮）横向排列 */
  gap: 15px; /* 子元素之间的间距：15px */
}

/* 登录/注册按钮样式：渐变背景、毛玻璃效果、hover动画 */
.header-button {
  background: linear-gradient(135deg, #090725, #2b0b8c); /* 紫色系渐变背景，现代感强 */
  color: white; /* 文本白色，与背景形成对比 */
  padding: 12px 24px; /* 增加内边距，使按钮更大更易点击 */
  border-radius: 8px; /* 圆角：8px，柔和不尖锐 */
  text-decoration: none; /* 移除a标签默认下划线 */
  font-weight: 600; /* 增加字体粗细，使按钮更醒目 */
  font-size: 18px; /* 增加按钮字体大小 */
  transition: all 0.3s ease; /* 所有属性过渡：0.3秒，动画平滑 */
  backdrop-filter: blur(10px); /* 毛玻璃效果：模糊背景10px，增强层次感 */
  border: 1px solid rgba(255, 255, 255, 0.2); /* 增加边框透明度，使边框更明显 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影，增强立体感 */
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

/* 用户下拉菜单样式 */
.user-dropdown {
  cursor: pointer;
}

.user-button {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 按钮hover状态：鼠标悬浮时的样式变化 */
.header-button:hover {
  background: linear-gradient(135deg, #0f0488, #320e6b); /* 渐变背景加深，反馈明显 */
  transform: translateY(-2px); /* 向上偏移2px，模拟"浮起"效果 */
  box-shadow: 0 5px 15px rgba(79, 70, 229, 0.3); /* 紫色阴影：增强立体感和点击欲望 */
}

/* 页面切换动画样式：基于Vue过渡系统的类名规则 */
/* fade-enter-active：进入动画执行期间的样式 */
/* fade-leave-active：离开动画执行期间的样式 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease; /* 过渡属性：透明度，0.3秒，缓动效果 */
}

/* fade-enter-from：进入动画开始时的初始样式 */
/* fade-leave-to：离开动画结束时的最终样式 */
.fade-enter-from,
.fade-leave-to {
  opacity: 0; /* 透明度为0，即完全透明 */
}
</style>