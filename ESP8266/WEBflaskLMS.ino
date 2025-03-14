#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "ESP8266_CAR_1";    // WiFi Name
const char* password = "12345678";  // Password (min 8 chars)

ESP8266WebServer server(80);
const int ledPin = D4;  // LED pin
bool ledState = false;

// Toggle LED state (inverted logic)
void handleToggle() {
  ledState = !ledState;
  digitalWrite(ledPin, ledState ? LOW : HIGH);  // Inverted
  server.send(200, "text/plain", ledState ? "ON" : "OFF");
}

// Status endpoint
void handleStatus() {
  server.send(200, "text/plain", "CONNECTED");
}

void setup() {
  Serial.begin(115200);

  // Set ESP8266 as an Access Point
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("ESP8266 AP IP Address: ");
  Serial.println(IP);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);  // Default OFF (inverted)

  // API routes
  server.on("/toggle", handleToggle);
  server.on("/status", handleStatus);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}