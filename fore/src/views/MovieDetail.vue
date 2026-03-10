<template>
  <div class="movie-detail" v-if="movie">
    <!-- 面包屑导航 -->
    <div class="breadcrumb">
      <div class="container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: `/category/${movie.type}` }">{{ typeLabel }}</el-breadcrumb-item>
          <el-breadcrumb-item>{{ movie.title }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>

    <!-- 电影信息主体 -->
    <div class="movie-main">
      <div class="container">
        <div class="movie-content">
          <!-- 左侧海报 -->
          <div class="movie-poster">
            <img :src="movie.poster" :alt="movie.title">
          </div>

          <!-- 右侧详情 -->
          <div class="movie-info">
            <h1 class="movie-title">电影名：{{ movie.title }}</h1>
            <div class="detail-item">
                <span class="label">又名：</span>
                <span class="value">{{ movie.aka || '' }}</span>
            </div>
            <div class="detail-item">
                <span class="label">上映年份：</span>
                <span class="value">{{ movie.year || '' }}</span>
            </div>
            <div class="detail-item">
                <span class="label">导演：</span>
                <span class="value">{{ movie.director || '' }}</span>
            </div>
            <div class="detail-item">
                <span class="label">编剧：</span>
                <span class="value">{{ movie.scriptwriter || '' }}</span>
            </div>
            <div class="detail-item">
                <span class="label">主演：</span>
                <span class="value">{{ movie.actors || '' }}</span>
            </div>
            <div class="detail-item">
                <span class="label">地区：</span>
                <span class="value">{{ getRegionName(movie.region) }}</span>
            </div>
            <div class="detail-item">
                <span class="label">类型：</span>
                <span class="value">{{ formattedGenre }}</span>
            </div>
            <div class="detail-item">
                <span class="label">语言：</span>
                <span class="value">{{ movie.language || '' }}</span>
            </div>
            <div class="detail-item">
                <span class="label">片长（或集数）：</span>
                <span class="value">{{ movie.duration || '' }}{{ movie.type === 'tv' ? '集' : '分钟' }}</span>
            </div>
            <div class="detail-item">
                <span class="label">豆瓣评分：</span>
                <span class="value">{{ movie.rating }}分</span>
            </div>

            <div class="movie-actions">
              <el-button 
                type="default" 
                @click="toggleFavorite">
                <el-icon><star :style="{ color: isFavorite ? '#ff9900' : '' }" /></el-icon>
                {{ isFavorite ? '已收藏' : '收藏' }}
              </el-button>
            </div>
          </div>
        </div>

        <!-- 简介区域 - 移到海报下方 -->
        <div class="movie-plot-section">
          <h2 class="section-title">简介</h2>
          <div class="plot-content-container">
            <p class="plot-content" v-html="movie.plot || '暂无简介'"></p>
          </div>
        </div>

        <!-- 影评区 -->
        <div class="movie-reviews">
          <h2 class="section-title">影评</h2>
          <div class="review-form">
            <el-input
              type="textarea"
              :rows="3"
              placeholder="发表你的影评..."
              v-model="reviewText"
            ></el-input>
            <div class="review-submit">
              <el-rate v-model="reviewRating" class="review-rating"></el-rate>
              <el-button type="primary" @click="submitReview">发表影评</el-button>
            </div>
          </div>

          <div class="review-list">
            <div class="review-item" v-for="review in reviews" :key="review.id">
              <div class="review-avatar">
                <img :src="review.user.avatar" :alt="review.user.name">
              </div>
              <div class="review-content">
                <div class="review-header">
                  <span class="review-user">{{ review.user.name }}</span>
                  <el-rate v-model="review.rating" disabled size="small"></el-rate>
                  <span class="review-time">{{ review.time }}</span>
                </div>
                <div class="review-text">{{ review.text }}</div>
                <div class="review-actions">
                  <span class="action-btn" @click="likeReview(review)">
                    <el-icon><star /></el-icon> {{ review.likes }}
                  </span>
                  <span class="action-btn" @click="replyReview(review)">
                    <el-icon><chat-dot-round /></el-icon> 回复
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="load-more" v-if="hasMoreReviews">
            <el-button @click="loadMoreReviews" :loading="loadingReviews">加载更多影评</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 相关推荐 -->
    <div class="related-movies">
      <div class="container">
        <h2 class="section-title">相关推荐</h2>
        <div class="movie-list">
          <div class="movie-item" v-for="relatedMovie in relatedMovies" :key="relatedMovie.id" @click="handleRelatedMovieClick(relatedMovie.id)">
            <div class="movie-poster">
              <img :src="relatedMovie.poster" :alt="relatedMovie.title">
            </div>
            <h3 class="movie-title">{{ relatedMovie.title }}</h3>
            <div class="movie-rating">
              <el-rate :model-value="relatedMovie.rating / 2" disabled text-color="#ff9900" :max="5" :precision="0.5"></el-rate>
            </div>
          </div>
        </div>
      </div>
    </div>

    </div>
  <div v-else class="loading-container">
    <el-skeleton :rows="10" animated />
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, onActivated, onDeactivated } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Star,  ChatDotRound } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { movieApi,interactionApi } from '@/api/api'
//import { useStore } from 'vuex'


