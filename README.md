# ESDKuihDadar

## Notes:
Ensure no port conflicts with docker containers

### How to run?

#### Running Docker Compose
docker-compose up
#### If you want to run the service in the background, you can add the -d flag:
docker-compose up -d
#### Viewing logs: If you are running the service in the background, you can use the following command to view the output logs of the service:
docker-compose logs
#### If you wish to follow the logs of a specific service, you can specify the service name:
docker-compose logs <service_name>
#### Stopping the service: When you are done and want to stop the service, you can run the following command:
docker-compose down
