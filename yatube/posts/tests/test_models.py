from posts.models import Comment, Follow, Group, Like, Post
from posts.tests.test_settings import AllSettings


class Addition(AllSettings):
    def setUp(self):
        super().setUp()
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user_2,
            text='Идеально!'
        )
        self.like = Like.objects.create(
            user=self.user,
            post=self.post
        )
        self.follow = Follow.objects.create(
            user=self.user,
            author=self.user_2
        )

    def check_verbose_name(self, model, **kwargs):
        """
        The function checks the verbose_name of the models

        The entrance accepts:
            ~ model - the model for which we are checking
            ~ ** kwargs - key-field dictionary, value - what lies
        """
        for value, expected in kwargs['kwargs'].items():
            with self.subTest(value=value):
                self.assertEqual(
                    model._meta.get_field(value).verbose_name,
                    expected,
                    f'Incorrect verbose_name for {value} in {model} model'
                )

    def check_help_text(self, model, **kwargs):
        """
        The function checks help_text for models

        The entrance accepts:
            ~ model - the model for which we are checking
            ~ ** kwargs - key-field dictionary, value - what lies
        """
        for value, expected in kwargs['kwargs'].items():
            with self.subTest(value=value):
                self.assertEqual(
                    model._meta.get_field(value).help_text,
                    expected,
                    f'Incorrect help_text value for {value} in {model} model'
                )


class GroupModelTest(Addition):
    def test_verbose_name_from_group(self):
        field_verboses = {
            'title': self.group._meta.get_field('title').verbose_name,
            'slug': self.group._meta.get_field('slug').verbose_name,
            'description':
                self.group._meta.get_field('description').verbose_name
        }
        self.check_verbose_name(Group, kwargs=field_verboses)

    def test_help_text_from_group(self):
        field_help_texts = {
            'title': self.group._meta.get_field('title').help_text,
            'slug': self.group._meta.get_field('slug').help_text,
            'description': self.group._meta.get_field('description').help_text
        }
        self.check_help_text(Group, kwargs=field_help_texts)

    def test_str_from_group(self):
        self.assertEqual(
            str(self.group),
            self.group.title,
            'Incorrect __str__ value in Group model'
        )


class PostModelTest(Addition):
    def test_verbose_name_from_post(self):
        field_verboses = {
            'text': self.post._meta.get_field('text').verbose_name,
            'author': self.post._meta.get_field('author').verbose_name,
            'pub_date': self.post._meta.get_field('pub_date').verbose_name,
            'group': self.post._meta.get_field('group').verbose_name,
            'image': self.post._meta.get_field('image').verbose_name
        }
        self.check_verbose_name(Post, kwargs=field_verboses)

    def test_help_text_from_post(self):
        field_help_texts = {
            'text': self.post._meta.get_field('text').help_text,
            'group': self.post._meta.get_field('group').help_text,
            'image': self.post._meta.get_field('image').help_text,
        }
        self.check_help_text(Post, kwargs=field_help_texts)

    def test_str_from_post(self):
        self.assertEqual(
            str(self.post),
            self.post.text[:15],
            'Incorrect __str__ value in Post  model'
        )


class CommentModelTest(Addition):
    def test_verbose_name_from_comment(self):
        field_verboses = {
            'post': self.comment._meta.get_field('post').verbose_name,
            'author': self.comment._meta.get_field('author').verbose_name,
            'text': self.comment._meta.get_field('text').verbose_name,
            'created': self.comment._meta.get_field('created').verbose_name,
        }
        self.check_verbose_name(Comment, kwargs=field_verboses)

    def test_help_text_from_comment(self):
        field_help_texts = {
            'text': self.comment._meta.get_field('text').help_text,
        }
        self.check_help_text(Comment, kwargs=field_help_texts)

    def test_str_from_comment(self):
        self.assertEqual(
            str(self.comment),
            f'<{self.comment.author}> -> {self.comment.text[:20]}',
            'Incorrect __str__ value in Comment  model'
        )


class FollowModelTest(Addition):
    def test_verbose_name_from_follow(self):
        field_verboses = {
            'user': self.follow._meta.get_field('user').verbose_name,
            'author': self.follow._meta.get_field('author').verbose_name,
        }
        self.check_verbose_name(Follow, kwargs=field_verboses)

    def test_str_from_follow(self):
        self.assertEqual(
            str(self.follow),
            f'{self.follow.user} подписан на {self.follow.author}'
        )


class LikeModelTest(Addition):
    def test_verbose_name_from_like(self):
        field_verboses = {
            'user': self.like._meta.get_field('user').verbose_name,
            'post': self.like._meta.get_field('post').verbose_name,
        }
        self.check_verbose_name(Like, kwargs=field_verboses)

    def test_str_from_like(self):
        self.assertEqual(
            str(self.like),
            f'{self.like.user} поставил лайк посту {self.like.post.id}'
        )
