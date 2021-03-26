from basic_sim_model import BasicSimulation
from build_packets import build_packets
from pathlib import Path
import socket
from scapy.supersocket import StreamSocket
from bmp import BMPHeader
import time

import typer


def main(
    scenario_path: Path = typer.Argument(
        ..., exists=True, file_okay=True, readable=True,
    ),
    ip: str = typer.Option("127.0.0.1"),
    port: int = typer.Option(1790),
):
    # build scenario packets
    sim = BasicSimulation.parse_file(scenario_path)
    packets = build_packets(sim)

    # send the packets
    s = socket.socket()
    s.connect((ip, port))
    ss = StreamSocket(s, BMPHeader)

    ss.send(packets.initialization)
    time.sleep(1)
    for p in packets.peers_up:
        ss.send(p)
    time.sleep(1)
    for p in packets.updates:
        ss.send(p)
    while True:
        pass


if __name__ == "__main__":
    typer.run(main)
