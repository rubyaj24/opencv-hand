int ledPin = 13;  // Built-in LED pin
int count = 0;    // To store received data

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    count = Serial.read() - '0';  // Convert received character to integer

    // Blink LED based on the count
    for (int i = 0; i < count; i++) {
      digitalWrite(ledPin, HIGH);
      delay(500);
      digitalWrite(ledPin, LOW);
      delay(500);
    }
  }
}
