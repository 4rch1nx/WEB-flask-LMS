#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>  // Include the Servo library

const char* ssid = "ESP8266_CAR_1";  // WiFi Name
const char* password = "12345678";   // Password (min 8 chars)

ESP8266WebServer server(80);
const int ledPin = D4;  // LED pin
bool ledState = false;

Servo sFL;
const int sFL_pin = D5;
Servo sFR;
const int sFR_pin = D6;
Servo sRL;
const int sRL_pin = D7;
Servo sRR;
const int sRR_pin = D8;

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

// Servo speed control (with argument)
void handleServo() {
  // Check if the request contains the "speed" argument
  if (server.hasArg("speed")) {
    String speedStr = server.arg("speed");  // Get the speed argument as a string
    int speed = speedStr.toInt();           // Convert to integer

    // Validate the speed value (must be between 0 and 180)
    if (speed >= 0 && speed <= 180) {
      sFL.write(speed);  // Set the servo position (angle)
      server.send(200, "text/plain", "Servo set to " + String(speed));
    } else {
      server.send(400, "text/plain", "Invalid speed. Must be between 0 and 180.");
    }
  } else {
    server.send(400, "text/plain", "Missing 'speed' argument.");
  }
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

  // Attach the servo to the specified pin
  sFL.attach(sFL_pin);
  sFR.attach(sFR_pin);
  sRL.attach(sRL_pin);
  sRR.attach(sRR_pin);

  // API routes
  server.on("/toggle", handleToggle);
  server.on("/status", handleStatus);
  server.on("/servo", handleServo);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
