#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]



def run(
    pg_user: str = "root",
    pg_pass: str = "root",
    pg_host: str = "localhost",
    pg_port: int = 5432,
    pg_db: str = "ny_taxi",
    year: int = 2021,
    month: int = 1,
    target_table: str = "yellow_taxi_data",
    chunksize: int = 100000,
    prefix: str = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow",
):
    url = f"{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz"

    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table, con=engine, if_exists="replace"
            )
            first = False
        df_chunk.to_sql(name=target_table, con=engine, if_exists="append")


@click.command()
@click.option("--pg-user", default="root", show_default=True, help="Postgres user")
@click.option("--pg-pass", default="root", show_default=True, help="Postgres password")
@click.option("--pg-host", default="localhost", show_default=True, help="Postgres host")
@click.option("--pg-port", default=5432, show_default=True, help="Postgres port", type=int)
@click.option("--pg-db", default="ny_taxi", show_default=True, help="Postgres database")
@click.option("--year", default=2021, show_default=True, type=int, help="Dataset year")
@click.option("--month", default=1, show_default=True, type=int, help="Dataset month")
@click.option(
    "--target-table",
    default="yellow_taxi_data",
    show_default=True,
    help="Destination table name",
)
@click.option(
    "--chunksize",
    default=100000,
    show_default=True,
    type=int,
    help="Number of rows per chunk",
)
@click.option(
    "--prefix",
    default="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow",
    show_default=True,
    help="Base URL prefix for the dataset",
)
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize, prefix):
    """Ingest NYC taxi data into Postgres."""

    run(
        pg_user=pg_user,
        pg_pass=pg_pass,
        pg_host=pg_host,
        pg_port=pg_port,
        pg_db=pg_db,
        year=year,
        month=month,
        target_table=target_table,
        chunksize=chunksize,
        prefix=prefix,
    )


if __name__ == "__main__":
    main()
    














