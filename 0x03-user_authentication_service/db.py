#!/usr/bin/env python3
"""main file for database"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user import Base, User

class DB:
    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)

    def add_user(self, email, hashed_password):
        session = self._Session()
        user = User(email=email, hashed_password=hashed_password)
        session.add(user)
        session.commit()
        session.close()
        return user

    def find_user_by(self, **kwargs):
        session = self._Session()
        user = session.query(User).filter_by(**kwargs).first()
        session.close()
        if user is None:
            raise ValueError("User not found")
        return user

    def update_user(self, user_id, **kwargs):
        session = self._Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user is None:
            session.close()
            raise ValueError("User not found")
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
        session.close()
