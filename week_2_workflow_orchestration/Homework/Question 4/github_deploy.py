
from etl_web_to_gcp import etl_web_to_gcs
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

github_block = GitHub.load("question4")

docker_dep = Deployment.build_from_flow(
    flow=etl_web_to_gcs, # flow name in parameterized_flow.py
    name='q-4', # name of deployment
    storage=github_block, # docker block
    entrypoint="./etl_web_to_gcp.py:etl_web_to_gcs",
    parameters={'color': 'green', 'year':'2020', 'months':[1,2]}
)


if __name__ == '__main__':
    docker_dep.apply()  # aplying parameters and creating deployment