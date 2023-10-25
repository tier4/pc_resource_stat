import os
import matplotlib.pyplot as plt
from datetime import datetime

directory = "../data2/"

# addr looks like "127.0.0.1.57337"
def extract_port(addr):
    tmp = addr.split('.')
    return tmp[4]


port_to_cmd = {}
port_to_pid = {}
port_to_tid = {}
with open(os.path.join(directory, 'lsof.txt'), 'r') as f:
    lines = f.read().split('\n')
    for line in lines[1:]:
        if not line:
            continue

        values = line.split()
        if len(values) != 11:
            continue

        cmd = values[0]
        pid = int(values[1])

        name = values[-1].split(':')

        if len(name) == 2:
            if name[0] in ('localhost', '*', 'autoware'):
                port = int(name[1])
            
                port_to_cmd[port] = cmd
                port_to_pid[port] = pid
        

pid_to_cmd = {}
with open(os.path.join(directory, 'ps.txt'), 'r') as f:
    lines = f.read().split('\n')
    for line in lines[1:]:
        if not line:
            continue

        values = line.split()
        pid = int(values[1])
        cmd = values[11:]

        pid_to_cmd[pid] = cmd


len_sum_per_port = {}
with open(os.path.join(directory, 'tcpdump.txt'), 'r') as f:
    lines = f.read().split('\n')
    for line in lines:
        if not line:
            continue

        values = line.split()
        if len(values) != 8:
            continue

        time = values[0]
        src = int(extract_port(values[2]))
        dst = int(extract_port(values[4])[:-1])

        if values[-2] != 'length':
            continue
            
        length = int(values[-1])

        if src in len_sum_per_port:
            len_sum_per_port[src] += length
        else:
            len_sum_per_port[src] = length

        if dst in len_sum_per_port:
            len_sum_per_port[dst] += length
        else:
            len_sum_per_port[dst] = length


len_sum_per_port = dict(sorted(len_sum_per_port.items(), key=lambda item: item[1], reverse=True))


plt.figure(figsize=(15, 10))

index = 0
for port, packet_sum in len_sum_per_port.items():

    logs_per_second = {}
    with open(os.path.join(directory, 'tcpdump.txt'), 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            if not line:
                continue

            values = line.split()
            if len(values) != 8:
                continue

            timestamp_str = values[0]
            timestamp = datetime.strptime(timestamp_str, "%H:%M:%S.%f")
            timestamp = timestamp.replace(microsecond=0)
            
            src = int(extract_port(values[2]))
            dst = int(extract_port(values[4])[:-1])

            if src != port and dst != port:
                continue

            if values[-2] != 'length':
                continue
            
            length = int(values[-1])
            if timestamp in logs_per_second:
                logs_per_second[timestamp] += length
            else:
                logs_per_second[timestamp] = length

    plt.plot(logs_per_second.keys(), logs_per_second.values(), label=f"port={port}")
    
    index += 1
    if index == 10:
        break

plt.legend(loc="upper left")
plt.xlabel('Time')
plt.ylabel('packets (Bytes)')
plt.title('Tx & Rx Packets over time')
plt.grid(True)
plt.tight_layout()

plt.show()