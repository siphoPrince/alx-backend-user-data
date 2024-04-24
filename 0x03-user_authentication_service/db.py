#!/usr/bin/env python3
"""main file for database"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class Database:
    """A class to interact with the database
    """

    def __init__(self):
        """Initialize the database
        """
        self._engine = create_engine("sqlite:///users.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Get a session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by specified criteria
        """
        allowed_keys = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']
        for key in kwargs.keys():
            if key not in allowed_keys:
                raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes in the database
        """
        user_to_update = self.find_user_by(id=user_id)
        allowed_keys = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']
        for key, value in kwargs.items():
            if key in allowed_keys:
                setattr(user_to_update, key, value)
            else:
                raise ValueError
        self._session.commit()
