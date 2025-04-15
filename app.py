import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import adafruit_dht
import board
import RPi.GPIO as GPIO
import time
import json
import subprocess
from RPLCD.i2c import CharLCD

# === LCD Setup ===
lcd = CharLCD('PCF8574', 0x27)
lcd.clear()

# === Flask Setup ===
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)

# DHT11
DHT_SENSOR = adafruit_dht.DHT11(board.D4)

# Ultrasonic Sensor 1
TRIG1 = 23
ECHO1 = 24

# Ultrasonic Sensor 2
TRIG2 = 13
ECHO2 = 19

# PIR Sensor (added)
PIR_PIN = 17

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN)  # Set PIR pin as input

def get_distance(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.05)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    timeout = time.time() + 0.04
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return 0

    while GPIO.input(echo) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return 0

    duration = pulse_end - pulse_start
    distance = duration * 17150
    return round(distance, 2)

def update_lcd(temp, hum, dist1, dist2):
    lcd.clear()
    lcd.write_string(f"T:{temp:.1f}C H:{hum:.1f}%")
    lcd.crlf()
    lcd.write_string(f"D1:{dist1:.0f} D2:{dist2:.0f}")

def sensor_loop():
    while True:
        try:
            temperature = DHT_SENSOR.temperature
            humidity = DHT_SENSOR.humidity
        except RuntimeError:
            temperature, humidity = None, None

        dist1 = get_distance(TRIG1, ECHO1)
        dist2 = get_distance(TRIG2, ECHO2)
        motion = dist1 < 100 or dist2 < 100

        pir_motion = GPIO.input(PIR_PIN)  # Read PIR motion

        temp = temperature if temperature is not None else 0
        hum = humidity if humidity is not None else 0

        update_lcd(temp, hum, dist1, dist2)

        data = {
            'temperature': temp,
            'humidity': hum,
            'distance1': dist1,
            'distance2': dist2,
            'motion': motion,
            'pir_motion': bool(pir_motion)  # Send PIR motion status
        }

        socketio.emit('sensor_data', data)
        time.sleep(0.0001)

@app.route('/')
def index():
    return render_template('index.html')

def run_ngrok():
    print("Starting ngrok tunnel...")
    subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #replace with this line for custom domain [subprocess.Popen(["ngrok", "http","--domain=p******.ngrok-free.app", "5000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)]
    time.sleep(5)
    try:
        result = subprocess.run(["curl", "-s", "http://localhost:4040/api/tunnels"],
                                capture_output=True, text=True, timeout=5)
        if result.stdout:
            tunnels = json.loads(result.stdout)
            public_url = tunnels['tunnels'][0]['public_url']
            print(f"🌍 Public URL: {public_url}")
        else:
            print("❌ ngrok tunnel not found.")
    except Exception as e:
        print(f"❌ Error retrieving ngrok URL: {e}")

if __name__ == '__main__':
    try:
        socketio.start_background_task(sensor_loop)
        socketio.start_background_task(run_ngrok)
        socketio.run(app, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        lcd.clear()
        GPIO.cleanup()
