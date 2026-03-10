<template>
  <div class="movie-analysis">
    <div class="header">
      <h1>影视数据分析平台</h1>
      <p>基于您收藏的影视数据进行多维度分析</p>
    </div>

    <div class="filters">
      <el-select v-model="selectedYear" placeholder="选择年份" @change="updateCharts">
        <el-option label="全部年份" value="all"></el-option>
        <el-option label="2024" value="2024"></el-option>
        <el-option label="2023" value="2023"></el-option>
        <el-option label="2022" value="2022"></el-option>
        <el-option label="2021" value="2021"></el-option>
        <el-option label="2020" value="2020"></el-option>
        <el-option label="2019" value="2019"></el-option>
        <el-option label="2018" value="2018"></el-option>
      </el-select>

      <el-select v-model="selectedRegion" placeholder="选择地区" @change="updateCharts">
        <el-option label="全部地区" value="all"></el-option>
        <el-option label="中国大陆" value="1"></el-option>
        <el-option label="美国" value="2"></el-option>
        <el-option label="韩国" value="3"></el-option>
        <el-option label="日本" value="4"></el-option>
        <el-option label="其他" value="5"></el-option>
      </el-select>
    </div>

    <div class="charts-container">
      <!-- 电影类型分布（饼图） -->
      <div class="chart-card">
        <h2>影视类型分布</h2>
        <div ref="genreChart" class="chart"></div>
      </div>

      <!-- 电影评分分布（柱状图） -->
      <div class="chart-card">
        <h2>影视评分分布</h2>
        <div ref="ratingChart" class="chart"></div>
      </div>

      <!-- 地区影视产量对比 -->
      <div class="chart-card">
        <h2>地区收藏分布</h2>
        <div ref="regionChart" class="chart"></div>
      </div>
    </div>

    <div class="data-table">
      <h2>收藏影视明细</h2>
      <el-table
        :data="filteredMovies"
        border
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="title" label="影视名称" width="200">
          <template #default="scope">
            <div class="table-title">
              <img
                :src="scope.row.poster"
                alt="海报"
                class="poster-img"
                v-if="scope.row.poster"
              />
              <span>{{ scope.row.title }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="genre" label="类型">
          <template #default="scope">
            {{ formatGenre(scope.row.genre) }}
          </template>
        </el-table-column>

        <el-table-column prop="year" label="年份" width="100"></el-table-column>

        <el-table-column prop="rating" label="评分" width="100">
          <template #default="scope">
            {{ scope.row.rating ? scope.row.rating.toFixed(1) : '暂无' }}
          </template>
        </el-table-column>

        <el-table-column prop="region" label="地区" width="120">
          <template #default="scope">
            {{ getRegionName(scope.row.region) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="goToDetail(scope.row.id)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch} from 'vue';
import * as echarts from 'echarts';
import { interactionApi, movieApi } from '@/api/api';
import { ElMessage } from "element-plus";
import { useRouter } from 'vue-router';
import { formatGenre } from '@/utils/genre.js';

// 路由
const router = useRouter();

// 筛选条件
const selectedYear = ref('all');
const selectedRegion = ref('all');
const loading = ref(false);

// 原始电影数据（从API获取）
const movies = ref([]);

// 地区映射
const regionCodeMap = {
  1: '中国大陆',
  2: '美国',
  3: '韩国',
  4: '日本',
  5: '其他'
};

// 过滤后的电影数据
const filteredMovies = computed(() => {
  return movies.value.filter(movie => {
    // 年份匹配
    const yearMatch = selectedYear.value === 'all' ||
      movie.year.toString() === selectedYear.value;

    // 地区匹配
    const regionMatch = selectedRegion.value === 'all' ||
      movie.region.toString() === selectedRegion.value;

    return yearMatch && regionMatch;
  });
});

// 图表实例引用
const genreChart = ref(null);
const ratingChart = ref(null);
const regionChart = ref(null);

// 图表实例
let genreChartInstance = null;
let ratingChartInstance = null;
let regionChartInstance = null;

// 获取用户收藏的影视数据
const fetchFavorites = async () => {
  loading.value = true;

  try {
    const response = await interactionApi.getFavorites();
    console.log('收藏接口返回:', response);

    // 防御性检查
    if (!response || typeof response !== 'object') {
      throw new Error('收藏接口返回数据格式错误');
    }

    // 如果 response.data 不存在，尝试使用 response 本身
    const favoriteData = response;

    if (!favoriteData || !Array.isArray(favoriteData) || favoriteData.length === 0) {
      ElMessage.info('您还没有收藏任何影视');
      movies.value = [];
      updateCharts();
      return;
    }

    // 获取收藏的影视ID列表
    const favoriteMovies = favoriteData;
    const movieIds = favoriteMovies.map(fav => fav.mid).filter(Boolean);
    console.log('收藏记录:', favoriteMovies);
    console.log('提取的 movieIds:', movieIds);

    if (movieIds.length === 0) {
      ElMessage.warning('收藏列表中没有有效的影视数据');
      movies.value = [];
      return;
    }

    // 批量获取影视详情
    const movieResponse = await movieApi.getMovieList({ ids: movieIds.join(',') });
    console.log('电影详情接口返回:', movieResponse);

    // 检查 movieResponse 是否包含 results
    if (!movieResponse || !movieResponse.results || !Array.isArray(movieResponse.results)) {
      throw new Error('电影详情接口返回数据格式错误');
    }

    console.log('电影详情数据:', movieResponse.results);

    // 创建一个 Set 来存储需要的 movieIds，用于快速查找
    const requiredIdsSet = new Set(movieIds);

    // 格式化数据，并且只保留 id 在 requiredIdsSet 中的电影
    const formattedMovies = movieResponse.results
      .filter(movie => requiredIdsSet.has(movie.id))
      .map(movie => ({
        id: movie.id,
        title: movie.title || movie.name,
        genre: movie.genre || movie.types,
        rating: movie.rating || movie.rate,
        year: movie.year || movie.release_year,
        region: movie.region,
        poster: movie.poster || movie.poster_url,
        director: movie.director,
        actors: movie.actors
      }));

    movies.value = formattedMovies;

    // 更新图表
    await nextTick();
    updateCharts();
  } catch (error) {
    console.error('获取收藏数据失败:', error);
    ElMessage.error('获取数据失败，请检查网络连接或稍后重试');
  } finally {
    loading.value = false;
  }
}




// 更新图表数据
const updateCharts = () => {
  if (filteredMovies.value.length === 0) {
    // 如果没有数据，清空图表
    if (genreChartInstance) genreChartInstance.clear();
    if (ratingChartInstance) ratingChartInstance.clear();
    if (regionChartInstance) regionChartInstance.clear();
    return;
  }

  // 初始化图表实例（如果尚未初始化）
  if (!genreChartInstance && genreChart.value) {
    genreChartInstance = echarts.init(genreChart.value);
  }
  if (!ratingChartInstance && ratingChart.value) {
    ratingChartInstance = echarts.init(ratingChart.value);
  }
  if (!regionChartInstance && regionChart.value) {
    regionChartInstance = echarts.init(regionChart.value);
  }

  // 更新各图表
  updateGenreChart();
  updateRatingChart();
  updateRegionChart();
};

// 更新类型分布饼图
const updateGenreChart = () => {
  const genreMap = {};

  filteredMovies.value.forEach(movie => {
    if (!movie.genre) return;

    // 拆分类型（如"剧情/爱情" → ["剧情", "爱情"]）
    const genres = movie.genre.split('/').map(item => item.trim()).filter(Boolean);

    genres.forEach(genre => {
      genreMap[genre] = (genreMap[genre] || 0) + 1;
    });
  });

  const chartData = Object.entries(genreMap).map(([name, value]) => ({ name, value }));

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'middle'
    },
    series: [
      {
        name: '影视类型',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{d}%'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true
        },
        data: chartData
      }
    ]
  };

  genreChartInstance.setOption(option, true);
};

