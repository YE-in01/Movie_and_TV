<template>
  <!-- 根容器，用于包裹整个分类页面 -->
  <div class="category-page">
    <div class="container">
      <!-- 页面头部区域：包含标题、Top250快捷入口和筛选器 -->
      <div class="category-header">
        <!-- 动态显示当前分类的标题，如“电影”、“电视剧”等 -->
        <h1>{{ categoryTitle }}</h1>
        <!-- 
          Top250快捷入口：
          - 使用 v-if 条件渲染，仅当分类类型为 'movie' (电影) 时显示
          - router-link 用于导航到电影分类页面，并附带 ?sort=top250 查询参数
          - @click 事件绑定，点击时触发 handleTop250Click 方法
        -->







        <!-- 筛选器折叠/展开按钮 -->
        <div class="filters-toggle" @click="toggleFilters">
          <span class="toggle-text">{{ isFiltersOpen ? '收起筛选' : '展开筛选' }}</span>
          <span class="toggle-icon">{{ isFiltersOpen ? '▼' : '▶' }}</span>
        </div>

        <!-- 筛选器容器 -->
        <div class="category-filters" v-show="isFiltersOpen">
          <!-- 地区筛选器组 -->
          <div class="filter-group">
            <span class="filter-label">地区：</span>
            <!-- 
              el-radio-group 是 Element Plus 的单选框组组件
              - v-model 双向绑定到 filters.region，用于存储用户选择的地区
              - @change 事件，当选择变化时触发 applyFilters 方法，应用筛选
            -->
            <el-radio-group v-model="filters.region" @change="applyFilters">
              <el-radio-button label="">全部</el-radio-button>
              <el-radio-button label="中国">中国</el-radio-button>
              <el-radio-button label="美国">美国</el-radio-button>
              <el-radio-button label="韩国">韩国</el-radio-button>
              <el-radio-button label="日本">日本</el-radio-button>
              <el-radio-button label="其他">其他</el-radio-button>
            </el-radio-group>
          </div>

          <!-- 类型筛选器组 -->
          <div class="filter-group">
            <span class="filter-label">类型：</span>
            <!-- 
              el-checkbox-group 是 Element Plus 的复选框组组件
              - v-model 双向绑定到 filters.genres (一个数组)，存储用户选择的多个类型
              - @change 事件，当选择变化时触发 applyFilters 方法
            -->
            <el-checkbox-group v-model="filters.genres" @change="applyFilters">
              <!-- 类型选项将根据categoryType动态生成 -->
              <el-checkbox v-for="genre in availableGenres" :key="genre" :label="genre">{{ genre }}</el-checkbox>
            </el-checkbox-group>
          </div>

          <!-- 年份筛选器组 -->
          <div class="filter-group">
            <span class="filter-label">年份：</span>
            <!-- 
              el-select 是 Element Plus 的下拉选择框组件
              - v-model 双向绑定到 filters.year，存储用户选择的年份
              - @change 事件，当选择变化时触发 applyFilters 方法
            -->
            <el-select v-model="filters.year" placeholder="选择年份" @change="applyFilters">
              <el-option label="全部" value=""></el-option>
              <el-option label="2022" value="2022"></el-option>
              <el-option label="2021" value="2021"></el-option>
              <el-option label="2020" value="2020"></el-option>
              <el-option label="更早" value="earlier"></el-option>
            </el-select>
          </div>

          <!-- 排序方式筛选器组 -->
          <div class="filter-group">
            <span class="filter-label">排序：</span>
            <!-- 
              el-select 下拉选择框，用于选择排序方式
              - v-model 双向绑定到 filters.sort
              - @change 事件，触发 applyFilters 方法
            -->
            <el-select v-model="filters.sort" placeholder="选择排序方式" @change="applyFilters">
              <el-option label="最新上映" value="year_desc"></el-option>
              <el-option label="评分最高" value="rating_desc"></el-option>
              <el-option label="猜你喜欢" value="recommend"></el-option>
            </el-select>
          </div>
        </div>
      </div>

      <!-- 页面主要内容区域：用于展示影视列表或无结果提示 -->
      <div class="category-content">
        <!-- 
          影视列表：
          - 使用 v-if 条件渲染，仅当 categoryMovies 数组有数据时显示
          - v-for 指令循环遍历 categoryMovies 数组，为每个电影/电视剧生成一个 .movie-item 元素
          - :key 为每个列表项提供唯一标识 (这里使用 movie.id)，这是 Vue 高效更新 DOM 的关键
        -->
        <div class="movie-list" v-if="categoryMovies.length > 0">
          <div class="movie-item" v-for="movie in categoryMovies" :key="movie.id">
            <!-- 路由链接，点击后跳转到具体影视的详情页 -->
            <router-link :to="'/movie/' + movie.id">
              <div class="movie-poster">
                <!-- 绑定电影海报图片的 src 和 alt 属性 -->
                <img :src="movie.poster" :alt="movie.title">
                <div class="movie-rating">
                  <!-- 
                    el-rate 是 Element Plus 的评分组件
                    - v-model 绑定电影的 rating 值
                    - disabled 属性设置为 true，表示评分不可交互，仅用于展示
                  -->
                  <el-rate :model-value="movie.rating / 2" disabled text-color="#ff9900" :max="5" :precision="0.5"></el-rate>
                </div>
                <!-- 显示电影上映年份 -->
                <div class="movie-year">{{ movie.year }}</div>
              </div>
              <!-- 显示电影标题 -->
              <h3 class="movie-title">{{ movie.title }}</h3>
              <!-- 显示电影类型和地区信息 -->
              <p class="movie-info">{{ formatGenre(movie.genre) }} · {{ movie.region }}</p>
            </router-link>
          </div>
        </div>

        <!-- 
          无结果提示：
          - 使用 v-else 条件渲染，当 categoryMovies 数组为空时显示
          - el-empty 是 Element Plus 的空状态组件，用于友好地提示用户没有找到匹配内容
          - 提供一个“重置筛选条件”的按钮，点击后触发 resetFilters 方法
        -->
        <div class="no-results" v-else>
          <el-empty description="没有找到相关内容">
            <el-button type="primary" @click="resetFilters">重置筛选条件</el-button>
          </el-empty>
        </div>

        <!-- 
          分页组件：
          - 使用 v-if 条件渲染，仅当有影视数据时显示
          - el-pagination 是 Element Plus 的分页组件
          - :total 总数据条数
          - :page-size 每页显示的条数
          - :current-page 当前页码
          - @current-change 事件，当用户切换页码时触发 handlePageChange 方法
        -->
        <div class="pagination" v-if="categoryMovies.length > 0">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="totalResults"
            :page-size="pageSize"
            :current-page="currentPage"
            @current-change="handlePageChange"
          >
          </el-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 1. 从 Vue 中导入所需的组合式 API
