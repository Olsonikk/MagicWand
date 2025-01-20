#include "Arduino_BMI270_BMM150.h"
#define SAMPLE_COUNT 100

float ax, ay, az;
float gx, gy, gz;

int inde = 0;
int buttonstate = 1;
void setup() {
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
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  buttonstate = digitalRead(D5);
  if (buttonstate == LOW) {
    unsigned long StartTime = millis();
    digitalWrite(LEDG, LOW);
    
      while(1){
        if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
          IMU.readAcceleration(ax, ay, az);
          IMU.readGyroscope(gx,gy,gz);

          unsigned int CurrentTime = millis(); //TIMESTAMP 
          Serial.print("[");
          Serial.print(CurrentTime - StartTime);

          Serial.print(", ");
          Serial.print(ax);
          Serial.print(", ");
          Serial.print(ay);
          Serial.print(", ");
          Serial.print(az);

          Serial.print(", ");


          Serial.print(gx);
          Serial.print(", ");
          Serial.print(gy);
          Serial.print(", ");
          Serial.print(gz);
          Serial.print(", ");

          Serial.print("], ");
          inde++;
        }
        
        
        if(inde == 50)
        {
          digitalWrite(LEDR, LOW);
        }
        else if(inde == SAMPLE_COUNT)
        {
          break;
        }
        delay(5);
      }
      inde = 0;
      Serial.println("");
      digitalWrite(LEDG, HIGH);
      digitalWrite(LEDR, HIGH);
    }
}
