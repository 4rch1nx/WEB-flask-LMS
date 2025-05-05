from flask import Flask, render_template
import requests

app = Flask(__name__)
ESP_IP = "http://192.168.4.1"  # ESP8266 AP mode IP


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/toggle_led")
def toggle_led():
    try:
        response = requests.get(f"{ESP_IP}/toggle", timeout=2)
        return response.text
    except requests.exceptions.RequestException:
        return "Error"


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/sensors")
def sensors():
    return render_template("error.html")


@app.route("/algorithm")
def algorithm():
    return render_template("error.html")


@app.route("/check_status")
def check_status():
    try:
        response = requests.get(f"{ESP_IP}/status", timeout=2)
        if response.text == "CONNECTED":
            return "ESP8266 is Online"
    except requests.exceptions.RequestException:
        return "ESP8266 is Offline"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3030)
