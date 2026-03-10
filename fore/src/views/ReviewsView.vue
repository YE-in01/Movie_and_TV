<template>
  <div class="reviews-page">
    <div class="page-header">
      <h1 class="page-title">影评中心</h1>
      <p class="page-description">分享您的观影感受，发现更多精彩观点</p>
    </div>

    <div class="reviews-container">
      <!-- 影评筛选和排序 -->
      <div class="filter-bar">
        <div class="filter-group">
          <span class="filter-label">分类：</span>
          <el-radio-group v-model="reviewFilter.type" @change="applyFilters">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="movie">电影</el-radio-button>
            <el-radio-button label="tv">电视剧</el-radio-button>
            <el-radio-button label="variety">综艺</el-radio-button>
          </el-radio-group>
        </div>

        <div class="filter-group">
          <span class="filter-label">排序：</span>
          <el-select v-model="reviewFilter.sort" @change="applyFilters" style="width: 150px;">
            <el-option label="最新发布" value="newest"></el-option>
            <el-option label="最多点赞" value="mostLiked"></el-option>
            <el-option label="最多回复" value="mostReplied"></el-option>
            <el-option label="评分最高" value="highestRated"></el-option>
          </el-select>
        </div>

        <div class="filter-group">
          <el-input
            v-model="reviewFilter.keyword"
            placeholder="搜索影评"
            @keyup.enter="applyFilters"
            style="width: 200px;"
          >
            <template #append>
              <el-button icon="el-icon-search" @click="applyFilters"></el-button>
            </template>
          </el-input>
        </div>
      </div>

      <!-- 我的影评 -->
      <div class="my-reviews-section">
        <el-card class="section-card sci-fi-card">
          <template #header>
            <div class="card-header">
              <span>我的影评</span>
              <el-button type="primary" size="small" @click="showWriteReviewDialog = true">写影评</el-button>
            </div>
          </template>

          <div v-if="myComments.length > 0" class="reviews-list">
            <div v-for="comment in myComments" :key="comment.id" class="review-item">
              <div class="review-movie">
                <img :src="comment.moviePoster" :alt="comment.movieTitle" class="movie-poster">
                <div class="movie-info">
                  <router-link :to="'/movie/' + comment.movieId" class="movie-title">{{ comment.movieTitle }}</router-link>
                  <p class="movie-meta">{{ comment.movieYear }} · {{ formatGenre(comment.movieGenre) }}</p>
                </div>
                <div class="movie-rating">
                  <el-rate v-model="comment.rating" disabled text-color="#ff9900"></el-rate>
                </div>
              </div>

              <div class="review-content">
                <p>{{ comment.content }}</p>
                <div class="review-meta">
                  <span class="review-time">{{ formatTime(comment.createTime) }}</span>
                  <div class="review-actions">
                    <span class="action-item" @click="editComment(comment)">
                      <el-icon><Edit /></el-icon>编辑
                    </span>
                    <span class="action-item" @click="deleteComment(comment.id)">
                      <el-icon><Delete /></el-icon>删除
                    </span>
                    <span class="action-item" :class="{ active: comment.isLiked }" @click="toggleLike(comment)">
                      <el-icon><Star /></el-icon>{{ comment.likeCount }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="empty-state">
            <el-empty description="您还没有发表任何影评">
              <el-button type="primary" @click="showWriteReviewDialog = true">发表第一条影评</el-button>
            </el-empty>
          </div>

          <div class="pagination-container" v-if="myComments.length > 0">
            <el-pagination
              background
              layout="prev, pager, next"
              :total="myCommentsTotal"
              :page-size="myCommentsPageSize"
              :current-page="myCommentsPage"
              @current-change="handleMyCommentsPageChange"
            >
            </el-pagination>
          </div>
        </el-card>
      </div>

      <!-- 热门影评 -->
      <div class="hot-reviews-section">
        <el-card class="section-card sci-fi-card">
          <template #header>
            <div class="card-header">
              <span>热门影评</span>
              <el-tabs v-model="hotCommentsTab" class="review-tabs">
                <el-tab-pane label="推荐" name="recommended"></el-tab-pane>
                <el-tab-pane label="最新" name="newest"></el-tab-pane>
                <el-tab-pane label="关注" name="following"></el-tab-pane>
              </el-tabs>
            </div>
          </template>

          <div class="reviews-list">
            <div v-for="comment in hotComments" :key="comment.id" class="review-item">
              <div class="review-user">
                <el-avatar :size="40" :src="comment.userAvatar">{{ comment.username.charAt(0) }}</el-avatar>
                <div class="user-info">
                  <span class="username">{{ comment.username }}</span>
                  <span class="user-level">Lv.{{ comment.userLevel }}</span>
                </div>
                <el-button 
                  v-if="!comment.isFollowing" 
                  type="text" 
                  size="small" 
                  @click="followUser(comment.userId)"
                  class="follow-btn"
                >
                  + 关注
                </el-button>
                <el-button 
                  v-else 
                  type="text" 
                  size="small" 
                  @click="unfollowUser(comment.userId)"
                  class="follow-btn following"
                >
                  已关注
                </el-button>
              </div>

              <div class="review-movie">
                <img :src="comment.moviePoster" :alt="comment.movieTitle" class="movie-poster">
                <div class="movie-info">
                  <router-link :to="'/movie/' + comment.movieId" class="movie-title">{{ comment.movieTitle }}</router-link>
                  <p class="movie-meta">{{ comment.movieYear }} · {{ formatGenre(comment.movieGenre) }}</p>
                </div>
                <div class="movie-rating">
                  <el-rate v-model="comment.rating" disabled text-color="#ff9900"></el-rate>
                </div>
              </div>

              <div class="review-content">
                <p>{{ comment.content }}</p>
                <div class="review-images" v-if="comment.images && comment.images.length > 0">
                  <div v-for="(image, index) in comment.images" :key="index" class="review-image">
                    <img :src="image" alt="影评图片" @click="previewImage(image)">
                  </div>
                </div>
                <div class="review-meta">
                  <span class="review-time">{{ formatTime(comment.createTime) }}</span>
                  <div class="review-actions">
                    <span class="action-item" :class="{ active: comment.isLiked }" @click="toggleLike(comment)">
                      <el-icon><Star /></el-icon>{{ comment.likeCount }}
                    </span>
                    <span class="action-item" @click="showReplyDialog(comment)">
                      <el-icon><ChatDotRound /></el-icon>{{ comment.replyCount }}
                    </span>
                    <span class="action-item" @click="shareComment(comment)">
                      <el-icon><Share /></el-icon>分享
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="pagination-container">
            <el-pagination
              background
              layout="prev, pager, next"
              :total="hotCommentsTotal"
              :page-size="hotCommentsPageSize"
              :current-page="hotCommentsPage"
              @current-change="handleHotCommentsPageChange"
            >
            </el-pagination>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 写影评对话框 -->
    <el-dialog
      v-model="showWriteReviewDialog"
      title="写影评"
      width="50%"
      class="write-review-dialog sci-fi-dialog"
    >
      <div class="write-review-form">
        <div class="movie-select">
          <span class="form-label">选择影视作品：</span>
          <el-autocomplete
            v-model="selectedMovie.title"
            :fetch-suggestions="queryMovies"
            placeholder="请输入电影/电视剧名称"
            @select="handleMovieSelect"
            style="width: 100%;"
          >
            <template #default="{ item }">
              <div class="movie-suggestion">
                <img :src="item.poster" :alt="item.title" class="suggestion-poster">
                <div class="suggestion-info">
                  <div class="suggestion-title">{{ item.title }}</div>
                  <div class="suggestion-meta">{{ item.year }} · {{ item.genre }}</div>
                </div>
              </div>
            </template>
          </el-autocomplete>
        </div>

        <div class="rating-select">
          <span class="form-label">评分：</span>
          <el-rate v-model="newComment.rating" show-text></el-rate>
        </div>

        <div class="review-textarea">
          <span class="form-label">影评内容：</span>
          <el-input
            v-model="newComment.content"
            type="textarea"
            :rows="6"
            placeholder="分享您的观影感受..."
            maxlength="500"
            show-word-limit
          ></el-input>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showWriteReviewDialog = false">取消</el-button>
          <el-button type="primary" @click="submitComment">发布</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Delete, Star, ChatDotRound, Share } from '@element-plus/icons-vue'
