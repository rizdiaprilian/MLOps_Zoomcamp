## **Machine Learning Operations Introduction**

**What I have done this week?**
- Essential concept of MLOps
- Setup virtual machine EC2 in AWS
- Preparing working environment with anaconda and docker inside the VM (https://github.com/ayoub-berdeddouch/mlops-journey/blob/main/intro-01.md)
- Downloading NY taxi dataset in parquet files
- MLOps maturity model


## **Cloud Environment Setup**

This section covers the initial configuration on working environment required before proceeding to following throughout this course. In this case, the option is to rent an EC2 virtual machine on AWS as to getting all requirements prepared. 

Remainder: running this instance may cost a few dollars to spend up with. It is better to stop (or delete) the instance before leaving.

On a sidenote, all of these configurations were done on my personal Windows notebook. Bash terminals used are Git Bash and VSCode.

**Phase 1: Launch an EC2 Instance**

- Go to AWS Console and select `Launch Instance` to begin. 
- Configuration:
  - Application and OS Images: `Ubuntu Server 22.04`, `64-bit (x86)`
  - Instance type: `t2.xlarge`
  - Key pair: Input the name of your choice. 
  ![image](https://user-images.githubusercontent.com/42743243/177284775-471be899-e768-4c3f-bc3b-cca3072353ce.png)
  - Configure storage: 30 GiB (as you will work with Docker images)

- When the EC2 instance has run successfully, write down the public IP. 

**Phase 2: Connect to Ubuntu EC2 server**

- The key is downloaded in `.pem` format and it is required to move this key, pem_file, to directory `\.ssh` within home directory.
- Execute the following command from .ssh directory to change the permission of .pem file to protect it
- Protect the key in the .ssh directory with this command: `chmod 400 pem_file`
- Execute the following command to connect to the server: `ssh -i pem_file ubuntu@public_ip`

- For ease of connecting the server add the connection details in config file in .ssh directory.

    `nano ~/.ssh/config`
