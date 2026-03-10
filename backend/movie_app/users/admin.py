from django.contrib import admin
from movie_app.users.models import Users
from movie_app.users.models import Collect

# Register your models here.

admin.site.register(Users)
admin.site.register(Collect)