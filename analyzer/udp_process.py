import os
import matplotlib.pyplot as plt
from datetime import datetime

size = 10000000
inode_tx = [0 for x in range(0, size)]
inode_rx = [0 for x in range(0, size)]
inode_pid = [[] for x in range(0, size)]
pid_command = [[] for x in range(0, size)]
tid_command = [[] for x in range(0, size)]

threshold = 10000


def parse_network_data(data):    
    lines = data.split('\n')
    for line in lines[1:]:
        if not line:
            continue

        values = line.split()
        tx = int(values[4].split(':')[0], 16)
        rx = int(values[4].split(':')[1], 16)
        inode = int(values[9])

        inode_tx[inode] += tx
        inode_rx[inode] += rx


def parse_lsof_data(data):
    lines = data.split('\n')

    for line in lines[1:]:
        if not line:
            continue

        values = line.split()
        pid = int(values[1])
        inode = int(values[5])

        inode_pid[inode].append(pid)


def parse_ps_data(data):
    lines = data.split('\n')

    commands = {}

    for line in lines[1:]:
        if not line:
            continue

        values = line.split()
        
        pid = int(values[1])
        tid = int(values[2])
        command = values[11]
        
        pid_command[pid].append(command)
        tid_command[tid].append(line)


dirname = "../data"
for filename in os.listdir(dirname):
    if filename.startswith("lsof"):
        with open(os.path.join(dirname, filename), 'r') as f:
            parse_lsof_data(f.read())

    if filename.startswith("ps"):
        with open(os.path.join(dirname, filename), 'r') as f:
            parse_ps_data(f.read())


directory = dirname + "/net_udp"
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as f:
            data = f.read()
            try:
                parse_network_data(data)
            except Exception as e:
                print(f"Error processing {filename}: {e}")


inodes = []
for inode, tx in enumerate(inode_tx):
    if tx > threshold:
        inodes.append(inode)

def parse_network_data(data, inode):    
    lines = data.split('\n')
    for line in lines[1:]:
        if not line:
            continue

        values = line.split()
        tx = int(values[4].split(':')[0], 16)
        rx = int(values[4].split(':')[1], 16)
        drop = int(values[12])

        if inode == int(values[9]):
            data = {
                "tx": tx,
                "rx": rx,
                "drop": drop
            }

            return data

    data = {
        "tx": tx,
        "rx": rx,
        "drop": drop
    }

    return data


all_files_data = {}

def diff(lst):
    if lst == []:
        return []

    result = []
    prev = lst[0]
    for v in lst:
        result.append(max(0, v - prev))
        prev = v

    return result

for inode in inodes:
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as f:
                data = f.read()
                try:
                    parsed_data = parse_network_data(data, inode)
                    all_files_data[filename] = parsed_data
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    time_stamps = sorted([datetime.strptime(fname.split('.')[0], "%Y-%m-%dT%H:%M:%S%z") for fname in all_files_data.keys()])

    node = ""
    ns = ""
    for tid in inode_pid[inode]:
        for command in tid_command[tid]:
            values = command.split()
            for v in values:
                if v.startswith("__node"):
                    node = v
                if v.startswith("__ns"):
                    ns = v

    if node == "" and ns == "":
        continue

    # tx queue Plot
    plt.figure(figsize=(10, 5))
    tx_values = [all_files_data[fname]['tx'] for fname in sorted(all_files_data.keys())]
    rx_values = [all_files_data[fname]['rx'] for fname in sorted(all_files_data.keys())]
    drop_values = [all_files_data[fname]['drop'] for fname in sorted(all_files_data.keys())]
    plt.plot(time_stamps, tx_values, label='tx')
    # plt.plot(time_stamps, rx_values, label='rx')
    # plt.plot(time_stamps, drop_values, label='drop')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('tx queue')
    plt.title('{},{}'.format(node, ns))
    plt.grid(True)
    plt.tight_layout()

plt.show()