import pandas as pd


def distribute_bets(obj):
    b_house = int(obj["num_apostas"] * obj["pb_vitoria_casa"])
    b_draw = int(obj["num_apostas"] * obj["pb_empate"])
    b_out = int(obj["num_apostas"] * obj["pb_derrota_casa"])
    return [b_house, b_draw, b_out]


if __name__ == "__main__":
    df = pd.read_csv("./output/tables/jogos.csv")
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
                match i:
                    case 0:
                        selected = obj["time_casa"]
                    case 1:
                        selected = "Empate"
                    case 2:
                        selected = obj["time_fora"]
                bet_obj = {
                    **obj,
                    "id_aposta": last_id,
                    "palpite": selected,
                    "valor": 200.0,
                }
                last_id += 1
                bets_df = pd.concat(
                    [bets_df, pd.DataFrame([bet_obj])], ignore_index=True
                )
    bets_df.to_csv("./output/gen_tables/bets.csv", index=False)
    print("Apostas feitas, salvo em ./output/tables/bets.csv!")
