import logging


def configurar_logger(nome_arquivo_log):
    """
    Configura o logger para escrever logs em português no arquivo especificado.
    """
    logger = logging.getLogger("pg_db_manager")
    logger.setLevel(logging.INFO)
    # Evita múltiplos handlers duplicados
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh = logging.FileHandler(nome_arquivo_log, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
