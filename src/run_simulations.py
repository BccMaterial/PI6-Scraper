import pandas as pd

from utils import transform


def distribute_bets(obj):
    b_house = int(obj["num_apostas"] * obj["pb_vitoria_casa"])
    b_draw = int(obj["num_apostas"] * obj["pb_empate"])
    b_out = int(obj["num_apostas"] * obj["pb_derrota_casa"])
    return [b_house, b_draw, b_out]


if __name__ == "__main__":
    df = pd.read_csv("./output/tables/jogos.csv")
    teams_df = pd.read_csv("./output/gen_tables/times.csv")
    last_odds_df = transform.get_all_last_odds(
        pd.read_csv("./output/gen_tables/odds_1.csv")
    )
    output_file = "./output/gen_tables/apostas.csv"

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
                bet_obj = {
                    **obj,
                    "id_time_fora": transform.get_team_id(teams_df, obj["time_fora"]),
                    "id_time_casa": transform.get_team_id(teams_df, obj["time_casa"]),
                    "id_aposta": last_id,
                    "palpite": selected,
                    "valor": 200.0,
                    "multiplicador_aposta": obj[multiplier_column],
                    "id_perfil": None,
                }

                bet_obj["lucro"] = (
                    bet_obj["valor"] * bet_obj[multiplier_column]
                    if bet_obj["vencedor"] == bet_obj["palpite"]
                    else bet_obj["valor"] * -1
                )
                last_id += 1
                bets_df = pd.concat(
                    [bets_df, pd.DataFrame([bet_obj])], ignore_index=True
                )
    bets_df.to_csv(output_file, index=False)
    print(f'Apostas feitas, salvo em "{output_file}"!')
