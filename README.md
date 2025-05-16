# 📡 TCP BBRv1 vs BBRv3 Congestion Control Analysis using NEST

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

## 📦 NEST Installation (from GitLab)

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

### 1. 📂 Example Directory Structure

Navigate to the NEST examples:
```bash
cd ~/nest/examples/tcp
```
You'll find example files like:
    tcp-bbr-point-to-point-3.py – Simple point-to-point test using BBR congestion control.

You can copy and modify this script to test different:
   1. Topologies (star, dumbbell, etc.)
   2. Parameters (bandwidth, delay, queue size)
   3. Congestion control algorithms (BBRv1, BBRv3, CUBIC, etc.)
   4. Flow patterns (single/multiple flows, UDP/TCP mix)