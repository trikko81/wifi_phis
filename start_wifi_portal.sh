#!/bin/bash
# Wi-Fi Captive Portal Startup Script

# Activate your Python virtual environment
echo "Activating virtual environment..."
source ~/venv/bin/activate

# Restart dnsmasq
echo "Restarting dnsmasq..."
sudo systemctl restart dnsmasq

# Restart hostapd
echo "Restarting hostapd..."
sudo systemctl restart hostapd

# Ensure wlan0 has static IP for AP
echo "Setting IP for wlan0..."
sudo ip addr flush dev wlan0
sudo ip addr add 192.168.4.1/24 dev wlan0
sudo ip link set wlan0 up

# Start Flask portal
echo "Starting Flask portal..."
sudo $(which python) ~/wifi_phis/portal/app.py>
