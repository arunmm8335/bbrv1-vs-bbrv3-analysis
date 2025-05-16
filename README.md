# 📡 TCP BBRv1 vs BBRv3 Congestion Control Analysis using NEST

This project compares the performance of **TCP BBRv1** and **TCP BBRv3** congestion control algorithms using [Google's official BBR implementation](https://github.com/google/bbr/blob/v3/README.md) and the [NEST framework](https://gitlab.com/nitk-nest/nest).

---

## 📁 Project Structure
```bash
bbr-projects/
├── bbr1_experiments/ # BBRv1-based test scripts
├── bbrv3_experiements/ # BBRv3-based test scripts
├── bbr_testcases/ # NEST-compatible topologies and flows
├── bbr-comparisons/ # Analysis scripts and output plots
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

## 📦 NEST Installation (from GitLab)

NEST (Network Emulation & Simulation Tool) is used to test congestion control algorithms in emulated networks.
