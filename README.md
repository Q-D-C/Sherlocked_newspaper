# Sherlocked Newspaper Setup

## How to Install:

### Configure WiFi Networks on Static IP

#### If Setting Up at the Location:

```bash
sudo nmcli dev wifi connect "SSID" password "password"
sudo nmcli connection modify SSID ipv4.method manual ipv4.addresses "192.168.1.100/24" ipv4.gateway "192.168.1.1" ipv4.dns "8.8.8.8 8.8.4.4"
```

#### If Setting Up Off-Site:
```bash
sudo nmcli dev wifi connect "home-SSID" password "home-password"
sudo nmcli connection add type wifi ifname wlan0 con-name remoteSSID ssid "remote-SSID"
sudo nmcli connection modify RemoteSSID wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify RemoteSSID wifi-sec.psk "remote-password"
sudo nmcli connection modify RemoteSSID ipv4.method manual ipv4.addresses "192.168.1.100/24" ipv4.gateway "192.168.1.1" ipv4.dns "8.8.8.8 8.8.4.4"
sudo nmcli connection up remoteSSID
```

### Update system
```bash
sudo apt update
sudo apt upgrade
```

### Clone GitHub Repository
```bash
sudo apt install git -y
git clone https://github.com/Q-D-C/Sherlocked_newspaper.git
cd Sherlocked_newspaper
```

### Put API Key into `website.py`

### Install pip
```bash
sudo apt install python3-pip -y
```

### Install Sendinblue API
```bash
pip install sib-api-v3-sdk --break-system-packages
```

### Install Flask
```bash
sudo apt install python3-pip -y
sudo pip3 install Flask --break-system-packages
```

### Create and Enable Service
```bash
sudo nano /etc/systemd/system/website.service
```

#### Copy This into the `website.service`:
```ini
[Unit]
Description=Start website at boot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/Sherlocked_newspaper/website.py
WorkingDirectory=/home/pi/Sherlocked_newspaper
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

### Enable the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable website.service
sudo systemctl start website.service
sudo systemctl status website.service
```

### Schedule Reboot at Midnight
```bash
sudo crontab -e
```

#### Add the Following Line to the Cron Job:
```bash
0 0 * * * /sbin/reboot
```
