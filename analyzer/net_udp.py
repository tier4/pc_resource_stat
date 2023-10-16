import os
import matplotlib.pyplot as plt
from datetime import datetime

def parse_network_data(data):
    tx_sum = 0
    rx_sum = 0
    drops_sum = 0
    
    lines = data.split('\n')
    for line in lines[1:]:
        if not line:
            continue

        values = line.split()
        tx_sum += int(values[4].split(':')[0], 16)
        rx_sum += int(values[4].split(':')[1], 16)
        drops_sum += int(values[12])

    data = {
        "tx_sum": tx_sum,
        "rx_sum": rx_sum,
        "drops_sum": drops_sum
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

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as f:
            data = f.read()
            try:
                parsed_data = parse_network_data(data)
                all_files_data[filename] = parsed_data
            except Exception as e:
                print(f"Error processing {filename}: {e}")

time_stamps = sorted([datetime.strptime(fname.split('.')[0], "%Y-%m-%dT%H:%M:%S%z") for fname in all_files_data.keys()])

# tx queue Plot
plt.figure(figsize=(10, 5))
values = [all_files_data[fname]['tx_sum'] for fname in sorted(all_files_data.keys())]
for i in range(len(values)):
    if values[i] > 5e6:
        print(time_stamps[i])
plt.plot(time_stamps, values, label='tx_sum')
plt.legend()
plt.xlabel('Time')
plt.ylabel('tx_queue sum')
plt.title('tx_queue sum over Time')
plt.grid(True)
plt.tight_layout()

# rx queue Plot
plt.figure(figsize=(10, 5))
values = [all_files_data[fname]['rx_sum'] for fname in sorted(all_files_data.keys())]
for i in range(len(values)):
    if values[i] > 5e6:
        print(time_stamps[i])
plt.plot(time_stamps, values, label='rx_sum')
plt.legend()
plt.xlabel('Time')
plt.ylabel('rx_queue sum')
plt.title('rx_queue sum over Time')
plt.grid(True)
plt.tight_layout()

# Drop Plot
plt.figure(figsize=(10, 5))
values = [all_files_data[fname]['drops_sum'] for fname in sorted(all_files_data.keys())]
diff_values = diff(values)
plt.plot(time_stamps, diff_values, label='drops_sum')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Drops')
plt.title('Drops over Time')
plt.grid(True)
plt.tight_layout()

plt.show()

