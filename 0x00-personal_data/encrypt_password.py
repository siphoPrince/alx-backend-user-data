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
