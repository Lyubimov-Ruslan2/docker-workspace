import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click
import os

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, url):
    engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")

    print(f"Downloading data from {url}...")
    
    if url.endswith('.parquet'):
        df = pd.read_parquet(url)
    else:
        df = pd.read_csv(url)

    print(f"Inserting data into table: {target_table}...")
    
    df.head(0).to_sql(name=target_table, con=engine, if_exists="replace")
    
    df.to_sql(name=target_table, con=engine, if_exists="append")
    print("Success!")

@click.command()
@click.option("--pg-user", default="root")
@click.option("--pg-pass", default="root")
@click.option("--pg-host", default="localhost")
@click.option("--pg-port", default=5432, type=int)
@click.option("--pg-db", default="ny_taxi")
@click.option("--target-table", required=True, help="Name of the table in Postgres")
@click.option("--url", required=True, help="URL of the .csv or .parquet file")
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, url):
    run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, url)

if __name__ == "__main__":
    main()