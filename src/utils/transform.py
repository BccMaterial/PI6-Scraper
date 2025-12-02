from datetime import datetime, timedelta

import pandas as pd


def add_extration_date_column(file_name: str):
    parsed_date = datetime.strptime(file_name.replace("-dados.csv", ""), "%Y-%m-%d")
    parsed_date = parsed_date.replace(hour=0, minute=0, second=0)
    return parsed_date


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


def distinct_teams_from_df_list(df_all):

    distinct_teams = (
        pd.concat([df_all["time_casa"], df_all["time_fora"]])
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )
    df_times = (
        distinct_teams.to_frame(name="time")
        .reset_index()
        .rename(columns={"index": "id"})
    )
    df_times["id"] = df_times.index + 1
    return df_times


def distinct_games_from_df_list(df_all):
    df_all = df_all.copy()
    df_all["data_jogo"] = pd.to_datetime(df_all["data_jogo"])
    df_all["data_sem_horario"] = df_all["data_jogo"].dt.date

    # Encontrar o índice da última partida para cada combinação de time_casa, time_fora e data
    idx = df_all.groupby(["time_casa", "time_fora", "data_sem_horario"])[
        "data_jogo"
    ].idxmax()

    # Selecionar as linhas com os horários mais recentes
    df_teams = df_all.loc[idx, ["time_casa", "time_fora", "data_jogo"]].reset_index(
        drop=True
    )

    # Remover a coluna auxiliar
    df_teams = df_teams.drop(columns=["data_sem_horario"], errors="ignore")

    # Adicionar ID sequencial
    df_teams = df_teams.reset_index().rename(columns={"index": "id_jogo"})
    df_teams["id_jogo"] = df_teams["id_jogo"] + 1

    return df_teams


def get_all_last_odds(df):
    # Encontrar os índices das linhas com data_extracao máxima em cada grupo
    idx = df.groupby(
        [
            "time_casa",
            "time_fora",
            "data_jogo",
        ]
    )["data_extracao"].idxmax()

    # Selecionar as linhas completas usando os índices
    return df.loc[idx].reset_index(drop=True)


def merge_last_odds_with_games(games_df, last_odds_df):
    games_df.dropna(subset=["num_apostas"])
    return games_df.merge(
        last_odds_df[
            [
                "time_casa",
                "time_fora",
                "data_jogo",
                "mult_vitoria_time_1",
                "mult_empate",
                "mult_vitoria_time_2",
            ]
        ],
        on=["time_casa", "time_fora", "data_jogo"],
        how="left",
    )

def merge_last_odds_with_games_no_draw(games_df, last_odds_df):
    games_df.dropna(subset=["num_apostas"])
    return games_df.merge(
        last_odds_df[
            [
                "time_casa",
                "time_fora",
                "data_jogo",
                "mult_vitoria_time_1",
                "mult_vitoria_time_2",
            ]
        ],
        on=["time_casa", "time_fora", "data_jogo"],
        how="left",
    )

def get_team_id(df, team):
    found_team = df[df["time"] == team].head(1)

    if not found_team.empty:
        return found_team.iloc[0]["id"]
    else:
        return None
