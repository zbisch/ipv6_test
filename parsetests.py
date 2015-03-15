import numpy
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
        test.add(data['client'])

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
# set of clients who passed ipv4 ping tests
ping4 = set()
for client in pings:
    for trial in cdata[client]['ipv6_pings']:
        if trial['ipv4_ping']['failed'] == False:
            ping4.add(client)

# ipv4 ping test speed results
speed4 = defaultdict(list)
avg4 = dict()
avg4list = []
avg4total = 0
line = ""
ind = 0
for client in ping4:
    for trial in cdata[client]['ipv6_pings']:
        try:
            line = trial['ipv4_ping']['out']
            while 1:
                start = line.index('time')+5
                end = line[start:].index(' ') + start
                speed4[client].append(float(line[start:end]))
                line = line[end:]

        except ValueError:
            pass
    avg4[client] = numpy.mean(speed4[client])
    avg4list.append(avg4[client])
avg4total = numpy.mean(avg4list)
        
        
# set of clients who passed ipv6 ping tests
ping6 = set()
for client in pings:
    for trial in cdata[client]['ipv6_pings']:
        if trial['ipv6_ping']['failed'] == False:
            ping6.add(client)

print len(ping6)
# ipv4 ping test speed results
speed6 = defaultdict(list)
avg6 = dict()
avg6list = []
avg6total = 0
line = ""
ind = 0
for client in ping6:
    for trial in cdata[client]['ipv6_pings']:
        try:
            line = trial['ipv6_ping']['out']
            while 1:
                start = line.index('time')+5
                end = line[start:].index(' ') + start
                speed6[client].append(float(line[start:end]))
                line = line[end:]

        except ValueError:
            pass
    avg6[client] = numpy.mean(speed6[client])
    avg6list.append(avg6[client])
avg6total = numpy.mean(avg6list)

print "routable: ", len(routable)
print "have dns: ", len(hasdns)
print "error set: ", len(errset)
print "mixed set: ", len(mixed)
print "test set: ", len(test)
print "pings set: ", len(pings)
print "troutes set: ", len(troutes)
print "wget set: ", len(wget)
print "ping4: ", len(ping4), ", avg: ", avg4total
print "ping6: ", len(ping6), ", avg: ", avg6total
