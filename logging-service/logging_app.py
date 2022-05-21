#!flask/bin/python

from flask import Flask, request
import hazelcast
import sys

clients = hazelcast.HazelcastClient

client = hazelcast.HazelcastClient(
    cluster_name="my-cluster",
    cluster_members=[sys.argv[1]]
)

my_map = client.get_map("my-distributed-map").blocking()
# mssgs_dict = {}  # local dict that contains all the messages

app = Flask(__name__)


@app.route('/logging', methods=['GET', 'POST'])
def logg_requests():
    if request.method == 'GET':
        all_msg = ''
        for i in my_map.values():
            all_msg += i
            all_msg += '\n'
        return all_msg

    if request.method == 'POST':
        mssg_d = request.form.to_dict()  # dict containing POST data
        pair = mssg_d.popitem()
        mssg_uuid = pair[0]
        mssg = pair[1]  # next(iter(mssg_dict.values())) list(mssg_dict.values())[0]
        my_map.put(mssg_uuid, mssg)
        print(mssg)
        return mssg


if __name__ == '__main__':
    app.run(debug=True, port=int(sys.argv[2]))  # 8000
    client.shutdown()
