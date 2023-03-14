import unittest
from main import app


class TestHelloWithDay(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_username_good_day(self):
        username = 'Хорошего понедельника!'
        count_copy = 0
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()

        for i_word in response_text.split():
            if i_word in username.split():
                count_copy += 1

        self.assertTrue(count_copy < 2)