import { formatGenre } from '@/utils/genre.js'

export default {
  name: 'ReviewsView',
  components: {
    Edit,
    Delete,
    Star,
    ChatDotRound,
    Share
  },
  setup() {
    // 影评筛选条件
    const reviewFilter = ref({
      type: 'all',
      sort: 'newest',
      keyword: ''
    })

    // 热门影评标签页
    const hotCommentsTab = ref('recommended')

    // 写影评对话框
    const showWriteReviewDialog = ref(false)

    // 图片预览URL
    const previewImageUrl = ref(null)

    // 选中的电影
    const selectedMovie = ref({
      id: null,
      title: ''
    })

    // 新影评内容
    const newComment = ref({
      rating: 0,
      content: ''
    })

    // 我的影评
    const myComments = ref([])

    // 热门影评
    const hotComments = ref([])

    // 分页信息
    const myCommentsPage = ref(1)
    const myCommentsPageSize = ref(10)
    const myCommentsTotal = ref(0)

    const hotCommentsPage = ref(1)
    const hotCommentsPageSize = ref(10)
    const hotCommentsTotal = ref(0)

    // 电影搜索建议
    const movieSuggestions = ref([])

    // 格式化时间
    const formatTime = (time) => {
      const date = new Date(time)
      const now = new Date()
      const diff = now - date

      if (diff < 60000) {
        return '刚刚'
      } else if (diff < 3600000) {
        return Math.floor(diff / 60000) + '分钟前'
      } else if (diff < 86400000) {
        return Math.floor(diff / 3600000) + '小时前'
      } else if (diff < 2592000000) {
        return Math.floor(diff / 86400000) + '天前'
      } else {
        return date.toLocaleDateString()
      }
    }

    // 应用筛选条件
    const applyFilters = () => {
      // 这里应该调用API获取筛选后的影评
      console.log('应用筛选条件:', reviewFilter.value)
      ElMessage.success('筛选条件已应用')
    }

    // 查询电影建议
    const queryMovies = (queryString, cb) => {
      // 这里应该调用API搜索电影
      const results = queryString
        ? movieSuggestions.value.filter(item => item.title.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
        : movieSuggestions.value

      cb(results)
    }

    // 选择电影
    const handleMovieSelect = (item) => {
      selectedMovie.value = item
      newComment.value.movieId = item.id
    }

    // 提交影评
    const submitComment = () => {
      if (!newComment.value.movieId) {
        ElMessage.warning('请选择要评论的影视作品')
        return
      }

      if (!newComment.value.content.trim()) {
        ElMessage.warning('请输入影评内容')
        return
      }

      if (newComment.value.rating === 0) {
        ElMessage.warning('请为作品评分')
        return
      }

      // 这里应该调用API提交影评
      console.log('提交影评:', newComment.value)

      ElMessage.success('影评发布成功')
      showWriteReviewDialog.value = false

      // 重置表单
      newComment.value = {
        movieId: null,
        rating: 0,
        content: ''
      }
      selectedMovie.value = {
        id: null,
        title: '',
        poster: ''
      }
    }

    // 编辑评论
    const editComment = (comment) => {
      console.log('编辑评论:', comment)
      ElMessage.info('编辑评论功能开发中')
    }

    // 删除评论
    const deleteComment = (commentId) => {
      ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用API删除评论
        console.log('删除评论:', commentId)

        // 从列表中移除评论
        const index = myComments.value.findIndex(item => item.id === commentId)
        if (index !== -1) {
          myComments.value.splice(index, 1)
        }

        ElMessage.success('评论已删除')
      }).catch(() => {
        // 用户取消删除
      })
    }

    // 点赞/取消点赞
    const toggleLike = (comment) => {
      comment.isLiked = !comment.isLiked
      comment.likeCount += comment.isLiked ? 1 : -1

      // 这里应该调用API更新点赞状态
      console.log('点赞状态更新:', comment.id, comment.isLiked)
    }

    // 显示回复对话框
    const showReplyDialog = (comment) => {
      console.log('回复评论:', comment)
      ElMessage.info('回复功能开发中')
    }

    // 分享评论
    const shareComment = (comment) => {
      console.log('分享评论:', comment)
      ElMessage.info('分享功能开发中')
    }

    // 关注用户
    const followUser = (userId) => {
      // 这里应该调用API关注用户
      console.log('关注用户:', userId)

      // 更新UI
      const comment = hotComments.value.find(item => item.userId === userId)
      if (comment) {
        comment.isFollowing = true
      }

      ElMessage.success('关注成功')
    }

    // 取消关注用户
    const unfollowUser = (userId) => {
      // 这里应该调用API取消关注
      console.log('取消关注用户:', userId)

      // 更新UI
      const comment = hotComments.value.find(item => item.userId === userId)
      if (comment) {
        comment.isFollowing = false
      }

      ElMessage.success('已取消关注')
    }

    // 预览图片
    const previewImage = (url) => {
      console.log('预览图片:', url)
      ElMessage.info('图片预览功能开发中')
    }

    // 我的评论分页
    const handleMyCommentsPageChange = (page) => {
      myCommentsPage.value = page
      // 这里应该调用API获取新页面的数据
      console.log('我的评论翻页:', page)
    }

    // 热门评论分页
    const handleHotCommentsPageChange = (page) => {
      hotCommentsPage.value = page
      // 这里应该调用API获取新页面的数据
      console.log('热门评论翻页:', page)
    }

    onMounted(() => {
      // 这里可以初始化数据
    })

    return {
      reviewFilter,
      hotCommentsTab,
      showWriteReviewDialog,
      previewImageUrl,
      selectedMovie,
      newComment,
      myComments,
      hotComments,
      myCommentsPage,
      myCommentsPageSize,
      myCommentsTotal,
      hotCommentsPage,
      hotCommentsPageSize,
      hotCommentsTotal,
      formatTime,
      formatGenre,
      applyFilters,
      queryMovies,
      handleMovieSelect,
      submitComment,
      editComment,
      deleteComment,
      toggleLike,
      showReplyDialog,
      shareComment,
      followUser,
      unfollowUser,
      previewImage,
      handleMyCommentsPageChange,
      handleHotCommentsPageChange
    }
  }
}
</script>

