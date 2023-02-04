
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
