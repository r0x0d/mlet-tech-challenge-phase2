from datetime import datetime
import pandas


def convert_raw_to_dataframe(data: dict[str, list[str]]) -> pandas.DataFrame:
    """Convert a dynamic dictionary to a pandas dataframe"""
    dataframe = pandas.DataFrame.from_dict(data, orient="index").transpose()
    dataframe['qtde_teorica'] = dataframe['qtde_teorica'].str.replace('.', '', regex=False)
    dataframe['qtde_teorica'] = pandas.to_numeric(dataframe['qtde_teorica'], errors='coerce')

    # Remover o separador de milhar e substituir virgula por ponto
    dataframe['participacao_percentual'] = dataframe['participacao_percentual'].str.replace('.', '', regex=False)
    dataframe['participacao_percentual'] = dataframe['participacao_percentual'].str.replace(',', '.', regex=False)
    dataframe['participacao_percentual'] = pandas.to_numeric(dataframe['participacao_percentual'], errors='coerce')

    dataframe["data_pregao"] = datetime.now().strftime("%d/%m/%Y")
    return dataframe


def write_to_parquet(dataframe: pandas.DataFrame, filename: str) -> None:
    """Write a given dataframe to parquet file."""
    pandas.DataFrame.to_parquet(dataframe, filename)
