#include <Arduino.h>
#include <HTTPClient.h>
#include <WiFi.h>

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* TELEMETRY_URL = "http://10.222.201.152:5000/api/telemetry";

constexpr int MQ136_PIN = 2;
constexpr int BATTERY_PIN = 3;
constexpr char DEVICE_ID[] = "ESP32-SB-001";
constexpr unsigned long SEND_INTERVAL_MS = 5000;

unsigned long lastSend = 0;

void connectToWifi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }
  Serial.println();
  Serial.print("Device IP: ");
  Serial.println(WiFi.localIP());
}

void sendTelemetry() {
  if (WiFi.status() != WL_CONNECTED) {
    connectToWifi();
  }

  const int gasRaw = analogRead(MQ136_PIN);
  const int batteryRaw = analogRead(BATTERY_PIN);
  const float exposurePpm = max(0.0f, (gasRaw / 4095.0f) * 15.0f);
  const char* status = exposurePpm >= 10.0f ? "DANGER" : exposurePpm >= 5.0f ? "WARNING" : "SAFE";

  String payload = "{\"device_id\":\"" + String(DEVICE_ID) +
    "\",\"gas_raw\":" + String(gasRaw) +
    ",\"exposure\":" + String(exposurePpm, 1) +
    ",\"battery_raw\":" + String(batteryRaw) +
    ",\"status\":\"" + status + "\"}";

  HTTPClient http;
  http.begin(TELEMETRY_URL);
  http.addHeader("Content-Type", "application/json");
  const int responseCode = http.POST(payload);
  Serial.printf("Telemetry response: %d\n", responseCode);
  http.end();
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  connectToWifi();
}

void loop() {
  if (millis() - lastSend >= SEND_INTERVAL_MS) {
    lastSend = millis();
    sendTelemetry();
  }
}