// 更新评分分布柱状图
const updateRatingChart = () => {
  // 创建评分区间数组 [0-1, 1-2, ..., 9-10]
  const ratingRanges = Array(10).fill(0);

  filteredMovies.value.forEach(movie => {
    const rating = movie.rating;
    if (rating !== undefined && rating !== null && !isNaN(rating)) {
      // 将评分映射到区间索引
      const index = Math.min(Math.floor(rating), 9);
      if (index >= 0 && index < 10) {
        ratingRanges[index]++;
      }
    }
  });

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '影视数量',
        type: 'bar',
        data: ratingRanges,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#2378f7' },
              { offset: 0.7, color: '#2378f7' },
              { offset: 1, color: '#83bff6' }
            ])
          }
        }
      }
    ]
  };

  ratingChartInstance.setOption(option, true);
};

// 更新地区分布图
const updateRegionChart = () => {
  const regionMap = {};

  filteredMovies.value.forEach(movie => {
    const regionName = regionCodeMap[movie.region] || '未知地区';
    regionMap[regionName] = (regionMap[regionName] || 0) + 1;
  });

  const regions = Object.keys(regionMap);
  const values = Object.values(regionMap);

  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: '地区分布',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {c} ({d}%)'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true
        },
        data: regions.map((name, index) => ({
          value: values[index],
          name: name
        }))
      }
    ]
  };

  regionChartInstance.setOption(option, true);
};



