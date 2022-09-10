# **MLOps Final Project: UK House Price**

## **Problem Statement**

The practical implementation of MLOps to real-world case is showcased in this repository. UK house price is chosen as the center of project given the fact that the surge in property price in the UK raises concerns among public.

Link on description about [UK house price](https://www.gov.uk/government/publications/about-the-uk-house-price-index/about-the-uk-house-price-index)
The data source is available in [report and download links](https://www.gov.uk/government/collections/uk-house-price-index-reports-2022)

The aiming from working on this problem is to predict the volatility of surging prices within a period between January 2019 and June 2022. Metric used are:
  - y_hat: forecasting estimation
  - y_hat_lower: lower bound
  - y_hat_upper: upper bound

Prophet is used to meet its forecasting purpose. The information about Prophet is provided [here](https://github.com/facebook/prophet)

## **Project Structure**

This project is developed and tested using cloud service AWS. As such, any configuration made for running programs and services is adjusted to make full use of AWS services, with most of progrmas utilize S3 bucket mainly for storing and reproducing models after completing machine learning experiment.

Structures are constructed as follows:
- [experiment & orchestration](https://github.com/rizdiaprilian/MLOps_Zoomcamp/tree/master/UK_house_price/experiment_orchestration)
- [deployment](https://github.com/rizdiaprilian/MLOps_Zoomcamp/tree/master/UK_house_price/deployment)
- [monitoring](https://github.com/rizdiaprilian/MLOps_Zoomcamp/tree/master/UK_house_price/monitoring_ML)
- [testing](https://github.com/rizdiaprilian/MLOps_Zoomcamp/tree/master/UK_house_price/test_directory)

## **Initialization**

The practice largely follows the same order as what we have been learning throughout the course. Services and Technologies use are:
- MLFlow: Experimentation tracking and reproducibility tool
- Prefect Orion (Prefect 2.0.3 is used here): Orchestration 
- Flask application: Model deployment from AWS S3 and MLFlow  
- Evidently, Grafana, MongoDB: Monitoring data drift

### **Preparing Environment**

Environemt setting used here is `Pipfile` as the purpose is to gain better module utilization specified for this project. To launch the environment in `UK_house_price` directory, steps to be followed through are:
1) Run `pipenv install scikit-learn pandas prophet --version==3.9`. `Pipfile` and `Pipfile.lock` shall appear that collection of modules.
2) Enter the environment with command `pipenv shell`
3) To make it easier for writing command without clutter from relative directory, change with command `PS1="> "`
4) Check whether python VSCode is inside pipenv with command `which python`

It is recommended to see more details of module installation as much of everything covered as demonstrated [here](https://www.youtube.com/watch?v=IXSiYkP23zo&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&index=5)

To start working with this project, always start with directory `UK_house_price` as are all depending modules are located there. However, it is also helpful to replicate Pipfile in sub directories and launch new virtualenv there. 

### **Pre-Commit**

To better identify simple, minor issues and make sure that testing runs well before submission to github, pre-commit hooks is configured for this project.

1) Inside `UK_house_price` initialize empty git with `git init`.
2) Create pre-commit yaml file with command `pre-commit sample-config > .pre-commit-config.yaml` 
3) Install pre-commit after `.git` appears in directory.
![image](https://user-images.githubusercontent.com/42743243/189482497-0402ad99-f447-434a-9851-74188d9b527e.png)
4) Generate `.gitignore` to exclude files/folders from hooks.
5) Add them with `git add <files/folders>`. You can also use `git rm --cached <files/folders>` if you wish to exclude some files and folders from testing hooks.
6) Command `git commit -m "<message>"` will show the process of fixing files (if there are sign of code issues detected)
![image](https://user-images.githubusercontent.com/42743243/189483558-370dc1b4-491f-4460-88d2-2a9a2dc11f7a.png)
![image](https://user-images.githubusercontent.com/42743243/189483596-6862bc98-ef17-4bde-a1be-6b867cc05e0f.png)
7) To see which files that receive fixing, go with command `git diff`. Press `Q` to exit from the command
8) repeat the process 5) and 6) and observe whether changes made on code pass all tests. 
9) View commit (if success) with `git log`
![image](https://user-images.githubusercontent.com/42743243/189483952-dcfd6999-50eb-4533-9664-1c751a4b7698.png)
10) Remove `.git` from directory with `rm -rf .git`.



