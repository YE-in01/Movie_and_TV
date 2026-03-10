<template>
  <div class="home">
    <!-- 科幻背景粒子效果 -->
    <div class="particles-container">
      <div class="particle" v-for="i in 100" :key="i" :style="{
        width: Math.random() * 4 + 'px',
        height: Math.random() * 4 + 'px',
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 20 + 's',
        animationDuration: Math.random() * 20 + 20 + 's'
      }"></div>
    </div>
    
    <!-- 顶部搜索栏 -->
    <header class="top-header">
      <div class="search-container">
        <el-input
          v-model="searchKeyword"
          placeholder="请输入关键词搜索"
          class="search-input"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon class="el-icon--left">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="18" height="18">
                <path fill="currentColor" d="M909.6 854.5L649.9 594.8C690.2 542.7 712 479 712 412c0-80.2-31.3-155.4-87.9-212.1-56.6-56.7-132-87.9-212.1-87.9s-155.5 31.3-212.1 87.9C143.2 256.5 112 331.8 112 412c0 80.1 31.3 155.5 87.9 212.1C256.5 680.8 331.8 712 412 712c67 0 130.6-21.8 182.7-62l259.7 259.6a8.2 8.2 0 0 0 11.6 0l43.6-43.5a8.2 8.2 0 0 0 0-11.6zM570.4 570.4C528 612.7 471.8 636 412 636s-116-23.3-158.4-65.6C211.3 528 188 471.8 188 412s23.3-116 65.6-158.4C296 211.3 352.2 188 412 188s116 23.3 158.4 65.6C612.7 296 636 352.2 636 412s-23.3 116-65.6 158.4z"></path>
              </svg>
            </el-icon>
          </template>

        </el-input>
      </div>
    </header>

    <!-- 轮播图 -->
    <div class="banner sci-fi-banner">
      <el-carousel :interval="4000" type="card" height="400px" class="sci-fi-carousel" indicator-position="bottom" arrow="hover" :loop="true" card-width="200px" card-margin="20px">
        <el-carousel-item v-for="item in bannerMovies" :key="item.id">
          <router-link :to="'/movie/' + item.id" class="banner-card">
            <div class="banner-card-poster">
              <img :src="item.poster" :alt="item.title" class="banner-img">
            </div>
            <div class="banner-card-info">
              <h3 class="banner-card-title">{{ item.title }}</h3>
              <p class="banner-card-desc">{{ item.review || item.description || '暂无简介' }}</p>
            </div>
          </router-link>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 内容区域 -->
    <main class="main-content sci-fi-main-content">
      <div class="container">
        <!-- 热门电影 -->
        <section class="movie-section sci-fi-section">
          <div class="section-header sci-fi-section-header">
            <h2 class="sci-fi-section-title">热门电影</h2>
            <router-link to="/category/movie" class="more-link sci-fi-more-link">更多 ></router-link>
          </div>
          <div class="movie-list sci-fi-movie-grid">
            <div class="movie-item sci-fi-movie-card" v-for="movie in hotMovies" :key="movie.id">
              <router-link :to="'/movie/' + movie.id" class="sci-fi-movie-link">
                <div class="movie-poster sci-fi-poster">
                  <img :src="movie.poster" :alt="movie.title" class="sci-fi-poster-img">
                  <div class="movie-rating sci-fi-rating">
                    <el-rate :model-value="movie.rating / 2" disabled text-color="#ff9900" :max="5" :precision="0.5"></el-rate>
                  </div>
                  <div class="poster-overlay"></div>
                  <div class="poster-glow"></div>
                </div>
                <h3 class="movie-title sci-fi-movie-title">{{ movie.title }}</h3>
                <p class="movie-info sci-fi-movie-info">{{ movie.year }} · {{ formatGenre(movie.genre) }}</p>
              </router-link>
            </div>
          </div>
        </section>

        <!-- 热门电视剧 -->
        <section class="movie-section sci-fi-section">
          <div class="section-header sci-fi-section-header">
            <h2 class="sci-fi-section-title">热门电视剧</h2>
            <router-link to="/category/tv" class="more-link sci-fi-more-link">更多 ></router-link>
          </div>
          <div class="movie-list sci-fi-movie-grid">
            <div class="movie-item sci-fi-movie-card" v-for="tv in hotTVShows" :key="tv.id">
              <router-link :to="'/movie/' + tv.id" class="sci-fi-movie-link">
                <div class="movie-poster sci-fi-poster">
                  <img :src="tv.poster" :alt="tv.title" class="sci-fi-poster-img">
                  <div class="movie-rating sci-fi-rating">
                    <el-rate :model-value="tv.rating / 2" disabled text-color="#ff9900" :max="5" :precision="0.5"></el-rate>
                  </div>
                  <div class="poster-overlay"></div>
                  <div class="poster-glow"></div>
                </div>
                <h3 class="movie-title sci-fi-movie-title">{{ tv.title }}</h3>
                <p class="movie-info sci-fi-movie-info">{{ tv.year }} · {{ formatGenre(tv.genre) }}</p>
              </router-link>
            </div>
          </div>
        </section>

        <!-- 热门综艺 -->
        <section class="movie-section sci-fi-section">
          <div class="section-header sci-fi-section-header">
            <h2 class="sci-fi-section-title">热门综艺</h2>
            <router-link to="/category/variety" class="more-link sci-fi-more-link">更多 ></router-link>
          </div>
          <div class="movie-list sci-fi-movie-grid">
            <div class="movie-item sci-fi-movie-card" v-for="variety in hotVarietyShows" :key="variety.id">
              <router-link :to="'/movie/' + variety.id" class="sci-fi-movie-link">
                <div class="movie-poster sci-fi-poster">
                  <img :src="variety.poster" :alt="variety.title" class="sci-fi-poster-img">
                  <div class="movie-rating sci-fi-rating">
                    <el-rate :model-value="variety.rating / 2" disabled text-color="#ff9900" :max="5" :precision="0.5"></el-rate>
                  </div>
                  <div class="poster-overlay"></div>
                  <div class="poster-glow"></div>
                </div>
                <h3 class="movie-title sci-fi-movie-title">{{ variety.title }}</h3>
                <p class="movie-info sci-fi-movie-info">{{ variety.year }} · {{ formatGenre(variety.genre) }}</p>
              </router-link>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer sci-fi-footer">
      <div class="container">
        <div class="footer-content sci-fi-footer-content">
          <div class="footer-section sci-fi-footer-section">
            <h3 class="sci-fi-footer-title">关于我们</h3>
            <p class="sci-fi-footer-text">影视天地是一个提供最新、最热门影视资源的在线平台，致力于为用户提供优质的体验。</p>
          </div>
          <div class="footer-section sci-fi-footer-section">
            <h3 class="sci-fi-footer-title">快速链接</h3>
            <ul class="sci-fi-footer-links">
              <li><router-link to="/" class="sci-fi-footer-link">首页</router-link></li>
              <li><router-link to="/category/movie" class="sci-fi-footer-link">电影</router-link></li>
              <li><router-link to="/category/tv" class="sci-fi-footer-link">电视剧</router-link></li>
              <li><router-link to="/category/variety" class="sci-fi-footer-link">综艺</router-link></li>
            </ul>
          </div>
          <div class="footer-section sci-fi-footer-section">
            <h3 class="sci-fi-footer-title">联系我们</h3>
            <p class="sci-fi-footer-text">邮箱:contact@movieheaven.com</p>
            <p class="sci-fi-footer-text">电话:400-123-4567</p>
          </div>
        </div>
        <div class="copyright sci-fi-copyright">
          <div class="footer-glow"></div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { movieApi } from '@/api/api'
