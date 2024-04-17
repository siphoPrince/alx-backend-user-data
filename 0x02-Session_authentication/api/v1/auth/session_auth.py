#!/usr/bin/env python3
""" Manages user sessions """

import uuid
from typing import Optional, Dict
from flask import session

from .user import User  # Assuming user.py resides in a subfolder "api.v1.user"
from .auth import Auth  # Assuming auth.py resides in a subfolder "api.v1.auth"


class SessionManager(Auth):
    """ Handles user authentication through sessions """

    session_user_map: Dict[str, str] = {}  # Dictionary to store session ID -> user ID

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """ Generates a new session ID for a given user

        Args:
            user_id: The user's unique identifier (optional)

        Returns:
            A newly generated session ID or None if user_id is invalid
        """

        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.session_user_map[session_id] = user_id
        return session_id

    def get_user_by_session_id(self, session_id: Optional[str] = None) -> Optional[User]:
        """ Retrieves a User object based on the session ID

        Args:
            session_id: The session identifier (optional)

        Returns:
            A User object if a matching session is found, otherwise None
        """

        if not session_id or not isinstance(session_id, str):
            return None

        user_id = self.session_user_map.get(session_id)
        return User.get(user_id) if user_id else None

    def get_current_user(self) -> Optional[User]:
        """ Retrieves the currently logged-in user based on session data

        Returns:
            A User object if a user is logged in, otherwise None
        """

        session_id = session.get("session_id")
        return self.get_user_by_session_id(session_id)

    def destroy_session(self, session_id: Optional[str] = None) -> bool:
        """ Deletes a user's session (logout)

        Args:
            session_id: The session identifier to remove (optional, uses current session if not provided)

        Returns:
            True if the session was successfully deleted, False otherwise
        """

        if not session_id:
            session_id = session.get("session_id")

        if not session_id or not isinstance(session_id, str):
            return False

        if session_id not in self.session_user_map:
            return False

        del self.session_user_map[session_id]
        session.pop("session_id", None)  # Remove session ID from flask session data
        return True
