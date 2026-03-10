from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from movie_app.movie.models import Movie
from movie_app.movie.serializers import MovieSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
import re

# Create your views here.

class MovieViewSet(ModelViewSet):
    authentication_classes = []  # 空列表禁用认证
    permission_classes = [AllowAny] # 允许任何用户访问
    queryset = Movie.objects.all()  # 获取数据
    serializer_class = MovieSerializer  # 序列化器

    filter_backends = [OrderingFilter]  # 启用排序过滤器
    ordering_fields = ['rate', 'release_year']  # 支持按评分、年份排序
    ordering = ['-rate']  # 默认按评分降序（热门）

    def get_queryset(self):
        queryset = super().get_queryset()
        # 处理 ids 参数
        ids = self.request.query_params.get('ids')
        if ids:
            id_list = ids.split(',')
            queryset = queryset.filter(id__in=id_list)
        # 0. 按名称搜索
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        # 1. 按category_id过滤类型（电影、电视剧、综艺）
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=int(category_id))

        # 2. 地区筛选
        region = self.request.query_params.get('region')
        if region and region != '全部':
            # 处理地区名称映射到对应的数字ID
            region_mapping = {
                '中国': 1,
                '美国': 2,
                '韩国': 3,
                '日本': 4,
                '其他': 5
            }
            if region in region_mapping:
                queryset = queryset.filter(region=region_mapping[region])

        # 3. 年份筛选
        year = self.request.query_params.get('year')
        if year and year != '选择年份':
            try:
                # 支持单个年份或年份范围
                if '-' in year:
                    start_year, end_year = year.split('-')
                    queryset = queryset.filter(release_year__gte=int(start_year), release_year__lte=int(end_year))
                else:
                    queryset = queryset.filter(release_year=int(year))
            except ValueError:
                pass

        # 4. 类型筛选
        types = self.request.query_params.get('types')
        if types:
            # 处理多个类型，使用OR条件
            from django.db.models import Q
            type_list = types.split(',')
            type_filters = Q()
            for type_name in type_list:
                type_filters |= Q(types__icontains=type_name)
            queryset = queryset.filter(type_filters)

        # 5. Top250筛选
        # if self.request.query_params.get('top250') == 'true':
        #     queryset = queryset.filter(rate__gte=8).order_by('-rate')
        # if self.request.query_params.get('top250') == 'true':
        #     queryset = queryset.order_by('-rate')

        # 6. 热门筛选逻辑
        if self.request.query_params.get('hot') == 'true':
            queryset = queryset.filter(rate__gt=8, release_year__gte=2022)

        # 7. 排序逻辑增强 - 处理sort参数
        sort = self.request.query_params.get('sort')
        # 优先使用自定义sort逻辑，无论是否有ordering参数
        if sort:
            if sort == 'year_asc':
                queryset = queryset.order_by('release_year')
            elif sort == 'year_desc':
                queryset = queryset.order_by('-release_year')
            elif sort == 'rating_asc':
                queryset = queryset.order_by('rate')
            elif sort == 'rating_desc':
                queryset = queryset.order_by('-rate')
            # 否则保持OrderingFilter的默认排序或之前的排序
        return queryset

    # def list(self, request, *args, **kwargs):
    #     """
    #     重写 list 方法以支持 top250 限制
    #     """
    #     response = super().list(request, *args, **kwargs)
    #     if request.query_params.get('top250') == 'true':
    #         # 限制返回结果为前250条
    #         if hasattr(response, 'data') and isinstance(response.data, list):
    #             response.data = response.data[:250]
    #         elif hasattr(response, 'data') and 'results' in response.data:
    #             response.data['results'] = response.data['results'][:250]
    #     return response


@authentication_classes([])
@permission_classes([AllowAny])
@api_view(['GET'])
def get_related_movies(request, movie_id):
    try:
        current_movie = Movie.objects.get(id=movie_id)

        # 获取当前内容的类型（category_id）和题材类型
        current_category = current_movie.category_id
        current_types = re.split(r'/', current_movie.types.strip())

        # 筛选：同类型 + 同题材（排除自身）
        # 替换整个筛选部分：
        related_movies = Movie.objects.filter(
            category_id=current_category,  # 保证类型一致（电影/电视/综艺）
        )

        # 添加类型标签的筛选条件，使用OR逻辑，增加灵活性
        has_type_filter = False
        from django.db.models import Q
        type_filter = Q()
        
        # 收集所有非空类型标签
        valid_types = [t for t in current_types if t.strip()]
        
        if valid_types:
            # 使用OR条件匹配任何一个类型标签
            for type_tag in valid_types:
                type_filter |= Q(types__icontains=type_tag.strip())
            related_movies = related_movies.filter(type_filter)
            has_type_filter = True

        # 排除当前电影
        related_movies = related_movies.exclude(id=movie_id)
        
        # 如果没有找到相关电影，返回同类型的热门电影
        if not related_movies.exists():
            related_movies = Movie.objects.filter(category_id=current_category).exclude(id=movie_id).order_by('-rate')[:10]
        else:
            # 限制数量并排序
            related_movies = related_movies.order_by('-rate')[:10]

        serializer = MovieSerializer(related_movies, many=True)
        return Response(serializer.data)

    except Movie.DoesNotExist:
        return Response({"error": "内容不存在"}, status=404)
