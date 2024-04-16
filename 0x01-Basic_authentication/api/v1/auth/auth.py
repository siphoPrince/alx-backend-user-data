#!/usr/bin/env python3
"""main uth file"""


from flask import request
from typing import List, TypeVar


class Auth:
    """main auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.

        Args:
            path (str): The request path.
            excluded_paths (List[str]):
            List of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The authorization header.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The current user.
        """
        return None