export default {
  name: 'MovieDetail',
  components: {
    Star,
    ChatDotRound
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    // 使用computed使movieId成为响应式的，以便路由参数变化时自动更新
    const movieId = computed(() => route.params.id)
    const movie = ref(null)
    const isFavorite = ref(false)
    const reviewText = ref('')
    const reviewRating = ref(0)
    const reviews = ref([])
    const hasMoreReviews = ref(true)
    const loadingReviews = ref(false)
    
    // 辅助函数：将地区数字转换为地区名称
    const getRegionName = (regionId) => {
      const regionMap = {
        1: '中国',
        2: '美国',
        3: '韩国',
        4: '日本',
        5: '其他'
      }
      return regionMap[regionId] || ''
    }
    
    // 辅助函数：将分类类型转换为中文名称
    const getTypeName = (type) => {
      const typeMap = {
        'movie': '电影',
        'tv': '电视剧',
        'variety': '综艺'
      }
      return typeMap[type] || ''
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
    const formattedGenre = computed(() => {
      if (!movie.value || !movie.value.genre) return '未知类型'
      
      // 处理不同格式的genre数据
      let genres = movie.value.genre
      
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
    })

    // 计算属性
    const typeLabel = computed(() => {
      if (!movie.value) return ''
      const typeMap = {
        'movie': '电影',
        'tv': '电视剧',
        'variety': '综艺'
      }
      return typeMap[movie.value.type] || '影视'
    })

    // 获取电影详情
    const fetchMovieDetail = async () => {
      try {
        // 从后端API获取电影详情 - 使用movieId.value确保获取最新值
        const movieResponse = await movieApi.getMovieDetail(movieId.value)
        // 正确处理响应数据（处理Django REST Framework可能的不同返回格式）
        movie.value = movieResponse || {}
        
        // 从后端API获取相关推荐电影 - 使用movieId.value确保获取最新值
        const relatedResponse = await movieApi.getRelatedMovies(movieId.value)
        // 正确处理响应数据（处理Django REST Framework可能的不同返回格式）
        relatedMovies.value = Array.isArray(relatedResponse) ? relatedResponse : (relatedResponse.results || [])
        
        // 获取电影收藏状态
        await fetchFavoriteStatus()
        
        // 注意：后端暂未实现影评功能
        reviews.value = []
      } catch (error) {
        ElMessage.error('获取电影详情失败，请稍后重试')
        console.error('获取电影详情失败:', error)
      }
    }


    // 获取电影收藏状态
    const fetchFavoriteStatus = async () => {
      // 修改后的登录状态检查
    //   try {
    //     // 检查用户是否已登录 - 使用多个字段进行验证
    //     const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    //     const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    //
    //     // 如果任一登录状态为真，则认为已登录
    //     if (isAuthenticated || isLoggedIn) {
    //       // 从后端获取用户收藏列表
    //       const favoritesResponse = await interactionApi.getFavorites().then(response => {console.log('收藏列表:', response.data)});
    //       const favorites = Array.isArray(favoritesResponse) ? favoritesResponse : (favoritesResponse.results || [])
    //       isFavorite.value = favorites.some(favorite => favorite.movie === movieId.value || favorite.movie?.id === movieId.value)
    //     } else {
    //       isFavorite.value = false
    //     }
    //   } catch (error) {
    //     console.error('获取收藏状态失败:', error)
    //     isFavorite.value = false
    //   }
    // }
      try {
        // 检查用户是否已登录
        const token = localStorage.getItem('token')
        if (!token) {
          isFavorite.value = false
          return
        }

        // 从后端获取用户收藏列表，检查当前电影是否在收藏列表中
        const favoritesResponse = await interactionApi.getFavorites()
        const favorites = Array.isArray(favoritesResponse) ? favoritesResponse : (favoritesResponse.results || [])
        isFavorite.value = favorites.some(favorite => favorite.movie === movieId.value || favorite.movie?.id === movieId.value)
      } catch (error) {
        console.error('获取收藏状态失败:', error)
        isFavorite.value = false
      }
    }
    
    const relatedMovies = ref([])

    

    // 切换收藏状态
    const toggleFavorite = async () => {
      try {
        // 检查用户是否已登录
        const token = localStorage.getItem('token')
        if (!token) {
          ElMessage.warning('请先登录再进行收藏操作')
          return
        }
        
        if (isFavorite.value) {
          // 取消收藏
          await interactionApi.unfavoriteMovie(movieId.value)
          isFavorite.value = false
          ElMessage.success('取消收藏成功')
        } else {
          // 添加收藏
          await interactionApi.favoriteMovie(movieId.value)
          isFavorite.value = true
          ElMessage.success('收藏成功')
        }
      } catch (error) {
        console.error('切换收藏状态失败:', error)
        // 重新获取收藏状态，确保状态同步
        await fetchFavoriteStatus()
        ElMessage.error('操作失败，请稍后重试')
      }
    }
    
    // 滚动到影评区
    const scrollToReview = () => {
      const reviewSection = document.querySelector('.movie-reviews')
      if (reviewSection) {
        reviewSection.scrollIntoView({ behavior: 'smooth' })
      }
    }

    // 提交影评 - 后端暂未实现
    const submitReview = () => {
      ElMessage.warning('影评功能暂未开放')
    }

    // 点赞影评 - 后端暂未实现
    const likeReview = () => {
      ElMessage.warning('点赞功能暂未开放')
    }

    // 回复影评
    const replyReview = (review) => {
      reviewText.value = `@${review.user.name} `
      // 滚动到影评框
      document.querySelector('.review-form').scrollIntoView({ behavior: 'smooth' })
    }

    // 加载更多影评 - 后端暂未实现
    const loadMoreReviews = () => {
      ElMessage.warning('影评功能暂未开放')
    }

    // 处理相关电影点击事件
    const handleRelatedMovieClick = (id) => {
      router.push(`/movie/${id}`)
    }

    onMounted(() => {
      fetchMovieDetail()
    })

    // 组件从缓存中激活时执行
    onActivated(() => {
      // 当组件被激活时（从缓存中恢复），重新获取数据
      fetchMovieDetail()
    })

    // 组件被缓存前执行
    onDeactivated(() => {
      // 组件被缓存前的清理工作（如果需要）
    })
    
    // 监听路由参数id的变化，当用户点击相关推荐电影时重新加载数据
    watch(
      () => route.params.id,
      (newId, oldId) => {
        if (newId !== oldId) {
          fetchMovieDetail()
        }
      }
    )

    return {
      movie,
      typeLabel,
      formattedGenre,
      isFavorite,
      reviewText,
      reviewRating,
      reviews,
      hasMoreReviews,
      loadingReviews,
      relatedMovies,
      toggleFavorite,
      submitReview,
      likeReview,
      replyReview,
      loadMoreReviews,
      scrollToReview,
      getRegionName,
      getTypeName,
      router,
      handleRelatedMovieClick,
    }
  }
}
</script>

<style scoped>
.loading-container {
  padding: 30px;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f172a 100%);
}

