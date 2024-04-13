#!/usr/bin/env python3
"""
Encrypt password file
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    print(hash_password(password).decode('utf-8'))
