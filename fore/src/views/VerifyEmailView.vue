<template>
  <div class="verify-email-page">
    <div class="verify-container">
      <div class="verify-form">
        <h2>邮箱验证</h2>

        <!-- 加载状态 -->
        <div v-if="loading" class="state-container">
          <el-spinner size="large" class="loading-spinner" />
          <p class="state-text">正在验证您的邮箱，请稍候...</p>
        </div>

        <!-- 验证成功 -->
        <div v-else-if="verified && !error" class="state-container success-state">
          <el-icon class="success-icon"><CircleCheck /></el-icon>
          <h3>验证成功！</h3>
          <p class="state-text">您的邮箱已成功验证，即将跳转到登录页面...</p>
          <el-button type="primary" @click="goToLogin" class="action-button">立即登录</el-button>
        </div>

        <!-- 验证失败/链接异常 -->
        <div v-else-if="error" class="state-container error-state">
          <el-icon class="error-icon"><CircleClose /></el-icon>
          <h3>验证失败</h3>
          <p class="error-message">{{ errorMessage }}</p>

          <!-- 重新发送验证邮件表单 -->
          <el-form :model="resendForm" :rules="resendRules" ref="resendFormRef" class="resend-form">
            <el-form-item prop="email">
              <el-input
                v-model="resendForm.email"
                placeholder="请输入您的注册邮箱"
                prefix-icon="el-icon-message"
                class="resend-input"
                type="email"
                clearable
              ></el-input>
            </el-form-item>
            <el-button
              type="primary"
              @click="handleResend"
              :loading="resendLoading"
              class="action-button"
            >
              重新发送验证邮件
            </el-button>
          </el-form>

          <div class="login-link">
            返回 <router-link to="/login">登录页面</router-link>
          </div>
        </div>

        <!-- 默认状态（参数缺失） -->
        <div v-else class="state-container">
          <p class="state-text">请通过注册邮箱中的验证链接访问此页面</p>
          <el-button type="primary" @click="goToLogin" class="action-button">返回登录</el-button>
        </div>
      </div>
      <div class="verify-image">
        <img src="@/assets/2.png" alt="验证背景图" onerror="this.style.display='none'">
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { CircleCheck, CircleClose } from '@element-plus/icons-vue'
import { userApi } from '@/api/api'

export default {
  name: 'VerifyEmailView',
  components: {
    CircleCheck,
    CircleClose
  },
  setup() {
    const router = useRouter()
    const route = useRoute()

    // 状态管理
    const loading = ref(false)       // 验证加载状态
    const verified = ref(false)      // 验证成功标识
    const error = ref(false)         // 验证失败标识
    const errorMessage = ref('')     // 错误提示信息
    const resendLoading = ref(false) // 重新发送邮件加载状态

    // 重新发送表单
    const resendForm = reactive({
      email: ''
    })

    // 表单验证规则
    const resendRules = {
      email: [
        { required: true, message: '请输入注册邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
      ]
    }
    const resendFormRef = ref(null)

    // 核心：验证邮箱（适配后端统一响应格式）
    const verifyEmail = async () => {
      // 1. 获取并解码URL参数（处理编码异常）
      let token = route.query.token || ''
      let email = route.query.email || ''

      // 解码参数（兼容后端编码逻辑）
      try {
        token = decodeURIComponent(token)
        email = decodeURIComponent(email)
      } catch (e) {
        console.warn('参数解码失败，使用原始值:', e)
      }

      // 2. 检查参数完整性
      if (!token || !email) {
        error.value = true
        errorMessage.value = '验证链接无效，请检查链接是否完整或重新获取验证邮件'
        // 自动填充邮箱到重发表单，提升用户体验
        resendForm.email = email
        return
      }

      // 3. 调用后端验证接口
      loading.value = true
      try {
        // 调用后端验证接口
        const response = await userApi.verifyEmail({ token, email })
        // 适配后端统一响应格式
        if (response.code === 200 || !response.code) {
          verified.value = true
          ElMessage.success('邮箱验证成功！')
          // 3秒后自动跳转到登录页
          setTimeout(() => {
            goToLogin()
          }, 3000)
        }
      } catch (err) {
        error.value = true
        // 适配后端错误信息格式
        if (err.data && err.data.detail) {
          errorMessage.value = err.data.detail
        } else if (err.data && err.data.error) {
          errorMessage.value = err.data.error
        } else {
          errorMessage.value = '验证链接无效或已过期（有效期1小时）'
        }
        // 自动填充邮箱到重发表单
        resendForm.email = email
      } finally {
        loading.value = false
      }
    }

    // 重新发送验证邮件
    const handleResend = async () => {
      // 表单验证
      resendFormRef.value.validate(async (valid) => {
        if (!valid) return

        resendLoading.value = true
        try {
          const response = await userApi.resendVerification({ email: resendForm.email })
          if (response.code === 200) {
            ElMessageBox.success(
              '验证邮件已重新发送，请查收邮箱（若未收到请检查垃圾邮件箱）',
              '发送成功'
            )
            resendForm.email = '' // 清空表单
          }
        } catch (err) {
          let msg = '发送失败，请稍后重试'
          if (err.data && err.data.error) {
            msg = err.data.error
          }
          ElMessage.error(msg)
        } finally {
          resendLoading.value = false
        }
      })
    }

    // 跳转到登录页
    const goToLogin = () => {
      router.push('/login')
    }

    // 页面加载时自动执行验证
    onMounted(() => {
      verifyEmail()
    })

    return {
      loading,
      verified,
      error,
      errorMessage,
      resendForm,
      resendRules,
      resendFormRef,
      resendLoading,
      handleResend,
      goToLogin
    }
  }
}
</script>

<style scoped>
/* 页面整体样式 */
.verify-email-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #0f172a;
  padding: 20px;
  color: #e2e8f0;
  box-sizing: border-box;
}

