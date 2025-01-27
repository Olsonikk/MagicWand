#include "model_with_labels.h"
#include "Arduino_BMI270_BMM150.h"
#include <Adafruit_NeoPixel.h>
#include <ArduinoBLE.h>

BLEService messageService("12345678-1234-1234-1234-1234567890ab"); // UUID usługi
BLEStringCharacteristic messageCharacteristic("87654321-4321-4321-4321-abcdefabcdef", BLERead | BLENotify, 20); // UUID charakterystyki


#define PIN D3  //LED pin
#define NUM_LEDS 1 //ile Ledow

#define SAMPLE_COUNT 100
#define FLATTENED_SIZE (SAMPLE_COUNT * 7)

Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRBW + NEO_KHZ800);

Eloquent::ML::Port::RandomForest classifier;
float ax, ay, az;
float gx, gy, gz;

float dataArray[SAMPLE_COUNT][7]; // Tablica do przechowywania odczytów: ax, ay, az, gx, gy, gz, timestamp
float flattenedArray[FLATTENED_SIZE]; // Spłaszczona tablica do predykcji
int indeks = 0;
int buttonState = 1;

void flattenData() {
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    for (int j = 0; j < 7; j++) {
      flattenedArray[i * 7 + j] = dataArray[i][j];
    }
  }
}

void setup() {
  strip.begin();      // Inicjalizacja NeoPixel
  strip.setBrightness(90);
  strip.show();       // Wyłączenie wszystkich diod na start
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D5, INPUT_PULLUP);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);

  Serial.begin(9600);
  //while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  if (!BLE.begin()) {
    Serial.println("- Starting Bluetooth® Low Energy module failed!");
    while (1);
  }
  
  // Konfiguracja urządzenia BLE
  BLE.setDeviceName("Nano33BLE");
  BLE.setLocalName("Nano33BLE");
  BLE.setAdvertisedService(messageService);

  // Dodanie charakterystyki do usługi
  messageService.addCharacteristic(messageCharacteristic);

  // Dodanie usługi do BLE
  BLE.addService(messageService);

  // Rozpoczęcie reklamowania urządzenia BLE
  BLE.advertise();
  Serial.println("Urządzenie BLE jest gotowe do parowania.");
}

void loop() {
  BLEDevice central = BLE.central();
  buttonState = digitalRead(D5);
  char res = Serial.read();

  BLE.poll();
  if (buttonState == LOW || res == 'x') {
    strip.setPixelColor(0, strip.Color(0, 0, 0, 0));
    strip.show();
    Serial.println("start");
    unsigned int startTime = millis();
    digitalWrite(LEDG, LOW);

    while (1) {
      if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
        IMU.readAcceleration(ax, ay, az);
        IMU.readGyroscope(gx, gy, gz);

        unsigned int currentTime = millis();
        dataArray[indeks][0] = (unsigned int) currentTime - startTime; // Timestamp
        dataArray[indeks][1] = ax;
        dataArray[indeks][2] = ay;
        dataArray[indeks][3] = az;
        dataArray[indeks][4] = gx;
        dataArray[indeks][5] = gy;
        dataArray[indeks][6] = gz;

        indeks++;

        if (indeks == 50) {
          digitalWrite(LEDR, LOW); // Sygnał, że osiągnięto 50 odczytów
        } else if (indeks == SAMPLE_COUNT) {
          break; // Zebrano wszystkie odczyty
        }
      }
    }

    // Serial.println("Zebrane dane:");
    // for (int i = 0; i < SAMPLE_COUNT; i++) {
    //   //Serial.print("[");
    //   for (int j = 0; j < 7; j++) {
    //     if (j == 0) {
    //       Serial.print((unsigned int)dataArray[i][j]); // Wyświetl czas jako liczba całkowita
    //     } else {
    //       Serial.print(dataArray[i][j], 2); // Wyświetl pozostałe wartości z 2 miejscami po przecinku
    //     }
    //     if (j < 6) Serial.print(", ");
    //   }
    //   Serial.println("");
    // }

    delay(100);
    // Spłaszczenie tablicy
    flattenData();
    String result = classifier.predictLabel(flattenedArray);
    // Predykcja
    Serial.println(result);
    messageCharacteristic.writeValue(result);

    if(result == "lumos")
    {
      fadeWhite(1500);
    }
    else if(result == "avada")
    {
      strip.setPixelColor(0, strip.Color(0, 200, 0, 0)); // RGB=0,0,0, W=brightness
      strip.show();
      delay(1000);
      strip.setPixelColor(0, strip.Color(0, 0, 0, 0)); // RGB=0,0,0, W=brightness
      strip.show();
    }
    else if(result == "wingardium")
    {
      strip.setPixelColor(0, strip.Color(200, 83, 244, 0)); // RGB=0,0,0, W=brightness
      strip.show();
      delay(1500);
      strip.setPixelColor(0, strip.Color(0, 0, 0, 0)); // RGB=0,0,0, W=brightness
      strip.show();
    }
    else if(result == "alohomora")
    {
      fadeWhite(200);
      strip.setPixelColor(0, strip.Color(0, 0, 0, 0)); // RGB=0,0,0, W=brightness
      strip.show();
    }

    indeks = 0; // Zresetuj indeks dla następnej próby
    digitalWrite(LEDG, HIGH);
    digitalWrite(LEDR, HIGH);
  }
}

void fadeWhite(int duration) {
  int steps = 255; // Rozdzielczość jasności (od 0 do 255)
  int delayTime = duration / steps;

  for (int i = 0; i <= steps; i++) {
    uint8_t brightness = i; // Jasność od 0 do 255
    strip.setPixelColor(0, strip.Color(0, 0, 0, brightness)); // RGB=0,0,0, W=brightness
    strip.show();
    delay(delayTime);
  }
}


