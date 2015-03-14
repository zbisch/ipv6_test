import json
import ast
from collections import defaultdict

arr = []
test = set()
cdata = defaultdict(lambda:defaultdict(list))

with open('ipv6_test', 'r') as f:
    for line in f:
        [offset, data] = line.split('\t')
        data = data.replace('\"_','"')
        data = data.replace('\"+','"')
        data = json.loads(json.loads(ast.literal_eval(data)))
        cdata[data['client']]['ipv6_test'].append(data)

pings = set()
with open('ipv6_pings', 'r') as f:
    for line in f:
        [offset, data] = line.split('\t')
        data = data.replace('\"_','"')
        data = data.replace('\"+','"')
        data = json.loads(json.loads(ast.literal_eval(data)))
        cdata[data['client']]['ipv6_pings'].append(data)
        pings.add(data['client'])

troutes = set()
with open('ipv6_traceroutes', 'r') as f:
    for line in f:
        [offset, data] = line.split('\t')
        data = data.replace('\"_','"')
        data = data.replace('\"+','"')
        data = json.loads(json.loads(ast.literal_eval(data)))
        cdata[data['client']]['ipv6_traceroutes'].append(data)
        troutes.add(data['client'])

wget = set()
with open('ipv6_wget', 'r') as f:
    for line in f:
        [offset, data] = line.split('\t')
        data = data.replace('\"_','"')
        data = data.replace('\"+','"')
        data = json.loads(json.loads(ast.literal_eval(data)))
        cdata[data['client']]['ipv6_wget'].append(data)
        wget.add(data['client'])

enabled = set()
success = False
for client in cdata:
    for trial in cdata[client]['ipv6_test']:
        success = trial['ipv6_enabled_test']['ipv6_enabled']
        if success:
            enabled.add(client)

olap1 = set()
for client in test:
    if client in pings:
        olap1.add(client)

olap2 = set()
for client in test:
    if client in troutes:
        olap2.add(client)

olap3 = set()
for client in test:
    if client in wget:
        olap3.add(client)

routable = set()
success = False
for client in enabled:
    for trial in cdata[client]['ipv6_test']:
        success = trial['ipv6_routable_test']['ipv6_routable']
        if success:
            routable.add(client)

hasdns = set()
errset = set()
mixed = set()
success = False
for client in routable:
    for trial in cdata[client]['ipv6_test']:
        try:
            success = trial['ipv6_dns_test']['ipv6_dns_success']
            if success:
                hasdns.add(client)
        except KeyError:
            if trial['ipv6_routable_test']['ipv6_routable']:
                errset.add(client)
            else:
                mixed.add(client)

success = False
for client in hasdns:
    for trial in cdata[client]['ipv6_pings']:
        print trial['client']
        print "hello"
        break
    break

print "routable: ", len(routable)
print "have dns: ", len(hasdns)
print "error set: ", len(errset)
print "mixed set: ", len(mixed)
print "test set: ", len(test)
print "pings set: ", len(pings)
print "overlap: ",  len(olap1)
print "troutes set: ", len(troutes)
print "overlap: ",  len(olap2)
print "wget set: ", len(wget)
print "overlap: ",  len(olap3)