// 获取地区名称
const getRegionName = (code) => {
  return regionCodeMap[code] || '未知地区';
};

// 跳转到影视详情页
const goToDetail = (id) => {
  router.push(`/movie/${id}`);
};

// 组件挂载时初始化
onMounted(async () => {
  await fetchFavorites();

  // 监听窗口大小变化，调整图表大小
  window.addEventListener('resize', () => {
    if (genreChartInstance) genreChartInstance.resize();
    if (ratingChartInstance) ratingChartInstance.resize();
    if (regionChartInstance) regionChartInstance.resize();
  });
});

// 监听筛选条件变化
watch([selectedYear, selectedRegion], () => {
  updateCharts();
});

</script>

<style scoped>
.movie-analysis {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  color: #1a237e;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.2rem;
  color: #666;
}

.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  justify-content: center;
}

.filters .el-select {
  width: 200px;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.chart-card h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.chart {
  width: 100%;
  height: 400px;
}

.data-table {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.data-table h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.poster-img {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }

  .filters {
    flex-direction: column;
    align-items: center;
  }

  .filters .el-select {
    width: 100%;
    max-width: 300px;
  }
}
</style>





<!--<template>-->
<!--  <div class="movie-analysis">-->
<!--    <div class="header">-->
<!--      <h1>电影数据分析平台</h1>-->
<!--      <p>多维度分析电影行业数据趋势</p>-->
<!--    </div>-->
<!--    -->
<!--    <div class="filters">-->
<!--      <el-select v-model="selectedYear" placeholder="选择年份" @change="updateCharts">-->
<!--        <el-option label="全部年份" value="all"></el-option>-->
<!--        <el-option label="2022" value="2022"></el-option>-->
<!--        <el-option label="2024" value="2024"></el-option>-->
<!--        <el-option label="2023" value="2023"></el-option>-->
<!--      </el-select>-->
<!--      -->
<!--      <el-select v-model="selectedRegion" placeholder="选择地区" @change="updateCharts">-->
<!--        <el-option label="全部地区" value="all"></el-option>-->
<!--        <el-option label="中国大陆" value="CN"></el-option>-->
<!--        <el-option label="美国" value="US"></el-option>-->
<!--        <el-option label="韩国" value="KR"></el-option>-->
<!--        <el-option label="日本" value="JP"></el-option>-->
<!--      </el-select>-->
<!--    </div>-->
<!--    -->
<!--    <div class="charts-container">-->
<!--      &lt;!&ndash; 电影类型分布（饼图） &ndash;&gt;-->
<!--      <div class="chart-card">-->
<!--        <h2>电影类型分布</h2>-->
<!--        <div ref="genreChart" class="chart"></div>-->
<!--      </div>-->
<!--      -->
<!--      &lt;!&ndash; 月度票房趋势（折线图） &ndash;&gt;-->
<!--      <div class="chart-card">-->
<!--        <h2>月度票房趋势</h2>-->
<!--        <div ref="boxOfficeChart" class="chart"></div>-->
<!--      </div>-->
<!--      -->
<!--      &lt;!&ndash; 电影评分分布（柱状图） &ndash;&gt;-->
<!--      <div class="chart-card">-->
<!--        <h2>电影评分分布</h2>-->
<!--        <div ref="ratingChart" class="chart"></div>-->
<!--      </div>-->
<!--      -->
<!--      &lt;!&ndash; 地区电影产量对比（雷达图） &ndash;&gt;-->
<!--      <div class="chart-card">-->
<!--        <h2>地区电影产量对比</h2>-->
<!--        <div ref="regionChart" class="chart"></div>-->
<!--      </div>-->
<!--    </div>-->
<!--    -->
<!--    <div class="data-table">-->
<!--      <h2>电影数据明细</h2>-->
<!--      <el-table :data="filteredMovies" border style="width: 100%">-->
<!--        <el-table-column prop="title" label="电影名称" width="200"></el-table-column>-->
<!--        <el-table-column prop="genre" label="类型"></el-table-column>-->
<!--        <el-table-column prop="releaseDate" label="上映日期"></el-table-column>-->
<!--        <el-table-column prop="rating" label="评分"></el-table-column>-->
<!--        <el-table-column prop="boxOffice" label="票房(亿)"></el-table-column>-->
<!--        <el-table-column prop="region" label="地区"></el-table-column>-->
<!--      </el-table>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted, computed } from 'vue';-->
<!--import * as echarts from 'echarts';-->

