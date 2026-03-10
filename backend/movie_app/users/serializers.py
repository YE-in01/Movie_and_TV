from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password

from movie.serializers import MovieSerializer
from .models import Users, Profile
import re
from .models import Collect

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = Users
        fields = ['uid', 'uname', 'email', 'phonenum', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'uid': {'read_only': True}
        }

    def validate_uname(self, value):
        """验证用户名合法性"""
        if len(value) < 3:
            raise serializers.ValidationError("用户名长度不能少于3个字符")
        if Users.objects.filter(uname=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_email(self, value):
        """验证邮箱格式和唯一性"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("邮箱格式不正确")
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return value

    def validate_phonenum(self, value):
        """验证手机号格式"""
        pattern = r'^1[3-9]\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("手机号格式不正确")
        return value

    def validate(self, data):
        # 验证密码一致性
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("两次密码不一致")
        # 密码强度验证
        if len(data['password']) < 6:
            raise serializers.ValidationError('密码长度不能少于6位')
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    uname = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True,required=True)
    def validate(self, data):
        try:
            # 尝试通过用户名或邮箱查找用户
            identifier = data['uname']

            # 判断是邮箱
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', identifier):
                user = Users.objects.get(email=identifier)
            # 否则当作用户名
            else:
                user = Users.objects.get(uname=identifier)
                
            if not check_password(data['password'], user.password):
                raise serializers.ValidationError("用户名或密码错误")
            # 可添加：未验证邮箱的提示（可选）
            # if not user.is_email_verified:
            #     raise serializers.ValidationError("请先验证邮箱")
            return {'user': user}
        except Users.DoesNotExist:
            raise serializers.ValidationError("用户不存在")


class CollectSerializer(serializers.ModelSerializer):
    """收藏记录序列化器"""
    movie = MovieSerializer(source='movie_tv', read_only=True)  # 映射 movie_tv 为 movie
    class Meta:
        model = Collect
        fields = ['id', 'user', 'movie_tv',"movie"]  # 对应collect表的字段
        read_only_fields = ['id']  # id自增，无需前端传入

    def validate(self, data):
        """验证是否重复收藏"""
        user = self.context['request'].user
        mid = data['mid']  # 影视ID
        # 检查该用户是否已收藏该影视
        if Collect.objects.filter(user=user, movie_tv_id=mid).exists():
            raise serializers.ValidationError("已收藏该内容，无需重复操作")
        return data


class ProfileSerializer(serializers.ModelSerializer):
    uname = serializers.CharField(source='user.uname', read_only=True)

    class Meta:
        model = Profile
        fields = ['uname', 'signature', 'gender', 'birthday', 'location']
