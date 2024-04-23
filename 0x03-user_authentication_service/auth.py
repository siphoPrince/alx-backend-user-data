#!/usr/bin/env python3
"""main auth.py"""


import bcrypt
import uuid
from db import DB
from user import User

class Auth:
    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except ValueError:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email, password):
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password.encode())
        except ValueError:
            return False

    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed

    def create_session(self, email):
        user = self._db.find_user_by(email=email)
        session_id = str(uuid.uuid4())
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_reset_password_token(self, email):
        user = self._db.find_user_by(email=email)
        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