// ref: 用于创建基本类型的响应式数据
// reactive: 用于创建对象类型的响应式数据
// computed: 用于创建计算属性
// onMounted: 生命周期钩子，在组件挂载后执行
// watch: 用于监听数据变化
import { ref, reactive, computed, onMounted, watch, onActivated, onDeactivated } from 'vue'
// 2. 从 Vue Router 中导入 useRoute，用于获取当前路由信息
import { useRoute } from 'vue-router'
// 3. 导入Element Plus组件
// 导入电影相关API
import { movieApi } from '../api/api.js'
// 导入类型工具函数
import { formatGenre } from '@/utils/genre.js'

export default {
  name: 'CategoryView', // 3. 定义组件名称
  // 4. 组合式 API 的入口函数 setup
  setup() {
    // 5. 获取当前路由实例，用于访问路由参数等信息
    const route = useRoute()
  // 6. 使用 ref 创建响应式数据（主要用于基本类型）
    const categoryType = ref('') // 存储当前分类类型 (如 'movie', 'tv')
    const categoryMovies = ref([]) // 存储当前分类下要展示的影视列表
    const totalResults = ref(0) // 存储符合筛选条件的总结果数，用于分页
    const pageSize = ref(20) // 存储每页显示的数量
    const currentPage = ref(1) // 存储当前页码
    const isFiltersOpen = ref(false) // 筛选框是否展开

    // 7. 使用 reactive 创建响应式数据（主要用于对象）
    // 这个对象用于存储用户选择的所有筛选条件
    const filters = reactive({
      region: '', // 地区筛选
      genres: [], // 类型筛选 (数组，支持多选)
      year: '', // 年份筛选
      sort: 'year_desc' // 排序方式，默认使用最新上映
})

    // 8. 类型分类配置，根据不同的影视类型显示不同的类型选项
    const genreConfig = {
      movie: ['剧情', '喜剧', '爱情', '动作', '科幻', '犯罪', '悬疑', '奇幻', '冒险', '历史', '战争', '动画'],
      tv: ['剧情', '爱情', '悬疑', '犯罪', '喜剧', '古装', '奇幻', '动作', '科幻', '武侠'],
      variety: ['悬疑', '家庭', '爱情']
    }

    // 9. 计算属性：根据当前分类类型返回可用的类型选项
    const availableGenres = computed(() => {
      return genreConfig[categoryType.value] || genreConfig.movie
    })

    // 10. 切换筛选框的折叠/展开状态
    const toggleFilters = () => {
      isFiltersOpen.value = !isFiltersOpen.value
    }

    // 8. 使用 computed 创建计算属性
    // 根据 categoryType 的值动态计算并返回分类标题
    const categoryTitle = computed(() => {
      // 定义一个类型到标题的映射对象
      const typeMap = {
        'movie': '电影',
        'tv': '电视剧',
        'variety': '综艺'
      }
      // 如果 typeMap 中存在对应的 key，则返回对应的值，否则返回默认值 '影视'
      return typeMap[categoryType.value] || '影视'
    })
    
    // 辅助函数：将前端类型转换为后端category_id
    const getCategoryIdByType = (type) => {
      const typeMap = {
        'movie': 1,
        'tv': 2,
        'variety': 3
      }
      return typeMap[type] || 1
    }
    
    // 辅助函数：将前端排序转换为后端排序参数
    const getOrderingBySort = (sort) => {
      const sortMap = {
        'rating_desc': '-rate',
        'year_desc': '-release_year',
        'year_asc': 'release_year'
      }
      return sortMap[sort] || '-release_year'
    }

    // 9. 定义核心函数：从后端获取和处理分类数据
    const fetchCategoryMovies = async () => {
      try {
        // 构建请求参数，确保与后端视图参数匹配
        const params = {
          category_id: getCategoryIdByType(categoryType.value),
          region: filters.region || undefined,
          year: filters.year || undefined,
          page: currentPage.value,
          page_size: pageSize.value
        }
        
        // 处理排序参数
        if (filters.sort) {
          params.sort = getOrderingBySort(filters.sort)
        }
        
        // 如果有类型筛选，添加到参数
        if (filters.genres.length > 0) {
          params.types = filters.genres.join(',')
        }

        // 添加调试信息
        console.log('请求参数:', params)
        // 调用后端API获取分类电影数据
        const response = await movieApi.getMovieList(params)
        
        // 处理后端返回的数据格式
        console.log('API响应数据:', response)
        const responseData = response || {}
        
        // 处理不同的响应格式
        let movies = []
        if (Array.isArray(responseData)) {
          movies = responseData
          totalResults.value = responseData.length
        } else if (responseData.results) {
          // Django REST Framework 标准分页格式
          movies = responseData.results
          totalResults.value = responseData.count
        } else if (responseData.list) {
          // 可能的自定义分页格式
          movies = responseData.list
          totalResults.value = responseData.total
        } else {
          // 默认处理
          movies = []
          totalResults.value = 0
        }
        
        // 如果是随机排序或猜你喜欢，在前端对电影列表进行随机打乱
        if (filters.sort === 'random' || filters.sort === 'recommend') {
          // 使用Fisher-Yates算法打乱数组
          // 先复制原始数组，确保打乱操作不会影响原始数据
          const shuffledMovies = [...movies]
          for (let i = shuffledMovies.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1))
            ;[shuffledMovies[i], shuffledMovies[j]] = [shuffledMovies[j], shuffledMovies[i]]
          }
          movies = shuffledMovies
        }
        
        // 如果是最新上映排序，在前端再进行一次排序确保正确
        if (filters.sort === 'year_desc') {
          movies.sort((a, b) => {
            // 确保年份是数字类型进行比较
            const yearA = Number(a.year || 0)
            const yearB = Number(b.year || 0)
            // 降序排列（最新的排在前面）
            return yearB - yearA
          })
        }
        // 设置最终的电影列表
        categoryMovies.value = movies
        
        console.log('处理后的电影数据:', categoryMovies.value)
      } catch (error) {
        console.error('获取分类电影数据失败:', error)
        // 重置数据，避免页面显示错误
        categoryMovies.value = []
        totalResults.value = 0
      }
    }

    // 应用过滤器
    const applyFilters = () => {
      currentPage.value = 1
      fetchCategoryMovies()
    }

    // 处理分页
    const handlePageChange = (page) => {
      // 重置页码为第1页（筛选后从第一页开始显示）
      currentPage.value = page
      // 重新获取并渲染电影列表
      fetchCategoryMovies()
    }

    // 重置过滤器 并重新获取并渲染电影列表
    const resetFilters = () => {
      // 清空所有筛选条件：地区、类型、年份
      filters.region = ''
      filters.genres = []
      filters.year = ''
      // 重置排序方式为默认的"最新上映"
      filters.sort = 'year_desc'
      // 重置页码为第1页（筛选后从第一页开始显示）
      currentPage.value = 1
      // 重新获取并渲染电影列表
      fetchCategoryMovies()
    }

    // 监听路由变化
    watch(() => route.params.type, (newType) => {
      // 更新当前分类类型
      if (newType) {
        categoryType.value = newType
        // 重置筛选条件
        resetFilters()
      }
    })
