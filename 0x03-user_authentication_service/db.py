#!/usr/bin/env python3

""" Custom Database Class for Data Management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from my_user import Base, CustomUser


class CustomDB:
    """ Custom Database Class
    """

    def __init__(self):
        """ Initializes class attributes
        """
        self._engine = create_engine("sqlite:///custom.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """ Private method that returns a session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> CustomUser:
        """ Save a new user to the database
        """
        user = CustomUser(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> CustomUser:
        """ Returns the first row found in the users table
            as filtered by the method's input arguments
        """
        user_keys = [
            'id',
            'email',
            'hashed_password',
            'session_id',
            'reset_token']

        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError
        result = self._session.query(CustomUser).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update user attributes and
            commit changes to the database
        """
        user_to_update = self.find_user_by(id=user_id)

        user_keys = [
            'id',
            'email',
            'hashed_password',
            'session_id',
            'reset_token']

        for key, value in kwargs.items():
            if key in user_keys:
                setattr(user_to_update, key, value)
            else:
                raise ValueError
        self._session.commit()
