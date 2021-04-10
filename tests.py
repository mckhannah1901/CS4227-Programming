import unittest

from app import user_registration, log_in, app


class UnitTest(unittest.TestCase):
    def test_register_positive(self):
        try:
            user_registration.register_new_user("firstname", "lastname", "email@email.com", "username", "password")
        except Exception:
            self.fail("User register test failed")

    def test_register_negative(self):
        with self.assertRaises(Exception):
            user_registration.register_new_user("", "", "", "", "")

    def test_login_positive(self):
        with app.test_request_context():
            try:
                log_in.log_in("email@email.com", "password")
            except Exception:
                self.fail("Login test failed")
