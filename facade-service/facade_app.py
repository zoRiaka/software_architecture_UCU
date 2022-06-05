#!flask/bin/python

from flask import Flask, request
from requests import post, get
import uuid
import sys
import random
import socket
import hazelcast
import consul

c = consul.Consul()
clients = hazelcast.HazelcastClient

client = hazelcast.HazelcastClient(
    cluster_name=c.kv.get('cluster_name')[1]['Value'].decode('utf-8')
)
c.agent.service.register('facade_service', sys.argv[1], sys.argv[1])
my_queue = client.get_queue(c.kv.get('queue_name')[1]['Value'].decode('utf-8')).blocking()
logging_list = [i[0] for i in c.agent.services().items() if i[1]['Service'] == 'logging_service']
messag_list = [i[0] for i in c.agent.services().items() if i[1]['Service'] == 'messages_service']
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

    messag_random = random.choice(messag_list)
    if not check_port(messag_random):
        while not check_port(messag_random):
            messag_list.remove(messag_random)
            messag_random = random.choice(messag_list)
    messg_url = "http://127.0.0.1:" + messag_random + "/messages"

    if request.method == 'GET':
        r_l = get(logging_url).content.decode("utf-8")
        r_m = get(messg_url).content.decode("utf-8")
        final_string = "Logging-service response: " + '\n' + r_l + "Messages-service response: " + r_m + '\n'
        return final_string

    if request.method == 'POST':
        mssg = request.get_data()
        my_queue.put(mssg)

        # generate random UUID
        mssg_uuid = uuid.uuid4().hex  # for a little shorter and more readable version convert uuid to a 32-character
        # hexadecimal string

        r = post(logging_url, data={mssg_uuid: mssg})
        r2 = post(messg_url)

        return mssg


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=int(sys.argv[1]))
