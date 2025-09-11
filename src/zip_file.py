import os
import zipfile

try:
    import pyminizip
except ImportError:
    print("Zip com senha não disponível para esta plataforma")


def zip_file(file_path, password: str = None, logger=None):
    zip_path = file_path + ".zip"
    if not password:
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(file_path, os.path.basename(file_path))
        if logger:
            logger.info(f"Arquivo {file_path} compactado para {zip_path}.")
    else:
        pyminizip.compress(file_path, None, zip_path, password, 5)
        if logger:
            logger.info(f"Arquivo {file_path} compactado com senha para {zip_path}.")
    return zip_path
