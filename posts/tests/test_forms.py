from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

import posts.tests.constants as constants
from posts.models import Comment, Post
from posts.tests.test_settings import AllSettings


class FormTest(AllSettings):
    def setUp(self):
        super().setUp()
        self.post_for_form = Post.objects.create(
            text='Тестовый пост с тестовым текстом',
            author=self.user,
            group=self.group,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user_2,
            text='Идеально!'
        )

    def test_add_post(self):
        post_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=constants.SMALL_GIF,
            content_type='image/gif'
        )
        form_data = {
            'text': constants.TEXT_POST_NEW,
            'group': self.group.id,
            'image': uploaded
        }

        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )

        post = Post.objects.first()
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(post.image)
        self.assertEqual(post.text, constants.TEXT_POST_NEW)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group)
        self.assertRedirects(response, reverse('posts:index'))

    def test_edit_post(self):
        post_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=constants.SMALL_GIF,
            content_type='image/gif'
        )
        form_data = {
            'text': constants.TEXT_POST_EDIT,
            'group': self.group.id,
            'image': uploaded
        }

        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                args=[self.user, self.post_for_form.id]
            ),
            data=form_data,
            follow=True
        )

        post = Post.objects.get(id=self.post_for_form.id)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(post.text, constants.TEXT_POST_EDIT)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group)
        self.assertIsNotNone(post.image)
        self.assertRedirects(
            response,
            reverse('posts:post', args=[self.user, self.post_for_form.id])
        )

    def test_add_post_with_txt(self):
        uploaded = SimpleUploadedFile(
            name='small.txt',
            content=constants.SMALL_GIF,
            content_type='text/txt'
        )
        form_data = {
            'text': constants.TEXT_POST_EDIT,
            'group': self.group.id,
            'image': uploaded
        }

        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )

        self.assertFormError(
            response,
            'form',
            'image',
            constants.ERROR_FOR_POSTFORM_IF_ADD_TXT
        )

    def test_add_comment(self):
        comments_count = Comment.objects.count()
        form_data = {
            'text': constants.TEXT_COMMENT,
        }

        response = self.authorized_client_2.post(
            reverse('posts:add_comment', args=[self.user, self.post.id]),
            data=form_data,
            follow=True
        )

        comment = Comment.objects.first()
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertEqual(comment.text, constants.TEXT_COMMENT)
        self.assertEqual(comment.author, self.user_2)
        self.assertRedirects(
            response, reverse(
                'posts:post', args=[self.user, self.post.id]
            )
        )

    def test_redirect_add_comment_unauthorized(self):
        comments_count = Comment.objects.count()
        form_data = {
            'text': constants.TEXT_COMMENT,
        }

        response = self.guest_client.post(
            reverse('posts:add_comment', args=[self.user, self.post.id]),
            data=form_data,
            follow=True
        )

        self.assertEqual(Comment.objects.count(), comments_count)
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse(
                'posts:add_comment', args=[self.user, self.post.id]
            )
        )
