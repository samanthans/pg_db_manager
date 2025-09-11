import os
import shutil
import subprocess
import sys


def get_pg_dump_path():
    """
    Returns the path to the pg_dump binary.
    Otherwise, tries to find pg_dump in the system PATH.
    """
    print("Getting pg_dump path")
    pg_bin = shutil.which("pg_dump")
    if pg_bin:
        return pg_bin
    if sys.platform.startswith("win"):
        curr_dir = os.path.dirname(__file__)
        pg_bin = os.path.abspath(os.path.join(curr_dir, "bin", "pg_dump.exe"))
        print(pg_bin)
        if os.path.isfile(pg_bin):
            return pg_bin
    raise Exception("Unable to find pg_dump binary")


def dump_db(
    db_name,
    output_file,
    host="localhost",
    port=5432,
    user=None,
    password=None,
    logger=None,
):
    """
    Exporta um banco PostgreSQL utilizando pg_dump.
    """
    pg_dump_bin = get_pg_dump_path()
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

    try:
        subprocess.run(cmd, check=True, env=env)
        if logger:
            logger.info(f"Banco exportado para {output_file}")
    except subprocess.CalledProcessError as e:
        if logger:
            logger.error(f"Erro exportando banco: {e}")
        else:
            print(f"Erro exportando banco: {e}")
