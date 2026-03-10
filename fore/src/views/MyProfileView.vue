<template>
  <div class="my-profile">
    <div class="page-header">
      <h1 class="page-title">个人中心</h1>
      <p class="page-description">管理您的个人信息和偏好设置</p>
    </div>

    <div class="profile-container">
      <el-row :gutter="20">
        <!-- 左侧个人信息卡片 -->
        <el-col :span="6">
          <el-card class="profile-card sci-fi-card">
            <div class="profile-avatar">
              <el-icon class="avatar-placeholder-icon"><User /></el-icon>
            </div>

            <div class="user-basic-info">
              <h2 class="username">{{ userInfo.username }}</h2>
              <div class="user-level">
                <el-tag :type="getLevelType(userInfo.level)" size="small">
                  Lv.{{ userInfo.level }} {{ getLevelName(userInfo.level) }}
                </el-tag>
              </div>
              <p class="user-signature">{{ userInfo.signature || '这个人很懒，什么都没有留下~' }}</p>
            </div>

            <div class="user-stats">
              <div class="stat-item">
                <p class="stat-value">{{ userInfo.reviewCount }}</p>
                <p class="stat-label">评论</p>
              </div>
              <div class="stat-item">
                <p class="stat-value">{{ userInfo.favoritesCount }}</p>
                <p class="stat-label">收藏</p>
              </div>
            </div>

            <div class="profile-actions">
              <el-button type="primary" @click="showEditProfileDialog = true">编辑资料</el-button>
              <el-button @click="showSettingsDialog = true">账号设置</el-button>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧内容区域 -->
        <el-col :span="18">
          <el-tabs v-model="activeTab" class="profile-tabs">


            <!-- 我的评论 -->
            <el-tab-pane label="我的评论" name="myComments">
              <el-card class="content-card sci-fi-card">
                <template #header>
                  <div class="card-header">
                    <span>我的评论</span>
                    <el-button type="primary" size="small" @click="$router.push('/reviews')">写评论</el-button>
                  </div>
                </template>

                <div v-if="myComments.length > 0" class="comments-list">
                  <div v-for="comment in myComments" :key="comment.id" class="comment-item">
                    <div class="comment-movie">
                      <img :src="comment.moviePoster" :alt="comment.movieTitle" class="movie-poster">
                      <div class="movie-info">
                        <router-link :to="'/movie/' + comment.movieId" class="movie-title">{{ comment.movieTitle }}</router-link>
                        <p class="movie-meta">{{ comment.movieYear }} · {{ formatGenre(comment.movieGenre) }}</p>
                      </div>
                      <div class="movie-rating">
                        <el-rate v-model="comment.rating" disabled text-color="#ff9900"></el-rate>
                      </div>
                    </div>

                    <div class="comment-content">
                      <p>{{ comment.content }}</p>
                      <div class="comment-meta">
                        <span class="comment-time">{{ formatTime(comment.createTime) }}</span>
                        <div class="comment-actions">
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
                  <el-empty description="您还没有发表任何评论">
                    <el-button type="primary" @click="$router.push('/reviews')">发表第一条评论</el-button>
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
            </el-tab-pane>

            <!-- 我的收藏 -->
            <el-tab-pane label="我的收藏" name="favorites">
              <el-card class="content-card sci-fi-card">
                <template #header>
                  <div class="card-header">
                    <span>我的收藏</span>
                    <div class="header-actions">
                      <el-select v-model="favoritesFilter" size="small" style="width: 120px;">
                        <el-option label="全部类型" value=""></el-option>
                        <el-option label="电影" value="movie"></el-option>
                        <el-option label="电视剧" value="tv"></el-option>
                        <el-option label="综艺" value="variety"></el-option>
                      </el-select>
                    </div>
                  </div>
                </template>

                <div v-if="favorites.length > 0" class="favorites-grid">
                  <div v-for="item in favorites" :key="item.id" class="favorite-item">
                    <div class="favorite-poster">
                      <img :src="item.poster" :alt="item.title">
                      <div class="favorite-actions">
                        <el-button type="text" icon="el-icon-view" @click="viewItem(item)"></el-button>
                        <el-button type="text" icon="el-icon-delete" @click="removeFromFavorites(item.id)"></el-button>
                      </div>
                    </div>
                    <router-link :to="'/' + item.type + '/' + item.id" class="favorite-title">{{ item.title }}</router-link>
                    <p class="favorite-meta">{{ item.year }} · {{ formatGenre(item.genre) }}</p>
                    <div class="favorite-rating">
                      <el-rate v-model="item.rating" disabled text-color="#ff9900" show-score></el-rate>
                    </div>
                  </div>
                </div>

                <div v-else class="empty-state">
                  <el-empty description="您还没有收藏任何内容"></el-empty>
                </div>

                <div class="pagination-container" v-if="favorites.length > 0">
                  <el-pagination
                    background
                    layout="prev, pager, next"
                    :total="favoritesTotal"
                    :page-size="favoritesPageSize"
                    :current-page="favoritesPage"
                    @current-change="handleFavoritesPageChange"
                  >
                  </el-pagination>
                </div>
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </div>

    <!-- 编辑个人资料对话框 -->
    <el-dialog
      v-model="showEditProfileDialog"
      title="编辑个人资料"
      width="50%"
      class="edit-profile-dialog sci-fi-dialog"
    >
      <el-form :model="editProfileForm" :rules="profileRules" ref="profileFormRef" label-width="80px">

          

        
        <el-form-item label="用户名" prop="username">
          <el-input v-model="editProfileForm.username"></el-input>
        </el-form-item>
        <el-form-item label="个性签名" prop="signature">
          <el-input 
            v-model="editProfileForm.signature" 
            type="textarea" 
            :rows="3"
            maxlength="100"
            show-word-limit
            placeholder="介绍一下自己吧..."
          ></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="editProfileForm.gender">
            <el-radio label="male">男</el-radio>
            <el-radio label="female">女</el-radio>
            <el-radio label="secret">保密</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="生日" prop="birthday">
          <el-date-picker
            v-model="editProfileForm.birthday"
            type="date"
            placeholder="选择日期"
            style="width: 100%;"
            value-format="YYYY-MM-DD"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item label="所在地" prop="location">
          <el-cascader
            v-model="editProfileForm.location"
            :options="locationOptions"
            placeholder="请选择所在地"
            style="width: 100%;"
          >
          </el-cascader>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditProfileDialog = false">取消</el-button>
          <el-button type="primary" @click="saveProfile">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 账号设置对话框 -->
    <el-dialog
      v-model="showSettingsDialog"
      title="账号设置"
      width="50%"
      class="settings-dialog sci-fi-dialog"
    >
      <el-tabs v-model="settingsTab" class="settings-tabs">
        <el-tab-pane label="账号安全" name="security">
          <div class="security-settings">
            <div class="setting-item">
              <div class="setting-info">
                <h4>登录密码</h4>
                <p>定期更换密码，保护账号安全</p>
              </div>
              <el-button type="text" @click="showChangePasswordDialog = true">修改</el-button>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>用户名</h4>
                <p>{{ userInfo.username || '未设置' }}</p>
              </div>
              <el-button type="text" @click="showEditProfileDialog = true">修改</el-button>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>绑定邮箱</h4>
                <p>已绑定：{{ userInfo.email || '未绑定' }}</p>
              </div>
              <el-button type="text" @click="showEmailDialog = true">{{ userInfo.email ? '更换' : '绑定' }}</el-button>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="隐私设置" name="privacy">
          <div class="privacy-settings">
            <el-form :model="privacyForm" label-width="120px">
              <el-form-item label="谁可以看我的影评">
                <el-radio-group v-model="privacyForm.reviewVisibility">
                  <el-radio label="everyone">所有人</el-radio>
                  <el-radio label="followers">仅粉丝</el-radio>
                  <el-radio label="myself">仅自己</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="谁可以看我的收藏">
                <el-radio-group v-model="privacyForm.favoritesVisibility">
                  <el-radio label="everyone">所有人</el-radio>
                  <el-radio label="followers">仅粉丝</el-radio>
                  <el-radio label="myself">仅自己</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="接收评论回复通知">
                <el-switch v-model="privacyForm.replyNotification"></el-switch>
              </el-form-item>

              <el-form-item label="接收系统通知">
                <el-switch v-model="privacyForm.systemNotification"></el-switch>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>

        <el-tab-pane label="偏好设置" name="preference">
          <div class="preference-settings">
            <el-form :model="preferenceForm" label-width="120px">
              <el-form-item label="主题设置">
                <el-radio-group v-model="preferenceForm.theme">
                  <el-radio label="auto">跟随系统</el-radio>
                  <el-radio label="dark">深色模式</el-radio>
                  <el-radio label="light">浅色模式</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="语言设置">
                <el-select v-model="preferenceForm.language" style="width: 100%;">
                  <el-option label="简体中文" value="zh-CN"></el-option>
                  <el-option label="繁體中文" value="zh-TW"></el-option>
                  <el-option label="English" value="en-US"></el-option>
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
      </el-tabs>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showSettingsDialog = false">取消</el-button>
          <el-button type="primary" @click="saveSettings">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showChangePasswordDialog"
      title="修改密码"
      width="40%"
      class="change-password-dialog sci-fi-dialog"
    >
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="80px">
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password></el-input>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showChangePasswordDialog = false">取消</el-button>
          <el-button type="primary" @click="changePassword">确认修改</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 邮箱绑定对话框 -->
    <el-dialog
      v-model="showEmailDialog"
      :title="userInfo.email ? '更换邮箱' : '绑定邮箱'"
      width="40%"
      class="email-dialog sci-fi-dialog"
    >
      <el-form :model="emailForm" :rules="emailRules" ref="emailFormRef" label-width="80px">
        <el-form-item label="邮箱地址" prop="email">
          <el-input v-model="emailForm.email" type="email" placeholder="请输入邮箱地址"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <div class="code-input-container">
            <el-input v-model="emailForm.code" placeholder="请输入验证码"></el-input>
            <el-button 
              type="primary" 
              :disabled="codeCountdown > 0" 
              @click="sendEmailCode"
              class="code-button"
            >
              {{ codeCountdown > 0 ? `${codeCountdown}秒后重试` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEmailDialog = false">取消</el-button>
          <el-button type="primary" @click="bindEmail" :loading="emailSubmitting">确认{{ userInfo.email ? '更换' : '绑定' }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Delete, Star, User } from '@element-plus/icons-vue'
import { userApi } from '@/api/api'
import { formatGenre } from '@/utils/genre.js'

export default {
  name: 'MyProfileView',
  components: {
    Edit,
    Delete,
    Star,
    User
  },
  setup() {
    // 当前激活的标签页
    const activeTab = ref('myComments')

    const settingsTab = ref('security')

    // 对话框显示状态
    const showEditProfileDialog = ref(false)
    const showSettingsDialog = ref(false)
    const showChangePasswordDialog = ref(false)
    const showEmailDialog = ref(false)

    // 用户信息
    const userInfo = ref({
      id: null,
      username: '',
      level: 1,
      signature: '',
      email: '',
      reviewCount: 0,
      favoritesCount: 0
    })


    
    // 我的评论
    const myComments = ref([])

    // 我的收藏
    const favorites = ref([])

    

    // 筛选条件
    const favoritesFilter = ref('')

    // 分页数据

    const myCommentsPage = ref(1)
    const myCommentsPageSize = ref(10)
    const myCommentsTotal = ref(0)

    const favoritesPage = ref(1)
    const favoritesPageSize = ref(12)
    const favoritesTotal = ref(0)

    

    

    // 编辑个人资料表单
    const editProfileForm = reactive({
      username: '',
      signature: '',
      gender: 'secret',
      birthday: null,
      location: [],

    })

    // 表单验证规则
    const profileRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ]
    }

    // 地区选项
     const locationOptions = [
      {
        value: 'beijing',
        label: '北京',
        children: [
          { value: 'dongcheng', label: '东城区' },
          { value: 'xicheng', label: '西城区' },
         { value: 'chaoyang', label: '朝阳区' },
          { value: 'haidian', label: '海淀区' }
        ]
      },
      {
        value: 'shanghai',
        label: '上海',
        children: [
          { value: 'huangpu', label: '黄浦区' },
          { value: 'xuhui', label: '徐汇区' },
          { value: 'changning', label: '长宁区' },
          { value: 'jingan', label: '静安区' }
        ]
      }
      // 更多地区选项...
    ]

    // 隐私设置表单
    const privacyForm = reactive({
      reviewVisibility: 'everyone',
      favoritesVisibility: 'everyone',
      
      replyNotification: true,
      systemNotification: false
    })

    // 偏好设置表单
    const preferenceForm = reactive({
      theme: 'auto',
      language: 'zh-CN'
    })

    // 修改密码表单
    const passwordForm = reactive({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
    
    // 邮箱绑定表单
    const emailForm = reactive({
      email: '',
      code: ''
    })
    
    // 邮箱验证码倒计时
    const codeCountdown = ref(0)
    
    // 邮箱提交状态
    const emailSubmitting = ref(false)

    // 邮箱验证规则
    const emailRules = {
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      code: [
        { required: true, message: '请输入验证码', trigger: 'blur' },
        { len: 6, message: '验证码长度应为6位', trigger: 'blur' }
      ]
    }
    
    // 密码验证规则
    const passwordRules = {
      currentPassword: [
        { required: true, message: '请输入当前密码', trigger: 'blur' }
      ],
      newPassword: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请确认新密码', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== passwordForm.newPassword) {
              callback(new Error('两次输入密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }

    // 获取用户等级类型
    const getLevelType = (level) => {
      if (level >= 1 && level <= 3) return 'info'
      if (level >= 4 && level <= 6) return 'success'
      if (level >= 7 && level <= 9) return 'warning'
      if (level >= 10) return 'danger'
      return ''
    }

    // 获取用户等级名称
    const getLevelName = (level) => {
      if (level >= 1 && level <= 3) return '新手'
      if (level >= 4 && level <= 6) return '影迷'
      if (level >= 7 && level <= 9) return '达人'
      if (level >= 10) return '专家'
      return ''
    }

    // 格式化时间
    const formatTime = (timeStr) => {
      const date = new Date(timeStr)
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



    // 编辑评论
    const editComment = (comment) => {
      // 跳转到评论编辑页面
      console.log('编辑评论:', comment)
      ElMessage.info('跳转到评论编辑页面')
    }

    // 删除评论
    const deleteComment = (id) => {
      ElMessageBox.confirm(
        '确定要删除这条评论吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        const index = myComments.value.findIndex(item => item.id === id)
        if (index !== -1) {
          myComments.value.splice(index, 1)
          myCommentsTotal.value -= 1
          ElMessage.success('评论已删除')
        }
      }).catch(() => {})
    }

    // 点赞/取消点赞
    const toggleLike = (comment) => {
      comment.isLiked = !comment.isLiked
      if (comment.isLiked) {
        comment.likeCount += 1
        ElMessage.success('已点赞')
      } else {
        comment.likeCount -= 1
        ElMessage.info('已取消点赞')
      }
    }

    // 查看收藏项
    const viewItem = (item) => {
      // 跳转到详情页
      ElMessage.info(`跳转到${item.type}详情页`)
    }

    // 从收藏中移除
    const removeFromFavorites = (id) => {
      ElMessageBox.confirm(
        '确定要取消收藏吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        const index = favorites.value.findIndex(item => item.id === id)
        if (index !== -1) {
          favorites.value.splice(index, 1)
          favoritesTotal.value -= 1
          ElMessage.success('已取消收藏')
        }
      }).catch(() => {})
    }

    // 保存个人资料
    const saveProfile = () => {
      // 构造发送给后端的数据
      const profileData = {
        username: editProfileForm.username,
        signature: editProfileForm.signature,
        gender: editProfileForm.gender,
        birthday: editProfileForm.birthday,
        location: editProfileForm.location
      };

      // 调用API更新用户资料
      userApi.updateUserInfo(profileData)
        .then(data => {
          // 更新本地用户信息
          userInfo.value.username = data.uname;
          userInfo.value.signature = data.signature;
          showEditProfileDialog.value = false;
          ElMessage.success('个人资料已保存');
        })
        .catch(error => {
          ElMessage.error(error.response?.data?.error || '个人资料更新失败，请稍后重试');
        });
    };

    // 保存设置
    const saveSettings = () => {
      // 保存隐私设置
      const privacyData = {
        reviewVisibility: privacyForm.reviewVisibility,
        favoritesVisibility: privacyForm.favoritesVisibility,
        replyNotification: privacyForm.replyNotification,
        systemNotification: privacyForm.systemNotification
      };
      
      // 保存偏好设置
      const preferenceData = {
        theme: preferenceForm.theme,
        language: preferenceForm.language
      };
      
      // 调用API保存设置
      Promise.all([
        userApi.updatePrivacySettings(privacyData),
        userApi.updatePreferenceSettings(preferenceData)
      ])
      .then(() => {
        showSettingsDialog.value = false;
        ElMessage.success('设置已保存');
        // 应用主题设置
        applyTheme(preferenceForm.theme);
      })
      .catch(error => {
        ElMessage.error(error.response?.data?.error || '设置保存失败，请稍后重试');
      });
    }

    // 发送邮箱验证码
    const sendEmailCode = () => {
      // 验证邮箱格式
      if (!emailForm.email) {
        ElMessage.error('请先输入邮箱地址');
        return;
      }
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(emailForm.email)) {
        ElMessage.error('请输入正确的邮箱格式');
        return;
      }
      
      // 调用API发送验证码
      userApi.sendEmailCode({ email: emailForm.email })
        .then(() => {
          ElMessage.success('验证码已发送，请查收邮件');
          // 开始倒计时
          codeCountdown.value = 60;
          const timer = setInterval(() => {
            codeCountdown.value--;
            if (codeCountdown.value <= 0) {
              clearInterval(timer);
            }
          }, 1000);
        })
        .catch(error => {
          ElMessage.error(error.response?.data?.error || '发送验证码失败，请稍后重试');
        });
    };
    
    // 绑定/更换邮箱
    const bindEmail = () => {
      // 简单验证
      if (!emailForm.email) {
        ElMessage.error('请输入邮箱地址');
        return;
      }
      
      if (!emailForm.code) {
        ElMessage.error('请输入验证码');
        return;
      }
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(emailForm.email)) {
        ElMessage.error('请输入正确的邮箱格式');
        return;
      }
      
      emailSubmitting.value = true;
      
      // 调用API绑定/更换邮箱
      userApi.bindEmail({
        email: emailForm.email,
        code: emailForm.code
      })
      .then(() => {
        ElMessage.success(userInfo.value.email ? '邮箱更换成功' : '邮箱绑定成功');
        userInfo.value.email = emailForm.email;
        showEmailDialog.value = false;
        
        // 重置表单
        emailForm.email = '';
        emailForm.code = '';
        codeCountdown.value = 0;
      })
      .catch(error => {
        ElMessage.error(error.response?.data?.error || (userInfo.value.email ? '邮箱更换失败' : '邮箱绑定失败'));
      })
      .finally(() => {
        emailSubmitting.value = false;
      });
    };
    
    // 应用主题
    const applyTheme = (theme) => {
      if (theme === 'auto') {
        // 跟随系统主题
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
      } else {
        // 应用指定主题
        document.documentElement.setAttribute('data-theme', theme);
      }
      
      // 保存主题到本地存储，以便在页面刷新后保持
      localStorage.setItem('user-theme', theme);
    };
    
    // 修改密码
    const changePassword = () => {
      // 字段名转换，匹配后端期望的格式
      const changePasswordData = {
        old_password: passwordForm.currentPassword,
        new_password: passwordForm.newPassword,
        confirm_password: passwordForm.confirmPassword
      }
      
      // 调用API修改密码
      userApi.changePassword(changePasswordData)
        .then(() => {
          showChangePasswordDialog.value = false
          showSettingsDialog.value = false
          ElMessage.success('密码修改成功')
          // 清空表单
          passwordForm.currentPassword = ''
          passwordForm.newPassword = ''
          passwordForm.confirmPassword = ''
        })
        .catch(error => {
          ElMessage.error(error.response?.data?.error || '密码修改失败，请稍后重试')
        })
    }

    // 分页处理函数

    const handleMyCommentsPageChange = (page) => {
      myCommentsPage.value = page
      // 这里应该调用API获取对应页的数据
    }

    const handleFavoritesPageChange = (page) => {
      favoritesPage.value = page
      // 这里应该调用API获取对应页的数据
    }

    

    

    onMounted(() => {
      // 页面加载时获取用户数据
      getUserInfo()
    })
    
    // 获取用户信息
    const getUserInfo = () => {
      userApi.getUserInfo()
        .then(data => {
          userInfo.value = {
            ...userInfo.value,
            username: data.uname,
            signature: data.signature || '',
            email: data.email || '',

          };

          // 更新编辑表单数据
          editProfileForm.username = data.uname;
          editProfileForm.signature = data.signature || '';
          editProfileForm.gender = data.gender || 'secret';
          editProfileForm.birthday = data.birthday || null;
          editProfileForm.location = data.location || '';

        })
        .catch(error => {
          console.error('获取用户信息失败:', error);
          ElMessage.error('获取用户信息失败，请稍后重试');
        });
        
      // 获取用户隐私设置
      userApi.getPrivacySettings()
        .then(data => {
          privacyForm.reviewVisibility = data.reviewVisibility || 'everyone';
          privacyForm.favoritesVisibility = data.favoritesVisibility || 'everyone';
          privacyForm.replyNotification = data.replyNotification !== undefined ? data.replyNotification : true;
          privacyForm.systemNotification = data.systemNotification !== undefined ? data.systemNotification : false;
        })
        .catch(error => {
          console.error('获取隐私设置失败:', error);
        });
        
      // 获取用户偏好设置
      userApi.getPreferenceSettings()
        .then(data => {
          preferenceForm.theme = data.theme || 'auto';
          preferenceForm.language = data.language || 'zh-CN';
          // 应用主题设置
          applyTheme(preferenceForm.theme);
        })
        .catch(error => {
          console.error('获取偏好设置失败:', error);
        });
    };

    return {
      // 标签页
      activeTab,
      settingsTab,

      // 对话框
      showEditProfileDialog,
      showSettingsDialog,
      showChangePasswordDialog,
      showEmailDialog,

      // 用户信息
      userInfo,

      // 数据列表
      myComments,
      favorites,

      // 筛选条件
      favoritesFilter,

      // 分页
      myCommentsPage,
      myCommentsPageSize,
      myCommentsTotal,
      favoritesPage,
      favoritesPageSize,
      favoritesTotal,

      // 表单
      editProfileForm,
      profileRules,
      locationOptions,
      privacyForm,
      preferenceForm,
      passwordForm,
      passwordRules,
      emailForm,
      emailRules,
      codeCountdown,
      emailSubmitting,

      // 方法
      getLevelType,
      getLevelName,
      formatTime,
      formatGenre,
      editComment,
      deleteComment,
      toggleLike,
      viewItem,
      removeFromFavorites,
      saveProfile,
      saveSettings,
      changePassword,
      sendEmailCode,
      bindEmail,
      applyTheme,
      getUserInfo,
      handleMyCommentsPageChange,
      handleFavoritesPageChange
    }
  }
}
</script>

<style scoped>
.my-profile {
  padding: 20px;
  min-height: calc(100vh - 60px);
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 5px;
}

.page-description {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.profile-container {
  margin-top: 20px;
}

/* 个人信息卡片 */
.profile-card {
  text-align: center;
  margin-bottom: 20px;
}

.profile-avatar {
  position: relative;
  margin-bottom: 15px;
}

.avatar-uploader {
  display: inline-block;
}

.avatar-uploader .avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
  border: 3px solid rgba(100, 200, 255, 0.3);
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
  border-radius: 50%;
  background-color: rgba(20, 30, 48, 0.7);
  border: 3px dashed rgba(100, 200, 255, 0.3);
  cursor: pointer;
}

.avatar-edit-hint {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: #ffffff;
  padding: 5px 0;
  border-bottom-left-radius: 60px;
  border-bottom-right-radius: 60px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.profile-avatar:hover .avatar-edit-hint {
  opacity: 1;
}

.user-basic-info {
  margin-bottom: 20px;
}

.username {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #ffffff;
}

.user-level {
  margin-bottom: 10px;
}

.user-signature {
  color: #ffffff;
  font-size: 16px;
  margin: 0;
  line-height: 1.5;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  padding: 15px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #ffffff;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  margin: 0;
}

.profile-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* 内容卡片 */
.content-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

/* 标签页样式 */
.profile-tabs :deep(.el-tabs__header) {
  margin-bottom: 15px;
}

.profile-tabs :deep(.el-tabs__item) {
  color: rgba(255, 255, 255, 0.7);
}

.profile-tabs :deep(.el-tabs__item.is-active) {
  color: #00ccff;
}

.profile-tabs :deep(.el-tabs__active-bar) {
  background-color: #00ccff;
}



/* 评论列表样式 */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  padding: 15px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.05);
}

.comment-movie {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.movie-poster {
  width: 60px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 10px;
}

.movie-info {
  flex: 1;
}

.movie-title {
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
}

.movie-title:hover {
  color: #00ccff;
}

.movie-meta {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  margin: 5px 0;
}

.movie-rating {
  margin-left: 10px;
}

.comment-content p {
  color: #ffffff;
  line-height: 1.5;
  margin-bottom: 10px;
  font-size: 16px;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
}

.comment-actions {
  display: flex;
  gap: 15px;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  transition: color 0.3s;
}

.action-item:hover {
  color: #00ccff;
}

.action-item.active {
  color: #ff6b6b;
}

/* 收藏网格样式 */
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.favorite-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s;
}

.favorite-item:hover {
  transform: translateY(-5px);
}

.favorite-poster {
  position: relative;
  margin-bottom: 10px;
}

.favorite-poster img {
  width: 100%;
  height: 260px;
  object-fit: cover;
  border-radius: 8px;
}

.favorite-actions {
  position: absolute;
  top: 0;
  right: 0;
  padding: 5px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.3s;
}

.favorite-item:hover .favorite-actions {
  opacity: 1;
}

.favorite-actions .el-button {
  background-color: rgba(0, 0, 0, 0.6);
  color: #ffffff;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.favorite-title {
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
  display: block;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.favorite-title:hover {
  color: #00ccff;
}

.favorite-meta {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  margin: 5px 0;
}

.favorite-rating {
  margin-top: 5px;
}

/* 用户列表样式 */
.user-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.05);
  transition: background-color 0.3s;
}

