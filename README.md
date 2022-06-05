# Lab5: Microservices with Consul

## Requirments:
to install requirements throught requirements.txt run:

```
pip install -r requirements.txt
```
If you want to use curl for testing, make sure you have it installed as well.

## Usage:

Firstly, you need to connect to the Consul agent. One of the way to do it using docker:
```
sudo docker run  -p 8500:8500 -p 8600:8600/udp --name=consul consul:v0.6.4 agent -server -bootstrap -ui -client=0.0.0.0
```
Then, connect to the hazelcast cluster.
In order to create hazelcast cluster with three nodes using docker execute the following commands in separate terminals:
```
docker network create hazelcast-network
docker run     -it     --network hazelcast-network     --rm     -e HZ_CLUSTERNAME=my-cluster     -p 5701:5701 hazelcast/hazelcast:5.0.3

docker run     --name my-second-member --network hazelcast-network     -e HZ_CLUSTERNAME=my-cluster     -p 5702:5701 hazelcast/hazelcast:5.0.3

docker run     --name my-third-member --network hazelcast-network     -e HZ_CLUSTERNAME=my-cluster     -p 5703:5701 hazelcast/hazelcast:5.0.3
```
After that, update to the proper parameters and run config.py:
```
python config.py
```
Then, run multiple instances of the servers.

Please note that in order for the requests to work correctly you would neet to firstly connect to logging and messages services and only after that to the facade service.

You can run the services separately by executing:

```
python facade_app.py [port to use]
python logging_app.py [number from 1-3 that represents the cluster member to which you wish to connect] [port to use]
python messages_app.py [number from 1-3 that represents the cluster member to which you wish to connect] [port to use]

# EXAMPLE:
python logging_app.py 1 8000
python logging_app.py 2 8001
python logging_app.py 3 8002  # all three from the seperate terminals

python messages_app.py 1 8800
python messages_app.py 2 8801

python facade_app.py 8888
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
Messages you send will be stored by logging service in HazelCast distributed map and also in distributed queue by facade service and later in local memory of messages service
You can view all of them by sending GET request to the facade service.

## Results:

See results in results.pdf
