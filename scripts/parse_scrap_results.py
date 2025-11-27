import os
from datetime import datetime, timedelta

import pandas as pd


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


def add_date_column(file_name: str, day: str, time: str):
    weekdays = {
        "seg.": 0,
        "ter.": 1,
        "qua.": 2,
        "qui.": 3,
        "sex.": 4,
        "sáb.": 5,
        "dom.": 6,
    }
    months = {
        "jan.": 1,
        "fev.": 2,
        "mar.": 3,
        "abr.": 4,
        "mai.": 5,
        "jun.": 6,
        "jul.": 7,
        "ago.": 8,
        "set.": 9,
        "out.": 10,
        "nov.": 11,
        "dez.": 12,
    }
    print(time.split(":"))
    splitted_time = [int(x) for x in time.split(":")]
    parsed_date = datetime.strptime(file_name.replace("-dados.csv", ""), "%Y-%m-%d")
    parsed_date = parsed_date.replace(hour=splitted_time[0], minute=splitted_time[1])

    target_weekday = weekdays.get(day, -1)
    if target_weekday == -1:
        # TODO: Parse "1 de out."
        splitted_date = day.split(" ")
        t_day, t_month = int(splitted_date[0]), months.get(splitted_date[2], -1)

        if t_month == -1:
            print(f"Invalid date! Got month {t_month}")
            raise ValueError(f"Data inválida: {t_month}")

        new_date = parsed_date.replace(day=t_day, month=t_month)
        return new_date

    current_weekday = parsed_date.weekday()
    days_to_add = (target_weekday - current_weekday) % 7
    new_date = parsed_date + timedelta(days=days_to_add)
    return new_date


if __name__ == "__main__":
    empate_anula_path = "./output/empate_anula"
    empate_conta_path = "./output/empate_conta"

    empate_anula_files = list_directory(empate_anula_path)
    empate_conta_files = list_directory(empate_conta_path)

    for file_name in empate_conta_files:
        file_name = str(file_name)
        print(f"Validando arquivo {file_name}")
        df = pd.read_csv(
            os.path.join(empate_conta_path, file_name),
            dtype={"dia_jogo": str, "hora_jogo": str},
        )
        if len(df) == 0:
            continue

        df["dia_jogo"] = df["dia_jogo"].astype(str)
        df["hora_jogo"] = df["hora_jogo"].astype(str)
        df["data_jogo"] = df.apply(
            lambda row: add_date_column(file_name, row["dia_jogo"], row["hora_jogo"]),
            axis=1,
        )
        print(df)
        input()