// 组件挂载时执行
    onMounted(() => {
      //从路由参数中获取分类类型，若没有则默认取'movie'
      categoryType.value = route.params.type || 'movie'
      
      // 初始加载时获取并渲染电影列表
      fetchCategoryMovies()
    })

    // 组件从缓存中激活时执行
    onActivated(() => {
      // 当组件被激活时（从缓存中恢复），重新获取数据
      fetchCategoryMovies()
    })

    // 组件被缓存前执行
    onDeactivated(() => {
      // 组件被缓存前的清理工作（如果需要）
    })

    return {
      categoryType, // 当前分类类型
      categoryMovies, // 当前分类下的电影列表（分页后）
      totalResults, // 总结果数
      pageSize, // 每页显示数量
      currentPage, // 当前页码
      filters, // 筛选条件（地区、类型、年份、排序）
      categoryTitle, // 分类标题
      applyFilters, // 应用筛选方法
      handlePageChange, // 分页变化处理方法
      resetFilters, // 重置筛选方法

      isFiltersOpen, // 筛选框是否展开
      availableGenres, // 可用的类型选项
      toggleFilters, // 切换筛选框折叠/展开状态的方法
      formatGenre // 类型格式化函数
    }
  }
}
</script>

<style scoped>
/* 1. 页面整体布局与容器
   ========================================================================== */

