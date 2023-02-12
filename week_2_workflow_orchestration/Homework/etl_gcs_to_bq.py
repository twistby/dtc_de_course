
import os
from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task()
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download data from GCS."""
    gsc_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("dtc-gcs")

    absolute_path = os.path.dirname(__file__)
    relative_path = f'data/from_gcs'
    full_path = os.path.join(absolute_path, relative_path)


    gcs_block.get_directory(from_path=gsc_path, local_path=full_path)

    return Path(full_path)


@task()
def transform_parquet_to_df(path: Path) -> pd.DataFrame:
    """Transform parquet file to DataFrame"""
    df = pd.read_parquet(path)

    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write daat to BigQuery."""
    
    gcp_credentials_block = GcpCredentials.load("doc-gcp-creds")
    
    df.to_gbq(
        destination_table='dtc_zoomcamp.trips',
        project_id='lithe-vault-375510',
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists='append'
    )

@flow(log_prints=True)
def etl_to_bq(color: str, year: int, month: int) -> int:
    """Main ETL flow to load data into Big Query"""
    processed_rows = 0
    path = extract_from_gcs(color, year, month)
    df = transform_parquet_to_df(path)
    write_bq(df)
    processed_rows += int(df.shape[0])
    df.iloc[0:0]

    print(f'Processed {processed_rows} rows')
    return processed_rows


@flow(log_prints=True)
def gcs_to_bq_parent_flow(color: str = 'yellow', year: int = 2020, months: list[int] = [1, 2] ):
    """Parent flow."""
    total_processed_rows = 0
    for month in months:
        total_processed_rows += etl_to_bq(color, year, month)
    
    print(f'Total number of processed rows: {total_processed_rows}')


if __name__ == '__main__':
    color = 'yellow'
    year = 2020
    months = [1]
    gcs_to_bq_parent_flow(color, year, months)
