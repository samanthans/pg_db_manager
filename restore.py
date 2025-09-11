import argparse
import os
import shutil
import tempfile
from src.logger import get_logger
from src.encrypt import decrypt_file
from src.zip_file import unzip_file
import subprocess


parser = argparse.ArgumentParser(description="Restores a PostgreSQL backup")
parser.add_argument("backup", help="Backup file path", type=str)
db_conn = parser.add_argument_group("Conexão com o banco")
db_conn.add_argument("--db", type=str, help="Nome do banco")
db_conn.add_argument("--user", "-u", type=str, help="Nome do usuário")
db_conn.add_argument("--password", "-p", type=str, help="Senha do banco")
db_conn.add_argument("--host", type=str, default="127.0.0.1", help="Endereço do banco")
db_conn.add_argument("--port", type=int, default=5432, help="Porta")
options = parser.add_argument_group("Opções para o restore")
options.add_argument("--decrypt", action="store_true", help="Descriptografar o backup")
options.add_argument("--key", type=str, help="Chave para descriptografar o backup")
options.add_argument("--unzip", action="store_true", help="Descompactar o backup")

options.add_argument(
    "--pg-restore-path", type=str, help="Caminho para o executável do pg_restore"
)

args = parser.parse_args()


def main():
    logger = get_logger("restore.log")
    logger.info("Iniciando processo de restauração do banco de dados.")
    tmp_dir = None
    input_file = args.backup
    # Handle unzip and decrypt
    if args.unzip or args.decrypt:
        tmp_dir = tempfile.TemporaryDirectory()
        work_file = input_file
        if args.unzip:
            logger.info("Descompactando o backup.")
            work_file = unzip_file(work_file, output_dir=tmp_dir.name)
        if args.decrypt:
            logger.info("Descriptografando o backup.")
            if not args.key:
                logger.error("Chave de descriptografia não informada.")
                raise ValueError("Chave de descriptografia não informada.")
            work_file = decrypt_file(work_file, key=args.key)
        input_file = work_file
    # Restore using pg_restore
    pg_restore_path = shutil.which("pg_restore")
    if args.pg_restore_path:
        pg_restore_path = args.pg_restore_path
    if not pg_restore_path:
        raise Exception(
            "pg_restore não encontrado, forneca o caminho pelo argumento --pg-restore-path"
        )

    pg_restore_bin = pg_restore_path
    cmd = [
        pg_restore_bin,
        "-h",
        args.host,
        "-p",
        str(args.port),
        "-d",
        args.db,
        "-U",
        args.user,
        input_file,
    ]
    env = None
    if args.password:
        env = {**os.environ, "PGPASSWORD": args.password}
    try:
        subprocess.run(cmd, check=True, env=env)
        logger.info(f"Banco restaurado de {input_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro restaurando banco: {e}")
        print(f"Erro restaurando banco: {e}")
    if tmp_dir:
        tmp_dir.cleanup()
    logger.close_and_delete()


if __name__ == "__main__":
    main()