.breadcrumb {
  padding: 15px 0;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f172a 100%);
  border-bottom: 1px solid rgba(100, 200, 255, 0.2);
  font-size: 18px;
}

.breadcrumb .el-breadcrumb {
  font-size: 18px;
}

.breadcrumb .el-breadcrumb__item {
  font-size: 18px;
}

.breadcrumb .el-breadcrumb__item a {
  color: rgba(255, 255, 255, 0.9) !important;
}

.breadcrumb .el-breadcrumb__item.is-active {
  color: #ffffff !important;
  font-weight: bold;
}

.movie-main {
  padding: 30px 0;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f172a 100%);
}

.movie-content {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  align-items: flex-start;
}

/* 主页面海报容器样式 */
.movie-content .movie-poster {
  flex-shrink: 0;
  width: 300px; /* 主页面海报固定宽度 */
  position: relative;
}

/* 主页面海报图片样式 */
.movie-content .movie-poster img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 153, 255, 0.3);
  border: 1px solid rgba(100, 200, 255, 0.2);
}

/* 全局字体大小调整 */
.movie-detail {
  font-size: 16px;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f172a 100%);
  color: #ffffff;
}

/* 简介区域样式 */
.movie-plot-section {
  margin-top: 30px;
  padding: 20px;
  background: rgba(20, 30, 48, 0.8);
  border-radius: 8px;
  border: 1px solid rgba(100, 200, 255, 0.2);
  box-shadow: 0 2px 12px rgba(0, 153, 255, 0.2);
}

