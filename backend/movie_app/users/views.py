import logging
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from .models import Users, Collect, Movie, Profile
from .serializers import UserRegisterSerializer, UserLoginSerializer, ProfileSerializer, CollectSerializer
from .utils import generate_verify_token, send_verification_email ,verify_token
from rest_framework.permissions import IsAuthenticated, AllowAny

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        # 1. 验证并保存用户
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 2. 创建默认用户资料
        try:
            Profile.objects.create(user=user)
        except Exception as e:
            logger.error(f"创建用户资料失败（用户ID：{user.uid}）: {str(e)}")

        # 3. 调用公共函数发送验证邮件（is_resend=False 标识首次发送）
        send_success, send_msg = send_verification_email(user.email, is_resend=False)

        # 4. 构造响应信息（邮件发送失败不影响注册成功）
        response_msg = "注册成功，请查收邮件验证邮箱（若未收到请检查垃圾邮件箱）"
        if not send_success:
            response_msg += f"【注：邮件发送失败：{send_msg}，可在验证页面重新发送】"

        return Response({
            "code": 201,
            "message": response_msg,
            "data": {
                "uname": user.uname,
                "uid": user.uid,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    authentication_classes = []  # 空列表禁用认证
    permission_classes = [AllowAny]  # 允许任何用户访问
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # 生成令牌（无论邮箱是否验证）
        refresh = RefreshToken.for_user(user)

        if not user.is_email_verified:
            return Response({
                "message": "登录成功，但邮箱未验证",
                "uid": user.uid,
                "uname": user.uname,
                "is_email_verified": False,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_202_ACCEPTED)

        return Response({
            "message": "登录成功",
            "uid": user.uid,
            "uname": user.uname,
            "is_email_verified": user.is_email_verified,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })



class ForgotPasswordView(APIView):
    authentication_classes = []  # 空列表禁用认证
    permission_classes = [AllowAny]  # 允许任何用户访问
    # 忘记密码
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "请提供邮箱"}, status=400)

        try:
            user = Users.objects.get(email=email)
            # 生成重置密码token（有效期30分钟）
            token = generate_verify_token(user.email)  # 复用之前的token生成函数
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}&email={user.email}"

            # 发送重置邮件
            try:
                send_mail(
                    subject="密码重置 - 影视平台",
                    message=f"请点击链接重置密码：\n{reset_url}\n（30分钟内有效）",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False
                )
                return Response({"message": "重置密码邮件已发送"})
            except Exception as e:
                logger.error(f"密码重置邮件发送失败: {e}")
                return Response({"message": "邮件发送失败，请稍后重试"}, status=500)
        except Users.DoesNotExist:
            # 为了安全，即使邮箱不存在也返回相同提示（避免泄露用户信息）
            return Response({"message": "若该邮箱已注册，重置密码邮件将发送"})


class ResetPasswordView(APIView):
    # 更新密码
    def post(self, request):
        token = request.data.get('token')
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # 基础参数校验
        if not all([token, email, new_password, confirm_password]):
            return Response({"error": "参数不完整"}, status=400)
        if new_password != confirm_password:
            return Response({"error": "两次密码不一致"}, status=400)

        # 验证token
        if verify_token(email, token):  # 复用之前的token验证函数
            try:
                user = Users.objects.get(email=email)
                # 更新密码（加密存储）
                user.password = make_password(new_password)
                user.save()
                return Response({"message": "密码重置成功"})
            except Users.DoesNotExist:
                return Response({"error": "用户不存在"}, status=404)
        else:
            return Response({"error": "无效的token或已过期"}, status=400)


class ChangePasswordView(APIView):
    # 修改密码
    permission_classes = [IsAuthenticated]  # 需登录（通过JWT token验证）
    def post(self, request):
        user = request.user  # 从请求中获取当前登录用户
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # 验证旧密码
        if not check_password(old_password, user.password):
            return Response({"error": "旧密码错误"}, status=400)
        # 验证新密码
        if new_password != confirm_password:
            return Response({"error": "两次新密码不一致"}, status=400)

        # 更新密码
        user.password = make_password(new_password)
        user.save()
        return Response({"message": "密码修改成功"})


# 自定义权限：仅允许邮箱已验证的用户
class IsEmailVerified(IsAuthenticated):
    def has_permission(self, request, view):
        # 先检查是否登录，再检查邮箱是否验证
        return super().has_permission(request, view) and request.user.is_email_verified



class CollectViewSet(viewsets.ViewSet):
    """收藏功能接口集"""
    #permission_classes = [IsEmailVerified]  # 仅登录且邮箱验证的用户可访问
    permission_classes = [IsAuthenticated]  # 确保用户已登录
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer

    def create(self, request):
        """添加收藏"""
        mid = request.data.get('mid')  # 获取前端传入的影视ID
        if not mid:
            return Response({"error": "请提供影视ID（mid）"}, status=400)

        # 验证影视是否存在
        try:
            movie = Movie.objects.get(pk=mid)
        except Movie.DoesNotExist:
            return Response({"error": "该影视不存在"}, status=404)

        # 检查是否已收藏
        if Collect.objects.filter(user=request.user, movie_tv=movie).exists():
            return Response({"error": "已收藏该内容，无需重复操作"}, status=400)

        # 创建收藏记录
        Collect.objects.create(user=request.user, movie_tv=movie)
        return Response({"message": "收藏成功"}, status=201)

    def destroy(self, request, pk=None):
        """取消收藏（pk为影视ID）"""
        try:
            # 查找用户对该影视的收藏记录
            collect = Collect.objects.get(user=request.user, movie_tv_id=pk)
            collect.delete()
            return Response({"message": "取消收藏成功"})
        except Collect.DoesNotExist:
            return Response({"error": "未找到收藏记录"}, status=404)

    def list(self, request):
        """查询用户的所有收藏"""
        if not request.user.is_authenticated:
            return Response({"error": "请先登录"}, status=401)

        collects = Collect.objects.filter(user=request.user).select_related('movie_tv')
        data = [{
            "id": collect.id,
            "mid": collect.movie_tv.id,
            "title": collect.movie_tv.name,
        } for collect in collects]
        return Response(data)


class ProfileView(APIView):
    """用户资料接口"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"User {request.user.uid} accessing profile")
        """获取用户资料"""
        try:
            # 获取用户的资料信息
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            # 如果用户资料不存在，创建一个默认资料
            profile = Profile.objects.create(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)


class ProfileUpdateView(APIView):
    """用户资料更新接口"""
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """更新用户资料"""
        try:
            profile = Profile.objects.get(user=request.user)

            # 更新资料字段（不包括用户名）
            profile.signature = request.data.get('signature', profile.signature)
            profile.gender = request.data.get('gender', profile.gender)
            profile.birthday = request.data.get('birthday', profile.birthday)
            profile.location = request.data.get('location', profile.location)

            # 处理用户名更新
            new_uname = request.data.get('username')
            if new_uname and new_uname != profile.user.uname:
                # 检查用户名是否已存在
                if Users.objects.filter(uname=new_uname).exclude(uid=request.user.uid).exists():
                    return Response(
                        {"error": "用户名已存在"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 更新用户表中的用户名
                profile.user.uname = new_uname
                profile.user.save()

            profile.save()

            # 返回更新后的资料
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(
                {"error": "用户资料不存在"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"更新失败: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


# 重新发送验证邮件API（适配前端请求）
@method_decorator(csrf_exempt, name='dispatch')
class ResendVerificationAPIView(APIView):
    """重新发送验证邮件API（复用公共邮件发送逻辑）"""

    def post(self, request):
        email = request.data.get('email')

        # 1. 校验邮箱参数
        if not email:
            return Response({
                "code": 400,
                "error": "请输入注册邮箱",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        # 2. 校验用户是否存在
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({
                "code": 404,
                "error": "该邮箱未注册",
                "data": {}
            }, status=status.HTTP_404_NOT_FOUND)

        # 3. 校验邮箱是否已验证
        if user.is_email_verified:
            return Response({
                "code": 400,
                "error": "该邮箱已验证，无需重复发送",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        # 4. 调用公共函数发送邮件（is_resend=True 标识重新发送）
        success, msg = send_verification_email(email, is_resend=True)

        # 5. 返回响应
        if success:
            return Response({
                "code": 200,
                "message": "验证邮件已重新发送，请查收（若未收到请检查垃圾邮件箱）",
                "data": {}
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "code": 500,
                "error": msg,
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 邮箱验证API（供前端调用）
@method_decorator(csrf_exempt, name='dispatch')
class EmailVerifyAPIView(APIView):
    """邮箱验证接口（供前端调用）"""

    def post(self, request):
        token = request.data.get('token')
        email = request.data.get('email')

        if not token or not email:
            return Response({
                'detail': '验证链接不完整，请检查'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        if verify_token(email, token):
            try:
                user = Users.objects.get(email=email)
                if user.is_email_verified:
                    return Response({
                        'detail': '邮箱已验证，无需重复操作'
                    }, status=status.HTTP_200_OK)
                # 更新验证状态
                user.is_email_verified = True
                user.save()
                return Response({
                    'detail': '邮箱验证成功！'
                }, status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                return Response({
                    'detail': '用户不存在'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                'detail': '验证链接无效或已过期（有效期24小时）'
            }, status=status.HTTP_400_BAD_REQUEST)