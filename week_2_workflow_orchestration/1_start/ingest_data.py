#!/usr/bin/env python
# coding: utf-8

import os
from datetime import timedelta
from time import time

import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector


@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url: str):
    csv_name = 'output.csv'
    if url.endswith('gz'):
        csv_name = 'output.csv.gz'

    os.system(f"wget {url} -O {csv_name}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    return df

@task(log_prints=True)
def transform_data(df):
    print('pre: missing passenger count {df}'.format(df=df['passenger_count'].isin([0]).sum()))
    df = df[df['passenger_count'] != 0]
    print('post: missing passenger count {df}'.format(df=df['passenger_count'].isin([0]).sum()))

    return df


@task(log_prints=True, retries=3)
def ingest_data(table_name, df):

    database_block = SqlAlchemyConnector.load("postgres-connector")
    with database_block.get_connection(begin=False) as engine:
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')

@flow(name='Subflow', log_prints=True)
def log_subflow(table_name: str):
    print('Table name: {tn}'.format(tn=table_name))


@flow(name="Ingest Flow")
def main_flow(table_name: str ):
    table_name = table_name
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    
    log_subflow(table_name)
    
    row_data = extract_data(url)
    clean_data = transform_data(row_data)
    ingest_data(table_name, clean_data)


if __name__ == '__main__':
    main_flow("yellow_taxi_data")