/* 简介内容容器样式 */
.plot-content-container {
  width: 100%;
}

/* 简介内容文本样式 */
.plot-content {
  line-height: 1.8;
  color: #ffffff;
  text-align: justify;
  font-size: 16px;
  margin: 0;
  padding: 10px 0 0 0;
}

.movie-info {
  flex: 1;
}

.movie-title {
  font-size: 32px;
  margin-bottom: 15px;
  color: #ffffff;
  text-shadow: 0 0 5px rgba(0, 204, 255, 0.5);
}

.movie-meta {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.rating {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.rating-score {
  margin-left: 10px;
  font-size: 18px;
  color: #ff9900;
  font-weight: bold;
}

.movie-tags {
  display: flex;
  gap: 8px;
}

.movie-details {
  margin-bottom: 25px;
}

.detail-item {
  margin-bottom: 12px;
  line-height: 1.8;
  font-size: 16px;
}

.label {
  color: rgba(255, 255, 255, 0.7);
  margin-right: 5px;
}

.value {
  color: #ffffff;
}

.movie-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  margin-top: 30px;
  align-items: center;
}

.rating-stars {
  display: flex;
  gap: 5px;
}

.star-icon {
  cursor: pointer;
  font-size: 24px;
  transition: color 0.2s;
}

.star-icon:not(.active) .el-icon-star {
  color: transparent;
  stroke: #ff9900;
  stroke-width: 2;
}

.star-icon.active .el-icon-star {
  color: #ff9900;
  fill: #ff9900;
}

.section-title {
  font-size: 24px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(100, 200, 255, 0.2);
  color: #ffffff;
  text-shadow: 0 0 5px rgba(0, 204, 255, 0.5);
  font-weight: 700;
  letter-spacing: 1px;
}

.movie-plot {
  margin-bottom: 40px;
  width: 100%;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding-left: 0;
  margin-left: 0;
}

.movie-plot .label {
  flex-shrink: 0;
  margin-top: 0;
  color: rgba(255, 255, 255, 0.7);
}

.plot-content-container {
  flex: 1;
  width: calc(100% - 50px);
  overflow: hidden;
  border-radius: 8px;
  margin-top: 0;
  padding-top: 0;
}

/* 精美的滚动框样式 - 根据文本数量自动调整高度 */
.plot-content {
  line-height: 1.8;
  color: #ffffff;
  min-height: 100px; /* 设置最小高度，确保内容少时也有良好的显示效果 */
  max-height: 300px; /* 设置最大高度，超过后显示滚动条 */
  overflow-y: auto; /* 自动显示滚动条 */
  overflow-x: hidden;
  padding: 16px;
  background: rgba(20, 30, 48, 0.8);
  border: 1px solid rgba(100, 200, 255, 0.2);
  word-wrap: break-word;
  word-break: break-word;
  white-space: normal;
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  font-size: 16px;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 12px 0 rgba(0, 153, 255, 0.2);
  text-indent: 2em; /* 首行缩进两格 */
  transition: all 0.3s ease;
}

/* 调整段落间距 */
.plot-content br {
  display: block;
  margin: 4px 0;
  content: "";
}

/* 确保p标签没有额外的margin */
.plot-content p {
  margin: 0;
  padding: 0;
  color: #ffffff;
}

/* 调整div和其他块级元素的间距 */
.plot-content div,
.plot-content p,
.plot-content span {
  margin: 0;
  padding: 0;
  color: #ffffff;
}

/* Webkit浏览器滚动条样式 - 确保滚动条始终可见 */
.plot-content::-webkit-scrollbar {
  width: 8px;
  height: 0;
}

/* Firefox浏览器滚动条样式 */
.plot-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(100, 200, 255, 0.5) rgba(20, 30, 48, 0.8);
}

