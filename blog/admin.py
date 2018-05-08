from django.contrib import admin

# Register your models here.

from .models import Post, Category, Tag
import sys;

reload(sys);
sys.setdefaultencoding("utf8")

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)