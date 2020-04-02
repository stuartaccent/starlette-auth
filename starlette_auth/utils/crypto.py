import binascii
import hashlib
import hmac
import os
import secrets


def check_password(current: str, password: str) -> bool:
    salt = current[:64]
    stored_password = current[64:]
    password_hash = hashlib.pbkdf2_hmac(
        "sha512", password.encode("utf-8"), salt.encode("ascii"), 100000
    )
    password_hash = binascii.hexlify(password_hash).decode("ascii")  # type: ignore
    return password_hash == stored_password


def hash_password(password: str) -> str:
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    password_hash = hashlib.pbkdf2_hmac(
        "sha512", password.encode("utf-8"), salt, 100000
    )
    password_hash = binascii.hexlify(password_hash)
    return (salt + password_hash).decode("ascii")


def constant_time_compare(val1, val2):
    """Return True if the two strings are equal, False otherwise."""

    return secrets.compare_digest(
        bytes(val1, encoding="utf-8"), bytes(val2, encoding="utf-8")
    )


def salted_hmac(key_salt, value, secret):
    """
    Return the HMAC-SHA1 of 'value', using a key generated from key_salt and a
    secret. A different key_salt should be passed in for every application of HMAC.
    """

    assert secret, f"secret must be provided."

    key_salt = bytes(key_salt, encoding="utf-8")
    secret = bytes(secret, encoding="utf-8")

    # We need to generate a derived key from our base key.  We can do this by
    # passing the key_salt and our base key through a pseudo-random function and
    # SHA1 works nicely.
    key = hashlib.sha1(key_salt + secret).digest()

    # If len(key_salt + secret) > sha_constructor().block_size, the above
    # line is redundant and could be replaced by key = key_salt + secret, since
    # the hmac module does the same thing for keys longer than the block size.
    # However, we need to ensure that we *always* do this.
    return hmac.new(key, msg=bytes(value, encoding="utf-8"), digestmod=hashlib.sha1)
