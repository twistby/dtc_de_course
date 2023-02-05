
## Second week of Data Talk Club Data Engeniering Zoomcamp

### Workflow Orchestration
**What is Workflow?**
It is a set of sequences or steps of tasks and data processes between these steps. In other words, it tells us about the work's execution and data flow. In the previous workflow, the stage has a connection to the next one, which means data of earlier steps processes to the next one. If these steps are individual and no data flow between them, then it is not a workflow.

 **What is Orchestration?**
It is configuring, managing, and coordinating computer applications and services automatically. It is different from automation. Automation is automating a single task to make our business more efficient and productive, but it automates the whole process and workflow, which may contain different disparate systems.

 
Data orchestration tools automate the process of bringing data together from multiple sources, standardizing it, and preparing it for data analysis.


Here is a list of five popular open-source data orchestration tools

1. Airflow
2. Dagster
3. Argo
4. Prefect
5. Luigi

  
### Prefect
In this zoomcamp we using Prefect.

Installation
`pip install -U prefect
`

Also we need this packets:

 - pandas==1.5.2
 - prefect-sqlalchemy==0.2.2
 - prefect-gcp[cloud_storage]==0.2.4
 - protobuf==4.21.11
 - pyarrow==10.0.1
 - pandas-gbq==0.18.1
 - psycopg2-binary==2.9.5
 - sqlalchemy==1.4.46

To check Prefect version type
`prefect --version`

Using the script ***ingest_data.py*** from the first week. We consider this to be our flow.

We split it up into several tasks:
1. Extracting data
2. Transformation data
3. Ingestion data

To show that each flow can have sub-flows, we add a sub-flow that displays the name of the table where the information will be loaded.

For flows and sub-flows we using decorator ***@flow***

For tasks we using decorator ***@task***

When we execute the code python ***ingest_data.py***, we can see the Prefect logs in the terminal.

**Orion UI**

We can start Orion UI with the command prefect orion start. Then we can see the UI dashboard at `http://127.0.0.1:4200`

In the Orion dashboard we can see flow runs, flows, deployments, work queues, blocks, notification ...

**Blocks in Orion**

Blocks allow users to interface with external systems and configurations across flows.

 
We creating block with *SQLAlchemy Connector* to use it in code as sql-engine.

    database_block = SqlAlchemyConnector.load("postgres-connector")    
    with database_block.get_connection(begin=False) as engine:
		...




### ETL with GCP & Prefect

To register GCP blocks
  `prefect block register -m prefect_gcp`

**Part 1**

 
1. Load csv file from web to DataFrame

		pd.read_csv(file_url)

2. Clean data

3. Write data localy in parquet file

		df.to_parquet(path, compression='gzip')

4. Load parquet file in Google Cloud Storage

- in Orion UI

	- create GCP Credentials block
	- create GCS Bucket block
	- add GCP Credentials in GCS Bucket

  
- in code 

		gcs_buck = GcsBucket.load("block-name")
		gcs_buck.upload_from_path(from_path=local_path, to_path=gcs_path)	

**Part 2**

1. Load parquet file from Google Cloud Storage to local directory

		gcs_block.get_directory(from_path=gsc_path, local_path=local_path)

  
2. Load data from parquet file to pd.DataFrame

		df = pd.read_parquet(path)

  

3. Load pd.DataFrame to BigQuery

		gcp_credentials_block = GcpCredentials.load("doc-gcp-creds")

		df.to_gbq(
			destination_table='database_name.table_name',
			project_id='GCP project ID',
			credentials=gcp_credentials_block.get_credentials_from_service_account(),
			chunksize=500_000,
			if_exists='append'
		)


### Prefect flow deployment using CLI

  

1. Build

		prefect deployment build ./parameterized_flow.py:etl_parent_flow -n "Parameterized ETL"

  

We can change default parameters in flow_name-deployment.yaml file in section "parameters"

	parameters: {"color": "yellow", "year": 2021, "months": [2, 3]}

  

2. Apply

		prefect deployment apply etl_parent_flow-deployment.yaml

  

3. Start
 
Run the agent:
		
	prefect agent start --work-queue "default"

  
Run deployment from UI or from CLI:

	prefect deployment run "Deployment name" -p "parameters for flow"

  
  

### Prefect flow deployment using Docker and Python script

  

1. Create docker image from dockerfile:

		FROM prefecthq/prefect:2.7.11-python3.11

		COPY docker-requirements.txt .

		RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

		RUN mkdir -p /opt/prefect/data/yellow

		COPY 3_deployment /opt/prefect/flows/

  
2. Create Docker Container Block in UI

 
3. Create python script:

  

		from prefect.infrastructure.docker import DockerContainer

		from prefect.deployments import Deployment

		from parameterized_flow import etl_parent_flow
		  

		docker_block = DockerContainer.load("dtc") #Load docker-container block with link to docker image made befor
		  

		docker_dep = Deployment.build_from_flow(

		flow=etl_parent_flow, # flow name in parameterized_flow.py

		name='doker-flow', # name of deployment

		infrastructure=docker_block # docker block

		)
		  
		  

		if __name__ == '__main__':
			docker_dep.apply() # aplying parameters and creating deployment

  

4. Run flow in docker container

		prefect deployment run "Deployment name" -p "parameters for flow"