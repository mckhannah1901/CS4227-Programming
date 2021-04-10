import unittest
from flask_sqlalchemy import SQLAlchemy

from app import user_registration, log_in, models, db, app


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
        # add person to test db when it is set up
        #user_registration.register_new_user("first", "last", "email@email.ie", "name", "pass")
        try:
            log_in.log_in("email@email.ie", "pass")
        except Exception:
            self.fail("Login test failed")

    #def login_negative(self):
