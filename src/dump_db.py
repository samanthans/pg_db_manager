import os
import shutil
import subprocess
from src.logger import get_logger


def dump_db(
    db_name,
    output_file,
    host="localhost",
    port=5432,
    user=None,
    password=None,
    pg_dump_path=None,
):
    """
    Exporta um banco PostgreSQL utilizando pg_dump.
    """
    if not pg_dump_path:
        pg_dump_path = shutil.which("pg_dump")
        if not pg_dump_path:
            raise Exception(
                "pg_dump não encontrado, favor fornecer o caminho ou adicionar ao PATH"
            )
    pg_dump_bin = pg_dump_path
    cmd = [
        pg_dump_bin,
        "-h",
        host,
        "-p",
        str(port),
        "-d",
        db_name,
        "-F",
        "c",  # formato customizado
        "-f",
        output_file,
    ]
    if user:
        cmd.extend(["-U", user])

    env = None
    if password:
        env = {**os.environ, "PGPASSWORD": password}

    logger = get_logger()
    try:
        subprocess.run(cmd, check=True, env=env)
        logger.info(f"Banco exportado para {output_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar o dump: {e}")
        if logger:
            logger.error(f"Erro exportando banco: {e}")
        else:
            print(f"Erro exportando banco: {e}")
