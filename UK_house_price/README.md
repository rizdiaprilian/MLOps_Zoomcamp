### Project: UK House Price ###

# **UK House Price**

The practical implementation of MLOps on real-world case is showcased in this repository. UK house price is chosen as the center of project on the grounds many concerns of surge in property.


So far, we have managed to register machine learning in MLFlow as well as writing script to be orchestrated and ready for production. This step will bring further the model to be able to respond from given request in environment: deployment.

Setup preparation for model deployment can be done either in batch (offline) that allow prediction on newly unseen data arrives in periodic schedule or in real-time streaming (online) that the model always runs to serve anytime. 

## **Initialization**

The practice follows the same order as what we have been learning in week term. The structures is as follow:
- Experimentation tracking with MLFlow
- Orchestration with Prefect Orion (Prefect 2.0.3 is used here)
- Deployment from AWS S3 and MLFlow with Flask application
- Monitoring with MongoDB, Evidently
