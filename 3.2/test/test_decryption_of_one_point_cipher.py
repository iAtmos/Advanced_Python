import unittest
from main import app


class TestDecryptionCipherWithThreePoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.base_url = '/decoder/'

    def test_decryption_of_three_point_after_letter(self):
        answered = 'абра-кадабра'
        cipher = 'абра-кадабра.'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)

    def test_only_dot(self):
        answered = '<пустая строка>'
        cipher = '.'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)


