## **Machine Learning Operations Introduction**

**What I have done this week?**
- Essential concept of MLOps
- Setup virtual machine EC2 in AWS
- Preparing working environment with anaconda and docker inside the VM (https://github.com/ayoub-berdeddouch/mlops-journey/blob/main/intro-01.md)
- Downloading NY taxi dataset in parquet files
- MLOps maturity model


## **Environment Setup**

This section covers the initial configuration on working environment required before proceeding to following throughout this course. In this case, the option is to rent an EC2 virtual machine on AWS as to getting all requirements prepared.

On a sidenote, all of these configurations were done on my personal Windows notebook.

**Phase 1: EC2 Instance**

- Go to AWS Console to spin up an EC2 instance of Ubuntu flavour of t2.xlarge size.
- Download the secret access keys (.pem file)
- Take a note of the public IP

**Phase 2: Connect to Ubuntu EC2 server**

- [Optional] Move .pem secret access keys file to .ssh folder in home directory
- Execute the following command from .ssh directory to change the permission of .pem file to protect it

  `chmod 400 downloaded_pem_file`

- Execute the following command to connect to the server

    `ssh -i pem_file ubuntu@public_ip`

- For ease of connecting the server add the connection details in config file in .ssh directory.

    `nano ~/.ssh/config`
