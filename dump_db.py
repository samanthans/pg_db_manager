import os
import subprocess


def dump_db(
    db_name, output_file, host="localhost", port=5432, user=None, password=None
):
    """
    Exporta um banco PostgreSQL utilizando pg_dump.
    """
    cmd = [
        "pg_dump",
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
