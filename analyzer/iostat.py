import os
import matplotlib.pyplot as plt
from datetime import datetime

def parse_data(data):
    # データを行ごとに分割
    lines = data.strip().split('\n')

    # ヘッダー情報の取得
    header = lines[0].split()
    date = header[3]
    architecture = header[5].strip('()')
    cpu_count = header[6].strip('()').split()[0]

    # avg-cpu情報の取得
    avg_cpu_keys = lines[1].split()
    avg_cpu_values = list(map(float, lines[3].split()))
    avg_cpu_data = dict(zip(avg_cpu_keys, avg_cpu_values))

    # Device情報の取得
    device_keys = lines[5].split()
    devices = {}
    for line in lines[6:]:
        values = line.split()
        if len(values) == 0:
            break
        device_name = values[0]
        device_data = dict(zip(device_keys[1:], list(map(float, values[1:]))))
        devices[device_name] = device_data

    # Pythonのデータ型にまとめる
    output = {
        'header': {
            'version': header[0],
            'name': header[1].strip('()'),
            'date': date,
            'architecture': architecture,
            'cpu_count': cpu_count
        },
        'avg_cpu': avg_cpu_data,
        'devices': devices
    }

    return output


directory = "../data_shiojiri_4/iostat"
all_files_data = {}

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as f:
            data = f.read()
            parsed_data = parse_data(data)
            all_files_data[filename] = parsed_data

time_stamps = sorted([datetime.strptime(fname.split('.')[0], "%Y-%m-%dT%H:%M:%S%z") for fname in all_files_data.keys()])

# Read Plot
plt.figure(figsize=(10, 5))  # Create a new figure for reads
for device_name in all_files_data[list(all_files_data.keys())[0]]['devices'].keys():
    if not device_name.startswith('loop'):
        reads_per_second = [all_files_data[fname]['devices'][device_name]['kB_read/s'] for fname in sorted(all_files_data.keys())]
        plt.plot(time_stamps, reads_per_second, label=device_name)
plt.legend()
plt.xlabel('Time')
plt.ylabel('kB_read/s')
plt.title('Read Speed over Time')
plt.grid(True)
plt.tight_layout()

# Write Plot
plt.figure(figsize=(10, 5))  # Create a new figure for writes
for device_name in all_files_data[list(all_files_data.keys())[0]]['devices'].keys():
    if not device_name.startswith('loop'):
        writes_per_second = [all_files_data[fname]['devices'][device_name]['kB_wrtn/s'] for fname in sorted(all_files_data.keys())]
        plt.plot(time_stamps, writes_per_second, label=device_name)
plt.legend()
plt.xlabel('Time')
plt.ylabel('kB_wrtn/s')
plt.title('Write Speed over Time')
plt.grid(True)
plt.tight_layout()

plt.show()  # Show both plots
