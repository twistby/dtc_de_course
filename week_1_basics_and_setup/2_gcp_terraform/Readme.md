## Terraform and GCP

**Terraform** is an open-source infrastructure as code software tool that enables you to safely and predictably create, change, and improve infrastructure.

Task:
 - Create with Terraform 
    - Google Cloud Storage (GCS) as a Data Lake
    - BigQuery as a DataWarehause


### GCP 

- Creating GCP project
- In GCP -> IAM and admin -> Service Accounts -> generating KEY

**KEY can be downloaded only once**

Setting up environment valiable

`GOOGLE_APPLICATION_CREDENTIALS="/pass/to/key/key-name.json"`

Checking connection

`gcloud auth application-default login`

Adding Premissions to service-account (IAM):
- Storage Admin
- Storage Objects Admin
- BigQuery admin


### Installing terraform

Setting up **main.tf ** in sections "provider", "resource", ...

> Constants such as project name, region, bucket name and other we can store in file variables.tf
>**Make sure that this file in .gitignore**

Terraform comands:

`terraform init`: initialize and install

`terraform plan`: Match changes against the previus state

`terraform apply`: Apply changes to cloud

`terraform destroy`: Remove stack from cloud


After `terraform apply` GCP resources created.


### Setting up GCP enviroments 

##### SSH
Creating SSH key

`mkdir ~/.ssh if need`

`ssh-keygen -t rsa -f gcp -C andrei -b 2048`

Now we have public and private keys.
Adding public key to GCP -> Compute Engine -> Settings -> Metada -> SSH KEYS

In GCP creating instance Ubuntu 20.04
copy external ip of instance (34.65.104.164)

run

    `ssh -i ~/.ssh/gcp andrei@34.65.104.164`

and we connected to created instance.

Setting up SSH config file on local computer

    `touch config`

and add to file

	Host de-zoomcamp
		HostName 34.65.104.164
		User andrei
		IdentityFile ~/.ssh/gcp

We need to change config file if external ip of instance change.

After that we can connect to instance with

    `ssh de-zoomcamp`


### Setting up GCP VM instance

#### Installing Anaconda

`wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh`

`bash Anaconda3-2022.10-Linux-x86_64.sh`

To apply changes after installation

    `source .bashrc`

or logout and login

#### Insatlling Docker
`sudo apt-get update`

`sudo apt-get install docker.io`

`sudo groupadd docker`

`sudo gpasswd -a $USER docker`

`sudo service docker restart`

and now we need reconnect to instance

#### Installing Docker compose
In ~

`mkdir bin`

`cd bin` 

`wget https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -O docker-compose`

`chmod +x docker-compose`

`nano .bashrc`

at the end of file add 
    "export PATH=${HOME}/bin:${PATH}"

CTRL+O to save
CTRL+X to exit

To apply changes
`source .bashrc`

#### Installing pgcli with pip
`pip install pgcli`

##### Installing pgcli with anaconda 
`conda install -c conda-forge pgcli`

>I was not able to test this method because the conda was hanging on the "Solving enviroment:"
Judging by the information this is a problem with the latest conda release.

#### Installing Terraform
`wget https://releases.hashicorp.com/terraform/1.3.7/terraform_1.3.7_linux_amd64.zip`

Installing unzip

`sudo get install unzip`

`unzip terraform_1.3.7_linux_amd64.zip`


Setting up service account key in instance and authentification

Using SFTP
        
        `sftp de-zoomcamp`

        `put project_key.json`

`export GOOGLE_APPLICATION_CREDENTIALS=~/.gs/lithe-vault-375510-9fb095e6d9fb.json`

`gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS`


Cloning my de-course repo 
`git clone https://github.com/twistby/dtc_de_course.git`

Run terraform
`terrform init`

`terrform plan`

`terrform init`

Resource creation completed!


### Connecting to instance with VSC

Install Remote SSH VSC plugin
Shift+Command+P -> Connect to Host -> de_zoomcamp

#### Forwarding ports to local computer in VSC
Add manualy 8080 for pgadmin and 5432 for postgres
After start Jupyter notebook forwarding of two ports were added automaticaly.


### Documentation
 - https://developer.hashicorp.com/terraform/docs


