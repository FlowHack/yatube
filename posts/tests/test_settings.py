import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

import posts.tests.constants as constants
from posts.models import Group, Post

User = get_user_model()
settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class AllSettings(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group-test',
            description='Тестовая группа с тестовым slug'
        )
        cls.group_without_post = Group.objects.create(
            title='Тестовая группа_2',
            slug='test-group-2',
            description='Тестовая группа с тестовым slug_2'
        )

        cls.uploaded = SimpleUploadedFile(
            name='small.txt',
            content=constants.SMALL_GIF,
            content_type='text/txt'
        )

        cls.user = User.objects.create_user(
            username='Akakii',
            email='test_email@mail.ru',
            password='akakii228'
        )
        cls.user_2 = User.objects.create_user(
            username='Akakii_2',
            email='test_email@mail.ru',
            password='akakii_2228'
        )
        cls.user_3 = User.objects.create_user(
            username='Akakii_3',
            email='test_email@mail.ru',
            password='akakii_3228'
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.authorized_client_2 = Client()
        cls.authorized_client_2.force_login(cls.user_2)
        cls.authorized_client_3 = Client()
        cls.authorized_client_3.force_login(cls.user_3)
        cls.guest_client = Client()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.posts_follow = Post.objects.create(
            text='Тестовый пост с тестовым текстом от автора',
            author=self.user_2,
            group=self.group,
            image=self.uploaded
        )
        self.post = Post.objects.create(
            text='Тестовый пост с тестовым текстом',
            author=self.user,
            group=self.group,
            image=self.uploaded
        )
