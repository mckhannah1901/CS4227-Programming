import unittest

from flask import session

from app import user_registration, log_in, app, add_post


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

    def test_login_negative(self):
        with self.assertRaises(Exception):
            log_in.log_in("email@email1234.com", "password")

    def test_add_post_positive(self):
        with app.test_request_context():
            session['username'] = "bleh"
            session['id'] = 1234

            try:
                add_post.add_post("TEAAAAAAAAAAAAAAAAA!!!!", "Because it is.", "Existential")
            except Exception:
                self.fail("Add post test failed")

    #def test_add_post_negative(self):

    # def follow_user_test_positive(self):
    #
    # def follow_user_test_negative(self):

