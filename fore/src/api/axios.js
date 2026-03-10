import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://x.x.x.x:8000', // 基础URL，可通过环境变量配置
  timeout: 30000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    // 如果token存在，则添加到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }else{
        console.log('Token 不存在，请先登录')
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  // 第一个回调：响应成功（状态码2xx）的处理逻辑
  response => {
    const { data } = response  // 解构出响应的核心数据
    // 适配Django后端返回格式，直接返回响应数据
    return data // 返回完整的响应数据（而非整个response对象）
  },
  // 第二个回调：响应失败（网络错误/状态码非2xx）的处理逻辑
  error => {
    // 初始化默认错误提示
    let message = '网络异常，请稍后重试'

    if (error.response) {
      // 场景1：服务器已响应，但状态码不是2xx（如401/403/404/500）
      const { status } = error.response
      // 根据不同状态码定制错误提示
      switch (status) {
          case 401: {
              const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
              if (isLoggedIn) {
                  message = '登录超时，请重新登录'
                  localStorage.removeItem('token')
                  localStorage.removeItem('refreshToken')
                  localStorage.removeItem('isLoggedIn')
                  // 可以在这里添加跳转到登录页的逻辑
                  // window.location.href = '/login'
              } else {
                  // 用户未登录时的401错误通常是正常的，不显示警告
                  message = ''
              }
              break
          }
        case 403:
          message = '拒绝访问' // 权限不足（比如普通用户访问管理员接口）
          break
        case 404:
          message = '请求的资源不存在' // 接口路径错误/数据不存在
          break
        case 500:
          message = '服务器内部错误' // 后端代码报错
          break
        default:
          message = `请求失败(${status})` // 其他状态码（如400/405）
      }
    } else if (error.request) {
      // 场景2：请求已发出，但服务器无任何响应（如后端宕机、网络超时）
      message = '服务器无响应'
    }
    // 无论哪种错误，都用Element Plus的ElMessage提示用户
    // 只有当有错误消息时才显示
    if (message) {
      ElMessage.error(message)
    }
    // 抛出错误，让业务代码能捕获并处理（比如终止加载状态）
    return Promise.reject(error)
  }
)

export default service