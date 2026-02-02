import secrets
import string

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for _ in range(length):
        password += secrets.choice(chars)

    return password

print(generate_password(14))
print(generate_password(20))
