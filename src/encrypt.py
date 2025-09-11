from cryptography.fernet import Fernet
from src.logger import get_logger


def encrypt_file(file_path, key):
    logger = get_logger()
    cipher = Fernet(key)
    with open(file_path, "rb") as f:
        data = f.read()
    encrypted_data = cipher.encrypt(data)
    with open(file_path + ".enc", "wb") as f:
        f.write(encrypted_data)
    logger.info(f"Arquivo {file_path} criptografado para {file_path + '.enc'}.")
    return file_path + ".enc"


def generate_key(file_path):
    logger = get_logger()
    key = Fernet.generate_key()
    # Write the key as a base64-encoded string (utf-8) for CLI usage
    with open(file_path + ".key", "w", encoding="utf-8") as f:
        f.write(key.decode("utf-8"))
    logger.info(f"Chave gerada e salva em {file_path + '.key'}. (base64 string)")
    return key.decode("utf-8")


def decrypt_file(input_file, key):
    logger = get_logger()
    cipher = Fernet(key)
    with open(input_file, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    output_file = input_file.replace(".enc", "")
    with open(output_file, "wb") as f:
        f.write(decrypted_data)
    logger.info(f"Arquivo {input_file} descriptografado para {output_file}.")
    return output_file
