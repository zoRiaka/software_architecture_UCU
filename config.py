import consul

c = consul.Consul()
c.kv.put('cluster_name', 'my-cluster')
c.kv.put('queue_name', 'my-queue')
c.kv.put('map_name', 'my-map')
c.kv.put('client1', '172.19.0.2:5701')
c.kv.put('client2', '172.19.0.3:5701')
c.kv.put('client3', '172.19.0.4:5701')