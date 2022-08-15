# **Orchestration and ML Pipelines**

This week we take practices of orchestration and ML pipeline. 

We use API services from Prefect Orion to help us getting better productivity in managing ML pipelines in forms of flow and task.

![Image](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/Week3_Orchestration/Prefect_Orion_screenshot.png)

## **Negative Engineering**

A experimentation code in jupyter notebook needs to be converted to python script to better accomodate tasks in parallel/sequence such as scheduling, retrying failed process, preprocessing, retraining in pipeline, in particular when the code is placed inside production repository. 

In building data applications, writing code that actually works does not always lead to the computer being successful in bringing pieces of software working together as supposed to be. The term known as **Negative engineering** is introduced that reflects the situation when engineers must deal with various causes of failures that take around 90% of their time (and effort). Point of fails may come from:

- Retries when APIs fail
- Malformed data
- Notifications
- Observability into failures
- Conditional failure logic
- Timeouts

Engineers can expect a great deal of productivity boost to be doubled when the reduction on negative share to 80% is achieved. And a service such as **Prefect** offers right sets of functionalities to fulfill objectives of gathering relevant fail sources to be resolved as fast as possible.

## **Prefect**

An open-source tool for building **data workflows** that cover a series of steps to be performed in a certain order. Additional ability of Prefect allows for specifying more complex behaviours, i.e. passing resulting function or data to other steps, automatical retry when a task encounters a problem, or steps that only run when previous steps fail.

Core concepts include:
- **Task**: a python-type decorator to define a new task and it optionally receives input and returns output. There is no restriction on how much or how little a task can perform. However, it is encouraging to do a trade-off between task size and usability.
- **Flow**: a dependency that combines various tasks such as task orders and information transfer from one's task output to another task. Flow definition can be built by either Functional or Imperative API.
- **Flow Orchestration**: Prefect Core API provides powerful tool to describe task and flows to be run from notebook, python shell, or python script. Even more, UI and database backend can be fully utilized to help monitoring and orchestration on flow and tasks become easier. 

Prefect Orion (Prefect 2.0) is a step-up from Prefect 1.0 with new functionality. Currently, the latest version available is 2.0.4.

More information about Prefect Orion: 
- https://github.com/PrefectHQ/prefect
- https://docs.prefect.io/

### **Prefect Orion in Action**

The demonstration of prefect orion on NY Taxi homework is provided here: 
- [*Homework with Orion*](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/Week3_Orchestration/Prefect/homework_with_prefect_rev1.py)
- [*Homework with Cloud*](https://github.com/rizdiaprilian/MLOps_Zoomcamp/blob/master/Week3_Orchestration/Prefect/homework_with_prefect_cloud_rev1.py)


## **Prefect Cloud**

![image](https://user-images.githubusercontent.com/42743243/184643027-489617cd-7ebc-4bf3-808b-cf0f90cc250b.png)

Alternatively, you can also perform orchestration in Prefect Cloud. The steps taken to run the task in the cloud service is more or less the same as when you do in Orion.

A personal account is required to use this service. You can choose GitHub account to start the registration.

Generate API key with these steps:
- Hover to settings on the left bottom window and choose `account settings`
- Select `Generate API Key` and Cloud automatically generate random key.
- Take the screenshot on API key and store it to the place.
- Run the command on bash script: `prefect cloud login -k <API key>` and see if the response is such that Cloud is ready to serve.
- Run file 'prefect_with_cloud.py' and see how it goes through.

![image](https://user-images.githubusercontent.com/42743243/184643424-a9536293-4bbe-432d-b5e0-842e8d1122db.png)

