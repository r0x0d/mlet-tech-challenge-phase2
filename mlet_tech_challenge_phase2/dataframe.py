import pandas


def convert_raw_to_dataframe(data: dict[str, list[str]]) -> pandas.DataFrame:
    """Convert a dynamic dictionary to a pandas dataframe"""
    dataframe = pandas.DataFrame.from_dict(data, orient="index")
    return dataframe.transpose()


def write_to_parquet(dataframe: pandas.DataFrame, filename: str) -> None:
    """Write a given dataframe to parquet file."""
    pandas.DataFrame.to_parquet(dataframe, filename, engine="fastparquet")
