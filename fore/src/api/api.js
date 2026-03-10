import request from './axios'

// 简单的内存缓存实现
const cache = {
  // 缓存数据存储
  data: {},
  // 设置缓存，默认有效期5分钟
  set(key, value, ttl = 300000) {
    this.data[key] = {
      value,
      expires: Date.now() + ttl
    }
  },
  // 获取缓存，如果过期则返回null
  get(key) {
    const item = this.data[key]
    if (!item) return null
    if (Date.now() > item.expires) {
      delete this.data[key]
      return null
    }
    return item.value
  },
  // 删除缓存
  delete(key) {
    delete this.data[key]
  },
  // 清空缓存
  clear() {
    this.data = {}
  }
}

// 通用的缓存包装函数
const withCache = (fn, cacheKeyGen, ttl = 300000) => {
  return async (...args) => {
    const cacheKey = typeof cacheKeyGen === 'function' ? cacheKeyGen(...args) : cacheKeyGen
    const cachedData = cache.get(cacheKey)
    if (cachedData) {
      return cachedData
    }
    const data = await fn(...args)
    cache.set(cacheKey, data, ttl)
    return data
  }
}

// 用户相关API
export const userApi = {
  // 用户登录
  login: (data) => request.post('api/users/login/', data),
  // 用户注册
  register: (data) => request.post('api/users/register/', data),
  // 获取用户信息
  getUserInfo: () => request.get('api/users/profile/'),
  // 更新用户信息
  updateUserInfo: (data) => request.put('api/users/profile/update/', data),
  // 修改密码
  changePassword: (data) => request.post('api/users/change-password/', data),
  // 忘记密码
  forgotPassword: (data) => request.post('api/users/forgot-password/', data),
  // 验证邮箱
  verifyEmail: (data) => request.post('api/users/verify-email/', data),
  // 重新发送验证邮件
  resendVerification: (data) => request.post('api/users/resend-verification/', data),
  // 发送邮箱验证码
  sendEmailCode: (data) => request.post('api/users/email-code/', data),
  // 绑定/更换邮箱
  bindEmail: (data) => request.post('api/users/bind-email/', data),
  // 获取隐私设置
  getPrivacySettings: () => request.get('api/users/privacy/'),
  // 更新隐私设置
  updatePrivacySettings: (data) => request.put('api/users/privacy/', data),
  // 获取偏好设置
  getPreferenceSettings: () => request.get('api/users/preferences/'),
  // 更新偏好设置
  updatePreferenceSettings: (data) => request.put('api/users/preferences/', data),
  // 添加刷新 token 接口
  refreshToken: () => request.post('api/users/token/refresh/'),
  // 用户登出
  logout: () => request.post('api/users/logout/')
}

// 电影相关API
export const movieApi = {
  // 获取电影列表（添加缓存）
  getMovieList: withCache(
    async (params) => await request.get('api/movies/', { params }),
    (params) => `movieList_${JSON.stringify(params)}`
  ),
  // 获取电影详情（添加缓存）
  getMovieDetail: withCache(
    async (id) => await request.get(`api/movies/${id}/`),
    (id) => `movieDetail_${id}`
  ),
  // 获取相关电影（添加缓存）
  getRelatedMovies: withCache(
    async (id) => await request.get(`api/movies/${id}/related/`),
    (id) => `relatedMovies_${id}`
  ),

  // 获取电影分析
  getMoviesAnalysis: () => request.get('/api/movies/analysis')

}

// 影评相关API - 后端暂未实现
export const reviewApi = {
  // 后续后端实现后再添加相关接口
}

// 用户交互相关API - 后端部分实现
export const interactionApi = {
  // 收藏电影 - 对应后端的collects接口
  favoriteMovie: (movieId) => request.post('api/users/collects/', { mid: movieId }),
  // 取消收藏 - 对应后端的collects接口
  unfavoriteMovie: (movieId) => request.delete(`api/users/collects/${movieId}/`),
  // 获取收藏列表 - 对应后端的collects接口
  getFavorites: (params) => request.get('api/users/collects/', { params })
  //getFavorites: () => request.get('api/users/collects/')
  // 注意：后端暂未实现关注用户和观看历史功能
}

// 导出默认API对象
export default {
  user: userApi,
  movie: movieApi,
  review: reviewApi,
  interaction: interactionApi,
}