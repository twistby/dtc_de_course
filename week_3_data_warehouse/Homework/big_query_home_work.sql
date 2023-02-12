SELECT count(1) FROM `lithe-vault-375510.dtc_zoomcamp.external_fhv_tripdata`;

CREATE OR REPLACE TABLE lithe-vault-375510.dtc_zoomcamp.external_fhv_tripdata_non_partitoned AS
SELECT * FROM lithe-vault-375510.dtc_zoomcamp.external_fhv_tripdata;

SELECT count(*) FROM lithe-vault-375510.dtc_zoomcamp.external_fhv_tripdata_non_partitoned;

SELECT count(DISTINCT Affiliated_base_number) as abn_count FROM lithe-vault-375510.dtc_zoomcamp.external_fhv_tripdata_non_partitoned
GROUP BY Affiliated_base_number;

SELECT  DISTINCT Affiliated_base_number, count( 1) as abn_count FROM lithe-vault-375510.dtc_zoomcamp.external_fhv_tripdata
GROUP BY Affiliated_base_number;

SELECT count(1) from lithe-vault-375510.dtc_zoomcamp.external_fhv_tripdata_non_partitoned
where PUlocationID IS NULL AND DOlocationID IS NULL;

CREATE OR REPLACE TABLE lithe-vault-375510.dtc_zoomcamp.fhv_tripdata_partitoned_clustered
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
SELECT * FROM lithe-vault-375510.dtc_zoomcamp.external_fhv_tripdata;

SELECT DISTINCT Affiliated_base_number FROM lithe-vault-375510.dtc_zoomcamp.fhv_tripdata_partitoned_clustered
WHERE pickup_datetime BETWEEN  '2019-03-01' and '2019-03-31'

