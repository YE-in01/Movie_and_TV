<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-form">
        <h2>用户注册</h2>
        <el-form :model="registerForm" :rules="rules" ref="registerFormRef">
          <el-form-item prop="username">
            <el-input 
              v-model="registerForm.username" 
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
            ></el-input>
          </el-form-item>
          <el-form-item prop="email">
            <el-input 
              v-model="registerForm.email" 
              placeholder="请输入邮箱"
              prefix-icon="el-icon-message"
            ></el-input>
          </el-form-item>
          <el-form-item prop="phone">
            <el-input 
              v-model="registerForm.phone" 
              placeholder="请输入手机号"
              prefix-icon="el-icon-phone"
            ></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input 
              v-model="registerForm.password" 
              type="password" 
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item prop="confirmPassword">
            <el-input 
              v-model="registerForm.confirmPassword" 
              type="password" 
              placeholder="请确认密码"
              prefix-icon="el-icon-lock"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item prop="agreement" required>
            <el-checkbox v-model="registerForm.agreement">
              我已阅读并同意
              <a href="#" @click.prevent="showAgreement">《用户服务协议》</a>
              和
              <a href="#" @click.prevent="showPrivacy">《隐私政策》</a>
            </el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleRegister" class="register-btn" :loading="loading">注册</el-button>
          </el-form-item>
          <div class="login-link">
            已有账号? <router-link to="/login">立即登录</router-link>
          </div>
        </el-form>
      </div>
      <div class="register-image">
        <img src="@/assets/2.png" alt="注册背景图">
      </div>
    </div>

    <!-- 用户协议弹窗 -->
    <el-dialog
      title="用户服务协议"
      v-model="agreementVisible"
      width="50%"
      :before-close="handleAgreementClose"
    >
      <div class="agreement-content">
        <h3>1. 服务条款的确认和接纳</h3>
        <p>欢迎使用影视天地！本用户协议（以下简称"协议"）是您与影视天地之间关于使用影视天地服务的法律协议。</p>

        <h3>2. 服务内容</h3>
        <p>影视天地是一个提供影视内容浏览、搜索、评论等服务的在线平台。具体服务内容以影视天地实际提供的为准。</p>

        <h3>3. 用户注册</h3>
        <p>您需要注册一个账户才能使用影视天地的某些功能。您同意：</p>
        <p>a) 提供真实、准确、完整的个人资料；</p>
        <p>b) 及时更新您的注册资料；</p>
        <p>c) 对您的账户和密码保密，并对您账户下的所有活动承担责任。</p>

        <h3>4. 用户行为规范</h3>
        <p>您同意不会利用影视天地服务进行任何违法或不正当的活动，包括但不限于：</p>
        <p>a) 上传、发布或传播任何非法、有害、威胁、滥用、骚扰、诽谤、淫秽、粗俗或其他令人反感的内容；</p>
        <p>b) 侵犯任何人的专利、商标、商业秘密、版权或其他专有权利；</p>
        <p>c) 传播病毒、木马或其他恶意代码；</p>
        <p>d) 干扰或破坏影视天地服务或与服务连接的服务器。</p>

        <h3>5. 知识产权</h3>
        <p>影视天地服务中包含的任何文本、图片、图形、音频、视频、软件和其他材料（以下简称"内容"）的所有权归影视天地或其内容提供者所有，并受著作权法、商标法、专利法及其他知识产权法律的保护。</p>

        <h3>6. 免责声明</h3>
        <p>影视天地不对您因使用影视天地服务而导致的任何直接或间接损失承担责任。</p>

        <h3>7. 协议修改</h3>
        <p>影视天地有权随时修改本协议的条款，修改后的协议将在影视天地网站上公布。</p>

        <h3>8. 法律适用</h3>
        <p>本协议的订立、执行和解释及争议的解决均应适用中华人民共和国法律。</p>
      </div>
    </el-dialog>

    <!-- 隐私政策弹窗 -->
    <el-dialog
      title="隐私政策"
      v-model="privacyVisible"
      width="50%"
      :before-close="handlePrivacyClose"
    >
      <div class="privacy-content">
        <h3>1. 信息收集</h3>
        <p>我们收集的信息可能包括：</p>
        <p>a) 您提供给我们的信息（如注册信息）；</p>
        <p>b) 自动收集的信息（如IP地址、浏览器类型、访问时间等）；</p>
        <p>c) cookies和类似技术收集的信息。</p>

        <h3>2. 信息使用</h3>
        <p>我们使用收集的信息来：</p>
        <p>a) 提供、维护、保护和改进我们的服务；</p>
        <p>b) 处理您的请求和交易；</p>
        <p>c) 与您沟通；</p>
        <p>d) 个性化您的体验；</p>
        <p>e) 进行内部分析，以改进我们的产品和服务。</p>

        <h3>3. 信息共享</h3>
        <p>我们不会出售、交易或转让您的个人信息给第三方，除非：</p>
        <p>a) 获得您的同意；</p>
        <p>b) 法律要求；</p>
        <p>c) 为保护我们的权利、财产或安全；</p>
        <p>d) 与可信的第三方服务提供商共享，以提供服务。</p>

        <h3>4. 信息安全</h3>
        <p>我们采取合理的安全措施来保护您的个人信息免受未经授权的访问、使用或披露。</p>

        <h3>5. 数据保留</h3>
        <p>我们仅在必要的时间内保留您的个人信息，以实现收集信息的目的，除非法律要求或允许更长的保留期限。</p>

        <h3>6. 您的权利</h3>
        <p>您有权：</p>
        <p>a) 访问您的个人信息；</p>
        <p>b) 更正不准确的信息；</p>
        <p>c) 删除您的个人信息；</p>
        <p>d) 限制处理您的个人信息；</p>
        <p>e) 数据可携带权。</p>

        <h3>7. 隐私政策更新</h3>
        <p>我们可能会不时更新本隐私政策。更新后的政策将在我们的网站上公布。</p>

        <h3>8. 联系我们</h3>
        <p>如果您对本隐私政策有任何问题或疑虑，请通过contact@movieheaven.com联系我们。</p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ElMessageBox } from 'element-plus'
