from django.contrib.auth.models import AbstractUser
from django.db import models
from movie_app.movie.models import Movie

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 自定义用户管理器（必须实现）
class UserManager(BaseUserManager):
    def create_user(self, uname, email, password=None, **extra_fields):
        if not email:
            raise ValueError('必须提供邮箱')
        email = self.normalize_email(email)
        user = self.model(uname=uname, email=email,** extra_fields)
        user.set_password(password)  # 自动加密密码
        user.save(using=self._db)
        return user

    def create_superuser(self, uname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(uname, email, password,** extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    """用户模型类，继承AbstractBaseUser以支持Django认证系统"""
    uid = models.AutoField(primary_key=True, unique=True, verbose_name="用户ID")
    uname = models.CharField(max_length=100, unique=True, verbose_name="用户名")
    email = models.EmailField(unique=True, verbose_name="邮箱")  # 作为登录凭证需唯一
    phonenum = models.CharField(max_length=20, verbose_name="电话号码")
    is_email_verified = models.BooleanField(default=False, verbose_name="邮箱是否验证")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    is_staff = models.BooleanField(default=False, verbose_name="是否为管理员")

    # 必须定义的认证相关属性
    USERNAME_FIELD = 'uname'  # 登录时使用的字段（邮箱）
    REQUIRED_FIELDS = ['email']  # 创建超级用户时必须提供的字段

    objects = UserManager()  # 关联自定义用户管理器

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        app_label = 'users'
        managed = False

    def __str__(self):
        return self.uname

# class Users(models.Model):
#     """用户模型类，对应数据库中的用户表"""
#     uid = models.AutoField(primary_key=True, unique=True, verbose_name="用户ID")  # 自动增长
#     uname = models.CharField(max_length=100, unique=True, verbose_name="用户名")
#     email = models.EmailField(verbose_name="邮箱")
#     phonenum = models.CharField(max_length=20, verbose_name="电话号码")
#     password = models.CharField(max_length=128, verbose_name="密码")
#     is_email_verified = models.BooleanField(default=False, verbose_name="邮箱是否验证")
#
#
#     class Meta:
#         # 指定数据库表名，如果不指定，Django会默认使用"app名称_模型类名小写"作为表名
#         db_table = "users"  # 可根据实际表名修改
#         verbose_name = "用户"
#         verbose_name_plural = verbose_name
#         app_label = 'users'
#         managed = False
#
#     def __str__(self):
#         # 定义模型的字符串表示，方便在admin后台等地方显示
#         return self.uname

# 收藏关联模型（对应collect表）
class Collect(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="收藏记录ID")
    # 关联users表（通过uid字段）
    user = models.ForeignKey(
        Users,
        on_delete=models.DO_NOTHING,  # 已有表，避免自动删除
        db_column="uid",  # 对应collect表中的uid字段
        related_name="collections",  # 反向查询：用户的所有收藏
        verbose_name="关联用户"
    )
    # 关联movies_and_tv表（通过mid字段）
    movie_tv = models.ForeignKey(
        Movie,
        on_delete=models.DO_NOTHING,  # 已有表，避免自动删除
        db_column="mid",  # 对应collect表中的mid字段
        related_name="collect_records",  # 反向查询：影视的所有收藏记录
        verbose_name="关联影视"
    )

    class Meta:
        db_table = "collect"  # 对应数据库中的collect表
        managed = False  # 已有表，不允许Django管理表结构
        verbose_name = "收藏记录"
        verbose_name_plural = verbose_name
        # 如果数据库中有联合唯一约束，需同步定义（避免重复收藏）
        unique_together = ("user", "movie_tv")
        app_label = 'users'

    def __str__(self):
        return f"{self.user.uname} 收藏了 {self.movie_tv.name}"


class Profile(models.Model):
    """用户资料模型类，存储用户的详细信息"""
    # 用户ID，作为主键，并与Users表的uid关联
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,  # 同时删除：当用户被删除时，资料也一并删除
        primary_key=True,  # 使用user_id作为主键
        db_column="uid",  # 对应数据库字段名为uid
        related_name="profile",  # 反向查询：user.profile
        verbose_name="用户"
    )

    @property
    def uname(self):
        return self.user.uname

    # 个性签名，默认值为'无'
    signature = models.CharField(
        max_length=200,
        default='无',
        verbose_name="个性签名",
        blank=True
    )

    # 性别字段，可使用CharField或者IntegerField
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
        ('secret', '保密'),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='secret',
        verbose_name="性别"
    )

    # 生日字段，可为空
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name="生日"
    )

    # 所在地字段，使用TextField支持较长地址
    location = models.TextField(
        blank=True,
        verbose_name="所在地"
    )

    class Meta:
        db_table = "profile"  # 指定数据库表名
        verbose_name = "用户资料"
        verbose_name_plural = verbose_name
        app_label = 'users'

    def __str__(self):
        return f"{self.user.uname} 的资料"



