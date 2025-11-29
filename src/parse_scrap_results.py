import os

import pandas as pd

from utils import file, transform


def create_general_dataframe(file_list, files_directory):
    dataframes = list()
    print(f"File list: {file_list}")
    for file_name in file_list:
        file_name = str(file_name)
        df = pd.read_csv(
            os.path.join(files_directory, file_name),
            dtype={"dia_jogo": str, "hora_jogo": str},
        )
        if len(df) == 0:
            print(f"Arquivo {file_name} processado: {len(df)} linhas adicionadas")
            continue

        df["dia_jogo"] = df["dia_jogo"].astype(str)
        df["hora_jogo"] = df["hora_jogo"].astype(str)
        df["data_jogo"] = df.apply(
            lambda row: transform.add_date_column(
                file_name, row["dia_jogo"], row["hora_jogo"]
            ),
            axis=1,
        )
        df["data_extracao"] = df.apply(
            lambda _: transform.add_extration_date_column(file_name), axis=1
        )
        dataframes.append(df)
        print(f"Arquivo {file_name} processado: {len(df)} linhas adicionadas")

    if not dataframes:
        print("Aviso: Nenhum dataframe foi processado.")
        return pd.DataFrame()

    df_all = pd.concat(dataframes, ignore_index=True)
    df_all = df_all.reset_index().rename(columns={"index": "id_odd"})
    df_all["id_odd"] = df_all["id_odd"] + 1

    return df_all


def create_tables(df_list, output_directory):
    if all(df.empty for df in df_list):
        print("Aviso: nenhuma linha nos dataframes recebidos!")
        return

    for i, df in enumerate(df_list):
        df.sort_values("data_jogo")
        df_last_odds = transform.get_all_last_odds(df)
        df.to_csv(f"{output_directory}/odds_{i}.csv", index=False)
        df_last_odds.to_csv(f"{output_directory}/last_odds_{i}.csv", index=False)
        print(f"Dataframe {i} salvo em {output_directory}/odds_{i}.csv")

    df_all = pd.concat(df_list, ignore_index=True)
    df_times = transform.distinct_teams_from_df_list(df_all)
    if not df_times.empty:
        df_times.to_csv(f"{output_directory}/times.csv", index=False)
        print(f'Times salvos no arquivo "{output_directory}/times.csv"')

    df_games = transform.distinct_games_from_df_list(df_all)
    if not df_games.empty:
        df.sort_values("data_jogo")
        df_games.to_csv(f"{output_directory}/jogos.csv", index=False)
        print(f'Jogos salvos no arquivo "{output_directory}/jogos.csv"')


if __name__ == "__main__":
    output_directory = "./output/gen_tables"

    empate_conta_directory = "./output/empate_conta"
    empate_anula_directory = "./output/empate_anula"
    empate_conta_files = file.list_directory(empate_conta_directory)
    empate_anula_files = file.list_directory(empate_anula_directory)

    df_anula_all = create_general_dataframe(empate_anula_files, empate_anula_directory)
    df_conta_all = create_general_dataframe(empate_conta_files, empate_conta_directory)
    print(f"Total de linhas processadas:")
    print(f"\tEmpate anula: {len(df_anula_all)}")
    print(f"\tEmpate conta: {len(df_conta_all)}")

    create_tables([df_anula_all, df_conta_all], output_directory)