.plot-content::-webkit-scrollbar-track {
  background: rgba(20, 30, 48, 0.8);
  border-radius: 4px;
}

.plot-content::-webkit-scrollbar-thumb {
  background-color: rgba(100, 200, 255, 0.5);
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.plot-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(100, 200, 255, 0.8);
}

/* 额外保险：确保任何子元素不会导致水平滚动 */
.plot-content * {
  max-width: 100%;
  overflow-wrap: break-word;
  color: #ffffff;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .movie-plot {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .movie-plot .label {
    margin-bottom: 8px;
    margin-top: 0;
  }
  
  .plot-content-container {
    width: 100%;
  }
  
  .plot-content {
    height: 180px;
    font-size: 15px;
    padding: 12px;
  }
}

.movie-cast {
  margin-bottom: 40px;
}

.cast-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.cast-item {
  text-align: center;
}

.actor-avatar {
  width: 100px;
  height: 100px;
  margin: 0 auto 10px;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid rgba(100, 200, 255, 0.3);
}

.actor-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.actor-info h4 {
  margin-bottom: 5px;
  font-size: 16px;
  color: #ffffff;
}

.actor-info p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.trailer-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 比例 */
  height: 0;
  overflow: hidden;
  border: 1px solid rgba(100, 200, 255, 0.2);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 153, 255, 0.2);
}

.trailer-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.movie-reviews {
  margin-bottom: 40px;
}

.review-form {
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(20, 30, 48, 0.8);
  border-radius: 8px;
  border: 1px solid rgba(100, 200, 255, 0.2);
  box-shadow: 0 2px 12px rgba(0, 153, 255, 0.2);
}

.review-submit {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.review-rating {
  margin-right: 15px;
}

.review-list {
  margin-bottom: 20px;
}

.review-item {
  display: flex;
  padding: 20px 0;
  border-bottom: 1px solid rgba(100, 200, 255, 0.2);
}

.review-avatar {
  width: 50px;
  height: 50px;
  margin-right: 15px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid rgba(100, 200, 255, 0.3);
}

.review-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-content {
  flex: 1;
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.review-user {
  font-weight: bold;
  margin-right: 10px;
  color: #ffffff;
}

.review-time {
  margin-left: auto;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.review-text {
  line-height: 1.6;
  margin-bottom: 10px;
  color: #ffffff;
}

.review-actions {
  display: flex;
  gap: 15px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  font-size: 14px;
}

.action-btn:hover {
  color: #00ccff;
  text-shadow: 0 0 5px rgba(0, 204, 255, 0.5);
}

.load-more {
  text-align: center;
  margin-top: 20px;
}

.related-movies {
  padding: 30px 0;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f172a 100%);
}

.movie-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.movie-item {
  background-color: rgba(20, 30, 48, 0.8);
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  text-align: center;
  border: 1px solid rgba(100, 200, 255, 0.2);
  box-shadow: 0 2px 12px rgba(0, 153, 255, 0.2);
  cursor: pointer;
  display: block;
  text-decoration: none;
  z-index: 1;
}

.movie-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 153, 255, 0.4);
}



.related-movies .movie-poster {
  position: relative;
  padding-bottom: 150%;
  overflow: hidden;
}

.movie-poster img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.movie-item:hover .movie-poster img {
  transform: scale(1.05);
}

.movie-title {
  padding: 10px;
  font-size: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: bold;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 0 5px rgba(100, 200, 255, 0.3);
}

.movie-rating {
  padding: 0 10px 10px;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.related-movies .movie-info {
  display: none;
}



@media (max-width: 768px) {
  .movie-content {
    flex-direction: column;
  }

  .movie-poster {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }

  .cast-list {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  .movie-list {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>

