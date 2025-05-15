# 🧠 Import modules
from nest.topology import *
from nest.experiment import *
from nest.topology.network import Network
from nest.topology.address_helper import AddressHelper

# 🌐 Define nodes
h1 = Node("h1")
h2 = Node("h2")
r1 = Router("r1")
r2 = Router("r2")

# 🔧 Define networks & connections
n1 = Network("192.168.1.0/24")
n2 = Network("192.168.2.0/24")  # bottleneck
n3 = Network("192.168.3.0/24")

(eth1, etr1a) = connect(h1, r1, network=n1)
(etr1b, etr2a) = connect(r1, r2, network=n2)
(etr2b, eth2) = connect(r2, h2, network=n3)

# 🌍 Assign IPs
AddressHelper.assign_addresses()

# ⚙️ Set link attributes
eth1.set_attributes("1000mbit", "0.5ms")
etr1b.set_attributes("10mbit", "10ms", "fq_codel")  # bottleneck
etr2b.set_attributes("1000mbit", "0.5ms")
eth2.set_attributes("1000mbit", "0.5ms")
etr2a.set_attributes("10mbit", "10ms")
etr1a.set_attributes("1000mbit", "0.5ms")

# 🛣️ Set routes
h1.add_route("DEFAULT", eth1)
h2.add_route("DEFAULT", eth2)
r1.add_route("DEFAULT", etr1b)
r2.add_route("DEFAULT", etr2a)

# 🧪 Define experiment
exp = Experiment("tcp-bbr-point-to-point-3-fq_codel")

# 🎯 TCP BBR flow
flow1 = Flow(h1, h2, eth2.get_address(), 0, 200, 1)
exp.add_tcp_flow(flow1, "bbr")

# ➕ [💥 ADD HERE 💥] More flows...
flow2 = Flow(h1, h2, eth2.get_address(), 0, 200, 2)
exp.add_tcp_flow(flow2, "reno")


# 🚀 Run the experiment
exp.run()
