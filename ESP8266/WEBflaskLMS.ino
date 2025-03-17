#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266Servo.h>

const char* ssid = "ESP8266_CAR_1";
const char* password = "12345678";

ESP8266WebServer server(80);
const int ledPin = D4;
bool ledState = false;

Servo myServo;
const int servoPin = D3;  // 360° Servo on D3 (GPIO 0)

// Handle LED Toggle
void handleToggle() {
  ledState = !ledState;
  digitalWrite(ledPin, ledState ? LOW : HIGH);
  server.send(200, "text/plain", ledState ? "ON" : "OFF");
}

// Handle Servo Control
void handleServo() {
  if (server.hasArg("speed")) {
    int speed = server.arg("speed").toInt();  // Read speed parameter
    if (speed >= 0 && speed <= 180) {         // Valid range
      myServo.write(speed);
      Serial.println(speed);
      server.send(200, "text/plain", "Servo speed set to " + String(speed));
    } else {
      server.send(400, "text/plain", "Invalid speed (0-180)");
    }
  } else {
    server.send(400, "text/plain", "Missing speed parameter");
  }
}

// Stop Servo
void handleStopServo() {
  myServo.write(90);  // 90° stops a continuous rotation servo
  server.send(200, "text/plain", "Servo stopped");
}

void setup() {
  Serial.begin(115200);

  WiFi.softAP(ssid, password);
  Serial.print("ESP8266 AP IP Address: ");
  Serial.println(WiFi.softAPIP());

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  myServo.attach(servoPin);
  myServo.write(90);  // Start with servo stopped

  server.on("/toggle", handleToggle);
  server.on("/servo", handleServo);
  server.on("/servo/stop", handleStopServo);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}