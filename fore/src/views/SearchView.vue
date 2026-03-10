<template>
  <div class="search-page">
    <!-- 1. 增强粒子效果：分层悬浮+颜色渐变 -->
    <div class="particles-container">
      <!-- 主粒子层 -->
      <div class="particle" v-for="i in 80" :key="i" :style="{
        width: Math.random() * 8 + 'px',
        height: Math.random() * 8 + 'px',
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 20 + 's',
        animationDuration: Math.random() * 30 + 20 + 's',
        backgroundColor: `rgba(${100 + Math.random() * 155}, ${200 + Math.random() * 55}, 255, ${0.3 + Math.random() * 0.4})`,
        zIndex: Math.floor(Math.random() * 3)
      }"></div>
      <!-- 细线粒子层（模拟光线） -->
      <div class="line-particle" v-for="i in 30" :key="`line-${i}`" :style="{
        width: Math.random() * 30 + 10 + 'px',
        height: Math.random() * 2 + 'px',
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 15 + 's',
        animationDuration: Math.random() * 40 + 30 + 's',
        background: `linear-gradient(90deg, transparent, rgba(${150 + Math.random() * 105}, ${220 + Math.random() * 35}, 255, ${0.5 + Math.random() * 0.3}), transparent)`,
        transform: `rotate(${Math.random() * 360}deg)`,
        zIndex: 1
      }"></div>
    </div>
    
    <div class="container">
      <div class="search-header">
        <!-- 2. 标题全息投影效果 -->
        <h1 class="sci-fi-title" style="text-align: center;">
          <span class="title-hologram">搜索结果</span>
          <span class="title-glow"></span>
        </h1>
        
        <!-- 搜索框增强 -->
        <div class="search-box sci-fi-input-container">
          <el-input
            v-model="searchKeyword"
            placeholder="请输入关键词搜索"
            class="search-input sci-fi-input"
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button icon="el-icon-search" class="sci-fi-button" @click="handleSearch">
                <span class="button-pulse"></span>
              </el-button>
            </template>
          </el-input>
          <div class="input-glow"></div>
          <!-- 搜索框扫描线 -->
          <div class="input-scan-line"></div>
        </div>
      </div>

      <!-- 过滤器面板已移除 -->

      <!-- 搜索结果统计增强 -->
      <div class="search-info sci-fi-info" v-if="searchResults.length > 0" style="text-align: center;">
        <div class="info-hologram">
          <p class="sci-fi-text">找到 <span class="highlight sci-fi-highlight">{{ totalResults }}</span> 个相关结果</p>
          <div class="info-scan-line"></div>
        </div>
      </div>

      <!-- 加载状态（新增科幻加载动画） -->
      <div class="loading-sci-fi" v-if="isLoading">
        <div class="loading-container">
          <div class="loading-spinner"></div>
          <div class="loading-text">正在检索宇宙影视数据库...</div>
          <div class="loading-grid"></div>
        </div>
      </div>

      <!-- 搜索结果增强 -->
      <div class="search-results" v-if="searchResults.length > 0 && !isLoading" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div class="movie-list sci-fi-grid" style="max-width: 100%; width: auto;">
          <div class="movie-item sci-fi-card" v-for="movie in searchResults" :key="movie.id">
            <!-- 卡片全息投影效果 -->
            <div class="card-hologram"></div>
            <router-link :to="'/movie/' + movie.id" class="sci-fi-link">
              <div class="movie-poster sci-fi-poster">
                <img :src="movie.poster" :alt="movie.title" class="sci-fi-image">
                <!-- 新增海报扫描线 -->
                <div class="poster-scan-line"></div>
                <div class="movie-rating sci-fi-rating">
                  <el-rate v-model="movie.rating" disabled text-color="#ff9900"></el-rate>
                </div>
                <div class="movie-type sci-fi-type">{{ getTypeLabel(movie.type) }}</div>
                <!-- 新增全息光晕 -->
                <div class="poster-hologram-glow"></div>
                <div class="poster-overlay"></div>
                <div class="poster-glow"></div>
              </div>
              <h3 class="movie-title sci-fi-title-text">{{ movie.title }}</h3>
              <p class="movie-info sci-fi-info-text">{{ movie.year }} · {{ formatGenre(movie.genre) }} · {{ movie.region }}</p>
            </router-link>
          </div>
        </div>

        <!-- 分页增强 -->
        <div class="pagination sci-fi-pagination">
          <div class="pagination-hologram"></div>
          <el-pagination
            background
            layout="prev, pager, next"
            :total="totalResults"
            :page-size="pageSize"
            :current-page="currentPage"
            @current-change="handlePageChange"
            class="sci-fi-pager"
          >
          </el-pagination>
        </div>
      </div>

      <!-- 无结果增强 -->
      <div class="no-results sci-fi-no-results" v-else-if="!isLoading">
        <div class="no-results-hologram">
          <div class="no-results-grid"></div>
          <el-empty description="没有找到相关内容" class="sci-fi-empty">
            <el-button type="primary" @click="goHome" class="sci-fi-button">
              <span class="button-pulse"></span>
              返回首页
            </el-button>
          </el-empty>
          <div class="no-results-scan-line"></div>
        </div>
      </div>

      <!-- 相关推荐 -->
      <div class="related-movies">
        <div class="container">
          <h2 class="section-title">相关推荐</h2>
        </div>
        <div class="movie-list sci-fi-grid related-grid">
          <router-link :to="'/movie/' + movie.id" class="sci-fi-link" v-for="movie in relatedMovies" :key="movie.id">
            <div class="movie-item sci-fi-card">
              <!-- 卡片全息投影效果 -->
              <div class="card-hologram"></div>
              <div class="movie-poster sci-fi-poster">
                <img :src="movie.poster" :alt="movie.title" class="sci-fi-image">
                <!-- 海报扫描线 -->
                <div class="poster-scan-line"></div>
                <div class="movie-rating sci-fi-rating">
                  <el-rate v-model="movie.rating" disabled text-color="#ff9900"></el-rate>
                </div>
                <div class="movie-type sci-fi-type">{{ getTypeLabel(movie.type) }}</div>
                <!-- 全息光晕 -->
                <div class="poster-hologram-glow"></div>
                <div class="poster-overlay"></div>
                <div class="poster-glow"></div>
              </div>
              <h3 class="movie-title sci-fi-title-text">{{ movie.title }}</h3>
              <p class="movie-info sci-fi-info-text">{{ movie.year }} · {{ formatGenre(movie.genre) }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { movieApi } from '@/api/api.js'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'SearchView',
  setup() {
    const route = useRoute()
    const router = useRouter()

    const searchKeyword = ref('')
    const searchResults = ref([])
    const totalResults = ref(0)
    const pageSize = ref(20)
    const currentPage = ref(1)
    // 新增加载状态
    const isLoading = ref(false)
    // 相关推荐电影
    const relatedMovies = ref([])

    // 获取类型标签
    const getTypeLabel = (type) => {
      const typeMap = {
        'movie': '电影',
        'tv': '电视剧',
        'variety': '综艺'
      }
      return typeMap[type] || '影视'
    }

    // 类型ID到名称的映射
    const genreMap = {
      1: '动作',
      2: '喜剧',
      3: '爱情',
      4: '科幻',
      5: '悬疑',
      6: '惊悚',
      7: '恐怖',
      8: '犯罪',
      9: '剧情',
      10: '动画',
      11: '奇幻',
      12: '冒险',
      13: '传记',
      14: '历史',
      15: '战争',
      16: '西部',
      17: '音乐',
      18: '歌舞',
      19: '家庭',
      20: '儿童',
      21: '纪录片',
      22: '体育',
      23: '武侠',
      24: '古装',
      25: '灾难'
    }

    // 格式化类型字段
    const formatGenre = (genre) => {
      if (!genre) return '未知类型'
      
      // 处理不同格式的genre数据
      let genres = genre
      
      // 如果是字符串，按逗号分割
      if (typeof genres === 'string') {
        genres = genres.split(',').map(g => g.trim())
      }
      
      // 如果是数字，转换为数组
      if (typeof genres === 'number') {
        genres = [genres.toString()]
      }
      
      // 转换为中文名称
      const genreNames = genres.map(genre => {
        // 尝试转换为数字ID
        const genreId = parseInt(genre)
        return genreMap[genreId] || genre
      })
      
      return genreNames.join('、')
    }

    // 字段映射函数：将后端返回的字段名映射为前端需要的字段名
    const mapMovieFields = (movie) => {
      // 处理海报URL：如果是相对路径，添加后端URL前缀
      let posterUrl = movie.poster || movie.image_url;
      if (posterUrl && posterUrl.startsWith('/')) {
        // 相对路径，添加后端URL前缀
        posterUrl = `http://127.0.0.1:8000${posterUrl}`;
      }
      
      // 获取原始genre数据
      const rawGenre = movie.types || movie.genre
      
      return {
        id: movie.id,
        title: movie.name || movie.title,
        type: getCategoryType(movie.category_id),
        poster: posterUrl || `https://picsum.photos/seed/movie${movie.id}/300/450.jpg`,
        year: movie.release_year || movie.year || '未知年份',
        genre: formatGenre(rawGenre),
        region: getRegionName(movie.region),
        rating: movie.rate ? Number(movie.rate) / 2 : movie.rating || 0 // 如果评分是10分制，转换为5分制
      }
    }
    
    // 分类ID转类型
    const getCategoryType = (categoryId) => {
      const categoryMap = {
        1: 'movie',
        2: 'tv',
        3: 'variety'
      }
      return categoryMap[categoryId] || 'movie'
    }
    
    // 地区ID转名称
    const getRegionName = (regionId) => {
      const regionMap = {
        1: '中国大陆',
        2: '美国',
        3: '韩国',
        4: '日本',
        5: '英国',
        6: '其他'
      }
      return regionMap[regionId] || '其他'
    }
    
    // 获取相关推荐电影
    const fetchRelatedMovies = async () => {
      try {
        // 使用搜索结果中的第一部电影ID来获取相关推荐
        if (searchResults.value.length > 0) {
          const firstMovieId = searchResults.value[0].id
          const relatedResponse = await movieApi.getRelatedMovies(firstMovieId)
          // 正确处理响应数据
          const relatedData = Array.isArray(relatedResponse) ? relatedResponse : (relatedResponse.results || [])
          // 映射字段并限制为10个推荐
          relatedMovies.value = relatedData.slice(0, 10).map(mapMovieFields)
        } else {
          // 如果没有搜索结果，获取热门电影作为推荐
          const popularResponse = await movieApi.getMovieList({ limit: 10, ordering: '-rate' })
          const popularData = Array.isArray(popularResponse) ? popularResponse : (popularResponse.results || [])
          relatedMovies.value = popularData.map(mapMovieFields)
        }
      } catch (error) {
        console.error('获取相关推荐失败:', error)
      }
    }

    // 真实API搜索请求
    const fetchSearchResults = async () => {
      isLoading.value = true
      try {
        // 构建API查询参数
      const queryParams = {
        limit: pageSize.value,
        offset: (currentPage.value - 1) * pageSize.value
      }
      
      // 添加搜索关键词
      if (searchKeyword.value.trim()) {
        queryParams.name = searchKeyword.value.trim()
      }
      
      // 调用API获取真实数据
      const response = await movieApi.getMovieList(queryParams)
      
      // 处理后端返回的数据
      const data = response.results || response
      const mappedResults = data.map(mapMovieFields)
      
      // 直接使用映射后的结果
      let filteredResults = [...mappedResults]
        
        // 设置搜索结果
        searchResults.value = filteredResults
        totalResults.value = response.count || filteredResults.length
        
        // 获取相关推荐
        await fetchRelatedMovies()
      } catch (error) {
        console.error('搜索电影失败:', error)
        // 显示错误信息
        ElMessage.error(error.message || '搜索失败，请稍后重试')
      } finally {
        isLoading.value = false
      }
    }

    // 保持原有方法逻辑不变
    const handleSearch = () => {
      if (searchKeyword.value.trim()) {
        currentPage.value = 1
        fetchSearchResults()
      }
    }
    // applyFilters方法已移除
    const handlePageChange = (page) => {
      currentPage.value = page
      fetchSearchResults()
    }
    const goHome = () => {
      router.push('/')
    }

    watch(() => route.query.keyword, (newKeyword) => {
      if (newKeyword) {
        searchKeyword.value = newKeyword
        handleSearch()
      }
    })

    onMounted(() => {
      if (route.query.keyword) {
        searchKeyword.value = route.query.keyword
        handleSearch()
      } else {
        fetchSearchResults()
      }
    })

    // 处理相关电影点击事件
    const handleRelatedMovieClick = (id) => {
      router.push(`/movie/${id}`)
    }

    return {
      searchKeyword,
      searchResults,
      totalResults,
      pageSize,
      currentPage,
      relatedMovies,
      getTypeLabel,
      handleSearch,
      handlePageChange,
      goHome,
      handleRelatedMovieClick,
      isLoading // 暴露加载状态
    }
  }
}
</script>

