from django.shortcuts import render, get_object_or_404
from datetime import datetime as dt
from .models import Post, Group


def index(request):
    latest = Post.objects.all()[:10]

    return render(request, 'index.html', {'posts': latest, "year": year()})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = group.posts.all()[:12]
    return render(request, "group.html", {"group": group, "posts": posts, "year": year()})


def year():
    return dt.now().year
