from cryptography.fernet import Fernet


def encrypt_file(file_path, key, logger=None):
    cipher = Fernet(key)
    with open(file_path, "rb") as f:
        data = f.read()
    encrypted_data = cipher.encrypt(data)
    with open(file_path + ".enc", "wb") as f:
        f.write(encrypted_data)
    if logger:
        logger.info(f"Arquivo {file_path} criptografado para {file_path + '.enc'}.")
    return file_path + ".enc"


def generate_key(file_path, logger=None):
    key = Fernet.generate_key()
    with open(file_path + ".key", "wb") as f:
        f.write(key)
    if logger:
        logger.info(f"Chave gerada e salva em {file_path + '.key'}.")
    return key
