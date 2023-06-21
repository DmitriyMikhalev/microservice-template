from application.v1.models import Task, User
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED)
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class TestStatusCodes(APITestCase):
    """Example Test class."""
    @classmethod
    def setUpClass(cls) -> None:
        """
        Runs once before testing the class.
        Using for creating authorized via JWT client and a task object that is
        unavailable for any users (which you can get during testing). If you
        sure you want that database record, use object manager with filtering
        by 'author is _temp_user'.
        """
        super().setUpClass()

        user_data = {
            'username': 'test-user',
            'first_name': 'pass',
            'last_name': 'pass',
            'email': 'test_email@google.com',
            'password': 'pass'
        }
        cls.authorized_user = User.objects.create_user(**user_data)
        jwt_token_pair = RefreshToken.for_user(user=cls.authorized_user)
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(
            token=jwt_token_pair.access_token,
            user=cls.authorized_user
        )

        cls._temp_user = User.objects.create_user(
            password='dummy',
            username='user-name'
        )
        cls.unavailable_task = Task.objects.create(
            author=cls._temp_user,
            description='',
            start_date='2023-03-03',
            finish_date='2023-03-04'
        )
        cls.task = Task.objects.create(
            author=cls.authorized_user,
            description='123',
            start_date='2023-03-07',
            finish_date='2023-03-08'
        )
        cls.msg_template = ('{}: {} returned {} insted of {} for {}orized '
                            'client.')
        cls.prefix = 'application:api_v1:task-'  # namespaces chain

    def test_status_codes_authorized_correct_requests(self):
        task_id = Task.objects.filter(author=self.authorized_user).first().id
        request_payload = {
            'description': 'description',
            'start_date': '2023-05-06 05:00:00',
            'finish_date': '2023-06-07 10:00:00',
        }
        request_kwargs = {'data': request_payload, 'format': 'json'}
        path_settings = {
            # array of objects
            reverse(viewname=self.prefix + 'list'): {
                self.authorized_client.get: {
                    'kwargs': {},
                    'expected_status': HTTP_200_OK
                },
                self.authorized_client.post: {
                    'kwargs': request_kwargs,
                    'expected_status': HTTP_201_CREATED
                }
            },
            # single object
            reverse(kwargs={'pk': task_id}, viewname=self.prefix + 'detail'): {
                self.authorized_client.get: {
                    'kwargs': {},
                    'expected_status': HTTP_200_OK
                },
                self.authorized_client.patch: {
                    'kwargs': request_kwargs,
                    'expected_status': HTTP_200_OK
                },
                self.authorized_client.put: {
                    'kwargs': request_kwargs,
                    'expected_status': HTTP_200_OK
                },
                self.authorized_client.delete: {
                    'kwargs': request_kwargs,
                    'expected_status': HTTP_204_NO_CONTENT
                }
            },
        }
        for path, methods_settings in path_settings.items():
            for method, settings in methods_settings.items():
                with self.subTest(path=path, method=method, settings=settings):
                    kwargs = settings['kwargs']
                    expected_status = settings['expected_status']
                    response_code = method(path=path, **kwargs).status_code
                    method_name = method.__name__.upper()
                    msg_args = (method_name, path, response_code,
                                expected_status, 'auth')

                    self.assertEqual(
                        expected_status,
                        response_code,
                        msg=self.msg_template.format(*msg_args)
                    )

    def test_status_codes_unauthorized(self):
        task_id = Task.objects.filter(author=self._temp_user).first().id
        request_payload = {
            'description': 'new description',
            'start_date': '2023-03-02 00:00:00',
            'finish_date': '2023-03-03 00:00:00',
        }
        request_kwargs = {'data': request_payload, 'format': 'json'}
        path_methods = {
            # array of objects
            reverse(viewname=self.prefix + 'list'): {
                self.client.get: {},
                self.client.post: request_kwargs,
            },
            # single object
            reverse(kwargs={'pk': task_id}, viewname=self.prefix + 'detail'): {
                self.client.get: {},
                self.client.patch: request_kwargs,
                self.client.put: request_kwargs,
                self.client.delete: request_kwargs
            },
        }
        expected_code = HTTP_401_UNAUTHORIZED
        for path, methods_kwargs in path_methods.items():
            for method, kwargs in methods_kwargs.items():
                with self.subTest(path=path, method=method, kwargs=kwargs):
                    method_name = method.__name__.upper()
                    response_code = method(path=path, **kwargs).status_code
                    msg_args = (method_name, path, response_code,
                                expected_code, 'unauth')

                    self.assertEqual(
                        expected_code,
                        response_code,
                        msg=self.msg_template.format(*msg_args)
                    )
