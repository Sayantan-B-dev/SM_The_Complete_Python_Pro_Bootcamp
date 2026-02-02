
"""
===========================================================
TERMINAL-BASED MULTI-LEVEL ENCRYPTION / DECRYPTION SYSTEM
(WITH ROBUST ERROR HANDLING)
===========================================================
"""

# =========================
# STANDARD LIBRARIES
# =========================

import base64
import sys
import binascii

# =========================
# CRYPTOGRAPHY LIBRARY
# =========================

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


# =========================================================
# LEVEL 1: CAESAR CIPHER
# =========================================================

def caesar_encrypt(text, shift):
    encrypted = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            encrypted += chr((ord(ch) - base + shift) % 26 + base)
        else:
            encrypted += ch
    return encrypted


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# =========================================================
# LEVEL 2: XOR CIPHER
# =========================================================

def xor_cipher(text, key):
    result = ""
    for ch in text:
        result += chr(ord(ch) ^ key)
    return result


# =========================================================
# LEVEL 3: BASE64 (ENCODING)
# =========================================================

def base64_encrypt(text):
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def base64_decrypt(text):
    try:
        return base64.b64decode(text.encode("utf-8")).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        raise ValueError("Invalid Base64 input")


# =========================================================
# LEVEL 4: AES (FERNET)
# =========================================================

fernet_key = Fernet.generate_key()
fernet = Fernet(fernet_key)

def aes_encrypt(text):
    return fernet.encrypt(text.encode("utf-8")).decode("utf-8")


def aes_decrypt(text):
    try:
        return fernet.decrypt(text.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        raise ValueError("Invalid AES token or wrong key/session")


# =========================================================
# LEVEL 5: RSA
# =========================================================

rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
rsa_public_key = rsa_private_key.public_key()

def rsa_encrypt(text):
    encrypted_bytes = rsa_public_key.encrypt(
        text.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_bytes).decode("utf-8")


def rsa_decrypt(text):
    try:
        decrypted_bytes = rsa_private_key.decrypt(
            base64.b64decode(text),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_bytes.decode("utf-8")
    except (ValueError, binascii.Error):
        raise ValueError("RSA decryption failed (invalid data or key)")


# =========================================================
# INPUT HELPERS (ERROR-SAFE)
# =========================================================

def safe_int(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                raise ValueError
            if max_value is not None and value > max_value:
                raise ValueError
            return value
        except ValueError:
            print("Invalid number input. Try again.\n")


def safe_non_empty(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value
        print("Input cannot be empty.\n")


# =========================================================
# MAIN TERMINAL INTERFACE
# =========================================================

def main():
    print("\n🔐 MULTI-LEVEL SECURITY SYSTEM 🔐\n")

    while True:
        try:
            print("Choose operation:")
            print("1 → Encrypt")
            print("2 → Decrypt")
            print("0 → Exit")

            operation = input("\nEnter choice: ").strip()

            if operation == "0":
                print("Exiting program...")
                sys.exit()

            if operation not in ("1", "2"):
                print("Invalid operation choice.\n")
                continue

            print("\nChoose Security Level:")
            print("1 → Caesar Cipher")
            print("2 → XOR Cipher")
            print("3 → Base64")
            print("4 → AES")
            print("5 → RSA")

            level = input("\nEnter level: ").strip()

            if level not in ("1", "2", "3", "4", "5"):
                print("Invalid security level.\n")
                continue

            message = safe_non_empty("\nEnter your message: ")

            # =========================
            # ENCRYPTION
            # =========================

            if operation == "1":
                if level == "1":
                    shift = safe_int("Enter shift value: ")
                    result = caesar_encrypt(message, shift)

                elif level == "2":
                    key = safe_int("Enter numeric key (0–255): ", 0, 255)
                    result = xor_cipher(message, key)

                elif level == "3":
                    result = base64_encrypt(message)

                elif level == "4":
                    result = aes_encrypt(message)

                elif level == "5":
                    result = rsa_encrypt(message)

                print("\nEncrypted Message:")
                print(result)

            # =========================
            # DECRYPTION
            # =========================

            else:
                if level == "1":
                    shift = safe_int("Enter shift value: ")
                    result = caesar_decrypt(message, shift)

                elif level == "2":
                    key = safe_int("Enter numeric key (0–255): ", 0, 255)
                    result = xor_cipher(message, key)

                elif level == "3":
                    result = base64_decrypt(message)

                elif level == "4":
                    result = aes_decrypt(message)

                elif level == "5":
                    result = rsa_decrypt(message)

                print("\nDecrypted Message:")
                print(result)

            print("\n" + "=" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting safely...")
            sys.exit()

        except Exception as e:
            print(f"\nError: {e}\n")
            print("=" * 50 + "\n")


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()