<!--// 筛选条件-->
<!--const selectedYear = ref('all');-->
<!--const selectedRegion = ref('all');-->

<!--// 原始电影数据（后续将从API获取）-->
<!--const movies = ref([]);-->

<!--// 过滤后的电影数据-->
<!--const filteredMovies = computed(() => {-->
<!--  return movies.value.filter(movie => {-->
<!--    const yearMatch = selectedYear.value === 'all' || -->
<!--      new Date(movie.releaseDate).getFullYear().toString() === selectedYear.value;-->
<!--    const regionMatch = selectedRegion.value === 'all' || movie.region === selectedRegion.value;-->
<!--    return yearMatch && regionMatch;-->
<!--  });-->
<!--});-->

<!--// 图表实例引用-->
<!--const genreChart = ref(null);-->
<!--const boxOfficeChart = ref(null);-->
<!--const ratingChart = ref(null);-->
<!--const regionChart = ref(null);-->

<!--// 图表实例-->
<!--let genreChartInstance = null;-->
<!--let boxOfficeChartInstance = null;-->
<!--let ratingChartInstance = null;-->
<!--let regionChartInstance = null;-->

<!--// 初始化图表-->
<!--const initCharts = () => {-->
<!--  // 电影类型分布饼图-->
<!--  genreChartInstance = echarts.init(genreChart.value);-->
<!--  -->
<!--  // 月度票房趋势折线图-->
<!--  boxOfficeChartInstance = echarts.init(boxOfficeChart.value);-->
<!--  -->
<!--  // 电影评分分布柱状图-->
<!--  ratingChartInstance = echarts.init(ratingChart.value);-->
<!--  -->
<!--  // 地区电影产量对比雷达图-->
<!--  regionChartInstance = echarts.init(regionChart.value);-->
<!--  -->
<!--  // 更新图表数据-->
<!--  updateCharts();-->
<!--};-->

