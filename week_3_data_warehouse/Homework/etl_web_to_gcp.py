import os
from datetime import timedelta
from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket



@task(retries=3, log_prints=True, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(year: str, months: list[int]) -> pd.DataFrame:
    """Read data from url to pandas DataFrame"""
    links = []
    for month in months:
        dataset_file = f'fhv_tripdata_{year}-{month:02}'
        dataset_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz'
        links.append(dataset_url)

    df = pd.concat((pd.read_csv(f) for f in links), ignore_index=True)
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write data to local parquet file."""
    absolute_path = os.path.dirname(__file__)
    relative_path = f'data/'
    full_path = os.path.join(absolute_path, relative_path)
    path = Path(f'{full_path}/{dataset_file}.gz')
    df.to_csv(path, compression='gzip')

    return path


@task()
def write_to_gcs(path: Path, file_name: str) -> None:
    """Write parquet file to google cloud storage."""
    gcs_buck = GcsBucket.load("dtc-gcs")
    gcs_buck.upload_from_path(
        from_path=f"{path}",
        to_path=f'data/fhv/{file_name}.gz',
        timeout=600
    )


@flow(name="Ingest to FHV NY data")
def etl_web_to_gcs(year: int = 2019, months: list[int] = [1,2]) -> None:
    """The main ETL function"""
    dataset_file = f'fhv_tripdata_{year}.csv'
    df = fetch(year, months)
    path = write_local(df, dataset_file)
    write_to_gcs(path, dataset_file)


if __name__ == '__main__':
    year = 2019
    months = [3]
    etl_web_to_gcs(year, months)