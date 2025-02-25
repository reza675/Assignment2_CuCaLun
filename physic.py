import network
import time
import urequests
from machine import Pin
import dht

# Konfigurasi WiFi
# Konfigurasi WiFi
SSID = "Ziaf 5G"
PASSWORD = "zidanaffan"

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBUS-FzXu6L5Qrvz0JburU8VkLHbaZxQe8d"
DEVICE_LABEL = "esp32-sic6"
VARIABLES = {"temperature": "temperature", "humidity": "humidity", "motion": "motion"}
UBIDOTS_URL = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"
# Konfigurasi Flask API (ubah sesuai dengan alamat server Flask-mu)
FLASK_API_URL = "http://127.0.0.1:5000/sensor-data"  # Sesuaikan IP Flask

# Inisialisasi sensor
dht_sensor = dht.DHT11(Pin(4))  # DHT11 di GPIO4
pir_sensor = Pin(5, Pin.IN)  # PIR di GPIO5
led= Pin((18),Pin.OUT)
led.on()
# Koneksi ke WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

print("Connected to WiFi!")

# Fungsi Kirim Data ke Ubidots
def send_to_ubidots(temp, hum, motion):
    payload = {
        VARIABLES["temperature"]: {"value": temp},
        VARIABLES["humidity"]: {"value": hum},
        VARIABLES["motion"]: {"value": motion}
    }

    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
    response = urequests.post(UBIDOTS_URL, json=payload, headers=headers)
    print("Ubidots Response:", response.text)

# Fungsi Kirim Data ke Flask API
def send_to_flask(temp, hum, motion):
    payload = {
        "temperature": temp,
        "humidity": hum,
        "motion": motion
    }

    headers = {"Content-Type": "application/json"}
    response = urequests.post(FLASK_API_URL, json=payload, headers=headers)
    print("Flask Response:", response.text)

# Loop utama
while True:
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    motion_detected = 1 if pir_sensor.value() else 0

    send_to_ubidots(temperature, humidity, motion_detected)
    send_to_flask(temperature, humidity, motion_detected)

    time.sleep(10)  # Kirim setiap 10 detik