<!--// 更新图表数据-->
<!--const updateCharts = () => {-->
<!--  // 准备图表数据-->
<!--  const genreData = getGenreData();-->
<!--  const boxOfficeData = getBoxOfficeData();-->
<!--  const ratingData = getRatingData();-->
<!--  const regionData = getRegionData();-->
<!--  -->
<!--  // 更新电影类型分布饼图-->
<!--  genreChartInstance.setOption({-->
<!--    tooltip: { trigger: 'item' },-->
<!--    legend: { orient: 'vertical', left: 'left' },-->
<!--    series: [-->
<!--      {-->
<!--        name: '电影类型',-->
<!--        type: 'pie',-->
<!--        radius: ['40%', '70%'],-->
<!--        avoidLabelOverlap: false,-->
<!--        itemStyle: {-->
<!--          borderRadius: 10,-->
<!--          borderColor: '#fff',-->
<!--          borderWidth: 2-->
<!--        },-->
<!--        label: { show: false, position: 'center' },-->
<!--        emphasis: {-->
<!--          label: { show: true, fontSize: 20, fontWeight: 'bold' }-->
<!--        },-->
<!--        labelLine: { show: false },-->
<!--        data: genreData-->
<!--      }-->
<!--    ]-->
<!--  });-->
<!--  -->
<!--  // 更新月度票房趋势折线图-->
<!--  boxOfficeChartInstance.setOption({-->
<!--    tooltip: { trigger: 'axis' },-->
<!--    legend: { data: ['票房(亿)'] },-->
<!--    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },-->
<!--    xAxis: {-->
<!--      type: 'category',-->
<!--      data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']-->
<!--    },-->
<!--    yAxis: { type: 'value' },-->
<!--    series: [-->
<!--      {-->
<!--        name: '票房(亿)',-->
<!--        type: 'line',-->
<!--        data: boxOfficeData,-->
<!--        smooth: true,-->
<!--        areaStyle: {}-->
<!--      }-->
<!--    ]-->
<!--  });-->
<!--  -->
<!--  // 更新电影评分分布柱状图-->
<!--  ratingChartInstance.setOption({-->
<!--    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },-->
<!--    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },-->
<!--    xAxis: {-->
<!--      type: 'category',-->
<!--      data: ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']-->
<!--    },-->
<!--    yAxis: { type: 'value' },-->
<!--    series: [-->
<!--      {-->
<!--        name: '电影数量',-->
<!--        type: 'bar',-->
<!--        data: ratingData,-->
<!--        itemStyle: {-->
<!--          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [-->
<!--            { offset: 0, color: '#5470C6' },-->
<!--            { offset: 1, color: '#EE6666' }-->
<!--          ])-->
<!--        }-->
<!--      }-->
<!--    ]-->
<!--  });-->
<!--  -->
<!--  // 更新影视类型对比雷达图-->
<!--  regionChartInstance.setOption({-->
<!--    tooltip: { trigger: 'item' },-->
<!--    radar: {-->
<!--      indicator: [-->
<!--        { name: '剧情', max: 10 },-->
<!--        { name: '科幻', max: 10 },-->
<!--        { name: '动作', max: 10 },-->
<!--        { name: '动画', max: 10 },-->
<!--        { name: '悬疑', max: 10 },-->
<!--        { name: '战争', max: 10 }-->
<!--      ]-->
<!--    },-->
<!--    series: [-->
<!--      {-->
<!--        name: '中国大陆',-->
<!--        type: 'radar',-->
<!--        data: regionData.CN-->
<!--      },-->
<!--      {-->
<!--        name: '美国',-->
<!--        type: 'radar',-->
<!--        data: regionData.US-->
<!--      },-->
<!--      {-->
<!--        name: '韩国',-->
<!--        type: 'radar',-->
<!--        data: regionData.KR-->
<!--      },-->
<!--      {-->
<!--        name: '日本',-->
<!--        type: 'radar',-->
<!--        data: regionData.JP-->
<!--      }-->
<!--    ]-->
<!--  });-->
<!--};-->

<!--// 获取电影类型分布数据-->
<!--const getGenreData = () => {-->
<!--  const genreMap = {};-->
<!--  filteredMovies.value.forEach(movie => {-->
<!--    if (genreMap[movie.genre]) {-->
<!--      genreMap[movie.genre]++;-->
<!--    } else {-->
<!--      genreMap[movie.genre] = 1;-->
<!--    }-->
<!--  });-->
<!--  -->
<!--  return Object.entries(genreMap).map(([name, value]) => ({ name, value }));-->
<!--};-->

<!--// 获取月度票房数据-->
<!--const getBoxOfficeData = () => {-->
<!--  const monthData = new Array(12).fill(0);-->
<!--  filteredMovies.value.forEach(movie => {-->
<!--    const month = new Date(movie.releaseDate).getMonth();-->
<!--    monthData[month] += movie.boxOffice;-->
<!--  });-->
<!--  return monthData;-->
<!--};-->

