import os
import matplotlib.pyplot as plt
from datetime import datetime

inodes = {
    435123,
    435134,
    439280,
    440168,
    440190,
    443004,
    446738,
    447859,
    448867,
    451657,
    452745,
    454737,
}

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


directory = "../data_shiojiri_4/net_udp"
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

    # tx queue Plot
    plt.figure(figsize=(10, 5))
    tx_values = [all_files_data[fname]['tx'] for fname in sorted(all_files_data.keys())]
    rx_values = [all_files_data[fname]['rx'] for fname in sorted(all_files_data.keys())]
    drop_values = [all_files_data[fname]['drop'] for fname in sorted(all_files_data.keys())]
    plt.plot(time_stamps, tx_values, label='tx')
    # plt.plot(time_stamps, rx_values, label='rx')
    # plt.plot(time_stamps, diff(drop_values), label='drop')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('queue')
    plt.title('queue over Time (inode={})'.format(inode))
    plt.grid(True)
    plt.tight_layout()

plt.show()

