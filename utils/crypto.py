from passlib.hash import sha512_crypt

def generate_password_hash(password: str) -> str:
    """Generates a SHA-512 crypt hash for the given password."""
    return sha512_crypt.using(rounds=5000).hash(password)
