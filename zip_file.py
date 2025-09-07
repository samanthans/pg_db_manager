import os
import zipfile

import pyminizip


def zip_file(file_path, password: str = None):
    zip_path = file_path + ".zip"
    if password:
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(file_path, os.path.basename(file_path))
    else:
        pyminizip.compress(file_path, None, zip_path, password, 5)
    return zip_path
