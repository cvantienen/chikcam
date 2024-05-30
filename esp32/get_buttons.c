#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";

void setup() {
  Serial.begin(115200);
  delay(1000);

    // Connect to Wi-Fi network
  connectToWiFi();

  // Print network configuration
  printNetworkConfig();
}

void loop() {
  delay(100);
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Make a GET request to fetch the button status JSON
    http.begin("https://chikcam.com/esp32/uBdnK1AjstGFZ1HrCh3mqn2x49cEQ6yx/"); // Replace with the actual IP address or domain name of your server
    int httpResponseCode = http.GET();
    http.addHeader("Authorization", "155D2264685B61C8B7A37C5C95BBC"); // Replace YourSecretTokenHere with your actual token

    if (httpResponseCode == HTTP_CODE_OK) {
      String payload = http.getString();

      // Parse the JSON payload
      DynamicJsonDocument doc(1024);
      DeserializationError error = deserializeJson(doc, payload);

      if (error) {
        Serial.print("deserializeJson() failed: ");
        Serial.println(error.c_str());
      } else {
        // Extract button data
        JsonArray buttons = doc["buttons"];

        // Loop through each button
        for (JsonObject button : buttons) {
          const char* actionType = button["action_type"];
          int activationCount = button["activation_count"];

          // Here you can compare activationCount with the previous count and take action accordingly
          // For now, let's just print the data
          Serial.print("Action Type: ");
          Serial.println(actionType);
          Serial.print("Activation Count: ");
          Serial.println(activationCount);
          Serial.println();
        }
      }
    } else {
      Serial.print("HTTP request failed with error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
    connectToWiFi();
  }

  delay(5000); // Wait for 5 seconds before making the next request
}

void connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");
}

void printNetworkConfig() {
  Serial.println("Network Configuration:");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Subnet Mask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway IP: ");
  Serial.println(WiFi.gatewayIP());
  Serial.print("DNS Server: ");
  Serial.println(WiFi.dnsIP());
}
