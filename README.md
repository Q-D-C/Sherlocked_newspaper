how to install:

# Configure WiFi networks on static ip, for example by doing:
# If doing it at the location
sudo nmcli dev wifi connect "SSID" password "password"
sudo nmcli connection modify SSID ipv4.method manual ipv4.addresses "192.168.1.100/24" ipv4.gateway "192.168.1.1" ipv4.dns "8.8.8.8 8.8.4.4"

# If setting up off-site
sudo nmcli dev wifi connect "home-SSID" password "home-password"
sudo nmcli connection add type wifi ifname wlan0 con-name remoteSSID ssid "remote-SSID"
sudo nmcli connection modify RemoteSSID wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify RemoteSSID wifi-sec.psk "remote-password"
sudo nmcli connection modify RemoteSSID ipv4.method manual ipv4.addresses "192.168.1.100/24" ipv4.gateway "192.168.1.1" ipv4.dns "8.8.8.8 8.8.4.4"
sudo nmcli connection up remoteSSID

# Clone GitHub repository
sudo apt install git -y
git clone https://github.com/Q-D-C/Sherlocked_newspaper.git
cd Sherlocked_newspaper

#Put API key into website.py

# Install Sendinblue API
pip install sib-api-v3-sdk --break-system-packages

# Install Flask
sudo apt update
sudo apt install python3-pip -y
sudo pip3 install Flask --break-system-packages

# Create and enable service
sudo nano /etc/systemd/system/website.service

#Copy this into the website.service

[Unit]
Description=Start Flask website at boot
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

#enable the service
sudo systemctl daemon-reload
sudo systemctl enable website.service
sudo systemctl start website.service

# Schedule reboot at midnight
sudo crontab -e
# (Add the cron job)
0 0 * * * /sbin/reboot

