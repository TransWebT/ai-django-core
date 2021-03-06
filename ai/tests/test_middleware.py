import threading
import time
from unittest import TestCase
from unittest.mock import Mock

from ai.middleware.current_user import CurrentUserMiddleware


class CurrentUserMiddlewareTest(TestCase):
    def test_current_user_is_None_if_no_user_given(self):
        self.assertIsNone(CurrentUserMiddleware.get_current_user())

    def test_current_user_is_None_if_request_user_is_None(self):
        set_current_user(user=None)
        self.assertIsNone(CurrentUserMiddleware.get_current_user())

    def test_current_user_is_same_as_request_user(self):
        new_user = Mock(user_name='test_user')
        set_current_user(user=new_user)
        current_user = CurrentUserMiddleware.get_current_user()

        self.assertIsNotNone(current_user)
        self.assertEqual(current_user, new_user)
        self.assertEqual(current_user.user_name, 'test_user')

    def test_current_user_is_thread_safe(self):
        user1 = Mock(user_name='user1')
        user2 = Mock(user_name='user2')
        current_users = []

        first_thread = threading.Thread(target=set_current_user, args=(user1, 0, 5, current_users))
        second_thread = threading.Thread(target=set_current_user, args=(user2, 3, 0, current_users))
        first_thread.start()
        second_thread.start()
        first_thread.join()
        second_thread.join()

        self.assertEqual(current_users[0], user2)
        self.assertEqual(current_users[0].user_name, 'user2')
        self.assertEqual(current_users[1], user1)
        self.assertEqual(current_users[1].user_name, 'user1')


def set_current_user(user=None, delay_before_request=0, delay_after_request=0, current_users=None):
    request = Mock()
    request.user = user
    middleware = CurrentUserMiddleware()

    if delay_before_request:
        time.sleep(delay_before_request)
    middleware.process_request(request)
    if delay_after_request > 0:
        time.sleep(delay_after_request)

    if current_users is not None:
        current_users.append(CurrentUserMiddleware.get_current_user())
