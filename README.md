# Swaddle
 An application that allows to deploy applications in docker
 
## Tech stack
- Docker swarm
- Redis
- Poetry
- FastAPI

## Vision
The app is envisioned as a simple prejudiced deployment solution on top of docker swarm with complete post-deployment monitoring and maintenance. Little to no information regarding technical features are recorded except for the primitive performance attributes - cpu,network,io & availability.

## Main APIs
 - App
    - Endpoint to define apps including its git repo or docker-compose file directly as json
- Cluster
    - Endpoint to define a prospective group of servers which can work together to deploy the app
    - The cluster can have multiple servers. Each server credentials including ssh details has to be given
    - A set of commands can be configured to prepare the server environment
- Deploy
    - Endpoint to deploy or stop a list of apps in a server
    - Intelligently allocate cluster groups for the use of app
    - There is no need to mention the clusters to be deployed in.
- Scale
    - Used to manually scale the application as per the needs of user.
- Commands
    - Endpoint to add custom executable commands in server for usage in cluster preparation.


## Build
- Clone repo
- poetry install
- Start redis
    - Provide redis configuration in swaddle.env
 - Run `run.py` file to run the code

## TO DO
- [x] Auto cluster choosing for apps
- [x] Cluster preparation via ssh  
- [ ] Deploy testing in AWS
- [ ] Availability management
- [ ] Authentication and role specific activities like Command addition and Cluster addition