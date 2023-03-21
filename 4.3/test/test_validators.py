import unittest
from main import app


class TestValidators(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/registration'
        self.test_data = dict(email="s@gmail.com", phone=2222222222,
                              name="Hil", address="Avenue 5", index=434, comment="...")
        self.answer = ["200 OK", "400 BAD REQUEST"]

    def checking_response(self, answer: str):
        response = self.app.post(self.base_url, data=self.test_data)
        self.assertTrue(answer == response.status)

    def test_validator_true_email(self):
        self.test_data["email"] = "s@gmail.com"
        self.checking_response(self.answer[0])

    def test_validator_false_email(self):
        self.test_data["email"] = "ssss"
        self.checking_response(self.answer[1])

    def test_validator_true_number(self):
        self.test_data["phone"] = 2222222222
        self.checking_response(self.answer[0])

    def test_validator_false_number(self):
        self.test_data["phone"] = 22222
        self.checking_response(self.answer[1])

    def test_validator_true_name(self):
        self.test_data["name"] = "Hil"
        self.checking_response(self.answer[0])

    def test_validator_false_name(self):
        self.test_data["name"] = "s"
        self.checking_response(self.answer[1])

    def test_validator_index_true(self):
        self.test_data["index"] = 1
        self.checking_response(self.answer[0])

    def test_validator_index_false(self):
        self.test_data["index"] = -1
        self.checking_response(self.answer[1])

    def test_validator_coment_true(self):
        self.test_data["comment"] = "it`s good"
        self.checking_response(self.answer[0])

    def test_validator_coment_false(self):
        self.test_data["comment"] = "it`s goodddddddddddddddddddd"
        self.checking_response(self.answer[1])

    def test_validator_address_true(self):
        self.test_data["address"] = "Avenue 5"
        self.checking_response(self.answer[0])

    def test_validator_address_false(self):
        self.test_data["address"] = "svenue 5"
        self.checking_response(self.answer[1])