<style scoped>
.reviews-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #ffffff;
  text-shadow: 0 0 10px rgba(100, 200, 255, 0.5);
}

.page-description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
}

.reviews-container {
  max-width: 1200px;
  margin: 0 auto;
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: rgba(20, 30, 48, 0.7);
  border-radius: 8px;
  border: 1px solid rgba(100, 200, 255, 0.2);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-label {
  color: rgba(255, 255, 255, 0.9);
  white-space: nowrap;
}

.section-card {
  margin-bottom: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-tabs {
  margin-left: 20px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  padding: 20px;
  background-color: rgba(20, 30, 48, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(100, 200, 255, 0.1);
}

.comment-user {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.user-info {
  display: flex;
  flex-direction: column;
  margin-left: 12px;
}

.username {
  font-weight: bold;
  color: #ffffff;
}

.user-level {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 2px;
}

.follow-btn {
  margin-left: auto;
  color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(100, 200, 255, 0.3);
}

.follow-btn.following {
  color: rgba(255, 255, 255, 0.5);
  border-color: rgba(255, 255, 255, 0.2);
}

.comment-movie {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.movie-poster {
  width: 60px;
  height: 90px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 15px;
}

.movie-info {
  flex: 1;
}

.movie-title {
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
  display: block;
  margin-bottom: 5px;
}

.movie-title:hover {
  color: #00ccff;
}

.movie-meta {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.movie-rating {
  margin-left: 15px;
  display: flex;
  align-items: center;
}

.comment-content {
  margin-bottom: 15px;
}

.comment-content p {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  margin: 0 0 10px;
}

.comment-images {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.comment-image {
  width: 100px;
  height: 100px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
}

.comment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.comment-image:hover img {
  transform: scale(1.05);
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.comment-actions {
  display: flex;
  gap: 15px;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.3s;
}

.action-item:hover {
  color: #00ccff;
}

.action-item.active {
  color: #ff4757;
}

.empty-state {
  padding: 40px 0;
  text-align: center;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 写评论对话框样式 */
.write-comment-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-label {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 8px;
  display: block;
}

.movie-suggestion {
  display: flex;
  align-items: center;
  padding: 8px 0;
}

.suggestion-poster {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 10px;
}

.suggestion-info {
  flex: 1;
}

.suggestion-title {
  font-weight: bold;
  color: #ffffff;
}

.suggestion-meta {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 2px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .filter-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .filter-group {
    width: 100%;
    justify-content: space-between;
  }

  .comment-movie {
    flex-direction: column;
  }

  .movie-poster {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .movie-rating {
    margin-left: 0;
    margin-top: 10px;
  }

  .comment-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
