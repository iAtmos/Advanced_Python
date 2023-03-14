import unittest
from main import app


class TestDecryptionCipherWithThreePoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.base_url = '/decoder/'

    def test_deleting_entire_row(self):
        answered = '<пустая строка>'
        cipher = 'абра........'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)

    def test_decryption_three_dots_center(self):
        answered = 'a'
        cipher = 'абр......a.'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)

    def test_decryption_three_dots_after_late(self):
        answered = 'абра-кадабра'
        cipher = 'абрау...-кадабра'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)

    def test_line_points(self):
        answered = '<пустая строка>'
        cipher = '1.......................'
        response = self.app.get(self.base_url + cipher)
        response_text = response.data.decode()
        self.assertTrue(answered == response_text)