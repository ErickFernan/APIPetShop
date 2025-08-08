import logging
import os
import inspect

# Função para obter o nome do logger dinamicamente
def get_logger():
    # Obtém o nome do arquivo atual, sem o caminho
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_globals["__file__"])
    return logging.getLogger(filename)

# Configuração do logger
def configure_logger():
    # logger = logging.getLogger(__name__) # mudou este para pegar o nome e não o local
    logger = get_logger()
    logger.setLevel(logging.ERROR)  # Ajuste o nível conforme necessário
    handler = logging.StreamHandler()  # Ou use FileHandler para logar em um arquivo
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Função genérica para tratar exceções
def handle_exception(func_name, exception):
    logger = configure_logger()  # Obtém o logger com o nome do arquivo
    # Obtém o nome do arquivo e da linha onde a exceção ocorreu
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_globals["__file__"])  # Nome do arquivo
    lineno = frame.f_lineno  # Linha onde ocorreu

    logger.error(f"Erro no arquivo {filename}, linha {lineno}, ao executar {func_name}: {exception}")
    raise exception

def log_exception(func_name, exception):
    logger = configure_logger()  # Obtém o logger com o nome do arquivo
    # Obtém o nome do arquivo e da linha onde a exceção ocorreu
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_globals["__file__"])  # Nome do arquivo
    lineno = frame.f_lineno  # Linha onde ocorreu

    logger.error(f"Erro no arquivo {filename}, linha {lineno}, ao executar {func_name}: {exception}")
