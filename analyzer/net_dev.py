import os
import matplotlib.pyplot as plt
from datetime import datetime

def parse_network_data(data):
    lines = data.split('\n')
    
    interfaces_data = {}
    
    for line in lines[2:]:
        if not line:
            continue

        values = line.split()
        interface_name = values[0].strip(':')
        
        # Extract Receive and Transmit bytes values
        receive_bytes = int(values[1])
        receive_packets = int(values[2])
        receive_drop = int(values[4])
        transmit_bytes = int(values[9])
        transmit_packets = int(values[10])
        transmit_drop = int(values[12])
        
        interfaces_data[interface_name] = {
            "Receive": receive_bytes,
            "Receive Packets": receive_packets,
            "Receive Drop": receive_drop,
            "Transmit": transmit_bytes,
            "Transmit Packets": transmit_packets,
            "Transmit Drop": transmit_drop,
        }

    return interfaces_data

directory = "../data/net_dev"
all_files_data = {}

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as f:
            data = f.read()
            try:
                parsed_data = parse_network_data(data)
                all_files_data[filename] = parsed_data
            except Exception as e:
                print(f"Error processing {filename}: {e}")

time_stamps = [datetime.strptime(fname.split('.')[0], "%Y-%m-%dT%H:%M:%S%z") for fname in sorted(all_files_data.keys())]

def diff(lst):
    if lst == []:
        return []

    result = []
    prev = lst[0]
    for v in lst:
        result.append(v - prev)
        prev = v

    return result

# Receive Plot
plt.figure(figsize=(10, 5))
for interface_name in all_files_data[list(all_files_data.keys())[0]].keys():
    receive_values = [all_files_data[fname][interface_name]['Receive'] for fname in sorted(all_files_data.keys())]
    diff_values = diff(receive_values)
    plt.plot(time_stamps, diff_values, label=interface_name)
plt.legend(loc='upper left')
plt.xlabel('Time')
plt.ylabel('Bytes Received')
plt.title('Receive Bytes over Time')
plt.grid(True)
plt.tight_layout()

# Receive Packet Plot
plt.figure(figsize=(10, 5))
for interface_name in all_files_data[list(all_files_data.keys())[0]].keys():
    receive_values = [all_files_data[fname][interface_name]['Receive Packets'] for fname in sorted(all_files_data.keys())]
    diff_values = diff(receive_values)
    plt.plot(time_stamps, diff_values, label=interface_name)
plt.legend(loc='upper left')
plt.xlabel('Time')
plt.ylabel('Packets Received')
plt.title('Receive Packets over Time')
plt.grid(True)
plt.tight_layout()

# # Receive Drop Plot
plt.figure(figsize=(10, 5))
for interface_name in all_files_data[list(all_files_data.keys())[0]].keys():
    receive_values = [all_files_data[fname][interface_name]['Receive Drop'] for fname in sorted(all_files_data.keys())]
    plt.plot(time_stamps, diff(receive_values), label=interface_name)
plt.legend(loc='upper left')
plt.xlabel('Time')
plt.ylabel('Packets')
plt.title('Dropped Packets when Receive over Time')
plt.grid(True)
plt.tight_layout()

# Transmit Plot
plt.figure(figsize=(10, 5))
for interface_name in all_files_data[list(all_files_data.keys())[0]].keys():
    transmit_values = [all_files_data[fname][interface_name]['Transmit'] for fname in sorted(all_files_data.keys())]
    diff_values = diff(transmit_values)
    plt.plot(time_stamps, diff_values, label=interface_name)
plt.legend(loc='upper left')
plt.xlabel('Time')
plt.ylabel('Bytes Transmitted')
plt.title('Transmit Bytes over Time')
plt.grid(True)
plt.tight_layout()

# Transmit Packet Plot
plt.figure(figsize=(10, 5))
for interface_name in all_files_data[list(all_files_data.keys())[0]].keys():
    transmit_values = [all_files_data[fname][interface_name]['Transmit Packets'] for fname in sorted(all_files_data.keys())]
    diff_values = diff(transmit_values)
    plt.plot(time_stamps, diff_values, label=interface_name)
plt.legend(loc='upper left')
plt.xlabel('Time')
plt.ylabel('Packets Transmitted')
plt.title('Transmit Packets over Time')
plt.grid(True)
plt.tight_layout()

# Transmit Drop Plot
plt.figure(figsize=(10, 5))
for interface_name in all_files_data[list(all_files_data.keys())[0]].keys():
    receive_values = [all_files_data[fname][interface_name]['Transmit Drop'] for fname in sorted(all_files_data.keys())]
    plt.plot(time_stamps, diff(receive_values), label=interface_name)
plt.legend(loc='upper left')
plt.xlabel('Time')
plt.ylabel('Packets')
plt.title('Dropped Packets when Trasmit over Time')
plt.grid(True)
plt.tight_layout()

plt.show()

