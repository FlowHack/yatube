from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Comment, Post

User = get_user_model()


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )


class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'avatar',
            'first_name',
            'last_name',
            'username',
            'email',
        )


class StatusEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('status', )
