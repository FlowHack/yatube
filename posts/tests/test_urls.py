from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.urls import reverse

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

    def check_status_code(self, who, **kwargs):
        """
        The function checks the status_code when requested

        The entrance accepts: ~ who - from which client the request is made
        ~ ** kwargs - Fields where key is the name of the transition,
        value is the required status_code
        """
        for url, should_be_status_code in kwargs['kwargs'].items():
            with self.subTest():
                response = who.get(url)
                self.assertEqual(
                    response.status_code,
                    should_be_status_code,
                    f'{url} does not open for unauthorized user'
                )

    def check_redirects(self, who, **kwargs):
        """
        The function checks for redirects from pages

        The entrance accepts: ~ who - from which client the request is made
        ~ ** kwargs - Fields where key is the name of the transition,
        value is what should be
        """
        for url, redirect in kwargs['kwargs'].items():
            with self.subTest():
                response = who.get(url, follow=True)
                self.assertRedirects(
                    response,
                    redirect
                )


class StaticURLTests(Addition):
    def test_unauthorized(self):
        """
        Test of pages that do not need authorization (status_code)
        """
        test_urls = {
            reverse('posts:index'): 200,
            reverse('posts:group_posts', args=[self.group.slug]): 200,
            self.flat_about.url: 200,
            self.flat_spec.url: 200,
            reverse('posts:profile', args=[self.user]): 200,
            reverse('posts:post', args=[self.user, self.post.id]): 200,
            reverse('posts:groups'): 200,
            reverse('posts:all_authors'): 200,
            'Not_IT_URL': 404,
        }

        self.check_status_code(self.guest_client, kwargs=test_urls)

    def test_unauthorized_redirect(self):
        test_urls_redirected = {
            reverse('posts:new_post'):
                reverse('login') + '?next=' + reverse('posts:new_post'),
            reverse(
                'posts:post_edit',
                args=[self.user, self.post.id]
            ): reverse('login') + '?next=' + reverse(
                'posts:post_edit', args=[self.user, self.post.id]
            ),
            reverse('posts:follow_index'):
                reverse('login') + '?next=' + reverse('posts:follow_index')
        }
        self.check_redirects(self.guest_client, kwargs=test_urls_redirected)

    def test_authorized_redirect(self):
        """
        Testing redirecting authorized users from the edit page of someone
        else's post
        """
        test_urls_redirected = {
            reverse('posts:post_edit', args=[self.user, self.post.id]
                    ): reverse('posts:post', args=[self.user, self.post.id])
        }
        self.check_redirects(
            self.authorized_client_2, kwargs=test_urls_redirected
        )

    def test_authorized(self):
        """
        Accessibility test for pages that require authorization
        """
        test_urls = {
            reverse('posts:new_post'): 200,
            reverse('posts:post_edit', args=[self.user, self.post.id]): 200
        }
        self.check_status_code(self.authorized_client, kwargs=test_urls)

    def test_template(self):
        urls_templates_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_posts', args=[self.group.slug]): 'group.html',
            reverse('posts:new_post'): 'posts/new_post.html',
            reverse('posts:post_edit', args=[self.user, self.post.id]
                    ): 'posts/new_post.html',
            reverse('posts:profile', args=[self.user]): 'profile/profile.html',
            self.flat_about.url: 'flatpages/default.html',
            self.flat_spec.url: 'flatpages/default.html',
            reverse('posts:groups'): 'group/groups.html',
            reverse('posts:all_authors'): 'profile/authors.html'
        }
        for reverse_name, template in urls_templates_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    f'Wrong template used for page {reverse_name}'
                )
