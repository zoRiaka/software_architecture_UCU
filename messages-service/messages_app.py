#!flask/bin/python

from flask import Flask, request
import hazelcast
import sys
import consul

clients = hazelcast.HazelcastClient
c = consul.Consul()

member_name = c.kv.get('client' + sys.argv[1])[1]['Value'].decode('utf-8')
client = hazelcast.HazelcastClient(
    cluster_name="my-cluster",
    cluster_members=[member_name]
)


my_queue = client.get_queue(c.kv.get('queue_name')[1]['Value'].decode('utf-8')).blocking()
c.agent.service.register('messages_service', sys.argv[2], sys.argv[2])

messages = []

# , static_folder='/messages'
app = Flask(__name__)


@app.route('/messages', methods=['GET', 'POST'])
def messg_requests():
    if request.method == 'GET':
        return '\n'.join(messages)
    if request.method == 'POST':
        while not my_queue.is_empty():
            mess = my_queue.take()
            messages.append(mess.decode("utf-8"))
            print(mess.decode("utf-8"))
        return '\n'.join(messages)


if __name__ == '__main__':
    app.run(debug=True, port=int(sys.argv[2]))  # 8881?
    client.shutdown()
