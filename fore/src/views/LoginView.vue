<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-form">
        <h2>用户登录</h2>
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
          <el-form-item prop="username">
            <el-input 
              v-model="loginForm.username" 
              placeholder="请输入用户名/邮箱"
              prefix-icon="el-icon-user"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input 
              v-model="loginForm.password" 
              type="password" 
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
              show-password
            ></el-input>
          </el-form-item>
          <div class="remember-forgot">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <a href="#" class="forgot-password" @click.prevent="showForgotPasswordDialog">忘记密码?</a>
          </div>
          <el-form-item>
            <el-button type="primary" @click="handleLogin" class="login-btn" :loading="loading">登录</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="default" @click="handleGuestEnter" class="guest-btn">游客进入</el-button>
          </el-form-item>
          <div class="register-link">
            还没有账号? <router-link to="/register">立即注册</router-link>
          </div>
        </el-form>
      </div>
      <div class="login-image">
        <img src="@/assets/1.png" alt="登录背景图">
      </div>
    </div>

    <!-- 忘记密码对话框 -->
    <el-dialog
      title="忘记密码"
      v-model="showForgotPassword"
      width="400px"
      center
    >
      <el-form :model="forgotPasswordForm" :rules="forgotPasswordRules" ref="forgotPasswordFormRef">
        <el-form-item prop="email">
          <el-input 
            v-model="forgotPasswordForm.email" 
            placeholder="请输入注册邮箱"
            prefix-icon="el-icon-message"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showForgotPassword = false">取消</el-button>
          <el-button type="primary" @click="handleForgotPassword" :loading="forgotPasswordLoading">发送验证码</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { userApi } from '@/api/api'
//import store from "@/store"


export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const loginFormRef = ref(null)
    const loading = ref(false)
    const rememberMe = ref(false)
    
    // 忘记密码相关
    const showForgotPassword = ref(false)
    const forgotPasswordFormRef = ref(null)
    const forgotPasswordLoading = ref(false)

    const loginForm = reactive({
      username: '',
      password: ''
    })

    // 忘记密码表单
    const forgotPasswordForm = reactive({
      email: ''
    })

    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
      ]
    }

    // 忘记密码验证规则
    const forgotPasswordRules = {
      email: [
        { required: true, message: '请输入注册邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ]
    }


    const handleLogin = async () => {
      loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 调用实际的登录API，转换字段名
            const loginData = {
              uname: loginForm.username,
              password: loginForm.password
            }
            const response = await userApi.login(loginData)

            // 处理登录响应
            if (response) {
              // 统一处理登录成功情况，不区分邮箱是否验证
              ElMessage.success('登录成功')


              // 存储登录信息
              if (response.access) {
                // 正常登录成功，存储token
                localStorage.setItem('token', response.access)
                localStorage.setItem('refreshToken', response.refresh || '')
              }
              localStorage.setItem('isLoggedIn', 'true')
              localStorage.setItem('username', response.uname || loginForm.username)
              localStorage.setItem('id', response.id)

              // 触发自定义事件
              window.dispatchEvent(new CustomEvent('loginStatusChanged', { detail: { isLoggedIn: true, username: response.uname || loginForm.username } }))

              // 如果勾选了记住我
              if (rememberMe.value) {
                localStorage.setItem('rememberMe', 'true')
              }

              // 无论是否验证邮箱，都跳转到首页
              router.push('/')
            }
          } catch (error) {
            console.error('登录失败:', error)
            //增强错误处理，显示后端返回的具体错误信息
            let errorMessage = '登录失败，请检查用户名和密码'
            if (error.response && error.response.data && error.response.data.detail) {
              errorMessage = error.response.data.detail
            } else if (error.response && error.response.data && error.response.data.error) {
              errorMessage = error.response.data.error
            }
            ElMessage.error(errorMessage)
          } finally {
            loading.value = false
          }
        } else {
          return false
        }
      })
    }

    // 游客进入功能
    const handleGuestEnter = () => {
      // 设置游客信息
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('username', '游客')
      localStorage.setItem('id', 'guest')
      localStorage.setItem('isGuest', 'true')
      
      // 触发自定义事件
      window.dispatchEvent(new CustomEvent('loginStatusChanged', { detail: { isLoggedIn: true, username: '游客' } }))
      
      // 显示成功消息
      ElMessage.success('游客登录成功')
      
      // 跳转到首页
      router.push('/')
    }

    // 显示忘记密码对话框
    const showForgotPasswordDialog = () => {
      showForgotPassword.value = true
    }
    
    // 处理忘记密码
    const handleForgotPassword = async () => {
      forgotPasswordFormRef.value.validate(async (valid) => {
        if (valid) {
          forgotPasswordLoading.value = true
          try {
            // 调用忘记密码API
            await userApi.forgotPassword(forgotPasswordForm)
            ElMessage.success('验证码发送成功，请查收邮箱')
            showForgotPassword.value = false
            // 清空表单
            forgotPasswordForm.email = ''
          } catch (error) {
            console.error('发送验证码失败:', error)
            let errorMessage = '发送验证码失败，请稍后重试'
            if (error.response && error.response.data && error.response.data.detail) {
              errorMessage = error.response.data.detail
            } else if (error.response && error.response.data && error.response.data.error) {
              errorMessage = error.response.data.error
            }
            ElMessage.error(errorMessage)
          } finally {
            forgotPasswordLoading.value = false
          }
        } else {
          return false
        }
      })
    }

    return {
      loginForm,
      rules,
      loginFormRef,
      loading,
      rememberMe,
      handleLogin,
      handleGuestEnter,
      // 忘记密码相关
      showForgotPassword,
      forgotPasswordForm,
      forgotPasswordRules,
      forgotPasswordFormRef,
      forgotPasswordLoading,
      showForgotPasswordDialog,
      handleForgotPassword
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background-color: #0f172a;
  color: #e2e8f0;
  padding: 20px 0;
  box-sizing: border-box;
}

