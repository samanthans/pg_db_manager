import zipfile
import os

def zip_file(file_path):
    zip_path = file_path + '.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    return zip_path