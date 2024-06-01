#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>
#include <FastLED.h>

#define NUM_LEDS 8      /* The amount of pixels/leds you have */
#define DATA_PIN 14      /* The pin your data line is connected to */
#define LED_TYPE WS2812B /* I assume you have WS2812B leds, if not just change it to whatever you have */
#define BRIGHTNESS 255   /* Control the brightness of your leds */
#define SATURATION 255   /* Control the saturation of your leds */

CRGB leds[NUM_LEDS];

Servo myservo;  // create servo object to control a servo

int pos = 0; 

const char* ssid = "BASIL";
const char* password = "fluffypotato";

const int servoPin = 26;  // GPIO26

int prevActivationCounts[5] = {0}; // Store previous activation counts for 5 activation types

const char* actionTypeStrings[] = {"take_pic", "flashlight", "feed_snack", "text_to_talk", "play_song"};


void setup() {
  Serial.begin(115200);
  delay(1000);

  // setup LED
  FastLED.addLeds<LED_TYPE, DATA_PIN>(leds, NUM_LEDS);

  // Connect to Wi-Fi network
  connectToWiFi();
  // Print network configuration
  printNetworkConfig();

  // Allow allocation of all timers
	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50);    // standard 50 hz servo
	myservo.attach(servoPin, 1000, 2000); // attaches the servo on pin 18 to the servo object
	// using default min/max of 1000us and 2000us
	// different servos may require different min/max settings
	// for an accurate 0 to 180 sweep
}

void loop() {
  delay(100);

  feedSnack();

  rainbowLed();
  
  
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
  feedSnack();
  delay(5000); // Wait for 5 seconds before making the next request
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


void activateFunction(int actionIndex) {
  switch(actionIndex) {
    case 0:
      // Activate function for take_pic
      takePicture();
      break;
    case 1:
      // Activate function for flashlight
      turnOnFlashlight();
      break;
    case 2:
      // Activate function for feed_snack
      feedSnack();
      break;
    case 3:
      // Activate function for text_to_talk
    textToTalk();
      break;
    case 4:
      // Activate function for play_song
      playSong();
      break;
    default:
      // Handle unexpected action index
      Serial.println("Invalid action index");
  }
}

// Activation functions for each action type

void takePicture() {
  // Add your logic to take a picture
  Serial.println("Taking a picture");
  // Implement your code to take a picture here
}

void turnOnFlashlight() {
  // Add your logic to turn on the flashlight
  Serial.println("Turning on flashlight");
  // Implement your code to turn on the flashlight here
}

void feedSnack() {
  // Add your logic to feed a snack
  Serial.println("Feeding snack");
  // Sweep the servo back and forth
  for (pos = 0; pos <= 230; pos++) {
    myservo.write(pos);  // tell servo to go to position in variable 'pos'
    delay(15);           // waits 15ms for the servo to reach the position
  }
  
  // Rotate from 230 to 0 degrees
  for (pos = 230; pos >= 0; pos--) {
    myservo.write(pos);  // tell servo to go to position in variable 'pos'
    delay(15); 
  }
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

void rainbowLed() {
  for (int j = 0; j < 255; j++) {
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CHSV(i - (j * 2), SATURATION, BRIGHTNESS); /* The higher the value 4 the less fade there is and vice versa */ 
    }
    FastLED.show();
    delay(25); /* Change this to your hearts desire, the lower the value the faster your colors move (and vice versa) */
  }
}
