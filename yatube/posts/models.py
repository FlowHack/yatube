from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Exists, OuterRef

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def annotate_like(self, user):
        return self.annotate(
            liked=Exists(
                Like.objects.filter(
                    user=user.id, post_id=OuterRef('id')
                ).only('id')
            )
        )


class Group(models.Model):
    """
    Create model for groups
    """
    title = models.CharField(
        verbose_name='Название группы',
        help_text='Это заголовок группы',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Слаг группы',
        help_text='Это краткий url группы',
        null=False,
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Это краткое описание группы'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Create model for posts
    """
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Напишите текст вашего поста здесь!'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор поста',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа постов',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        help_text='Выберите здесь название группы, к которой вы хотите '
                  'отнести ваш пост!'
    )
    image = models.ImageField(
        verbose_name='Картинка поста',
        help_text='Вы можете прикрепить к своему посту картинку',
        upload_to='posts/',
        blank=True,
        null=True
    )

    objects = PostQuerySet().as_manager()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """
    Create model for comments
    """
    post = models.ForeignKey(
        Post,
        verbose_name='Пост, к которому прикреплён комментарий',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Напишите здесь текст вашего комментария!',
    )
    created = models.DateTimeField(
        verbose_name='Дата создания комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'<{self.author}> -> {self.text[:20]}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='На кого подписан',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique author'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class Like(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Кто ставит like',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Пост к которому ставят лайк',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'], name='unique post'
            )
        ]

    def __str__(self):
        return f'{self.user} поставил лайк посту {self.post.id}'
