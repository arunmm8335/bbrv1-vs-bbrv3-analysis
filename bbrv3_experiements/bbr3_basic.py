# SPDX-License-Identifier: GPL-2.0-only

from nest.topology import *
from nest.experiment import *
from nest.topology.network import Network
from nest.topology.address_helper import AddressHelper

# === Test Scenarios ===
scenarios = [
    {"name": "low_buffer",       "bw": "10mbit", "delay": "10ms", "qdisc": "pfifo",     "limit": "20"},
    {"name": "bufferbloat",      "bw": "10mbit", "delay": "10ms", "qdisc": "pfifo",     "limit": "1000"},
    {"name": "low_latency",      "bw": "10mbit", "delay": "1ms",  "qdisc": "fq_codel"},
    {"name": "high_latency",     "bw": "10mbit", "delay": "100ms", "qdisc": "fq_codel"},
    {"name": "ecn_red",          "bw": "10mbit", "delay": "10ms", "qdisc": "red",       "limit": "100", "ecn": "1"},
    {"name": "fq_pie_combo",     "bw": "10mbit", "delay": "10ms", "qdisc": "fq_pie"},
]

duration = 120  # seconds

for s in scenarios:
    exp_name = f"bbrv3-{s['name']}-bw{s['bw']}-delay{s['delay']}-q{s['qdisc']}"
    print(f"\n[INFO] Running Experiment: {exp_name}")

    # Nodes
    h1 = Node("h1")
    h2 = Node("h2")
    r1 = Router("r1")
    r2 = Router("r2")

    # Networks
    n1 = Network("192.168.1.0/24")
    n2 = Network("192.168.2.0/24")
    n3 = Network("192.168.3.0/24")

    (eth1, etr1a) = connect(h1, r1, network=n1)
    (etr1b, etr2a) = connect(r1, r2, network=n2)
    (etr2b, eth2) = connect(r2, h2, network=n3)

    AddressHelper.assign_addresses()

    # Basic edge links
    eth1.set_attributes("1000mbit", "1ms")
    etr2b.set_attributes("1000mbit", "1ms")
    eth2.set_attributes("1000mbit", "1ms")
    etr2a.set_attributes(s["bw"], s["delay"])
    etr1a.set_attributes("1000mbit", "1ms")

    # 🔥 Bottleneck link setup
    qdisc_args = {}
    if "limit" in s:
        qdisc_args["limit"] = s["limit"]
    if "ecn" in s:
        qdisc_args["ecn"] = s["ecn"]

    etr1b.set_attributes(s["bw"], s["delay"], s["qdisc"], **qdisc_args)

    # Routes
    h1.add_route("DEFAULT", eth1)
    h2.add_route("DEFAULT", eth2)
    r1.add_route("DEFAULT", etr1b)
    r2.add_route("DEFAULT", etr2a)

    # Experiment
    exp = Experiment(exp_name)
    flow = Flow(h1, h2, eth2.get_address(), 0, duration, 1)
    exp.add_tcp_flow(flow, "bbr")

    # Run it
    exp.run()
