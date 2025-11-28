import os

import pandas as pd

from utils import file, transform

if __name__ == "__main__":
    output_directory = "./output/parsed_tables"
    empate_conta_directory = "./output/empate_conta"
    empate_conta_files = file.list_directory(empate_conta_directory)
    dataframes = list()

    for file_name in empate_conta_files:
        file_name = str(file_name)
        df = pd.read_csv(
            os.path.join(empate_conta_directory, file_name),
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
        dataframes.append(df)
        print(f"Arquivo {file_name} processado: {len(df)} linhas adicionadas")

    if not dataframes:
        print("Aviso: Nenhum dataframe foi processado. Saindo...")
        exit(0)

    df_all = pd.concat(dataframes, ignore_index=True)
    df_all = df_all.reset_index().rename(columns={"index": "id_odd"})
    df_all["id_odd"] = df_all["id_odd"] + 1
    print(f"Total de linhas processadas: {len(df_all)}")

    if not df_all.empty:
        df_all.to_csv(f"{output_directory}/odds.csv", index=False)
        print('Odds salvas no arquivo "./output/parsed_tables/odds.csv"')
    else:
        print("Aviso: nenhuma linha no dataframe principal. Saindo...")
        exit(0)

    df_times = transform.distinct_teams_from_df_list(df_all)
    if not df_times.empty:
        df_times.to_csv(f"{output_directory}/times.csv", index=False)
        print(f'Times salvos no arquivo "{output_directory}/times.csv"')

    df_games = transform.distinct_games_from_df_list(df_all)
    if not df_games.empty:
        df_games.to_csv(f"{output_directory}/jogos.csv", index=False)
        print(f'Jogos salvos no arquivo "{output_directory}/jogos.csv"')
