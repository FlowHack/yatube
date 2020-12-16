from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        '<str:username>/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path('follow/', views.follow_index, name='follow_index'),
    path('authors/', views.authors_index, name='all_authors'),
    path(
        '<str:username>/follow/', views.profile_follow, name='profile_follow'
    ),
    path(
        '<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
    path(
        '<str:username>/<int:post_id>/like_or_unlike/',
        views.post_like_or_unlike,
        name='like_or_unlike'
    ),
    path('group/', views.groups, name='groups'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('new/', views.new_post, name='new_post'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path(
        '<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path(
        '<str:username>/<int:post_id>/delete',
        views.post_delete,
        name='post_delete'
    ),
    path(
        '<str:username>/<int:post_id>/<int:comment_id>/comment_delete',
        views.comment_delete,
        name='comment_delete'
    ),
    path('<str:username>/', views.profile, name='profile'),
    path(
        '<str:username>/edit_profile', views.profile_edit, name='profile_edit'
    ),
    path('<str:username>/edit_status', views.status_edit, name='status_edit')
]
