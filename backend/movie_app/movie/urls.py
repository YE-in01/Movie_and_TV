from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, get_related_movies


# 创建路由器
router = DefaultRouter()
# 注册电影视图集
router.register(r'', MovieViewSet, basename='movie')

urlpatterns = [
    # 相关电影接口
    path('<int:movie_id>/related/', get_related_movies, name='related_movies'),
    # 包含路由器生成的URL
    *router.urls
]