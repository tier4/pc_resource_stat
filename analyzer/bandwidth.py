import os
import numpy as np
import matplotlib.pyplot as plt


def parse_bandwidth(data):
    lines = data.split('\n')
    output = []
    for line in lines:
        line = line.strip().split(' ')
        if len(line) > 1 and line[2] == "from":
            value = float(line[0])
            order = line[1]
            if order == 'GB/s':
                value *= 1000000000
            elif order == 'MB/s':
                value *= 1000000
            elif order == 'KB/s':
                value *= 1000

            output.append(value)

    return output


directory = "../data/bandwidth"
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r') as f:
            data = f.read()
            try:
                parsed_data = parse_bandwidth(data)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

        plt.figure(figsize=(10, 5))
        plt.plot(np.arange(len(parsed_data)), parsed_data)
        plt.xlabel('Time Step')
        plt.ylabel('Bandwidth (B/s)')
        plt.title(filename.strip('.txt'))
        plt.grid(True)
        plt.tight_layout()

plt.show()