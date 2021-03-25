from flask import session


def log_out():
    session.pop('username', None)
    session.pop('id', None)
