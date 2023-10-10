import os
import matplotlib.pyplot as plt
from datetime import datetime

def parse_data(data):
    lines = data.strip().split('\n')

    mem = lines[1].strip().split()
    swap = lines[2].strip().split()

    output = {
        'mem': {
            'used': int(mem[2]),
            'free': int(mem[3]),
            'shared': int(mem[4]),
            'buff/cache': int(mem[5]),
            'avairable': int(mem[6])
        },
        'swap': {
            'used': int(swap[2]),
            'free': int(swap[3]),
        }
    }

    return output


directory = "../data/free"
all_files_data = {}

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as f:
            data = f.read()
            parsed_data = parse_data(data)
            all_files_data[filename] = parsed_data

time_stamps = sorted([datetime.strptime(fname.split('.')[0], "%Y-%m-%dT%H:%M:%S%z") for fname in all_files_data.keys()])

# Mem Plot
plt.figure(figsize=(10, 5))
for title in all_files_data[list(all_files_data.keys())[0]]['mem'].keys():
    value = [all_files_data[fname]['mem'][title] for fname in sorted(all_files_data.keys())]
    plt.plot(time_stamps, value, label=title)
plt.legend(loc='upper left')
plt.xlabel('Time')
plt.ylabel('Mem')
plt.title('Mem over Time')
plt.grid(True)
plt.tight_layout()

# Swap Plot
plt.figure(figsize=(10, 5))
for title in all_files_data[list(all_files_data.keys())[0]]['swap'].keys():
    value = [all_files_data[fname]['swap'][title] for fname in sorted(all_files_data.keys())]
    plt.plot(time_stamps, value, label=title)
plt.legend(loc='upper left')
plt.xlabel('Time')
plt.ylabel('Swap')
plt.title('Swap over Time')
plt.grid(True)
plt.tight_layout()


plt.show()  # Show both plots
