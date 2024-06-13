#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>

#define RELAY_PIN 33 // ESP32 pin GPIO16 connected to the IN pin of relay


Servo myservo;  // create servo object to control a servo

int pos = 0;

const char* ssid = "BASIL";
const char* password = "fluffypotato";

const int servoPin = 26;  // GPIO26

int prevActivationCounts[5] = {0}; // Store previous activation counts for 5 activation types

const char* actionTypeStrings[] = { "take_pic", "text_to_talk", "play_song", "flashlight", "feed_snack",};

unsigned long previousFeedTime = 0; // Keep track of the last time feedSnack was called

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi network
  connectToWiFi();
  // Print network configuration
  printNetworkConfig();

  // Allow allocation of all timers
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  myservo.attach(servoPin, 500, 2500); // attaches the servo on pin 18 to the servo object
  // different servos may require different min/max settings
  myservo.setPeriodHertz(50);    // standard 50 hz servo

  pinMode(RELAY_PIN, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousFeedTime >= 10000) {
    previousFeedTime = currentMillis;
    makeRequest();
  }
}

void connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 25) {
    delay(1000);
    Serial.println("Connecting...");
    attempts++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected to WiFi");
  } else {
    Serial.println("Failed to connect to WiFi");
  }
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

void makeRequest() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Make a GET request to fetch the button status JSON
    http.begin("https://chikcam.com/esp32/uBdnK1AjstGFZ1HrCh3mqn2x49cEQ6yx/"); // Replace with the actual IP address or domain name of your server
    http.addHeader("Authorization", "155D2264685B61C8B7A37C5C95BBC"); // Replace YourSecretTokenHere with your actual token
    int httpResponseCode = http.GET();

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

          // Check if activation count increased for the current action type
          for (int i = 0; i < 5; i++) {
            if (strcmp(actionType, actionTypeStrings[i]) == 0 && activationCount > prevActivationCounts[i]) {
              Serial.println(actionType);
              Serial.println(i);
              // Call corresponding function based on action type
              activateFunction(i);
              // Update previous activation count
              prevActivationCounts[i] = activationCount;
            }
          }
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
}

void activateFunction(int actionIndex) {
  switch(actionIndex) {
    case 0:
      // Activate function for flashlight
      textToTalk();
      break;
    case 1:
      // Activate function for text_to_talk
      takePic();
      break;
    case 2:
        // Activate function for play_song
      playSong();
      break;
    case 3:
      // Activate function for take_pic
      turnOnFlashlight();
      break;
    case 4:
      // Activate function for feed_snack
      feedSnack();
      break;
    default:
      // Handle unexpected action index
      Serial.println("Invalid action index");
  }
}

// Activation functions for each action type
void takePic() {
  // Add your logic to take a picture
  Serial.println("Taking a picture");
  // Implement your code to take a picture here
}

void turnOnFlashlight() {
  // Add your logic to turn on the flashlight
  Serial.println("Turning on flashlight");
  // Show the LEDs after setting white
  digitalWrite(RELAY_PIN, HIGH);
  delay(15000);
  digitalWrite(RELAY_PIN, LOW);
  delay(100);
}

void feedSnack() {
  // Add your logic to feed a snack
  Serial.println("Feeding snack");

  // Rotate the servo from 0 to 180 degrees
  for (int angle = 0; angle <= 180; angle++) {
    int pulseWidth = map(angle, 0, 180, 500, 2500);
    myservo.writeMicroseconds(pulseWidth);
    delay(8);
  }

  // Rotate the servo from 180 to 0 degrees
  for (int angle = 180; angle >= 0; angle--) {
    int pulseWidth = map(angle, 0, 180, 500, 2500);
    myservo.writeMicroseconds(pulseWidth);
    delay(8);
  }

  delay(100); // Optional delay
}

void textToTalk() {
  // Add your logic to convert text to speech
  Serial.println("Converting text to speech");
  // Implement your code to convert text to speech here
}

void playSong() {
  // Add your logic to play a song
  Serial.println("Playing a song");
  // Implement your code to play a song here
}