/*
  .category-page: 这是整个页面的根容器类。
  - padding: 20px 0;      在顶部和底部添加 20px 的内边距，增加页面呼吸感。
  - min-height: calc(100vh - 70px);  这是一个关键的布局技巧：
    * 100vh 代表整个视口（浏览器窗口）的高度。
    * 减去 70px 通常是为了给页面顶部的固定导航栏留出空间（假设导航栏高度为 70px）。
    * 确保即使页面内容很少时，页脚也能保持在视窗底部，形成一个完整的页面结构。
*/
.category-page {
  padding: 20px 0;
  min-height: calc(100vh - 70px);
}

/*
  .container: 这是一个通用的容器类，用于包裹页面内容。
  - max-width: 1200px;    限制内容的最大宽度，防止在超宽屏幕上内容被拉得太开，影响阅读体验。
  - margin: 0 auto;       左右外边距自动，使容器在页面中水平居中。
  - padding: 0 20px;      在小屏幕上，左右保留 20px 的内边距，避免内容紧贴屏幕边缘。
*/
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 2. 页面头部区域
   ========================================================================== */

/*
  .category-header: 包裹页面标题的容器。
  - margin-bottom: 30px;  与下方的内容区域保持 30px 的距离。
*/
.category-header {
  margin-bottom: 30px;
}

/*
  .category-header h1: 页面的主标题（例如“电影”、“电视剧”）。
  - font-size: 28px;      设置较大的字体，突出标题层级。
  - color: #303133;       使用白色。
  - margin-bottom: 10px;  与下方可能存在的副标题或内容保持距离。
*/
.category-header h1 {
  font-size: 28px;
  color: #eeeff1;
  margin-bottom: 10px;
}


/* 3. 筛选器折叠/展开按钮
   ========================================================================== */

/*
  .filters-toggle: 筛选器折叠/展开按钮的样式。
  - display: flex; 使用flex布局，方便内部元素对齐。
  - align-items: center; 垂直居中对齐内部元素。
  - justify-content: center; 水平居中对齐内部元素。
  - background-color: #f0f0f0; 浅灰色背景，与白色筛选器形成对比。
  - color: #606266; 灰色文字。
  - padding: 8px 16px; 设置内边距，让按钮大小适中。
  - border-radius: 4px; 小圆角，营造现代、友好的视觉效果。
  - cursor: pointer; 鼠标悬停时显示指针，表明可点击。
  - margin-bottom: 10px; 与下方的筛选区保持距离。
  - transition: all 0.3s; 为所有可过渡的属性设置0.3秒的过渡效果，让交互更平滑。
*/
.filters-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  color: #606266;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
  transition: all 0.3s;
}