<!--// 获取评分分布数据-->
<!--const getRatingData = () => {-->
<!--  const ratingData = new Array(10).fill(0);-->
<!--  filteredMovies.value.forEach(movie => {-->
<!--    const rating = Math.floor(movie.rating);-->
<!--    ratingData[rating]++;-->
<!--  });-->
<!--  return ratingData;-->
<!--};-->

<!--// 获取地区电影产量数据-->
<!--const getRegionData = () => {-->
<!--  const regions = { CN: {}, US: {}, KR: {}, JP: {} };-->
<!--  const genres = ['剧情', '科幻', '动作', '动画', '悬疑', '战争'];-->
<!--  -->
<!--  // 初始化数据-->
<!--  Object.keys(regions).forEach(region => {-->
<!--    genres.forEach(genre => {-->
<!--      regions[region][genre] = 0;-->
<!--    });-->
<!--  });-->
<!--  -->
<!--  // 统计数据-->
<!--  filteredMovies.value.forEach(movie => {-->
<!--    if (regions[movie.region] && regions[movie.region][movie.genre] !== undefined) {-->
<!--      regions[movie.region][movie.genre]++;-->
<!--    }-->
<!--  });-->
<!--  -->
<!--  // 格式化数据-->
<!--  return {-->
<!--    CN: genres.map(genre => regions.CN[genre]),-->
<!--    US: genres.map(genre => regions.US[genre]),-->
<!--    KR: genres.map(genre => regions.KR[genre]),-->
<!--    JP: genres.map(genre => regions.JP[genre])-->
<!--  };-->
<!--};-->

<!--// 组件挂载时初始化图表-->
<!--onMounted(() => {-->
<!--  initCharts();-->
<!--  -->
<!--  // 监听窗口大小变化，调整图表大小-->
<!--  window.addEventListener('resize', () => {-->
<!--    genreChartInstance.resize();-->
<!--    boxOfficeChartInstance.resize();-->
<!--    ratingChartInstance.resize();-->
<!--    regionChartInstance.resize();-->
<!--  });-->
<!--});-->
<!--</script>-->

<!--<style scoped>-->
<!--.movie-analysis {-->
<!--  padding: 20px;-->
<!--  background-color: #f5f7fa;-->
<!--  min-height: 100vh;-->
<!--}-->

<!--.header {-->
<!--  text-align: center;-->
<!--  margin-bottom: 30px;-->
<!--}-->

<!--.header h1 {-->
<!--  font-size: 2.5rem;-->
<!--  color: #1a237e;-->
<!--  margin-bottom: 10px;-->
<!--}-->

<!--.header p {-->
<!--  font-size: 1.2rem;-->
<!--  color: #666;-->
<!--}-->

<!--.filters {-->
<!--  display: flex;-->
<!--  gap: 20px;-->
<!--  margin-bottom: 30px;-->
<!--  justify-content: center;-->
<!--}-->

<!--.filters .el-select {-->
<!--  width: 200px;-->
<!--}-->

<!--.charts-container {-->
<!--  display: grid;-->
<!--  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));-->
<!--  gap: 20px;-->
<!--  margin-bottom: 30px;-->
<!--}-->

<!--.chart-card {-->
<!--  background-color: #fff;-->
<!--  border-radius: 10px;-->
<!--  padding: 20px;-->
<!--  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);-->
<!--}-->

<!--.chart-card h2 {-->
<!--  font-size: 1.5rem;-->
<!--  margin-bottom: 15px;-->
<!--  color: #333;-->
<!--  text-align: center;-->
<!--}-->

<!--.chart {-->
<!--  width: 100%;-->
<!--  height: 400px;-->
<!--}-->

<!--.data-table {-->
<!--  background-color: #fff;-->
<!--  border-radius: 10px;-->
<!--  padding: 20px;-->
<!--  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);-->
<!--}-->

<!--.data-table h2 {-->
<!--  font-size: 1.5rem;-->
<!--  margin-bottom: 15px;-->
<!--  color: #333;-->
<!--  text-align: center;-->
<!--}-->

<!--.el-table {-->
<!--  &#45;&#45;el-table-header-text-color: #333;-->
<!--  &#45;&#45;el-table-row-hover-bg-color: #f0f7ff;-->
<!--}-->
<!--</style>-->