<style scoped>
/* 页面基础样式 */
.search-page {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
}

/* 粒子效果容器样式 - 修复布局问题 */
.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

/* 主粒子样式 */
.particle {
  position: absolute;
  border-radius: 50%;
  animation: float 20s infinite ease-in-out;
}

/* 细线粒子样式 */
.line-particle {
  position: absolute;
  animation: float 30s infinite ease-in-out;
}

/* 容器样式 - 确保内容在粒子效果上方 */
.container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 搜索框容器样式 */
.sci-fi-input-container {
  position: relative;
  width: 100%;
  max-width: 600px; /* 设置合适的最大宽度 */
  margin: 0 auto;
}

/* 搜索框输入样式 */
.search-input {
  width: 100%;
  background-color: rgba(20, 30, 48, 0.7);
  border: 1px solid rgba(100, 200, 255, 0.3);
  border-radius: 4px;
}

/* 相关推荐网格样式 */
.related-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

/* 确保相关推荐项目响应式显示 */
@media (max-width: 1200px) {
  .related-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .related-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .related-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .related-grid {
    grid-template-columns: 1fr;
  }
}

/* 确保影片卡片样式一致 */
.sci-fi-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

/* 搜索结果网格样式 */
.movie-list.sci-fi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

/* 响应式设计 - 搜索结果 */
@media (max-width: 1200px) {
  .movie-list.sci-fi-grid {
    grid-template-columns: repeat(3, 1fr);
    max-width: 960px;
  }
}

@media (max-width: 992px) {
  .movie-list.sci-fi-grid {
    grid-template-columns: repeat(3, 1fr);
    max-width: 720px;
  }
}

@media (max-width: 768px) {
  .movie-list.sci-fi-grid {
    grid-template-columns: repeat(2, 1fr);
    max-width: 540px;
  }
}

@media (max-width: 576px) {
  .movie-list.sci-fi-grid {
    grid-template-columns: 1fr;
    max-width: 100%;
  }
}

.movie-item {
  position: relative;
  transition: transform 0.3s ease;
}

.movie-item:hover {
  transform: translateY(-5px);
}

/* 相关推荐部分与搜索结果部分的间距 */
.related-movies {
  margin-top: 40px;
}

/* 粒子浮动动画 */
@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}
</style>