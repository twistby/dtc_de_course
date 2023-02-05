FROM prefecthq/prefect:2.7.11-python3.11

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir
RUN mkdir -p /opt/prefect/data/yellow

COPY 3_deployment /opt/prefect/flows/
