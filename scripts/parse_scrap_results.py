import os
from pprint import pprint

import pandas as pd


def list_directories(dir_path: str):
    try:
        items = os.listdir(dir_path)
        files = [file for file in items if os.path.isfile(os.path.join(dir_path, file))]
        return files
    except FileNotFoundError:
        print(f'ERRO: Diretório "{dir_path}" não encontrado!')
        return []
    except PermissionError:
        print(f'ERRO: Permissão negada ao diretório "{dir_path}"!')


if __name__ == "__main__":
    empate_anula_path = "./output/empate_anula"
    empate_conta_path = "./output/empate_conta"

    empate_anula_files = list_directories(empate_anula_path)
    empate_conta_files = list_directories(empate_conta_path)

    print("------------------------")
    print("Arquivos - EMPATE ANULA")
    print("------------------------")

    pprint(empate_anula_files)
    print("")
    print("------------------------")
    print("Arquivos - EMPATE CONTA")
    print("------------------------")

    pprint(empate_anula_files)
