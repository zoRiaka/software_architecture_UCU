# Lab3: Microservices with Hazelcast

## Requirments:
to install requirements throught requirements.txt run:

```
pip install -r requirements.txt
```
If you want to use curl for testing, make sure you have it installed as well.

## Usage:
In order to create hazelcast cluster with three nodes using docker execute the following commands in separate terminals:
```
docker network create hazelcast-network
docker run     -it     --network hazelcast-network     --rm     -e HZ_CLUSTERNAME=my-cluster     -p 5701:5701 hazelcast/hazelcast:5.0.3

docker run     --name my-second-member --network hazelcast-network     -e HZ_CLUSTERNAME=my-cluster     -p 5702:5701 hazelcast/hazelcast:5.0.3

docker run     --name my-third-member --network hazelcast-network     -e HZ_CLUSTERNAME=my-cluster     -p 5703:5701 hazelcast/hazelcast:5.0.3
```
You can run the services separately by executing:

```
python facade_app.py [all the ports that are being used for logging services]
python logging_app.py [ip address of the cluster member to which you wish to connect] [port to use]
python messages_app.py

# EXAMPLE:
python logging_app.py 172.19.0.2:5701 8000
python logging_app.py 172.19.0.3:5701 8001
python logging_app.py 172.19.0.4:5701 8002  # all three from the seperate terminals

python facade_app.py 8000 8001 8002
```

To send POST/GET requests using curl execute:

```
curl -X POST [url] -d [message body]

# example:
curl -X POST http://127.0.0.1:8888/facade -d "Message N1: This is the first message."
```
```
curl -X GET [url]

# example:
curl -X GET http://127.0.0.1:8888/facade
```
Messages you send will be stored by logging service in HazelCast distributed map.
You can view all of them by sending GET request to the facade service.

## Results:

See results in results.pdf
