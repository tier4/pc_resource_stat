import os
import matplotlib.pyplot as plt
from datetime import datetime

directory = "../data2/"

target_pid = 106542

# addr looks like "127.0.0.1.57337"
def extract_port(addr):
    tmp = addr.split('.')
    return tmp[4]


ports = []
with open(os.path.join(directory, 'lsof.txt'), 'r') as f:
    lines = f.read().split('\n')
    for line in lines[1:]:
        if not line:
            continue

        values = line.split()
        if len(values) != 11:
            continue

        pid = int(values[1])
        if pid != target_pid:
            continue

        name = values[-1].split(':')

        if len(name) == 2:
            if name[0] in ('localhost', '*', 'autoware'):
                ports.append(int(name[1]))


dst_sum = {}
src_sum = {}
with open(os.path.join(directory, 'tcpdump.txt'), 'r') as f:
    lines = f.read().split('\n')
    for line in lines:
        if not line:
            continue

        values = line.split()
        if len(values) != 8:
            continue

        src = int(extract_port(values[2]))
        dst = int(extract_port(values[4])[:-1])

        if values[-2] != 'length':
            continue
            
        length = int(values[-1])

        if src in ports:
            if dst in src_sum:
                dst_sum[dst] += length
            else:
                dst_sum[dst] = length
        elif dst in ports:
            if src in src_sum:
                src_sum[src] += length
            else:
                src_sum[src] = length

src_sum = dict(sorted(src_sum.items(), key=lambda item: item[1], reverse=True))
dst_sum = dict(sorted(dst_sum.items(), key=lambda item: item[1], reverse=True))

plt.figure(figsize=(10, 5))
index = 0
for port, packet_sum in src_sum.items():
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
            if src != port:
                continue

            if values[-2] != 'length':
                continue
            
            length = int(values[-1])
            if timestamp in logs_per_second:
                logs_per_second[timestamp] += length
            else:
                logs_per_second[timestamp] = length

    plt.plot(logs_per_second.keys(), logs_per_second.values(), label=f"src:{port}")

    index += 1
    if index == 5:
        break

plt.legend(loc="upper left")
plt.xlabel('Time')
plt.ylabel('packets (Bytes)')
plt.title('Packets to pointcloud over time')
plt.grid(True)
plt.tight_layout()


plt.figure(figsize=(10, 5))
index = 0
for port, packet_sum in dst_sum.items():
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
            if dst != port:
                continue

            if values[-2] != 'length':
                continue
            
            length = int(values[-1])
            if timestamp in logs_per_second:
                logs_per_second[timestamp] += length
            else:
                logs_per_second[timestamp] = length

    plt.plot(logs_per_second.keys(), logs_per_second.values(), label=f"dst:{port}")

    index += 1
    if index == 5:
        break

plt.legend(loc="upper left")
plt.xlabel('Time')
plt.ylabel('packets (Bytes)')
plt.title("Packets from pointcloud over time")
plt.grid(True)
plt.tight_layout()
plt.show()