import { userApi } from '@/api/api'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const registerFormRef = ref(null)
    const loading = ref(false)
    const agreementVisible = ref(false)
    const privacyVisible = ref(false)

    const registerForm = reactive({
      username: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
      agreement: false
    })

    // 验证确认密码是否一致
    const validateConfirmPassword = (rule, value, callback) => {
      const password = registerForm.password;
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }

    // 验证手机号格式
    const validatePhone = (rule, value, callback) => {
      const phoneReg = /^1[3-9]\d{9}$/;
      if (value === '') {
        callback(new Error('请输入手机号'));
      } else if (value.length !== 11) { // 显式判断长度是否为11位
        callback(new Error('手机号长度必须为11位'));
      } else if (!phoneReg.test(value)) { // 长度正确后，再校验格式
        callback(new Error('请输入正确的手机号格式'));
      } else {
        callback(); // 校验通过
      }
    }

    // 验证邮箱格式
    const validateEmail = (rule, value, callback) => {
      const emailReg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (value === '') {
        callback(new Error('请输入邮箱'))
      } else if (!emailReg.test(value)) {
        callback(new Error('请输入正确的邮箱格式'))
      } else {
        callback()
      }
    }

    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, validator: validateEmail, trigger: 'blur' }
      ],
      phone: [
        { required: true, validator: validatePhone, trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, validator: validateConfirmPassword, trigger: 'blur' }
      ],
      agreement: [
        { required: true, message: '请阅读并同意用户协议和隐私政策', trigger: ['change', 'submit'] },
        { validator: (rule, value, callback) => {
          if (!value) {
            callback(new Error('必须同意用户协议和隐私政策才能继续注册'));
          } else {
            callback();
          }
        }, trigger: ['change', 'submit'] }
      ]
    }

    const handleRegister = async () => {
      // 额外的显式检查，确保复选框已勾选
      if (!registerForm.agreement) {
        ElMessage.error('请阅读并同意用户协议和隐私政策');
        return;
      }
      
      registerFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 准备注册数据，转换字段名为后端期望的格式
            const registerData = {
              uname: registerForm.username,
              email: registerForm.email,
              phonenum: registerForm.phone,
              password: registerForm.password,
              confirm_password: registerForm.confirmPassword
            }
            
            // 调用实际的注册API
            await userApi.register(registerData)
            
            // 处理注册成功响应
            ElMessage.success('注册成功，请查收邮箱验证邮件（若未收到请检查垃圾邮件箱）')
            // 显示邮箱验证提示
            ElMessageBox.alert(
              '我们已向您的邮箱发送了验证链接，请点击邮件中的链接完成验证后再登录。',
              '邮箱验证提示',
              {
                confirmButtonText: '前往登录',
                type: 'info'
              }
            ).then(() => {
              // 跳转到登录页面
              router.push('/login')
            })
          } catch (error) {
            console.error('注册失败:', error)
            // 增强错误处理，显示后端返回的具体错误信息
            let errorMessage = '注册失败，请稍后重试'
            if (error.response && error.response.data) {
              // 检查是否有详细错误信息
              if (error.response.data.detail) {
                errorMessage = error.response.data.detail
              } else if (error.response.data.error) {
                errorMessage = error.response.data.error
              } else {
                // 处理字段验证错误
                const fieldErrors = []
                for (const [, errors] of Object.entries(error.response.data)) {
                  fieldErrors.push(...errors)
                }
                if (fieldErrors.length > 0) {
                  errorMessage = fieldErrors.join('; ')
                }
              }
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

    const showAgreement = () => {
      agreementVisible.value = true
    }

    const showPrivacy = () => {
      privacyVisible.value = true
    }

    const handleAgreementClose = () => {
      agreementVisible.value = false
    }

    const handlePrivacyClose = () => {
      privacyVisible.value = false
    }

    return {
      registerForm,
      rules,
      registerFormRef,
      loading,
      agreementVisible,
      privacyVisible,
      handleRegister,
      showAgreement,
      showPrivacy,
      handleAgreementClose,
      handlePrivacyClose
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background-color: #0f172a;
  color: #e2e8f0;
  padding: 20px 0;
  box-sizing: border-box;
}

.register-container {
  width: 900px;
  height: 700px;
  display: flex;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  background-color: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(100, 200, 255, 0.2);
}

.register-form {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow-y: auto;
}

.register-form h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #ffffff;
  font-size: 24px;
  text-shadow: 0 0 5px rgba(100, 200, 255, 0.5);
}

.el-form-item {
  margin-bottom: 18px;
}

.register-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
}

