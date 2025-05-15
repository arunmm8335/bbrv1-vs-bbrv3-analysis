# SPDX-License-Identifier: GPL-2.0-only
# Copyright (c) 2019-2022 NITK Surathkal

########################
# SHOULD BE RUN AS ROOT
########################
from nest.topology import *
from nest.experiment import *
from nest.topology.network import Network
from nest.topology.address_helper import AddressHelper

# This program emulates point to point networks that connect two hosts `h1`
# and `h2` via two routers `r1` and `r2`. One TCP BBR flow is configured from
# `h1` to `h2`. The middle link is the bottleneck with limited bandwidth and high delay.

##############################################################################
#                              Network Topology                              #
#                                                                            #
#      100mbit, 1ms -->       5mbit, 50ms -->       100mbit, 1ms -->         #
# h1 -------------------- r1 -------------------- r2 -------------------- h2 #
#     <-- 100mbit, 1ms       <-- 5mbit, 50ms        <-- 100mbit, 1ms         #
#                                                                            #
##############################################################################

# Create two hosts `h1` and `h2`, and two routers `r1` and `r2`
h1 = Node("h1")
h2 = Node("h2")
r1 = Router("r1")
r2 = Router("r2")

# Set up IPv4 networks for each link
n1 = Network("192.168.1.0/24")  # h1 <-> r1
n2 = Network("192.168.2.0/24")  # r1 <-> r2 (bottleneck)
n3 = Network("192.168.3.0/24")  # r2 <-> h2

# Connect nodes
(eth1, etr1a) = connect(h1, r1, network=n1)
(etr1b, etr2a) = connect(r1, r2, network=n2)
(etr2b, eth2) = connect(r2, h2, network=n3)

# Assign IP addresses
AddressHelper.assign_addresses()

# ⚙️ Link attributes (test scenario: 5mbit, 50ms bottleneck with pfifo)
eth1.set_attributes("1000mbit", "0.5ms")
etr1b.set_attributes("10mbit", "10ms", "fq_codel")
etr2b.set_attributes("1000mbit", "0.5ms")

eth2.set_attributes("1000mbit", "0.5ms")
etr2a.set_attributes("10mbit", "10ms")
etr1a.set_attributes("1000mbit", "0.5ms")





# Set default routes
h1.add_route("DEFAULT", eth1)
h2.add_route("DEFAULT", eth2)
r1.add_route("DEFAULT", etr1b)
r2.add_route("DEFAULT", etr2a)

# Define the experiment
exp = Experiment("tcp-bbr-point-to-point-3-with_cubic")

# TCP BBR flow: h1 -> h2, runs from 0s to 200s
flow1 = Flow(h1, h2, eth2.get_address(), 0, 200, 1)
exp.add_tcp_flow(flow1, "bbr")

flow2 = Flow(h1, h2, eth2.get_address(), 0, 200, 2)
exp.add_tcp_flow(flow2, "cubic")


# Run the experiment
exp.run()
