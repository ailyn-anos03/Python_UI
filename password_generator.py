import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Example usage
password_length = int(input("Enter the desired password length: "))
print("Generated Password:", generate_password(password_length))