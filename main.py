import argparse

parser = argparse.ArgumentParser(
    description="Helper para manutenção de bancos postgresql"
)

parser.add_argument("path", type=str)
db_conn = parser.add_argument_group(help="Conexão com o banco")
db_conn.add_argument("--db", help="Nome do banco")
db_conn.add_argument("-h", help="Endereço do banco")
db_conn.add_argument("-p", help="Porta")

args = parser.parse_args()
print(args)
