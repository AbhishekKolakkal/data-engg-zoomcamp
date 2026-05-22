import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

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

parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

def ingest_data(url, engine, target_table, chunksize=100000):
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    # get first chunk
    first_chunk = next(df_iter)

    # create empty table first
    first_chunk.head(0).to_sql(
        name=target_table,
        con=engine,
        if_exists="replace"
    )
    print(f"Table {target_table} created")

    # insert first chunk
    first_chunk.to_sql(
        name=target_table,
        con=engine,
        if_exists="append"
    )
    print(f"Inserted first chunk: {len(first_chunk)} rows")

    # insert remaining chunks
    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

    print(f"Done ingesting into {target_table}")


def main():
    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    ingest_data(
        url=url,
        engine=engine,
        target_table='yellow_taxi_trips',
        chunksize=100000
    )

if __name__ == '__main__':
    main()