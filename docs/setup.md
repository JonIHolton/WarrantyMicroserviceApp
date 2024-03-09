
Navigate to root directory of microservice

<!-- activate virtual environment -->
$ source venv/bin/activate ;

deactivate virtual environment

$ deactivate


pip install -r requirements.txt

docker run --name claims_MONGO_DB -p 27017:27017 -d mongo

docker run --name claims_RabbitMQ -p 5672:5672 -p 15672:15672 -d rabbitmq:management


<!-- access MongoDB Shell -->
<!-- docker run -it --rm --network="host" mongo:latest mongosh --host localhost:27017 -->
docker exec -it claims_MONGO_DB mongosh

<!-- Docker volume for persistance -->
docker volume create mongo_data
docker run --name claims_MONGO_DB -p 27017:27017 -v mongo_data:/data/db -d mongo



<!-- Master admin -->
db.createUser({
  user: "ESDfullAdmin", 
  pwd: "kuihdadar", 
  roles: ["root"]
})


<!-- ClaimDB admin -->
db.createUser({
  user: "ESDAdmin",
  pwd: "kuihdadar",
  roles: [
    { role: "readWrite", db: "mydatabase" }
  ]
})