.login-container {
  width: 900px;
  height: 600px;
  display: flex;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  background-color: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(100, 200, 255, 0.2);
}

.login-form {
  flex: 1;
  padding: 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-form h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #ffffff;
  font-size: 24px;
  text-shadow: 0 0 5px rgba(100, 200, 255, 0.5);
}

.el-form-item {
  margin-bottom: 22px;
}

.remember-forgot {
  display: flex;
  justify-content: space-between;
  margin-bottom: 22px;
}

.forgot-password {
  color: #409eff;
  text-decoration: none;
  font-size: 14px;
}

.login-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
}

.guest-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
  margin-top: 10px;
}

.register-link {
  text-align: center;
  margin-top: 15px;
  color: #cbd5e1;
  font-size: 14px;
}

.register-link a {
  color: #409eff;
  text-decoration: none;
  font-weight: 500;
}



.login-image {
  flex: 1;
  overflow: hidden;
}

.login-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 平板设备适配 */
@media (max-width: 992px) {
  .login-container {
    width: 90%;
    height: auto;
  }
  
  .login-form h2 {
    font-size: 22px;
    margin-bottom: 25px;
  }
  
  .el-form-item {
    margin-bottom: 20px;
  }
  
  .remember-forgot {
    margin-bottom: 20px;
  }
}

/* 移动设备适配 */
@media (max-width: 768px) {
  .login-container {
    width: 95%;
    flex-direction: column;
    height: auto;
    max-height: none;
    overflow: visible;
  }

  .login-image {
    height: 180px;
    width: 100%;
  }
  
  .login-form {
    width: 100%;
    padding: 25px 15px;
    overflow-y: auto;
    max-height: none;
  }
  
  .login-form h2 {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .login-btn {
    height: 40px;
    font-size: 15px;
  }
  
  .guest-btn {
    height: 40px;
    font-size: 15px;
    margin-top: 10px;
  }
  
  .register-link {
    font-size: 13px;
  }
  
  .forgot-password {
    font-size: 13px;
  }
  
  /* 记住我和忘记密码布局调整 */
  .remember-forgot {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  /* 弹窗适配 */
  .el-dialog {
    width: 90% !important;
    margin: 20px auto !important;
  }
}

/* 小屏手机适配 */
@media (max-width: 480px) {
  .login-page {
    padding: 10px;
    min-height: 100vh;
    box-sizing: border-box;
  }
  
  .login-form {
    padding: 20px 12px;
  }
  
  .login-form h2 {
    font-size: 18px;
    margin-bottom: 15px;
  }
  
  .login-btn {
    height: 38px;
    font-size: 14px;
    min-height: 44px; /* 符合触摸界面最小尺寸标准 */
  }
  
  .guest-btn {
    height: 38px;
    font-size: 14px;
    min-height: 44px; /* 符合触摸界面最小尺寸标准 */
    margin-top: 10px;
  }
  
  .el-input__inner {
    font-size: 14px;
    padding: 12px 30px 12px 35px; /* 增加垂直内边距，提升触摸体验 */
    min-height: 44px; /* 符合触摸界面最小尺寸标准 */
  }
  
  /* 复选框文本调整 */
  .el-checkbox__label {
    font-size: 12px;
  }
  
  /* 增加触摸友好的点击区域 */
  .el-checkbox__input {
    transform: scale(1.1); /* 适当放大复选框 */
  }
  
  /* 增加链接的可点击区域 */
  .register-link a, .forgot-password {
    padding: 4px 0;
    display: inline-block;
  }
  
  /* 防止iOS下输入框自动放大 */
  input, textarea {
    font-size: 16px;
  }
}
</style>
