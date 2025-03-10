#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "ESP8266_CAR";
const char* password = "espvsflask25";

ESP8266WebServer server(80);
const int ledPin = D4;
bool ledState = false;

void handleToggle() {
    ledState = !ledState;
    digitalWrite(ledPin, ledState ? HIGH : LOW);
    server.send(200, "text/plain", ledState ? "ON" : "OFF");
}

void setup() {
    Serial.begin(115200);
    
    // Set ESP8266 as an Access Point
    WiFi.softAP(ssid, password);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("ESP8266 AP IP Address: ");
    Serial.println(IP);

    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW);

    // API route
    server.on("/toggle", handleToggle);
    
    server.begin();
    Serial.println("HTTP server started");
}

void loop() {
    server.handleClient();
}
