from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser
from mainapp.models import Product


class TestAuthappCase(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'django'
    password = 'geekbrains'

    def setUp(self) -> None:
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(
            self.username,
            self.password,
            age=29,
        )

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertTrue(response.context['user'].is_anonymous)

        self.assertNotContains(response, 'Пользователь', status_code=self.status_ok)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)
        response = self.client.get('/')
        # self.assertContains(response, 'Пользователь', status_code=self.status_ok)

    def test_basket_login_redirect(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='django', password='geekbrains')

        response = self.client.get('/basket/')
        print(response)
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(list(response.context['basket_list']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        # self.assertIn('Ваша корзина, Пользователь', response.content.decode())

    def test_user_logout(self):
        self.client.login(username='django', password='geekbrains')

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
