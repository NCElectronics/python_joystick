#define joyX A0
#define joyY A1

#define upButton 8
#define downButton 9
#define leftButton 10
#define rightButton 11

void setup() {
  pinMode(upButton, INPUT_PULLUP);
  pinMode(downButton, INPUT_PULLUP);
  pinMode(leftButton, INPUT_PULLUP);
  pinMode(rightButton, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(115200);
}

void loop() {
  int up = digitalRead(upButton);
  int down = digitalRead(downButton);
  int left = digitalRead(leftButton);
  int right = digitalRead(rightButton);

  if (up == LOW || down == LOW || left == LOW || right == LOW) {
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }

  int x = map(analogRead(joyX), 0, 1023, 512, -512);
  int y = map(analogRead(joyY), 0, 1023, -512, 512);

  Serial.print(
    String(x) + "," + String(y)
    + "," + String(up == LOW) + "," + String(down == LOW) + "," + String(left == LOW) + "," + String(right == LOW)
    + "\n");
}
