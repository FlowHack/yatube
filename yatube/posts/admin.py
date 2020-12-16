from django.contrib import admin

from .models import Comment, Follow, Group, Like, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug')
    search_fields = ('description',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'created')
    search_fields = ('post', 'author', 'text')
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user', )
    empty_value_display = '-пусто-'


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    list_filter = ('user', )
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)
