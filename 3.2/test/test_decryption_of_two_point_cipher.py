import unittest
from main import app


class TestDecryptionCipherWithThreePoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.base_url = '/decoder/'

    def test_decryption_two_point_after_letter(self):
        answered = 'абра-кадабра'
        cipher = 'абраа..-кадабра'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)

    def test_decryption_two_point_after_letter_one_before(self):
        answered = 'абра-кадабра'
        cipher = 'абраа..-.кадабра'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)

    def test_decryption_two_point_after_symbol(self):
        answered = 'абра-кадабра'
        cipher = 'абра--..кадабра'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)

    def test_decryption_points_between_numbers(self):
        answered = '23'
        cipher = '1..2.3'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)