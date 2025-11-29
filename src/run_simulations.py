import pandas as pd


def distribute_bets(obj):
    b_house = int(obj["num_apostas"] * obj["pb_vitoria_casa"])
    b_draw = int(obj["num_apostas"] * obj["pb_empate"])
    b_out = int(obj["num_apostas"] * obj["pb_derrota_casa"])
    return [b_house, b_draw, b_out]


def get_team_id(df, team):
    found_team = df[df["time"] == team].head(1)

    if not found_team.empty:
        return found_team.iloc[0]["id"]
    else:
        return None


if __name__ == "__main__":
    df = pd.read_csv("./output/tables/jogos.csv")
    teams_df = pd.read_csv("./output/gen_tables/times.csv")
    output_file = "./output/gen_tables/apostas.csv"

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
                        multiplier_column = ""
                    case 1:
                        selected = "Empate"
                    case 2:
                        selected = obj["time_fora"]
                bet_obj = {
                    **obj,
                    "id_time_fora": get_team_id(teams_df, obj["time_fora"]),
                    "id_time_casa": get_team_id(teams_df, obj["time_casa"]),
                    "id_aposta": last_id,
                    "palpite": selected,
                    "valor": 200.0,
                }
                last_id += 1
                bets_df = pd.concat(
                    [bets_df, pd.DataFrame([bet_obj])], ignore_index=True
                )
    bets_df.to_csv(output_file, index=False)
    print(f'Apostas feitas, salvo em "{output_file}"!')
