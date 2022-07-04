## **Machine Learning Operations Introduction**

**What I have done this week?**
- Essential concept of MLOps
- Setup virtual machine EC2 in AWS
- Preparing working environment with anaconda and docker inside the VM (https://github.com/ayoub-berdeddouch/mlops-journey/blob/main/intro-01.md)
- Downloading NY taxi dataset in parquet files
- MLOps maturity model


'Environment Setup'

This section is for outlining steps for configuring development environment with preference to Linux OS. For that matter, we are renting an Ubuntu server on AWS and setting up the environment to suit our need.

Note: I am on Windows Laptop, hence all the configurations done locally are pertaining to Windows OS only.

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
