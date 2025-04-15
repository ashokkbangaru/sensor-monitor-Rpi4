# 🛠️ Room Monitor Dashboard

This project is a real-time room monitoring system built with Flask, Socket.IO, and various sensors (DHT11, ultrasonic, and PIR). It features a live dashboard viewable via a web browser and an LCD display for local feedback.

## 🔧 Features

- 🌡️ Temperature & 💧 Humidity monitoring (DHT11)
- 📏 Distance sensing with two ultrasonic sensors
- 👀 Motion detection via PIR sensor
- 📟 LCD display for local sensor readout
- 🌐 Real-time web dashboard using Socket.IO
- 📈 Chart.js for live data visualization
- 📤 CSV data export functionality
- 🚀 Optional Ngrok tunnel for remote access

## 📂 Project Structure

```
sensor_monitor/
├── app.py                  # Main Flask app
├── templates/
│   └── index.html          # Web dashboard
├── ngrok_config.sh         # Webserver config
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 📦 Installation

1. **Clone the repo:**

   ```bash
   git clone https://github.com/ashokkbangaru/sensor-monitor-Rpi4.git
   cd sensor-monitor-Rpi4
   ```

2. **Install dependencies:**

   ```bash
   pip3 install -r requirements.txt
   ```

3. **(Optional) Set up Ngrok:**

   Run the included Bash script:

   ```bash
   chmod +x ngrok_config.sh
   ./ngrok_config.sh
   ```

## ⚙️ Run as a Service (systemd)

To ensure the app starts on boot and runs in the background, create a systemd service.

### 📝 Create the Service File

```bash
sudo nano /etc/systemd/system/roommonitor.service
```

Paste the following:

```ini
[Unit]
Description=Room Monitor Flask App
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/usr/projects/sensor_monitor/app.py
WorkingDirectory=/home/usr/projects/sensor_monitor
Restart=always
User=*****  #update with your username
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### 🌀 Reload, Enable, and Start the Service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable roommonitor.service
sudo systemctl restart roommonitor.service
```

### ✅ Check Service Status

```bash
sudo systemctl status roommonitor.service
```

You should see logs indicating the Flask app is running.

## 🌍 Access the Dashboard

- **Locally:** Visit `http://<raspberry-pi-ip>:5000`
- **Remotely (via Ngrok):** Use the public URL printed to your terminal

## 🧪 Sensors Used

- **DHT11** – Temperature and humidity
- **HC-SR04** – Ultrasonic distance sensors (x2)
- **PIR Sensor** – Passive infrared motion sensor
- **I2C LCD Display** – Displays current readings

## 📃 License

This project is licensed under the MIT License.

---

Enjoy monitoring your space in real-time! 🎉
