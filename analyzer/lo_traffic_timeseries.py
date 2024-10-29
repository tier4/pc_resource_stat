import argparse
import os
import re
from collections import defaultdict
from datetime import datetime

from matplotlib import pyplot as plt

DIR: str

NODE_PATTERN = r"__node:=(\S+)"
NS_PATTERN = r"__ns:=(\S+)"


def container_name_to_pid(container_name: str) -> str:
    node_name = container_name.split('/')[-1]
    ns_name = container_name.rstrip(node_name)[:-1]
    pids = set()

    with open(os.path.join(DIR, 'ps.txt'), 'r') as f:
        lines = f.read().split('\n')
        for line in lines[1:]:  # skip header
            splitted = line.split()
            cmd = ' '.join(splitted[11:])
            node_match = re.search(NODE_PATTERN, cmd)
            ns_match = re.search(NS_PATTERN, cmd)
            if node_match and ns_match and node_match.group(1) == node_name and ns_match.group(1) == ns_name:
                pids.add(splitted[1])

    assert len(pids) == 1, f"container_name_to_pid: {container_name} is not unique: {pids}"
    return pids.pop()


def get_all_ports(pid: str) -> list[str]:
    all_ports_set = set()
    with open(os.path.join(DIR, 'lsof.txt'), 'r') as f:
        lines = f.read().split('\n')
        for line in lines[1:]:  # skip header
            splitted = line.split()
            if len(splitted) != 11:
                continue

            if splitted[1] == pid:
                name = splitted[-1].split(':')
                if len(name) == 2:
                    if name[0] in ['localhost', '*', 'autoware']:
                        all_ports_set.add(name[1])

    return list(all_ports_set)


def extract_port(addr: str) -> str:
    # addr looks like "127.0.0.1.57337"
    tmp = addr.split('.')
    if tmp[4][-1] == ':':
        return tmp[4][:-1]
    else:
        return tmp[4]


def get_top_ports(
    all_ports: list[str],
    num: int
) -> tuple[list[str], list[str]]:
    send_sum: dict[str, int] = defaultdict(int)
    recv_sum: dict[str, int] = defaultdict(int)
    with open(os.path.join(DIR, 'tcpdump.txt'), 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            splitted = line.split()
            if len(splitted) != 8:
                continue
            if splitted[-2] != 'length':
                continue

            src = extract_port(splitted[2])
            dst = extract_port(splitted[4])
            length = int(splitted[-1])
            if src in all_ports:
                send_sum[src] += length
            elif dst in all_ports:
                recv_sum[dst] += length

    # sort items by value
    top_send_ports = [
        k for k, _ in sorted(
            send_sum.items(),
            key=lambda item: item[1],
            reverse=True)[: num]]
    top_recv_ports = [
        k for k, _ in sorted(
            recv_sum.items(),
            key=lambda item: item[1],
            reverse=True)[: num]]
    return top_send_ports, top_recv_ports


def plot_timeseries_core(
    container_name: str,
    top_ports: list[str],
    send_or_recv: str
) -> None:
    plt.figure(figsize=(10, 5))
    for port in top_ports:
        byte_per_second: dict[datetime, int] = defaultdict(int)
        with open(os.path.join(DIR, 'tcpdump.txt'), 'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                splitted = line.split()
                if len(splitted) != 8:
                    continue
                if splitted[-2] != 'length':
                    continue

                src = extract_port(splitted[2])
                dst = extract_port(splitted[4])
                if send_or_recv == 'send':
                    if src != port:
                        continue
                else:  # recv
                    if dst != port:
                        continue

                timestamp = datetime.strptime(splitted[0], "%H:%M:%S.%f")
                timestamp = timestamp.replace(microsecond=0)
                length = int(splitted[-1])
                byte_per_second[timestamp] += length

        plt.plot(byte_per_second.keys(), byte_per_second.values(),
                 label=f"{send_or_recv}:{port}")

    plt.legend(loc="upper left")
    plt.xlabel('Time')
    plt.ylabel('packets (Bytes)')
    plt.grid(True)
    plt.tight_layout()
    if send_or_recv == 'send':
        plt.title(f'Packets from {container_name} over time')
        plt.savefig(f"{DIR}/packets_from_{container_name.replace('/', '-')}.png")
    else:  # recv
        plt.title(f'Packets to {container_name} over time')
        plt.savefig(f"{DIR}/packets_to_{container_name.replace('/', '-')}.png")


def plot_timeseries(container_name: str) -> None:
    pid = container_name_to_pid(container_name)
    all_ports = get_all_ports(pid)
    top_send_ports, top_recv_ports = get_top_ports(all_ports, 5)
    plot_timeseries_core(container_name, top_send_ports, 'send')
    plot_timeseries_core(container_name, top_recv_ports, 'recv')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str)
    parser.add_argument('--container_names', nargs='*', type=str)
    args = parser.parse_args()

    DIR = args.dir
    for container_name in args.container_names:
        print(f"=== Analyzing {container_name} ===")
        plot_timeseries(container_name)
