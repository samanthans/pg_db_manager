import logging
import os


class SingletonLogger:
    _instance = None
    _log_path = None

    def __new__(cls, log_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger(log_path)
        elif log_path and cls._log_path != log_path:
            # Reconfigure logger if log_path changes
            cls._instance._init_logger(log_path)
        return cls._instance

    def _init_logger(self, log_path):
        self.logger = logging.getLogger("pg_db_manager")
        self.logger.setLevel(logging.INFO)
        self._log_path = log_path
        # Remove existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        if log_path:
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            fh = logging.FileHandler(log_path, encoding="utf-8")
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def close_and_delete(self):
        # Close and remove all handlers
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)
        # Delete log file if possible
        if self._log_path and os.path.exists(self._log_path):
            try:
                os.remove(self._log_path)
            except Exception as e:
                print(f"Não foi possível remover o log: {self._log_path}. Erro: {e}")


# Helper to get the singleton logger
def get_logger(log_path=None):
    return SingletonLogger(log_path)
