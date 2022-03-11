#!flask/bin/python

from flask import Flask, request
from requests import post, get
import uuid

# , static_folder='/facade'
app = Flask(__name__)


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    if request.method == 'GET':
        messg_url = "http://127.0.0.1:8880/messages"
        logging_url = "http://127.0.0.1:8000/logging"
        r_l = get(logging_url).content.decode("utf-8")
        r_m = get(messg_url).content.decode("utf-8")
        final_string = "Logging-service response: " + '\n' + r_l + "Messages-service response: " + r_m
        return final_string

    if request.method == 'POST':
        mssg = request.get_data()

        # generate random UUID
        mssg_uuid = uuid.uuid4().hex  # for a little shorter and more readable version convert uuid to a 32-character
        # hexadecimal string

        logging_url = "http://127.0.0.1:8000/logging"
        r = post(logging_url, data={mssg_uuid: mssg})

        return mssg


if __name__ == '__main__':
    app.run(debug=True, port=8080)
