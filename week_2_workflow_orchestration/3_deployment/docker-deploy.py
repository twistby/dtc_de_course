
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
    docker_dep.apply()  # aplying parameters and creating deployment