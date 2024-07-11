from mlet_tech_challenge_phase2.dataframe import (
    convert_raw_to_dataframe,
    write_to_parquet,
)
from mlet_tech_challenge_phase2.scrapper import WebScrapper, parse_data

# URL para mapear o endereço de consulta do pregão da B3
B3_AJUSTES_DO_PREGAO = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/derivativos/ajustes-do-pregao/"


def main() -> int:
    scrapper = WebScrapper()
    scrapper.navigate_to(
        B3_AJUSTES_DO_PREGAO,
        "Ajustes do pregão | B3",
    ).switch_to_iframe("bvmf_iframe")
    table_data = scrapper.get_table_data()
    parsed_data = parse_data(table_data)

    dataframe = convert_raw_to_dataframe(parsed_data)
    write_to_parquet(dataframe, "raw-bovespa.parquet")

    # client = get_client()
    # create_bucket(client, "raw-bovespa")
    return 0


if __name__ == "__main__":
    main()
