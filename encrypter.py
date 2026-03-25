import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)


def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    return open(KEY_FILE, "rb").read()


def encrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)

    with open(filepath, "rb") as file:
        original_data = file.read()

    encrypted_data = fernet.encrypt(original_data)

    encrypted_filepath = f"{filepath}.enc"
    with open(encrypted_filepath, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    os.remove(filepath)
    return encrypted_filepath


def decrypt_file(encrypted_filepath):
    key = load_key()
    fernet = Fernet(key)

    with open(encrypted_filepath, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    original_filepath = encrypted_filepath.replace(".enc", "")
    with open(original_filepath, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

    os.remove(encrypted_filepath)
    return original_filepath
