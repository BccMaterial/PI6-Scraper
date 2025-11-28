import os


def list_directory(dir_path: str):
    try:
        items = os.listdir(dir_path)
        files = [file for file in items if os.path.isfile(os.path.join(dir_path, file))]
        return files
    except FileNotFoundError:
        print(f'ERRO: Diretório "{dir_path}" não encontrado!')
        return []
    except PermissionError:
        print(f'ERRO: Permissão negada ao diretório "{dir_path}"!')
