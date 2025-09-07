import os
import shutil
import subprocess


def get_pg_dump_path():
    """
    Returns the path to the pg_dump binary.
    Otherwise, tries to find pg_dump in the system PATH.
    """
    if pg_bin := shutil.which("pg_dump"):
        return pg_bin
    raise Exception("Unable to find pg_dump binary")


def dump_db(
    db_name, output_file, host="localhost", port=5432, user=None, password=None
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
        "c",  # custom format
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
        print(f"Banco exportado para {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erro exportando banco: {e}")
