import pandas as pd

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
url = f'{prefix}/yellow_tripdata_2021-01.csv.gz'

# first read without fixing types
df = pd.read_csv(url, nrows=100)
print("=== Before fixing types ===")
print(df.dtypes)
print(df.shape)

# now fix the types
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

df = pd.read_csv(
    url,
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)

print("\n=== After fixing types ===")
print(df.dtypes)
print("\nFirst 5 rows:")
print(df.head())