.login-link {
  text-align: center;
  margin-top: 15px;
  color: #cbd5e1;
  font-size: 14px;
}

.login-link a {
  color: #409eff;
  text-decoration: none;
  font-weight: 500;
}

.register-form a {
  color: #409eff;
  text-decoration: none;
}

.register-image {
  flex: 1;
  overflow: hidden;
}

.register-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.agreement-content, .privacy-content {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 10px;
}

.agreement-content h3, .privacy-content h3 {
  margin-top: 15px;
  margin-bottom: 10px;
  color: #303133;
}

.agreement-content p, .privacy-content p {
  margin-bottom: 10px;
  line-height: 1.6;
  color: #606266;
}

/* 平板设备适配 */
@media (max-width: 992px) {
  .register-container {
    width: 90%;
    height: auto;
  }
  
  .register-form h2 {
    font-size: 22px;
    margin-bottom: 25px;
  }
  
  .el-form-item {
    margin-bottom: 16px;
  }
}

/* 移动设备适配 */
@media (max-width: 768px) {
  .register-container {
    width: 95%;
    flex-direction: column;
    height: auto;
    max-height: none;
    overflow: visible;
  }

  .register-image {
    height: 180px;
    width: 100%;
  }
  
  .register-form {
    width: 100%;
    padding: 25px 15px;
    overflow-y: auto;
    max-height: none;
  }
  
  .register-form h2 {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .register-btn {
    height: 40px;
    font-size: 15px;
  }
  
  .login-link {
    font-size: 13px;
  }
  
  /* 弹窗适配 */
  .el-dialog {
    width: 90% !important;
    margin: 20px auto !important;
  }
  
  .agreement-content, .privacy-content {
    max-height: 50vh;
    padding-right: 5px;
  }
}

/* 小屏手机适配 */
@media (max-width: 480px) {
  .register-page {
    padding: 10px;
    min-height: 100vh;
    box-sizing: border-box;
  }
  
  .register-form {
    padding: 20px 12px;
  }
  
  .register-form h2 {
    font-size: 18px;
    margin-bottom: 15px;
  }
  
  .register-btn {
    height: 38px;
    font-size: 14px;
    min-height: 44px; /* 符合触摸界面最小尺寸标准 */
  }
  
  .el-input__inner {
    font-size: 14px;
    padding: 12px 30px 12px 35px; /* 增加垂直内边距，提升触摸体验 */
    min-height: 44px; /* 符合触摸界面最小尺寸标准 */
  }
  
  /* 复选框文本调整 */
  .el-form-item__content {
    font-size: 12px;
  }
  
  /* 增加触摸友好的点击区域 */
  .el-checkbox__input {
    transform: scale(1.1); /* 适当放大复选框 */
  }
  
  /* 增加链接的可点击区域 */
  .login-link a, .register-form a {
    padding: 4px 0;
    display: inline-block;
  }
  
  /* 防止iOS下输入框自动放大 */
  input, textarea {
    font-size: 16px;
  }
}
</style>
