import os
import zipfile
from src.logger import get_logger

try:
    import pyminizip
except ImportError:
    pyminizip = None


def zip_file(file_path, password: str = None):
    logger = get_logger()
    zip_path = file_path + ".zip"
    if not password:
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(file_path, os.path.basename(file_path))
        logger.info(f"Arquivo {file_path} compactado para {zip_path}.")
    else:
        if not pyminizip:
            logger.info(
                "pyminizip não está instalado. Não é possível compactar com senha."
            )
            raise ImportError("pyminizip não está instalado.")
        pyminizip.compress(file_path, None, zip_path, password, 5)
        logger.info(f"Arquivo {file_path} compactado com senha para {zip_path}.")
    return zip_path


def unzip_file(input_file, output_dir):
    """Unzips the input file to the output directory and returns the path to the extracted file."""
    with zipfile.ZipFile(input_file, "r") as zip_ref:
        zip_ref.extractall(output_dir)
        extracted_files = zip_ref.namelist()
    # Return the first extracted file's path
    if extracted_files:
        return os.path.join(output_dir, extracted_files[0])
    else:
        raise ValueError("Nenhum arquivo encontrado no zip.")
