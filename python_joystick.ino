#define joyX A0
#define joyY A1
 
void setup() {
  Serial.begin(115200);
}
 
void loop() {
  int x = map(analogRead(joyX), 0, 1023, -512, 512);
  int y = map(analogRead(joyY), 0, 1023, -512, 512);

  Serial.print(String(x) + "," + String(y) + "\n");
  delay(100);
}
