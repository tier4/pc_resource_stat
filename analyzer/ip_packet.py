import pandas as pd
import matplotlib.pyplot as plt
import os

num = 30

def find_process_name(pid):
    dirname = "../data"
    for filename in os.listdir(dirname):
        if filename.startswith("ps"):
            with open(os.path.join(dirname, filename), 'r') as f:

                output = ""
                lines = f.readlines()
                for line in lines[1:]:
                    words = line.split()
                    if int(words[2]) == pid:
                        for word in words:
                            if len(word) > 6 and word[0:6] == "__ns:=":
                                output = word[6:] + output

                            if len(word) > 8 and word[0:8] == "__node:=":
                                output = output + word[8:]

            
                        break

    return output


def plot_traffic(logfile):
    df = pd.read_csv(logfile, header=None, names=["timestamp", "pid", "comm", "bytes"])
    df_grouped = df.groupby(["pid"]).sum().nlargest(num, "bytes")
    top_pids = df_grouped.index.get_level_values(0).tolist()

    plt.figure(figsize=(10, 5))

    for pid in df_grouped.index:
        data = df[(df["pid"] == pid)]
        process_name = find_process_name(pid)
        plt.plot(data["timestamp"].values, data["bytes"].values, label="{}".format(process_name))

    plt.legend(loc="upper left")
    plt.xlabel('Time')
    plt.ylabel('Bytes per Second')
    plt.title("Top {} IP Packets {}".format(num, logfile))
    plt.grid(True)
    plt.tight_layout()

plot_traffic("../ip_traffic/send.log")
plot_traffic("../ip_traffic/recv.log")

plt.show()