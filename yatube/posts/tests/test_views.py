from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.urls import reverse

import posts.settings as posts_settings
from posts.models import Follow, Group, Post
from posts.tests.test_settings import AllSettings


class Addition(AllSettings):
    def setUp(self):
        super().setUp()
        site = Site.objects.get(pk=1)
        self.flat_about = FlatPage.objects.create(
            url='/about-author/',
            title='about',
            content='<b>content</b>'
        )
        self.flat_spec = FlatPage.objects.create(
            url='/about-spec/',
            title='about spec',
            content='<b>content</b>'
        )
        self.flat_about.sites.add(site)
        self.flat_spec.sites.add(site)

    def check_context_form(self, response):
        """
        The function checks the context of the form

        The entrance accepts:
            ~ response - received request response
        """
        list_field = {
            'text': forms.CharField,
            'group': forms.ChoiceField
        }
        for value, expected in list_field.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def check_context_page(self, response, check_with, expected_count):
        """
        The function checks context ['page']

        The entrance accepts:
            ~ response - the result of the request
            ~ check_with - what to compare the first post from page to
            ~ expected_count - how many posts should be on one page
        """
        page = response.context['page']
        first_item = page[0]
        page_len = len(page)

        self.assertEqual(first_item, check_with)
        self.assertEqual(page_len, expected_count)


class ViewsTest(Addition):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(15):
            Post.objects.create(
                author=cls.user,
                text=f'Текст поста {i}',
                group=cls.group,
            )

        for i in range(15):
            Group.objects.create(
                title='Тестовый title',
                slug=f'groups-{i}',
                description='Тестовый description'
            )

        for i in range(15):
            Post.objects.create(
                author=cls.user_2,
                text=f'Текст поста автора {i}',
                group=cls.group,
            )

    def test_show_correct_context_index(self):
        response = self.authorized_client.get(reverse('posts:index'))

        count_posts_all = response.context['paginator'].count

        self.check_context_page(response, self.post,
                                posts_settings.NUMBER_ITEM_PAGINATOR_POST)
        self.assertEqual(count_posts_all, Post.objects.count())

    def test_show_correct_follow_index(self):
        self.follow_1 = Follow.objects.create(
            user=self.user,
            author=self.user_2
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))

        count_posts_all = response.context['paginator'].count

        self.check_context_page(response, self.posts_follow,
                                posts_settings.NUMBER_ITEM_PAGINATOR_POST)
        self.assertEqual(count_posts_all, self.user_2.posts.count())

    def test_show_correct_follow_index_not_following(self):
        self.follow_1 = Follow.objects.create(
            user=self.user,
            author=self.user_2
        )
        response = self.authorized_client_3.get(reverse('posts:follow_index'))

        count_posts_all = response.context['paginator'].count

        self.assertEqual(count_posts_all, 0)

    def test_show_correct_context_group(self):
        response = self.authorized_client.get(
            reverse('posts:group_posts', args=[self.group.slug])
        )

        group = response.context['group']

        self.check_context_page(response, self.post,
                                posts_settings.NUMBER_ITEM_PAGINATOR_POST)
        self.assertEqual(group, self.group)

    def test_show_correct_context_groups(self):
        response = self.authorized_client.get(reverse('posts:groups'))

        self.check_context_page(
            response,
            self.group,
            posts_settings.NUMBER_ITEM_PAGINATOR_ALL_GROUPS
        )

    def test_show_correct_context_new_post(self):
        response = self.authorized_client.get(reverse('posts:new_post'))

        self.check_context_form(response)

    def test_show_correct_context_group_without_post(self):
        response = self.authorized_client.get(
            reverse('posts:group_posts', args=[self.group_without_post.slug])
        )

        paginator_len = response.context['paginator'].count

        self.assertEqual(paginator_len, 0)

    def test_show_correct_context_edit(self):
        response = self.authorized_client.get(
            reverse('posts:post_edit', args=[self.user, self.post.id]))

        post = response.context['post']

        self.assertEqual(post, self.post)
        self.check_context_form(response)

    def test_show_correct_context_profile(self):
        response = self.authorized_client.get(
            reverse('posts:profile', args=[self.user])
        )

        author = response.context['author']

        self.check_context_page(response, self.post,
                                posts_settings.NUMBER_ITEM_PAGINATOR_POST)
        self.assertEqual(author, self.user)

    def test_show_correct_context_post(self):
        response = self.authorized_client.get(
            reverse('posts:post', args=[self.user, self.post.id])
        )

        post = response.context['post']

        self.assertEqual(post, self.post)

    def test_show_correct_context_flatpages(self):
        list_content_flatpage = {
            'about': self.flat_about.content,
            'terms': self.flat_spec.content
        }

        for reverse_name, contents in list_content_flatpage.items():
            with self.subTest():
                response = self.authorized_client.get(reverse(reverse_name))
                self.assertEqual(
                    response.context['flatpage'].content,
                    contents
                )

    def test_cash(self):
        response = self.authorized_client.get(reverse('posts:index'))
        should_be_content = response.content
        Post.objects.create(
            text='Просто текст',
            author=self.user
        )

        response = self.authorized_client.get(reverse('posts:index'))
        content_without_new_post = response.content

        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        content_with_new_post = response.content

        self.assertEqual(content_without_new_post, should_be_content)
        self.assertNotEqual(content_with_new_post, should_be_content)


class FollowTest(Addition):
    def test_follow(self):
        follow_count = Follow.objects.count()
        response = self.authorized_client_2.get(
            reverse('posts:profile_follow', args=[self.user])
        )

        self.assertRedirects(
            response,
            reverse('posts:profile', args=[self.user])
        )

        self.assertEqual(Follow.objects.count(), follow_count + 1)
        follow = Follow.objects.last()
        self.assertEqual(follow.user, self.user_2)
        self.assertEqual(follow.author, self.user)

    def test_unfollow(self):
        Follow.objects.create(
            user=self.user,
            author=self.user_2
        )
        response = self.authorized_client.get(
            reverse('posts:profile_unfollow', args=[self.user_2])
        )

        self.assertRedirects(
            response,
            reverse('posts:profile', args=[self.user_2])
        )
        self.assertEqual(Follow.objects.count(), 0)

# class LikeTest(Addition):
#     def test_like(self):
#         like_count = Like.objects.count()
#
#         response = self.authorized_client_2.get(
#             reverse('posts:like_or_unlike', args=[self.user, self.post.id])+'?next='+reverse('posts:profile', args=[self.user.username])
#         )
#
#         self.assertRedirects(
#             response,
#             reverse(response.request['QUERY_STRING'].split('=')[1])
#         )
#         #
#         # self.assertEqual(Follow.objects.count(), follow_count + 1)
#         # like = Like.objects.last()
#         # self.assertEqual(follow.user, self.user_2)
#         # self.assertEqual(follow.author, self.user)
