# Lab1: Basic architecture of the micro-services

## Requirments:
to install requirements throught requirements.txt run:

```
pip install -r requirements.txt
```
If you want to use curl for testing, make sure you have it installed as well.

## Usage:
You can run the services separately by executing:

```
python facade_app.py
python logging_app.py
python messages_app.py
```

To send POST/GET requests using curl execute:

```
curl -X POST [url] -d [message body]

# example:
curl -X POST http://127.0.0.1:8080/facade -d "Message N1: This is the first message."
```
```
curl -X GET [url]

# example:
curl -X GET http://127.0.0.1:8080/facade
```
Messages you send will be stored by logging service in local dictionary.
You can view all of them by sending GET request to the facade service.

## Results:
