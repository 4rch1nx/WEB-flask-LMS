from flask import Flask, render_template
import requests

app = Flask(__name__)

ESP_IP = "http://192.168.4.1"  # ESP8266 AP mode IP

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/sensors")
def home():
    return render_template("error.html", 501)

@app.route("/toggle_led")
def toggle_led():
    try:
        response = requests.get(f"{ESP_IP}/toggle")
        return response.text
    except requests.exceptions.RequestException:
        return "Error: ESP not reachable"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
