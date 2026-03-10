from rest_framework import serializers

from movie_app.movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    # 添加字段映射，使前端能正确获取数据
    title = serializers.CharField(source='name', read_only=True)
    poster = serializers.SerializerMethodField(read_only=True)
    rating = serializers.FloatField(source='rate', read_only=True)
    year = serializers.IntegerField(source='release_year', read_only=True)
    genre = serializers.CharField(source='types', read_only=True)
    description = serializers.CharField(source='review', read_only=True)
    plot = serializers.CharField(source='review', read_only=True)
    aka = serializers.CharField(source='alternate_name', read_only=True)
    releaseDate = serializers.DateField(source='release_date', read_only=True)
    type = serializers.SerializerMethodField(read_only=True)

    def get_poster(self, obj):
        if obj.poster_url and hasattr(obj.poster_url, 'url'):
            # 对于ImageField，直接使用其url属性
            return obj.poster_url.url
        return None
        
    def get_type(self, obj):
        # 将category_id转换为对应的类型名称
        category_map = {
            1: 'movie',
            2: 'tv',
            3: 'variety'
        }
        return category_map.get(obj.category_id, 'movie')

    class Meta:
        model = Movie
        fields = ["id", "name", "title", "poster", "rate", "rating", "release_year", "year", "types",
                  "genre", "category_id", "region", "actors", "director", "scriptwriter", "language",
                  "release_date", "releaseDate", "duration", "alternate_name", "aka", "review", "description", "plot", "type"]