.user-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
  display: block;
  margin-bottom: 5px;
}

.user-name:hover {
  color: #00ccff;
}

.user-desc {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  margin: 5px 0;
}

.user-stats {
  display: flex;
  gap: 15px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
}

.user-actions {
  display: flex;
  gap: 10px;
}



/* 空状态样式 */
.empty-state {
  margin: 30px 0;
  text-align: center;
}

/* 对话框样式 */
.edit-profile-dialog :deep(.el-dialog__header),
.settings-dialog :deep(.el-dialog__header),
.change-password-dialog :deep(.el-dialog__header) {
  background-color: rgba(20, 30, 48, 0.8);
  border-bottom: 1px solid rgba(100, 200, 255, 0.2);
}

.edit-profile-dialog :deep(.el-dialog__title),
.settings-dialog :deep(.el-dialog__title),
.change-password-dialog :deep(.el-dialog__title) {
  color: #ffffff;
}

.edit-profile-dialog :deep(.el-dialog__body),
.settings-dialog :deep(.el-dialog__body),
.change-password-dialog :deep(.el-dialog__body) {
  background-color: rgba(30, 40, 60, 0.8);
}

/* 邮箱对话框样式 */
.code-input-container {
  display: flex;
  gap: 10px;
}

.code-button {
  flex-shrink: 0;
  width: 120px;
}

