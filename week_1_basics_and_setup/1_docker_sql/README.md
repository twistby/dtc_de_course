
# Docker and SQL

## 1. Docker

**Docker** is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.

Why we should use a docker:

   - Reproducibility
   - Local experiments
   - Integration tests (CI/CD)
   - Running tasks on the cloud
   - Spark
   - Serverless (Azure function, AWS Lambda, Google function)


####Tasks:
   - Create a container based on Ubuntu and install python, pandas and the postgres connection library inside the container, necessary for the date pipline.
   - Create a Postgres container for database. Connect with Postgres database in container from local machine via pgcli
   - Create container with pgAdmin. Connect with database container. Run pgAdmin on local machine.
   - Create container to ingest data to database.
   - Setup Docker Compose to satrt database container and PGAdmin conteiner


##### To check that docker is installed correctly we run:

`docker run hello-world`


#### Ubuntu container
#####     To create Ubuntu container we run

`docker run -it ubuntu bash`

> "run" - start new container from an image
>  "-it" mean "-i -t" intaractive terminal
> "ubuntu" - image name
> "bash" - execute bash after container start

**Every time we start the container, it starts with a clean slate. No changes created during the previous start-up are saved.**

####Python container
To create Python container we run

`docker ru -it python:3.9.1`
>"python:3.9.1" - python image name, 3.9.1 python version

`docker ru -it --entrypoint=bash python:3.9.1`

>"--entrypoint=bash"  what will be executed at the start of the container

**We can install pandas in container in -it mode. But this will have no effect the next time you start the container.**

####Dockerfile
A **Dockerfile** is a text document that contains all the commands a user could call on the command line to assemble a container

To install pandas in container we use next Dockerfile:

    FROM python:3.9.1

    RUN pip install pandas

    ENTRYPOINT [ "bash" ]

>"FROM" image name

>"RUN" what to do befor start container

>"ENTRYPOINT" what execute at the start of the container

To apply Dockerfile we need run "**build**" command, specify name and tag for new image and add the path to Dockerfile

 `docker build -t test:pandas . `

When we run test:pandas container pandas will already be installed

To copy a python script into a container and execute it when the container starts, change the docker file
        
    FROM python:3.9.1

    RUN pip install pandas

    WORKDIR /app
    COPY pipeline.py pipeline.py

    ENTRYPOINT [ "python", "pipeline.py" ]

>"WORKDIR /app" - creating directory in container and setting it as working

>"COPY pipeline.py pipeline.py" copy file from local machine to work directory in container



#### PostgreSQL

Running postgres in container:

	docker run -it \
		-e POSTGRES_USER="root" \
		-e POSTGRES_PASSWORD="root" \
		-e POSTGRES_DB="ny_taxi" \
		-v "/Users/andrey/git/dtc_de_course/week_1_basics_and_setup/1_docker_sql/ny-taxi-volume:/var/lib/postgresql/data:/var/lib/postgresql/data" \
		-p 5431:5432 \
	postgres:13

>"-v" directory, where sotore database out of container

>"-p" port mapping, **I use local port 5431 because I have postgres allready installed localy and port 5432 busy**

To connect to base via pgcli 

`pgcli -h localhost, -p 5431 -u root -d ny_taxi `

#### Jupyter notebook
Using Jupyter notebook to ingest data from csv file and load into the database in container. We need python, pandas and sqlalchemy. 

>upload-data.ipynb


#### PGAdmin
**pgAdmin** is the most popular and feature rich Open Source administration and development platform for PostgreSQL

Runnig PGAdmin container

	docker run -it \
		-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
		-e PGADMIN_DEFAULT_PASSWORD="root" \
		-p 8080:80 \
	dpage/pgadmin4 

Running PGAdmin in local browser: localhost:8080


####Docker network

PGAdmin cannot connect to the base because it is trying to find the base in its container. To fix this we need to put the database container and PGAdmin on the same network

  `docker network create pg-network`

To run Postgres container in network: 
 
	docker run -it 
			-e POSTGRES_USER="root" 
			-e POSTGRES_PASSWORD="root" \
			-e POSTGRES_DB="ny_taxi" \
			-v "/Users/andrey/git/dtc_de_course/week_1_basics_and_setup/1_docker_sql/ny-taxi-volume:/var/lib/postgresql/data:/var/lib/postgresql/data" \
			-p 5431:5432 \
		--network=pg-network \
		--name pg-database \
	postgres:13


To run PGAdmin container in network:

	docker run -it \
			-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
			-e PGADMIN_DEFAULT_PASSWORD="root" \
			-p 8080:80 \
		--network=pg-network \
		--name pgadmin \
	dpage/pgadmin4



#### Preparing the ingest_data script
Converting jupyter notebook to python script

`jupyter nbconvert --to=script upload-data.ipynb`

To pass to the script arguments using argparse 

 - Setting variable with data
`URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"`

 - Runnig script
		python ingest_data.py \
			--user=root \
			--password=root \
			--host=localhost \
			--port=5432
			--dbase=ny_taxi \
			--table_name=yellow_taxi_data \
			--url=${URL}


####Making Docker container with ingest script

Changing Dockerfile 

	FROM python:3.9.1

	RUN apt-get install wget
	RUN pip install pandas sqlalchemy psycopg2

	WORKDIR /app
	COPY ingest_data.py ingest_data.py

	ENTRYPOINT [ "python", "ingest_data.py"]

>"RUN apt-get install wget" - we need installed wget to download data file
>"RUN pip install pandas sqlalchemy psycopg2" - we need psycopg2 to excess postgres through python

Building docker image
`docker build -t taxi_ingest:v001 .`

Running docker container with arguments for ingest script in pg-network

`URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"`
        
	docker run -it \
		--network=pg-network \
		taxi_ingest:v001 \
			--user=root \
			--password=root \
			--host=pg-database \
			--port=5432 \
			--db=ny_taxi \
			--table_name=yellow_taxi_data \
			--url=${URL}

####Docker Compose

**Docker Compose** is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services.

Creating docker-compose.yaml for PostgreSQL and PGAdmin

	services:
    	pgdatabase:
                image: postgres:13
                environment:
                - name=value
                - POSTGRES_USER=root
                - POSTGRES_PASSWORD=root
                - POSTGRES_DB=ny_taxi
                volumes:
                - ./ny-taxi-volume:/var/lib/postgresql/data:rw
                ports:
                - "5432:5432"
            pgadmin:
                image: dpage/pgadmin4
                environment:
                - PGADMIN_DEFAULT_EMAIL=admin@admin.com
                - PGADMIN_DEFAULT_PASSWORD=root
                volumes:
                - ./data_pgadmin:/var/lib/pgadmin:rw
                ports:
                - "8080:80"

Running docker-compose
   `docker-compose up`

   `docker-compose up -d`

>"-d" deattach mode

Stopping docker-compose conteiners
   `docker-compose down`

Removing stoped docker-compose conteiners
`docker-compose rm`
    


##2. SQL
I am familiar with SQL, so I do not need to take notes on how to work with it.


##Homework

For homework I used the green taxi trips from January 2019 and dataset with zones

<https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz>

<https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv>

I used docker container taxi_ingest:v001 to ingest data to database in postgres:13 container

To load zones was created jupyter notebook upload-zones.ipynb and dataset was loaded via this notebook

All queries were made through pgadmin, running in dpage/pgadmin4 container
