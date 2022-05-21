#!flask/bin/python

from flask import Flask, request
from requests import post, get
import uuid
import sys
import random
import socket

logging_list = sys.argv[1:]

# , static_folder='/facade'
app = Flask(__name__)


def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', int(port)))
    sock.close()
    return result == 0


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    logg_random = random.choice(logging_list)
    if not check_port(logg_random):
        while not check_port(logg_random):
            logging_list.remove(logg_random)
            logg_random = random.choice(logging_list)
    logging_url = "http://127.0.0.1:" + logg_random + "/logging"
    if request.method == 'GET':
        messg_url = "http://127.0.0.1:8880/messages"
        r_l = get(logging_url).content.decode("utf-8")
        r_m = get(messg_url).content.decode("utf-8")
        final_string = "Logging-service response: " + '\n' + r_l + "Messages-service response: " + r_m + '\n'
        return final_string

    if request.method == 'POST':
        mssg = request.get_data()

        # generate random UUID
        mssg_uuid = uuid.uuid4().hex  # for a little shorter and more readable version convert uuid to a 32-character
        # hexadecimal string

        r = post(logging_url, data={mssg_uuid: mssg})

        return mssg


if __name__ == '__main__':
    app.run(debug=True, port=8888)
