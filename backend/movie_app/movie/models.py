from django.db import models

# Create your models here.

# 地区
Region = [
    (1, '中国'),
    (2, '美国'),
    (3, '韩国'),
    (4, '日本'),
    (5, '其他'),
]


class Movie(models.Model):
    # 影视信息
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='影视名')
    release_year = models.IntegerField(verbose_name='上映年份')
    director = models.CharField(max_length=100, verbose_name='导演')
    scriptwriter = models.CharField(max_length=100, verbose_name='编剧')
    actors = models.CharField(max_length=200, verbose_name='主演')
    region = models.SmallIntegerField(choices=Region, verbose_name='地区')
    types = models.CharField(max_length=50, verbose_name='类型')
    language = models.CharField(max_length=100, verbose_name='语言')
    release_date = models.DateField(verbose_name='上映日期')
    duration = models.CharField(max_length=50, verbose_name='时长(或集数)')
    alternate_name = models.CharField(max_length=100, blank=True, verbose_name='又名')
    poster_url = models.ImageField(upload_to='posters/', blank=True, verbose_name='海报')
    rate = models.FloatField(blank=True, verbose_name='豆瓣评分')
    review = models.TextField(max_length=500, blank=True, verbose_name='简介')
    category_id = models.IntegerField(verbose_name='分类名')

    class Meta:
        db_table = 'movies_and_tv'
        verbose_name = '影视管理'
        verbose_name_plural = '影视管理'
        app_label = 'movie'
        managed = False

    def __str__(self):
        return self.name


