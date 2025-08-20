from typing import Optional

import bcrypt
import requests
from flask import session


def check_limited(email: str, lookup_url: str) -> bool:
    """Check employee directory for limited privilege users"""
    try:
        res = requests.get(f"{lookup_url}/{email}", timeout=3)
        res.raise_for_status()
        return res.json().get("limited", True)
    except requests.exceptions.RequestException:
        return True


def check_password(plaintext: str, password_hash: str, salt: bytes) -> bool:
    return password_hash == hash_password(plaintext, salt)


def hash_password(plaintext: str, salt: bytes) -> str:
    return bcrypt.hashpw(bytes(plaintext, "ascii"), salt).decode("ascii")


def get_user_id() -> int:
    return session.get("user_id")


def set_user(user_id: Optional[int]):
    if user_id:
        session["user_id"] = user_id
    else:
        session.pop("user_id", None)
