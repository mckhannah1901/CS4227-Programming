import unittest

from flask import session

from app import user_registration, log_in, app, add_post, user_subscribing


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
                user_registration.register_new_user("firstname2", "lastname2", "email@email2.com", "username2", "password2")
                log_in.log_in("email@email2.com", "password2")
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

    def test_add_post_negative(self):
        with app.test_request_context():
            session['username'] = "bleh"
            session['id'] = 1234

            with self.assertRaises(Exception):
                add_post.add_post("email@email1234.com", "password", "")

    def test_follow_user_positive(self):
        with app.test_request_context():
            user_registration.register_new_user("firstname", "lastname", "email@email.com", "username", "password")  # If clean database, comment it out.
            user_registration.register_new_user("firstname4", "lastname4", "email@email4.com", "username4", "password4")
            log_in.log_in("email@email4.com", "password4")

            try:
                user_subscribing.follow_user("username")
            except Exception:
                self.fail("Add post test failed")

    def test_follow_user_negative(self):
        with app.test_request_context():
            user_registration.register_new_user("firstname3", "lastname3", "email@email3.com", "username3", "password3")
            log_in.log_in("email@email3.com", "password3")

            with self.assertRaises(Exception):
                user_subscribing.follow_user("bleh2")

