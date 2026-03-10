from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView  # 刷新token接口
from .views import (RegisterView, LoginView, EmailVerifyAPIView, ResetPasswordView, ForgotPasswordView, ChangePasswordView,
                    CollectViewSet, ResendVerificationAPIView, ProfileUpdateView, ProfileView)

router = DefaultRouter()
router.register(r'collects', CollectViewSet, basename='collect')  # 收藏接口路由


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # 注册
    path('login/', LoginView.as_view(), name='login'),  # 登录
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新token
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

   # API接口（供前端Vue页面调用）
    path('verify-email/', EmailVerifyAPIView.as_view(), name='api_email_verify'),
    path('resend-verification/', ResendVerificationAPIView.as_view(), name='api_resend_verification'),

    *router.urls
]