import { formatGenre } from '@/utils/genre.js'




export default {
  name: 'HomeView',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const searchKeyword = ref('')

    // 轮播图电影数据
    const bannerMovies = ref([])

    // 热门电影数据
    const hotMovies = ref([])

    // 热门电视剧数据
    const hotTVShows = ref([])
    
    // 热门综艺数据
    const hotVarietyShows = ref([])
    
    // 获取首页数据
    const fetchHomeData = async () => {
      try {
        // 由于后端没有专门的banner接口，我们可以使用前几个热门电影作为轮播图
        
        // 获取热门电影（使用category_id过滤）
        const hotMoviesResponse = await movieApi.getMovieList({ category_id: 1, ordering: '-rate', limit: 10 })
        // 处理后端返回的数据格式
        const hotMoviesData = Array.isArray(hotMoviesResponse) ? hotMoviesResponse : (hotMoviesResponse.results || [])
        console.log('热门电影数据:', hotMoviesData)
        console.log('热门电影数据长度:', hotMoviesData.length)
        // 确保只显示10个
        hotMovies.value = hotMoviesData.slice(0, 10)
        
        // 设置轮播图数据（使用前4个热门电影）
        bannerMovies.value = hotMoviesData.slice(0, 4)
        console.log('轮播图数据长度:', bannerMovies.value.length)
        
        // 获取热门电视剧（使用category_id过滤）
        const hotTVResponse = await movieApi.getMovieList({ category_id: 2, ordering: '-rate', limit: 10 })
        const hotTVData = Array.isArray(hotTVResponse) ? hotTVResponse : (hotTVResponse.results || [])
        console.log('热门电视剧数据长度:', hotTVData.length)
        // 确保只显示10个
        hotTVShows.value = hotTVData.slice(0, 10)
        
        // 获取热门综艺（使用category_id过滤）
        const hotVarietyResponse = await movieApi.getMovieList({ category_id: 3, ordering: '-rate', limit: 10 })
        const hotVarietyData = Array.isArray(hotVarietyResponse) ? hotVarietyResponse : (hotVarietyResponse.results || [])
        console.log('热门综艺数据长度:', hotVarietyData.length)
        // 确保只显示10个
        hotVarietyShows.value = hotVarietyData.slice(0, 10)
      } catch (error) {
        console.error('获取首页数据失败:', error)
        ElMessage.error('获取首页数据失败，请稍后重试')
      }
    }

    // 搜索处理函数
    const handleSearch = () => {
      if (searchKeyword.value.trim()) {
        router.push({
          name: 'Search',
          query: { keyword: searchKeyword.value }
        })
      }
    }
    
    // 监听路由变化，确保每次进入首页都刷新数据
    watch(
      () => route.path,
      (newPath) => {
        if (newPath === '/') {
          fetchHomeData()
        }
      },
      { immediate: true } // 立即执行一次
    )

    // 组件挂载时获取数据
    onMounted(() => {
      fetchHomeData()
    })

    return {
      searchKeyword,
      bannerMovies,
      hotMovies,
      hotTVShows,
      hotVarietyShows,
      handleSearch,
      formatGenre
    }
  }
}
</script>

