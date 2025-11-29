from pprint import pprint

import pandas as pd

from utils import transform


def int_no_error(string):
    try:
        val = int(string)
        return val
    except ValueError:
        return string


def float_no_error(string):
    try:
        val = float(string)
        return val
    except ValueError:
        return string


def get_winner_multiplier(game_obj):
    if game_obj["vencedor"] == "Empate":
        return game_obj["mult_empate"]
    if game_obj["vencedor"] == game_obj["time_casa"]:
        return game_obj["mult_vitoria_time_1"]
    if game_obj["vencedor"] == game_obj["time_fora"]:
        return game_obj["mult_vitoria_time_2"]


if __name__ == "__main__":
    df_profiles = pd.read_csv("./output/tables/perfis.csv")
    print("Bem vindo!")
    print(df_profiles)
    prof_id = input("Selecione um perfil: ")
    prof_obj = df_profiles[df_profiles["id_perfil"] == int(prof_id)].to_dict("records")
    df_odds = transform.get_all_last_odds(pd.read_csv("./output/gen_tables/odds_1.csv"))

    if not prof_obj:
        print(
            'Perfil não encontrado! Caso queira adicionar um perfil, edite o arquivo "./output/tables/perfis.csv".'
        )
        exit(0)

    prof_obj = prof_obj[0]
    print("Pegando rodadas...")
    df_games = pd.read_csv("./output/tables/jogos.csv")
    df_teams = pd.read_csv("./output/tables/times.csv")
    df_bets = pd.read_csv("./output/tables/apostas.csv")
    df_games = transform.merge_last_odds_with_games(df_games, df_odds)
    rounds = df_games["rodada"].unique().tolist()
    selected_round = -1
    while True:
        pprint(rounds)
        selected_round = int_no_error(input("Selecione uma rodada (* p/ todas): "))
        if int_no_error(selected_round) in rounds or selected_round == "*":
            break
        print("Rodada não encontrada! Selecione uma que está na lista.")

    if selected_round != "*":
        print("Selecionando partidas...")
        df_games = df_games[df_games["rodada"] == int(selected_round)]
    print("Partidas que você vai apostar:")
    print(df_games)
    print()
    last_id = df_bets["id_aposta"].max()
    for game in df_games.to_dict("records"):
        print(f'{game["data_jogo"]} - {game["time_casa"]} x {game["time_fora"]}')
        guess = input(
            f'Qual é o seu palpite? ({game["time_casa"]}/{game["time_fora"]}/Empate): '
        )
        bet_value = 0
        while True:
            bet_value = float_no_error(
                input(f'Quanto você quer apostar? (Saldo: {prof_obj["saldo"]}): ')
            )
            if bet_value == "+":
                prof_obj["saldo"] = 100.0
                continue

            if bet_value <= prof_obj["saldo"]:
                break
            print("Não pode apostar mais do que você tem!")

        prof_obj["saldo"] -= bet_value
        if game["vencedor"] == guess:
            money_to_add = bet_value * get_winner_multiplier(game)
            prof_obj["saldo"] += money_to_add
            print(f"+ {money_to_add}")
        else:
            print(f"- {bet_value}")

        bet_obj = {
            **game,
            "id_time_fora": transform.get_team_id(df_teams, game["time_fora"]),
            "id_time_casa": transform.get_team_id(df_teams, game["time_casa"]),
            "id_aposta": last_id,
            "palpite": guess,
            "valor": bet_value,
            "multiplicador_aposta": get_winner_multiplier(game),
            "id_perfil": prof_id,
        }
        bet_obj["lucro"] = (
            bet_obj["valor"] * get_winner_multiplier(game)
            if bet_obj["vencedor"] == bet_obj["palpite"]
            else bet_obj["valor"] * -1
        )
        last_id += 1
        df_bets = pd.concat([df_bets, pd.DataFrame([bet_obj])], ignore_index=True)
    df_bets.to_csv("./output/tables/apostas.csv", index=False)
    print(f'Apostas feitas, salvo em "./output/tables/apostas.csv"!')
