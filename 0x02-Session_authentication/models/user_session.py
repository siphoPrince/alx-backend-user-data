#!/usr/bin/env python3
""" user sessions code base"""

from typing import TypeVar, List, Iterable
from os import path
from models.base import Base
import json
import uuid


class UserSession(Base):
    """ main class"""

    def __init__(self, *args: list, **kwargs: dict):
        """ initialize for user"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

