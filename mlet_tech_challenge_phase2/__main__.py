from datetime import datetime

from mlet_tech_challenge_phase2.dataframe import (
    convert_raw_to_dataframe,
    write_to_parquet,
)
from mlet_tech_challenge_phase2.scrapper import WebScrapper
from mlet_tech_challenge_phase2.storage import S3Storage

# URL para mapear o endereço de consulta do pregão da B3
B3_CARTEIRA_DO_DIA = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br"


def main() -> int:
    scrapper = WebScrapper()
    scrapper.navigate_to(
        B3_CARTEIRA_DO_DIA,
        "Índices",
    ).select_search_type("2")

    table_data = scrapper.get_table_data()
    dataframe = convert_raw_to_dataframe(table_data)
    write_to_parquet(dataframe, "raw-bovespa.parquet")

    storage = S3Storage()
    storage.create_bucket(name="raw-bovespa")
    today = datetime.now()
    storage.upload_file(
        bucket="raw-bovespa",
        file_name="raw-bovespa.parquet",
        object_name=f"{today.year}/{today.month}/{today.day}/bovespa.parquet",
    )
    return 0


if __name__ == "__main__":
    main()
