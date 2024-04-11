#!/usr/bin/env python3
"""
Main file demonstrating secure password hashing with bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with random salt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """provided password matches the stored hashed password using bcrypt.
    """
   return bcrypt.checkpw(password.encode(), hashed_password)