<style scoped>
/* 科幻风格基础样式 */
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f172a 100%);
  position: relative;
  overflow: hidden;
}

/* 粒子效果 */
.particles-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  background-color: rgba(100, 200, 255, 0.5);
  border-radius: 50%;
  animation: float linear infinite;
}

@keyframes float {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) translateX(100px);
    opacity: 0;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

/* 顶部搜索栏样式 */
.top-header {
  padding: 15px 30px;
  border-bottom: 1px solid rgba(100, 200, 255, 0.2);
  border-radius: 30px; /* 圆角：8px，柔和不尖锐 */
}

.search-container {
  max-width: 500px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  background-color: rgba(20, 30, 48, 0.7);
  border: 1px solid rgba(100, 200, 255, 0.3);
  border-radius: 4px;
}

.search-input input {
  background-color: transparent;
  color: #ffffff;
  border: none;
}

.search-input input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

/* 轮播图样式 */
.banner {
  margin: 30px 0;
  position: relative;
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.sci-fi-banner {
  overflow: hidden;
  width: 100%;
}

.sci-fi-carousel {
  position: relative;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

/* 轮播图卡片样式 */
.banner-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  text-decoration: none;
  color: #333;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.banner-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* 轮播图海报样式 */
.banner-card-poster {
  width: 100%;
  height: 300px;
  overflow: hidden;
}

.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.banner-card:hover .banner-img {
  transform: scale(1.05);
}

/* 轮播图信息样式 */
.banner-card-info {
  padding: 15px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.banner-card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.banner-card-desc {
  font-size: 14px;
  color: #666;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  flex: 1;
}

/* 科幻风格调整 */
.sci-fi-carousel .el-carousel__item--card {
  background: rgba(20, 30, 48, 0.9);
  border: 1px solid rgba(100, 200, 255, 0.2);
  border-radius: 8px;
}

.sci-fi-carousel .banner-card {
  background: transparent;
  border: none;
  box-shadow: none;
}

.sci-fi-carousel .banner-card-title {
  color: #ffffff;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.sci-fi-carousel .banner-card-desc {
  color: rgba(255, 255, 255, 0.8);
}

/* 指示器样式 */
.sci-fi-carousel .el-carousel__indicator--horizontal {
  bottom: 10px;
}

.sci-fi-carousel .el-carousel__indicator__button {
  background: rgba(255, 255, 255, 0.3);
}

.sci-fi-carousel .el-carousel__indicator.is-active .el-carousel__indicator__button {
  background: #00ccff;
  box-shadow: 0 0 10px rgba(0, 204, 255, 0.5);
}

/* 箭头样式 */
.sci-fi-carousel .el-carousel__arrow {
  background: rgba(20, 30, 48, 0.8);
  border: 1px solid rgba(100, 200, 255, 0.3);
  color: #ffffff;
}

.sci-fi-carousel .el-carousel__arrow:hover {
  background: rgba(100, 200, 255, 0.3);
  color: #00ccff;
}

/* 内容区域样式 */
.main-content {
  flex: 1;
  padding-bottom: 40px;
}

.sci-fi-main-content {
  position: relative;
}

.movie-section {
  margin-bottom: 40px;
}

.sci-fi-section {
  margin-bottom: 50px;
  position: relative;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.sci-fi-section-header {
  margin-bottom: 30px;
  position: relative;
}

.section-header h2 {
  font-size: 22px;
  color: #333;
  position: relative;
  padding-left: 15px;
}

.sci-fi-section-title {
  font-size: 24px;
  color: #ffffff !important;
  position: relative;
  padding-left: 20px;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.9), 0 0 15px rgba(100, 200, 255, 1), 0 0 30px rgba(100, 200, 255, 0.6);
  font-weight: 700;
  letter-spacing: 1px;
  opacity: 1;
  z-index: 10;
  display: inline-block;
  padding: 8px 15px;
  border-radius: 4px;
}

.sci-fi-section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6px;
  height: 24px;
  background: linear-gradient(to bottom, #00ccff, #0099ff);
  border-radius: 3px;
  box-shadow: 0 0 10px rgba(0, 204, 255, 0.5);
  z-index: -1;
}

.more-link {
  color: #999;
  text-decoration: none;
  transition: color 0.3s;
}

.sci-fi-more-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s;
  position: relative;
}

.sci-fi-more-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #00ccff, transparent);
  transition: width 0.3s;
}

.sci-fi-more-link:hover::after {
  width: 100%;
}

.sci-fi-more-link:hover {
  color: #00ccff;
  text-shadow: 0 0 5px rgba(0, 204, 255, 0.5);
}

.movie-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.sci-fi-movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 25px;
}

