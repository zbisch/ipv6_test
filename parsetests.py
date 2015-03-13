import json
import ast
from collections import defaultdict
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


arr = []
client_ids = set()
cdata = defaultdict(lambda:defaultdict(list))

with open('ipv6_test', 'r') as f:
    for line in f:
        [offset, data] = line.split('\t')
        data = data.replace('\"_','"')
        data = data.replace('\"+','"')
        data = json.loads(json.loads(ast.literal_eval(data)))
        cdata[data['client']]['ipv6_test'].append(data)

with open('ipv6_pings', 'r') as f:
    for line in f:
        [offset, data] = line.split('\t')
        data = data.replace('\"_','"')
        data = data.replace('\"+','"')
        data = json.loads(json.loads(ast.literal_eval(data)))
        cdata[data['client']]['ipv6_pings'].append(data)

with open('ipv6_traceroutes', 'r') as f:
    for line in f:
        [offset, data] = line.split('\t')
        data = data.replace('\"_','"')
        data = data.replace('\"+','"')
        data = json.loads(json.loads(ast.literal_eval(data)))
        cdata[data['client']]['ipv6_traceroutes'].append(data)

with open('ipv6_wget', 'r') as f:
    for line in f:
        [offset, data] = line.split('\t')
        data = data.replace('\"_','"')
        data = data.replace('\"+','"')
        data = json.loads(json.loads(ast.literal_eval(data)))
        cdata[data['client']]['ipv6_wget'].append(data)

enabled = set()
success = False
for client in cdata:
    for trial in cdata[client]['ipv6_test']:
        success = trial['ipv6_enabled_test']['ipv6_enabled']
        if success:
            enabled.add(client)

routable = set()
success = False
for client in enabled:
    for trial in cdata[client]['ipv6_test']:
        success = trial['ipv6_routable_test']['ipv6_routable']
        if success:
            routable.add(client)

hasdns = set()
errset = set()
success = False
for client in routable:
    for trial in cdata[client]['ipv6_test']:
        try:
            success = trial['ipv6_dns_test']['ipv6_dns_success']
            if success:
                hasdns.add(client)
        except KeyError:
            errset.add(client)
                
print "routable: ", len(routable)
print "have dns: ", len(hasdns)
print "error set: ", len(errset)
