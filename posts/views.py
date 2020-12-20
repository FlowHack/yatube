from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

import posts.settings as addition_settings

from .forms import CommentForm, PostForm, ProfileEditForm, StatusEditForm
from .models import Comment, Follow, Group, Like, Post

User = get_user_model()


def index(request):
    post_list = Post.objects.all().annotate_like(request.user)
    paginator = Paginator(
        post_list, addition_settings.NUMBER_ITEM_PAGINATOR_POST
    )
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'posts/index.html',
        {'page': page, 'paginator': paginator}
    )


def authors_index(request):
    all_authors = User.objects.all().order_by('first_name')

    paginator = Paginator(
        all_authors, addition_settings.NUMBER_ITEM_PAGINATOR_ALL_AUTHORS
    )
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'profile/authors.html',
        {'page': page, 'paginator': paginator}
    )


def groups(request):
    all_groups = Group.objects.all().order_by('title')

    paginator = Paginator(
        all_groups, addition_settings.NUMBER_ITEM_PAGINATOR_ALL_GROUPS
    )

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'group/groups.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = group.posts.all().annotate_like(request.user)
    paginator = Paginator(
        posts, addition_settings.NUMBER_ITEM_PAGINATOR_POST
    )

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'group.html',
        {'group': group, 'page': page, 'paginator': paginator}
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:index')

    return render(request, 'posts/new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    is_following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user, author=author
    ).exists()
    paginator = Paginator(
        author.posts.all().annotate_like(request.user),
        addition_settings.NUMBER_ITEM_PAGINATOR_POST
    )

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user != author:
        return render(
            request,
            'profile/profile.html',
            {
                'page': page,
                'paginator': paginator,
                'author': author,
                'following': is_following,
            }
        )

    form = StatusEditForm(instance=author)
    return render(
        request,
        'profile/profile.html',
        {
            'page': page,
            'paginator': paginator,
            'author': author,
            'following': is_following,
            'form': form,
        }
    )


@login_required
def status_edit(request, username):
    author = get_object_or_404(User, username=username)

    if request.user != author:
        return redirect('posts:profile', author)

    form = StatusEditForm(
        request.POST or None,
        instance=author
    )

    if form.is_valid():
        form.save()

    return redirect('posts:profile', author)


def post_view(request, username, post_id):
    post = get_object_or_404(
        Post.objects.annotate_like(request.user),
        author__username=username,
        id=post_id
    )
    form = CommentForm()
    comments = post.comments.all()

    return render(
        request,
        'posts/post.html',
        {'post': post, 'comments': comments, 'form': form}
    )


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(
        Post.objects.annotate_like(request.user),
        author__username=username,
        id=post_id
    )
    author = post.author

    if request.user != author:
        return redirect('posts:post', author.username, post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )

    if form.is_valid():
        form.save()
        return redirect('posts:post', author, post_id)

    return render(
        request,
        'posts/new_post.html',
        {'form': form, 'post': post}
    )


@login_required
def profile_edit(request, username):
    author = get_object_or_404(User, username=username)

    if request.user != author:
        return redirect('posts:profile', author)

    form = ProfileEditForm(
        request.POST or None,
        files=request.FILES or None,
        instance=author
    )

    if form.is_valid():
        form.save()
        return redirect('posts:profile', author)

    return render(
        request,
        'profile/profile_edit.html',
        {'form': form, 'author': author}
    )


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(
        Post,
        author__username=username,
        id=post_id
    )
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('posts:post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(
        author__following__user=request.user
    ).annotate_like(request.user)
    paginator = Paginator(
        posts, addition_settings.NUMBER_ITEM_PAGINATOR_POST
    )

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'posts/follow.html', {'page': page, 'paginator': paginator}
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)

    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()

    return redirect('posts:profile', username=username)


@login_required
def post_like_or_unlike(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    if Like.objects.filter(user__username=username, post=post).exists():
        Like.objects.filter(user__username=username, post=post).delete()
    else:
        Like.objects.get_or_create(user=request.user, post=post)

    return redirect(request.GET.get('next') + f'#id_post_{post_id}')


@login_required
def post_delete(request, username, post_id):
    if request.user.username == username:
        Post.objects.filter(author__username=username, id=post_id).delete()

    return redirect('posts:index')


@login_required
def comment_delete(request, username, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if (request.user == comment.author) or (request.user.username == username):
        comment.delete()

    return redirect('posts:post', username, post_id)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