.movie-item {
  transition: transform 0.3s;
}

.sci-fi-movie-card {
  background-color: rgba(20, 30, 48, 0.8);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 153, 255, 0.2);
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid rgba(100, 200, 255, 0.2);
  position: relative;
}

.sci-fi-movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 153, 255, 0.4);
  border-color: rgba(100, 200, 255, 0.5);
}

.movie-item a {
  text-decoration: none;
  color: inherit;
}

.sci-fi-movie-link {
  display: block;
  text-decoration: none;
  color: #ffffff;
  height: 100%;
}

.movie-poster {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  aspect-ratio: 2/3;
}

.sci-fi-poster {
  position: relative;
  overflow: hidden;
  aspect-ratio: 2/3;
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.sci-fi-poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.movie-item:hover .movie-poster img {
  transform: scale(1.05);
}

.sci-fi-movie-card:hover .sci-fi-poster-img {
  transform: scale(1.05);
}

.poster-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(0deg, rgba(10, 14, 39, 0.7), transparent 50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.sci-fi-movie-card:hover .poster-overlay {
  opacity: 1;
}

.poster-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-shadow: inset 0 0 20px rgba(100, 200, 255, 0);
  transition: box-shadow 0.3s;
}

.sci-fi-movie-card:hover .poster-glow {
  box-shadow: inset 0 0 20px rgba(100, 200, 255, 0.5);
}

.movie-rating {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
}
</style>