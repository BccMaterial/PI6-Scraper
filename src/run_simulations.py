from operator import mul

import pandas as pd

from utils import transform


def distribute_bets(obj):
    b_house = int(obj["num_apostas"] * obj["pb_vitoria_casa"])
    b_draw = int(obj["num_apostas"] * obj["pb_empate"])
    b_out = int(obj["num_apostas"] * obj["pb_derrota_casa"])
    return [b_house, b_draw, b_out]

def calculate_fair_probs(obj):
    p_win = 1 / obj["mult_vitoria_time_1"]
    p_draw = 1 / obj["mult_empate"]
    p_lose = 1 / obj["mult_vitoria_time_2"]
    p_total = p_win + p_draw + p_lose
    return [p_win, p_draw, p_lose, p_total]

if __name__ == "__main__":
    bet_value = 50.0
    df = pd.read_csv("./output/tables/jogos_rod.csv")
    teams_df = pd.read_csv("./output/gen_tables/times.csv")
    last_odds_df = transform.get_all_last_odds(
        pd.read_csv("./output/gen_tables/odds_1.csv")
    )
    output_file = "./output/gen_tables/apostas_2.csv"

    df = transform.merge_last_odds_with_games(df, last_odds_df)

    print(df)
    print()
    print(f"Total de apostas: {df["num_apostas"].sum()}")
    bets_df = pd.DataFrame()

    obj_list = df.to_dict("records")
    last_id = 1
    for obj in obj_list:
        bet_tuple = distribute_bets(obj)
        for i, bets_count in enumerate(bet_tuple):
            for _ in range(0, bets_count):
                selected = None
                multiplier_column = None

                match i:
                    case 0:
                        selected = obj["time_casa"]
                        multiplier_column = "mult_vitoria_time_1"
                    case 1:
                        selected = "Empate"
                        multiplier_column = "mult_empate"
                    case 2:
                        selected = obj["time_fora"]
                        multiplier_column = "mult_vitoria_time_2"
                # bet_value = calculate_value(50, obj[multiplier_column])
                bet_obj = {
                    **obj,
                    "id_time_fora": transform.get_team_id(teams_df, obj["time_fora"]),
                    "id_time_casa": transform.get_team_id(teams_df, obj["time_casa"]),
                    "id_time_vencedor": transform.get_team_id(
                        teams_df, obj["vencedor"]
                    ),
                    "id_aposta": last_id,
                    "palpite": selected,
                    "valor": bet_value,
                    "multiplicador_aposta": obj[multiplier_column],
                    "id_perfil": None,
                }

                p_win, p_draw, p_lose, p_total = calculate_fair_probs(bet_obj)

                bet_obj = {
                    **bet_obj,
                    "pb_vitoria_casa_real": p_win,
                    "pb_empate_real": p_draw,
                    "pb_derrota_casa_real": p_lose,
                    "pb_total_real": p_total,
                }
                
                bet_obj["id_time_palpite"] = transform.get_team_id(
                    teams_df, bet_obj["palpite"]
                )
                bet_obj["lucro"] = (
                    bet_obj["valor"] * bet_obj[multiplier_column]
                    if bet_obj["vencedor"] == bet_obj["palpite"]
                    else bet_obj["valor"] * -1
                )
                last_id += 1
                print(f"Aposta {last_id} feita!")
                bets_df = pd.concat(
                    [bets_df, pd.DataFrame([bet_obj])], ignore_index=True
                )
    bets_df.to_csv(output_file, index=False)
    print(f'Apostas feitas, salvo em "{output_file}"!')
