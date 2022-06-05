#!flask/bin/python

from flask import Flask, request
import hazelcast
import sys
import consul

c = consul.Consul()
clients = hazelcast.HazelcastClient

member_name = c.kv.get('client' + sys.argv[1])[1]['Value'].decode('utf-8')
client = hazelcast.HazelcastClient(
    cluster_name="my-cluster",
    cluster_members=[member_name]
)

my_map = client.get_map(c.kv.get('map_name')[1]['Value'].decode('utf-8')).blocking()

c.agent.service.register('logging_service', sys.argv[2], sys.argv[2])

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
