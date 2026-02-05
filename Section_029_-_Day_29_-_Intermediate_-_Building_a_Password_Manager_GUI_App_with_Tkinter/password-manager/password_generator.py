import secrets
import string

SAFE_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"

def generate_strong_password(length=16):
    """
    Generates a cryptographically secure password.
    Ensures presence of letters, digits, and symbols.
    """

    if length < 12:
        raise ValueError("Password length should be at least 12")

    letters = string.ascii_letters
    digits = string.digits
    symbols = SAFE_SYMBOLS

    # Guarantee minimum complexity
    password_chars = [
        secrets.choice(letters),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    all_chars = letters + digits + symbols
    password_chars += [secrets.choice(all_chars) for _ in range(length - 3)]

    # Secure shuffle
    secrets.SystemRandom().shuffle(password_chars)

    return ''.join(password_chars)