/*
  .filters-toggle:hover: 鼠标悬停在按钮上时的状态。
  - background-color: #e0e0e0; 背景色加深，提供反馈。
  - color: #303133; 文字颜色加深。
*/
.filters-toggle:hover {
  background-color: #e0e0e0;
  color: #303133;
}

/*
  .toggle-text: 按钮内的文字。
  - margin-right: 5px; 与右侧的图标保持距离。
*/
.toggle-text {
  margin-right: 5px;
}

/*
  .toggle-icon: 按钮内的箭头图标。
  - font-size: 12px; 图标大小适中。
  - transition: transform 0.3s; 为图标旋转设置过渡效果。
*/
.toggle-icon {
  font-size: 12px;
  transition: transform 0.3s;
}

/* 3. Top250 快捷链接
   ========================================================================== */



/* 4. 筛选器区域
   ========================================================================== */

/*
  .category-filters: 包裹所有筛选条件（地区、类型、年份等）的容器。
  - background-color: #fff;  白色背景，与页面背景区分开。
  - padding: 20px;           内边距，让内部元素不拥挤。
  - border-radius: 8px;      圆角设计，现代美观。
  - box-shadow: ...;         一个淡淡的灰色阴影，使其在页面上“浮”起来，增强层次感。
*/
.category-filters {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/*
  .filter-group: 每个独立的筛选条件组（如“地区”、“类型”）的容器。
  - margin-bottom: 15px;    筛选组之间保持 15px 的距离。
  - display: flex;          使用 flex 布局，让标签和选项并排显示。
  - align-items: flex-start;  让标签和选项组在顶部对齐，这在选项组是多行时很重要。
*/
.filter-group {
  margin-bottom: 15px;
  display: flex;
  align-items: flex-start;
}

/*
  .filter-group:last-child: 选择最后一个 .filter-group 元素。
  - margin-bottom: 0;       移除最后一个筛选组的下边距，避免多余的空白。
*/
.filter-group:last-child {
  margin-bottom: 0;
}

/*
  .filter-label: 筛选条件的标签（如“地区：”、“类型：”）。
  - margin-right: 10px;    与右侧的选项保持距离。
  - color: #606266;        灰色文字，作为辅助信息，不抢风头。
  - font-weight: 500;      字体稍粗，明确其为标签。
  - white-space: nowrap;   防止标签文字换行。
  - min-width: 60px;       保证所有标签有一个最小宽度，使布局更整齐。
*/
.filter-label {
  margin-right: 10px;
  color: #606266;
  font-weight: 500;
  white-space: nowrap;
  min-width: 60px;
}

/* 5. 电影列表与电影项
   ========================================================================== */

/*
  .movie-list: 电影列表的容器。
  - display: grid;         使用 CSS Grid 布局，这是创建网格布局的最佳方式。
  - grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));  这是 Grid 的核心：
    * auto-fill: 自动填充列，直到容器空间用完。
    * minmax(200px, 1fr): 每列的宽度至少为 200px，最多为 1fr（可用空间的一份）。
    * 这意味着在大屏幕上会显示多列，小屏幕上会自动减少列数，实现了响应式布局。
  - gap: 20px;             网格单元（电影项）之间的间距。
  - margin-bottom: 30px;   与下方的分页控件保持距离。
*/
.movie-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

/*
  .movie-item: 单个电影卡片的容器。
  - background-color: #fff;  白色背景。
  - border-radius: 8px;      圆角。
  - overflow: hidden;        确保卡片内部的元素（如海报图片）不会超出圆角边界。
  - box-shadow: ...;         淡淡的阴影，增强立体感。
  - transition: ...;         为 transform 和 box-shadow 设置过渡效果。
*/
.movie-item {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

/*
  .movie-item:hover: 鼠标悬停在电影卡片上时的效果。
  - transform: translateY(-5px);  卡片向上移动 5px。
  - box-shadow: ...;              阴影加深、扩大，模拟卡片浮起的效果，增强交互体验。
*/
.movie-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/*
  .movie-item a: 包裹整个电影卡片的链接。
  - display: block;        将链接显示为块级元素，使其能包裹整个卡片。
  - text-decoration: none; 移除链接的下划线。
  - color: #333;           链接文字颜色为深灰色。
*/
.movie-item a {
  display: block;
  text-decoration: none;
  color: #333;
}

/*
  .movie-poster: 电影海报的容器。
  - position: relative;     设置为相对定位，为内部的绝对定位元素（评分、年份）提供参照。
  - height: 280px;         固定海报区域的高度，保证所有卡片高度一致。
  - overflow: hidden;       确保海报图片不会超出容器。
*/
.movie-poster {
  position: relative;
  height: 300px;
  overflow: hidden;
}

/*
  .movie-poster img: 海报图片。
  - width: 100%;           宽度占满容器。
  - height: 100%;          高度占满容器。
  - object-fit: cover;     这是处理图片的关键属性：
    * 使图片完全覆盖容器，同时保持其宽高比。
    * 如果图片和容器的宽高比不一致，图片会被裁剪以适应。
  - transition: transform 0.3s; 为图片的缩放设置过渡效果。
*/
.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

/*
  .movie-item:hover .movie-poster img: 鼠标悬停时，海报图片放大。
  - transform: scale(1.05);  图片放大 5%，创造一种“聚焦”的视觉效果，非常流行。
*/
.movie-item:hover .movie-poster img {
  transform: scale(1.05);
}

/*
  .movie-rating: 电影评分。
  - position: absolute;     绝对定位。
  - bottom: 10px; left: 10px; 在海报左下角定位。
  - background-color: rgba(0, 0, 0, 0.7);  半透明的黑色背景。
  - padding: 5px 8px;       内边距。
  - border-radius: 4px;     小圆角。
  (注意：这里缺少了 color 属性，通常评分会是黄色或白色)
*/
.movie-rating {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  padding: 5px 8px;
  border-radius: 4px;
}

/*
  .movie-year: 电影年份。
  - position: absolute;     绝对定位。
  - top: 10px; right: 10px; 在海报右上角定位。
  - background-color: rgba(0, 0, 0, 0.7);  半透明黑色背景。
  - color: #fff;            白色文字。
  - padding: 3px 8px;       内边距。
  - border-radius: 4px;     小圆角。
  - font-size: 14px;        字体稍小。
*/
.movie-year {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 14px;
}

/*
  .movie-title: 电影标题。
  - padding: 10px 10px 5px;  内边距，上右下左。
  - font-size: 16px;         字体大小。
  - font-weight: 500;        字体稍粗。
  - margin: 0;               清除默认外边距。
  - overflow: hidden;        超出容器宽度的部分隐藏。
  - text-overflow: ellipsis; 用省略号 (...) 表示被隐藏的文本。
  - white-space: nowrap;     不允许文字换行。
  这三个属性组合起来，实现了单行文本过长时的优雅截断。
*/
.movie-title {
  padding: 10px 10px 5px;
  font-size: 16px;
  font-weight: 500;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/*
  .movie-info: 电影附加信息（如导演、演员）。
  - padding: 0 10px 10px;   内边距。
  - color: #909399;         浅灰色文字，作为次要信息。
  - font-size: 14px;        字体稍小。
  - margin: 0;              清除默认外边距。
  - overflow: hidden;        同样实现单行文本截断。
  - text-overflow: ellipsis;
  - white-space: nowrap;
*/
.movie-info {
  padding: 0 10px 10px;
  color: #909399;
  font-size: 14px;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 6. 分页和无结果提示
   ========================================================================== */

/*
  .pagination: 分页控件的容器。
  - display: flex;          使用 flex 布局。
  - justify-content: center; 让分页控件在页面中水平居中。
  - margin-top: 20px;       与电影列表保持距离。
*/
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/*
  .no-results: 当筛选结果为空时显示的提示信息容器。
  - margin-top: 50px;       留出足够的上边距，使其在页面中居中显示。
  (通常这个类内部还会有文字样式和图标)
*/
.no-results {
  margin-top: 50px;
}

/* 7. 响应式设计
   ========================================================================== */

/*
  @media (max-width: 768px): 这是一个媒体查询，当浏览器窗口宽度小于或等于 768px 时（通常是平板或手机），
  以下的 CSS 规则将生效。
*/
@media (max-width: 768px) {

  /*
    在小屏幕上，筛选组改为垂直排列。
    - flex-direction: column;  子元素（标签和选项）垂直排列。
    - align-items: flex-start;  所有子元素靠左对齐。
  */
  .filter-group {
    flex-direction: column;
    align-items: flex-start;
  }

  /*
    标签在垂直排列时，需要有一个下边距。
  */
  .filter-label {
    margin-bottom: 5px;
  }

  /*
    在小屏幕上，电影卡片的最小宽度减小，以便显示更多列。
  */
  .movie-list {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>
