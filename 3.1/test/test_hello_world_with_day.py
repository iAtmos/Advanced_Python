import unittest
from main import app
from freezegun import freeze_time
import datetime


class TestHelloWithDay(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_correct_max_number_in_series_of_two(self):
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)


    @freeze_time("1955-11-12")
    def test_can_get_not_uncorrected_day(self):
        assert datetime.datetime.now() == datetime.datetime(1955, 11, 12)
        answer_data = "Хорошей субботы!"

        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = ' '.join(response.data.decode().split()[-2:])

        self.assertTrue(answer_data == response_text)

