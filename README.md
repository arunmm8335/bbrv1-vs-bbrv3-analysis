#  TCP BBRv1 vs BBRv3 Congestion Control Analysis using NEST

This project compares the performance of **TCP BBRv1** and **TCP BBRv3** congestion control algorithms using [Google's official BBR implementation](https://github.com/google/bbr/blob/v3/README.md) and the [NEST framework](https://gitlab.com/nitk-nest/nest).

---

## 📁 Project Structure
```bash
bbr-projects/
├── bbr1_experiments/ # BBRv1-based test plots
├── bbrv3_experiements/ # BBRv3-based test plots
├── bbr_testcases/ # NEST-compatible topologies and flows (scripts)
├── bbr-comparisons/ # Analysis and output plots
└── README.md # Setup and usage documentation
```

---

## ⚙️ Kernel Setup with BBRv3

Follow the official [BBRv3 Google guide](https://github.com/google/bbr/blob/v3/README.md) or steps below to enable BBRv3 in your Linux kernel.

### 1. Clone Linux Kernel Source

```bash
git clone https://github.com/google/bbr.git -b v3
cd bbr
```
### 2. Configure Kernel

```bash
make defconfig
make menuconfig
# Enable BBR and advanced congestion controls:
# → Networking support
#   → Networking options
#     → TCP: advanced congestion control
#       → Select BBR and mark it as built-in (*) or module (M)

```

### 3. Build & Install Kernel

```bash
make -j$(nproc)
sudo make modules_install
sudo make install
sudo update-grub
```

### 4. Reboot & Activate BBRv3
```bash
sudo reboot
uname -r
```

Then activate BBRv3:
```bash
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
sudo sysctl -w net.core.default_qdisc=fq
```
------------------------------------------------------------

##  NEST Installation (from GitLab)

NEST (Network Emulation & Simulation Tool) is used to test congestion control algorithms in emulated networks.

### 1. Clone NEST

```bash
git clone https://gitlab.com/nitk-nest/nest.git
cd nest
```

### 2. Install NEST (Two Methods)

You can install NEST using either of the following:

---
🔹 Method A: Using install.sh
```bash
sudo ./install.sh
```
🔹 Method B: Using setup.py (Alternative)
```bash
sudo python3 setup.py install
```

### 3. Activate NEST Environment
```bash
sudo su
cd nest
source nest_env.sh
```

--------------------------------

## 🚀 Running TCP BBR Experiments Using NEST

Once NEST is installed and activated, you can run experiments using example scripts or your own custom topologies.

### 1. Example Directory Structure

Navigate to the NEST examples:
```bash
cd ~/nest/examples/tcp
```
You'll find example files like:
```bash
tcp-bbr-point-to-point-3.py – Simple point-to-point test using BBR congestion control.
```

You can copy and modify this script to test different:
   1. Topologies (star, dumbbell, etc.)
   2. Parameters (bandwidth, delay, queue size)
   3. Congestion control algorithms (BBRv1, BBRv3, CUBIC, etc.)
   4. Flow patterns (single/multiple flows, UDP/TCP mix)

### 2. Running an Experiment
Use the following command format to run any experiment:
```bash
sudo PYTHONPATH=./venv/bin/python3 examples/tcp/tcp-bbr-point-to-point-3.py
```

### 3. Output & Logs
    1. The script will run the experiment using netperf and ss.
    2. It generates output .json files with detailed statistics and plots.
    3. You’ll see a progress bar and then output like:

```markdown
[INFO]: Parsing statistics...
[INFO]: Plotting results...
```
----------------------------------------------------
## 📊 Throughput Evaluation using iperf3

### 1. BBRv1 
![alt text](<iperf_bbrv1.png>)

### 2. BBRv3
![alt text](<iperf_bbrv3.png>)

----------------------------------------------------

## ✅ Cases Where BBRv3 Outperforms BBRv1

###  High Packet Loss Networks

1. BBR v1 tends to be too optimistic in the presence of random or bursty packet losses (e.g., Wi-Fi, cellular).
2. BBR v3 has improved loss tolerance and is less aggressive when losses are detected, reducing retransmissions and improving stability.

### High Latency + Shallow Buffers (Bufferbloat-Prone)

1. BBR v1 can cause queue buildup, leading to high latency spikes.
2. BBR v3 includes RTT fairness and pacing improvements, preventing queue buildup and reducing delay.

###  Multiple Competing Flows (Fairness)

1. BBR v1 adapts slowly to sudden bandwidth drops (common in 4G/5G or Wi-Fi handoffs).
2. BBR v3 improves bandwidth responsiveness, especially when bandwidth contracts quickly.

----------------------------------------------------------------------------------------------------------------------------------------------------------

##  Summary Table: BBRv3 vs BBRv1

| **Scenario**                    | **BBRv1 Behavior**            | **BBRv3 Improvement**                  |
|--------------------------------|-------------------------------|----------------------------------------|
| High packet loss               | Overestimates bandwidth       | Adapts better, fewer losses            |
| High RTT / bufferbloat         | Queues up, causes latency     | Maintains low latency                  |
| Competing flows (RTT fairness) | Favors low RTT flows          | Fairer bandwidth sharing               |
| Mobile / dynamic networks      | Slow to adapt                 | Reacts faster to bandwidth changes     |
| Long-lived transfers           | Oscillatory throughput        | Smooth, consistent delivery            |
| Encrypted/short flows          | Aggressive probing            | Controlled startup, lower jitter       |

----------------------------------------------------------------------------------------------------------------------------------------------------------

##  Conclusion

BBRv3 demonstrates clear improvements over BBRv1 across several real-world networking scenarios. It offers better bandwidth estimation under high loss, maintains lower latency in high RTT/bufferbloat conditions, and shows enhanced fairness in multi-flow environments. BBRv3 is also more adaptive in dynamic network conditions, making it suitable for mobile and modern Internet applications. These improvements contribute to smoother and more efficient TCP performance overall.

----------------------------------------------------------------------------------------------------------------------------------------------------------

## 📚 References

- [BBR Congestion Control - Google Open Source](https://opensource.googleblog.com/2016/09/tcp-bbr-congestion-control-comes-to.html)
- Neal Cardwell, Yuchung Cheng, et al. *BBR: Congestion-Based Congestion Control*, ACM Queue, 2017.
- [BBRv2/Bbr3 Discussion on Linux Kernel Mailing List](https://lore.kernel.org/netdev/)
- [BBRv3 GitHub and Kernel Patch Discussions](https://github.com/google/bbr)
- iperf3: [https://github.com/esnet/iperf](https://github.com/esnet/iperf)