/* 验证容器 */
.verify-container {
  display: flex;
  flex-direction: column;
  background-color: rgba(15, 23, 42, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  width: 100%;
  max-width: 500px;
  border: 1px solid rgba(100, 200, 255, 0.2);
}

/* 表单区域 */
.verify-form {
  flex: 1;
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.verify-form h2 {
  margin-bottom: 25px;
  color: #ffffff;
  font-size: 22px;
  font-weight: 600;
  text-shadow: 0 0 5px rgba(100, 200, 255, 0.5);
}

/* 状态容器通用样式 */
.state-container {
  width: 100%;
}

.state-text {
  color: #cbd5e1;
  margin-bottom: 20px;
  line-height: 1.6;
  font-size: 15px;
}

/* 加载状态 */
.loading-spinner {
  margin-bottom: 20px;
  color: #409eff;
}

/* 成功状态 */
.success-state .success-icon {
  font-size: 56px;
  color: #67c23a;
  margin-bottom: 20px;
}

.success-state h3 {
  color: #ffffff;
  font-size: 18px;
  margin-bottom: 15px;
}

/* 错误状态 */
.error-state .error-icon {
  font-size: 56px;
  color: #f56c6c;
  margin-bottom: 20px;
}

.error-state h3 {
  color: #ffffff;
  font-size: 18px;
  margin-bottom: 15px;
}

.error-message {
  color: #f56c6c;
  margin-bottom: 20px;
  padding: 0 10px;
  line-height: 1.6;
}

/* 重新发送表单 */
.resend-form {
  width: 100%;
  margin-bottom: 15px;
}

.resend-input {
  height: 45px;
  font-size: 15px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(100, 200, 255, 0.3);
  color: #ffffff;
}

.resend-input ::v-deep .el-input__inner {
  background-color: transparent;
  color: #ffffff;
  border: none;
}

/* 按钮样式 */
.action-button {
  width: 100%;
  margin-top: 10px;
  height: 45px;
  font-size: 16px;
  background-color: #409eff;
  border: none;
}

.action-button:hover {
  background-color: #66b1ff;
}

/* 登录链接 */
.login-link {
  margin-top: 20px;
  color: #cbd5e1;
  font-size: 14px;
}

.login-link a {
  color: #409eff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

/* 背景图片 */
.verify-image {
  height: 180px;
  width: 100%;
  background-color: #1e293b;
  overflow: hidden;
}

.verify-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 小屏手机适配 */
@media (max-width: 375px) {
  .verify-form {
    padding: 25px 15px;
  }

  .verify-form h2 {
    font-size: 20px;
    margin-bottom: 20px;
  }

  .success-icon, .error-icon {
    font-size: 48px !important;
  }

  .action-button {
    height: 42px;
    font-size: 15px;
  }

  .verify-image {
    height: 150px;
  }
}
</style>
<!--<template>-->
<!--  <div class="verify-email-page">-->
<!--    <div class="verify-container">-->
<!--      <div class="verify-form">-->
<!--        <h2>邮箱验证</h2>-->
<!--        -->
<!--        <div v-if="!loading && !verified">-->
<!--          <p class="verify-message">正在验证您的邮箱，请稍候...</p>-->
<!--        </div>-->
<!--        -->
<!--        <div v-if="loading">-->
<!--          <el-spinner size="large" class="loading-spinner" />-->
<!--          <p>验证中...</p>-->
<!--        </div>-->
<!--        -->
<!--        <div v-if="verified && !error">-->
<!--          <div class="success-icon">-->
<!--            <el-icon class="icon-success"><CircleCheck /></el-icon>-->
<!--          </div>-->
<!--          <h3>验证成功！</h3>-->
<!--          <p>您的邮箱已成功验证，现在可以使用全部功能了。</p>-->
<!--          <el-button type="primary" @click="goToLogin">立即登录</el-button>-->
<!--        </div>-->
<!--        -->
<!--        <div v-if="error">-->
<!--          <div class="error-icon">-->
<!--            <el-icon class="icon-error"><CircleClose /></el-icon>-->
<!--          </div>-->
<!--          <h3>验证失败</h3>-->
<!--          <p class="error-message">{{ errorMessage }}</p>-->
<!--          <el-form :model="resendForm" :rules="resendRules" ref="resendFormRef">-->
<!--            <el-form-item prop="email">-->
<!--              <el-input -->
<!--                v-model="resendForm.email" -->
<!--                placeholder="请输入您的注册邮箱"-->
<!--                prefix-icon="el-icon-message"-->
<!--              ></el-input>-->
<!--            </el-form-item>-->
<!--            <el-button type="primary" @click="handleResend" :loading="resendLoading">重新发送验证邮件</el-button>-->
<!--          </el-form>-->
<!--          <div class="login-link">-->
<!--            返回 <router-link to="/login">登录</router-link>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--      <div class="verify-image">-->
<!--        <img src="@/assets/2.png" alt="验证背景图">-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import { ref, reactive, onMounted } from 'vue'-->
<!--import { useRouter, useRoute } from 'vue-router'-->
<!--import { ElMessage } from 'element-plus'-->
<!--import { CircleCheck, CircleClose } from '@element-plus/icons-vue'-->
<!--import { userApi } from '../api/api.js'-->

<!--export default {-->
<!--  name: 'VerifyEmailView',-->
<!--  components: {-->
<!--    CircleCheck,-->
<!--    CircleClose-->
<!--  },-->
<!--  setup() {-->
<!--    const router = useRouter()-->
<!--    const route = useRoute()-->
<!--    const loading = ref(false)-->
<!--    const verified = ref(false)-->
<!--    const error = ref(false)-->
<!--    const errorMessage = ref('')-->
<!--    const resendFormRef = ref(null)-->
<!--    const resendLoading = ref(false)-->
<!--    -->
<!--    const resendForm = reactive({-->
<!--      email: ''-->
<!--    })-->
<!--    -->
<!--    const resendRules = {-->
<!--      email: [-->
<!--        { required: true, message: '请输入注册邮箱', trigger: 'blur' },-->
<!--        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }-->
<!--      ]-->
<!--    }-->
<!--    -->
<!--    // 验证邮箱-->
<!--    const verifyEmail = async () => {-->
<!--      const token = route.query.token-->
<!--      const email = route.query.email-->
<!--      -->
<!--      if (!token || !email) {-->
<!--        error.value = true-->
<!--        errorMessage.value = '验证链接无效，请检查链接是否正确。'-->
<!--        return-->
<!--      }-->
<!--      -->
<!--      loading.value = true-->
<!--      try {-->
<!--        await userApi.verifyEmail({ token, email })-->
<!--        verified.value = true-->
<!--        ElMessage.success('邮箱验证成功')-->
<!--      } catch (err) {-->
<!--        error.value = true-->
<!--        console.error('邮箱验证失败:', err)-->
<!--        // 解析错误信息-->
<!--        if (err.response && err.response.data) {-->
<!--          if (err.response.data.detail) {-->
<!--            errorMessage.value = err.response.data.detail-->
<!--          } else if (err.response.data.error) {-->
<!--            errorMessage.value = err.response.data.error-->
<!--          } else {-->
<!--            errorMessage.value = '验证失败，请检查链接是否过期或重新请求验证。'-->
<!--          }-->
<!--        } else {-->
<!--          errorMessage.value = '网络错误，请稍后重试。'-->
<!--        }-->
<!--      } finally {-->
<!--        loading.value = false-->
<!--      }-->
<!--    }-->
<!--    -->
<!--    // 重新发送验证邮件-->
<!--    const handleResend = async () => {-->
<!--      resendFormRef.value.validate(async (valid) => {-->
<!--        if (valid) {-->
<!--          resendLoading.value = true-->
<!--          try {-->
<!--            await userApi.resendVerification(resendForm)-->
<!--            ElMessage.success('验证邮件已重新发送，请查收您的邮箱')-->
<!--            // 重置表单-->
<!--            resendForm.email = ''-->
<!--          } catch (err) {-->
<!--            console.error('重新发送验证邮件失败:', err)-->
<!--            let msg = '发送失败，请稍后重试'-->
<!--            if (err.response && err.response.data && err.response.data.error) {-->
<!--              msg = err.response.data.error-->
<!--            }-->
<!--            ElMessage.error(msg)-->
<!--          } finally {-->
<!--            resendLoading.value = false-->
<!--          }-->
<!--        }-->
<!--      })-->
<!--    }-->
<!--    -->
<!--    // 跳转到登录页-->
<!--    const goToLogin = () => {-->
<!--      router.push('/login')-->
<!--    }-->
<!--    -->
<!--    // 页面加载时自动验证-->
<!--    onMounted(() => {-->
<!--      verifyEmail()-->
<!--    })-->
<!--    -->
<!--    return {-->
<!--      loading,-->
<!--      verified,-->
<!--      error,-->
<!--      errorMessage,-->
<!--      resendForm,-->
<!--      resendRules,-->
<!--      resendFormRef,-->
<!--      resendLoading,-->
<!--      handleResend,-->
<!--      goToLogin-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->

<!--<style scoped>-->
<!--.verify-email-page {-->
<!--  min-height: 100vh;-->
<!--  display: flex;-->
<!--  justify-content: center;-->
<!--  align-items: center;-->
<!--  background-color: #f5f7fa;-->
<!--  padding: 20px;-->
<!--}-->

<!--.verify-container {-->
<!--  display: flex;-->
<!--  background-color: #fff;-->
<!--  border-radius: 12px;-->
<!--  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);-->
<!--  overflow: hidden;-->
<!--  max-width: 900px;-->
<!--  width: 100%;-->
<!--}-->

<!--.verify-form {-->
<!--  flex: 1;-->
<!--  padding: 40px;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  align-items: center;-->
<!--  text-align: center;-->
<!--}-->

<!--.verify-form h2 {-->
<!--  margin-bottom: 30px;-->
<!--  color: #303133;-->
<!--  font-size: 24px;-->
<!--  font-weight: 600;-->
<!--}-->

<!--.verify-form h3 {-->
<!--  margin-bottom: 15px;-->
<!--  color: #303133;-->
<!--  font-size: 20px;-->
<!--}-->

<!--.verify-form p {-->
<!--  color: #606266;-->
<!--  margin-bottom: 20px;-->
<!--  line-height: 1.6;-->
<!--}-->

<!--.loading-spinner {-->
<!--  margin-bottom: 20px;-->
<!--}-->

<!--.success-icon .icon-success {-->
<!--  font-size: 64px;-->
<!--  color: #67c23a;-->
<!--  margin-bottom: 20px;-->
<!--}-->

<!--.error-icon .icon-error {-->
<!--  font-size: 64px;-->
<!--  color: #f56c6c;-->
<!--  margin-bottom: 20px;-->
<!--}-->

<!--.error-message {-->
<!--  color: #f56c6c;-->
<!--  margin-bottom: 20px;-->
<!--}-->

<!--.verify-form .el-button {-->
<!--  width: 100%;-->
<!--  margin-top: 10px;-->
<!--}-->

<!--.login-link {-->
<!--  margin-top: 20px;-->
<!--  color: #606266;-->
<!--}-->

<!--.login-link a {-->
<!--  color: #409eff;-->
<!--  text-decoration: none;-->
<!--}-->

<!--.login-link a:hover {-->
<!--  text-decoration: underline;-->
<!--}-->

<!--.verify-image {-->
<!--  flex: 1;-->
<!--  display: none;-->
<!--  background-color: #f0f2f5;-->
<!--}-->

<!--.verify-image img {-->
<!--  width: 100%;-->
<!--  height: 100%;-->
<!--  object-fit: cover;-->
<!--}-->

<!--/* 响应式设计 */-->
<!--@media (min-width: 768px) {-->
<!--  .verify-image {-->
<!--    display: block;-->
<!--  }-->
<!--}-->

<!--@media (max-width: 767px) {-->
<!--  .verify-container {-->
<!--    margin: 0;-->
<!--    box-shadow: none;-->
<!--  }-->
<!--  -->
<!--  .verify-form {-->
<!--    padding: 30px 20px;-->
<!--  }-->
<!--  -->
<!--  .verify-form h2 {-->
<!--    font-size: 20px;-->
<!--  }-->
<!--  -->
<!--  .success-icon .icon-success,-->
<!--  .error-icon .icon-error {-->
<!--    font-size: 48px;-->
<!--  }-->
<!--}-->
<!--</style>-->