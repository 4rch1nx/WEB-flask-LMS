/*
Дисклеймер

Этот код был написан недопрограммистом в 2 часа ночи с мухаморами и он работает на честном слове и святой воде.
Пожалуйста, не меняйте ничего в коде(а лучше даже не читайте)
Andrew-24coop, 2025
*/

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

const char* ssid = "ESP8266_CAR_1";
const char* password = "12345678";

ESP8266WebServer server(80);
const int ledPin = D4;
bool ledState = false;

Servo sFL;
const int sFL_pin = D7;
Servo sFR;
const int sFR_pin = D8;
Servo sRL;
const int sRL_pin = D6;
Servo sRR;
const int sRR_pin = D5;

void handleToggle() {
  ledState = !ledState;
  digitalWrite(ledPin, ledState ? LOW : HIGH);
  server.send(200, "text/plain", ledState ? "ON" : "OFF");
}

void handleStatus() {
  server.send(200, "text/plain", "CONNECTED");
}

void handleServoFL() {
  if (server.hasArg("speed")) {
    String speedStr = server.arg("speed");
    int speed = speedStr.toInt();

    if (speed >= 0 && speed <= 180) {
      sFL.write(speed);
      server.send(200, "text/plain", "Servo set to " + String(speed));
    } else {
      server.send(400, "text/plain", "Invalid speed. Must be between 0 and 180.");
    }
  } else {
    server.send(400, "text/plain", "Missing 'speed' argument.");
  }
}

void handleServoFR() {
  if (server.hasArg("speed")) {
    String speedStr = server.arg("speed");
    int speed = speedStr.toInt();

    if (speed >= 0 && speed <= 180) {
      sFR.write(speed);
      server.send(200, "text/plain", "Servo set to " + String(speed));
    } else {
      server.send(400, "text/plain", "Invalid speed. Must be between 0 and 180.");
    }
  } else {
    server.send(400, "text/plain", "Missing 'speed' argument.");
  }
}

void handleServoRL() {
  if (server.hasArg("speed")) {
    String speedStr = server.arg("speed");
    int speed = speedStr.toInt();

    if (speed >= 0 && speed <= 180) {
      sRL.write(speed);
      server.send(200, "text/plain", "Servo set to " + String(speed));
    } else {
      server.send(400, "text/plain", "Invalid speed. Must be between 0 and 180.");
    }
  } else {
    server.send(400, "text/plain", "Missing 'speed' argument.");
  }
}

void handleServoRR() {
  if (server.hasArg("speed")) {
    String speedStr = server.arg("speed");
    int speed = speedStr.toInt();

    if (speed >= 0 && speed <= 180) {
      sRR.write(speed);
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

  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("ESP8266 AP IP Address: ");
  Serial.println(IP);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  sFL.attach(sFL_pin);
  sFR.attach(sFR_pin);
  sRL.attach(sRL_pin);
  sRR.attach(sRR_pin);

  server.on("/toggle", handleToggle);
  server.on("/status", handleStatus);
  server.on("/servo_fl", handleServoFL);
  server.on("/servo_fr", handleServoFR);
  server.on("/servo_rl", handleServoRL);
  server.on("/servo_rr", handleServoRR);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