/* 设置样式 */
.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.setting-info h4 {
  color: #000000;
  margin-bottom: 5px;
}

.setting-info p {
  color: #666666;
  margin: 0;
}

/* 科幻风格样式 */
.sci-fi-card {
  background: rgba(20, 30, 48, 0.8);
  border: 1px solid rgba(100, 200, 255, 0.2);
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(100, 200, 255, 0.1);
  transition: all 0.3s ease;
}

.sci-fi-card:hover {
  box-shadow: 0 6px 20px rgba(100, 200, 255, 0.2);
  border-color: rgba(100, 200, 255, 0.3);
}

.sci-fi-dialog {
  background: rgba(30, 40, 60, 0.95);
  border: 1px solid rgba(100, 200, 255, 0.3);
}

.sci-fi-dialog :deep(.el-input__inner) {
  background-color: rgba(20, 30, 48, 0.8);
  border: 1px solid rgba(100, 200, 255, 0.2);
  color: #ffffff;
}

.sci-fi-dialog :deep(.el-input__inner:focus) {
  border-color: #00ccff;
  box-shadow: 0 0 0 2px rgba(0, 204, 255, 0.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-container .el-row {
    flex-direction: column;
  }

  .profile-container .el-col {
    width: 100% !important;
    margin-bottom: 20px;
  }



  .comment-movie {
    flex-direction: column;
    align-items: flex-start;
  }

  .movie-poster {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .movie-rating {
    margin-left: 0;
    margin-top: 5px;
  }

  .user-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .user-actions {
    margin-top: 15px;
  }
}
</style>    flex-direction: column;
    align-items: flex-start;
  }
