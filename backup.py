import argparse
import datetime
import os
import shutil
import tempfile
from os import path

import psycopg

from src.cleanup import cleanup_old_backups
from src.dump_db import dump_db
from src.encrypt import encrypt_file, generate_key
from src.logger import get_logger
from src.vacuum import vacuum_utility
from src.zip_file import zip_file

parser = argparse.ArgumentParser(
    description="Helper para manutenção de bancos postgresql"
)
parser.add_argument("path", help="Caminho para salvar o backup", type=str)
db_conn = parser.add_argument_group("Conexão com o banco")
db_conn.add_argument("--db", type=str, help="Nome do banco")
db_conn.add_argument("--user", "-u", type=str, help="Nome do banco")
db_conn.add_argument("--password", "-p", type=str, help="Nome do banco")
db_conn.add_argument("--host", type=str, default="127.0.0.1", help="Endereço do banco")
db_conn.add_argument("--port", type=int, default=5432, help="Porta")
options = parser.add_argument_group("Opções para o backup")
options.add_argument("--vacuum", action="store_true", help="Realizar o vacuum")
options.add_argument("--full", action="store_true", help="Vacuum no modo full")
options.add_argument("--zip", "-z", action="store_true", help="Compactar o backup")
options.add_argument(
    "--zip-pwd", type=str, help="Compactar o backup com a senha informada"
)
options.add_argument(
    "--encrypt", "-e", action="store_true", help="Criptografar o backup"
)
options.add_argument(
    "--copy", "-c", type=str, help="Armazenar cópia do backup no caminho"
)
options.add_argument("--key", type=str, help="Chave para criptografar o backup")
options.add_argument(
    "--pg-dump-path", type=str, help="Caminho para o binário do pg_dump"
)

options.add_argument(
    "--keep-old",
    type=int,
    default=5,
    help="Quantidade de backups anteriores para manter (os mais antigos serão excluidos)",
)


args = parser.parse_args()

db = psycopg.connect(
    dbname=args.db,
    user=args.user,
    password=args.password,
    host=args.host,
    port=args.port,
)


def get_filename(db_name: str):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{db_name}-backup-{timestamp}.dump"


def __main__():
    filename = get_filename(args.db)
    log_path = path.join(args.path, filename + ".log")
    logger = get_logger(log_path)
    logger.info("Iniciando processo de backup do banco de dados.")
    vacuum_utility(db, force=args.vacuum, full=args.full)
    tmp_dir = None
    if args.zip or args.zip_pwd or args.encrypt:
        tmp_dir = tempfile.TemporaryDirectory()
        dir_path = tmp_dir.name
        logger.info(
            f"Usando diretório temporário para arquivos intermediários: {dir_path}"
        )
    else:
        dir_path = args.path
    output_file_path = path.join(dir_path, filename)

    logger.info(f"Realizando dump do banco para o arquivo: {output_file_path}")
    dump_db(
        db_name=args.db,
        output_file=output_file_path,
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        pg_dump_path=args.pg_dump_path,
    )
    if not os.path.exists(output_file_path):
        logger.error(f"Arquivo de dump não encontrado: {output_file_path}")
        raise FileNotFoundError(f"Arquivo de dump não encontrado: {output_file_path}")
    if args.encrypt:
        logger.info("Criptografando o backup.")
        if not args.key:
            key_path = path.join(args.path, filename)
            key = generate_key(key_path)
        else:
            key = args.key
        output_file_path = encrypt_file(output_file_path, key=key)
    if args.zip_pwd:
        output_file_path = zip_file(file_path=output_file_path, password=args.zip_pwd)
    elif args.zip:
        output_file_path = zip_file(file_path=output_file_path)

    if args.copy:
        shutil.copy2(output_file_path, args.copy)

    # At the end of __main__(), after backup is complete:
    if args.keep_old > 0:
        cleanup_old_backups(args.db, args.path, args.keep_old)
        if args.copy:
            cleanup_old_backups(args.db, args.copy, args.keep_old)

    # No final
    if tmp_dir:
        shutil.copy2(output_file_path, args.path)
        tmp_dir.cleanup()

    # Delete logs if successful
    try:
        logger.close_and_delete()
    except Exception as e:
        print(f"Não foi possível remover o log: {log_path}. Erro: {e}")


if __name__ == "__main__":
    __main__()
