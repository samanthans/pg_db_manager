import argparse
import datetime
from os import path
import tempfile
import psycopg

from dump_db import dump_db
from encrypt import encrypt_file
from vacuum import vacuum_utility

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
    "--encrypt", "-e", action="store_true", help="Criptografar o backup"
)

args = parser.parse_args()
print(args)

db = psycopg.connect(
    dbname=args.db,
    user=args.user,
    password=args.password,
    host=args.host,
    port=args.port,
)


def get_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"backup_{timestamp}.dump"


def __main__():
    vacuum_utility(db, force=args.vacuum, full=args.full)
    use_tmp_dir = False
    if args.zip or args.encrypt:
        use_tmp_dir = True
        tmp_dir = tempfile.TemporaryDirectory()
    else:
        tmp_dir = args.path
    filename = get_filename()
    output_file = path.join(tmp_dir, filename)

    dump_db(
        db_name=args.db,
        output_file=output_file,
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
    )
    if args.encrypt:
        output_file = encrypt_file(output_file, key="teste")
    if args.zip:
        



    # No final
    if use_tmp_dir:
        tmp_dir.cleanup()
