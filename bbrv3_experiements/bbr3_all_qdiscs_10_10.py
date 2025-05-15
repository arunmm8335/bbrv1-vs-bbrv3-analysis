# SPDX-License-Identifier: GPL-2.0-only

from nest.topology import *
from nest.experiment import *
from nest.topology.network import Network
from nest.topology.address_helper import AddressHelper

# === Fixed Parameters ===
bw = "10mbit"
delay = "10ms"
duration = 120
qdiscs = ["pfifo", "codel", "fq_codel", "red", "pie" , "fq_pie"]  # Use only what your NEST setup supports

for qdisc in qdiscs:
    name = f"bbrv3-qdisc-{qdisc}-bw{bw}-delay{delay}-dur{duration}"
    print(f"\n[INFO] Running Experiment: {name}")

    # Nodes
    h1 = Node("h1")
    h2 = Node("h2")
    r1 = Router("r1")
    r2 = Router("r2")

    # Networks
    n1 = Network("192.168.1.0/24")
    n2 = Network("192.168.2.0/24")
    n3 = Network("192.168.3.0/24")

    # Connections
    (eth1, etr1a) = connect(h1, r1, network=n1)
    (etr1b, etr2a) = connect(r1, r2, network=n2)
    (etr2b, eth2) = connect(r2, h2, network=n3)

    AddressHelper.assign_addresses()

    # Link setup
    eth1.set_attributes("1000mbit", "1ms")
    etr1b.set_attributes(bw, delay, qdisc)
    etr2b.set_attributes("1000mbit", "1ms")
    eth2.set_attributes("1000mbit", "1ms")
    etr2a.set_attributes(bw, delay)
    etr1a.set_attributes("1000mbit", "1ms")

    # Routes
    h1.add_route("DEFAULT", eth1)
    h2.add_route("DEFAULT", eth2)
    r1.add_route("DEFAULT", etr1b)
    r2.add_route("DEFAULT", etr2a)

    # Experiment setup
    exp = Experiment(name)
    flow = Flow(h1, h2, eth2.get_address(), 0, duration, 1)
    exp.add_tcp_flow(flow, "bbr")

    # Run it
    exp.run()
