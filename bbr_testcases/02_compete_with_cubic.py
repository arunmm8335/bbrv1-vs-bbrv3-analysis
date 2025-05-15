# SPDX-License-Identifier: GPL-2.0-only
from nest.topology import *
from nest.experiment import *
from nest.topology.network import Network
from nest.topology.address_helper import AddressHelper

h1 = Node("h1")
h2 = Node("h2")
r1 = Router("r1")
r2 = Router("r2")

n1 = Network("192.168.1.0/24")
n2 = Network("192.168.2.0/24")
n3 = Network("192.168.3.0/24")

(eth1, etr1a) = connect(h1, r1, network=n1)
(etr1b, etr2a) = connect(r1, r2, network=n2)
(etr2b, eth2) = connect(r2, h2, network=n3)

AddressHelper.assign_addresses()

eth1.set_attributes("1000mbit", "1ms")
etr1b.set_attributes("10mbit", "10ms", "pfifo")
etr2b.set_attributes("1000mbit", "1ms")

eth2.set_attributes("1000mbit", "1ms")
etr2a.set_attributes("10mbit", "10ms")
etr1a.set_attributes("1000mbit", "1ms")



h1.add_route("DEFAULT", eth1)
h2.add_route("DEFAULT", eth2)
r1.add_route("DEFAULT", etr1b)
r2.add_route("DEFAULT", etr2a)

exp = Experiment("02_compete_with_cubic")

flow1 = Flow(h1, h2, eth2.get_address(), 0, 200, 1)
exp.add_tcp_flow(flow1, "bbr")


flow2 = Flow(h2, h1, eth1.get_address(), 0, 200, 2)
exp.add_tcp_flow(flow2, "cubic")

exp.run()
