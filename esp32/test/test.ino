//#include <SoftwareSerial.h>
char values;
char code[15];
int counter = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Hello World!");
  pinMode(19, OUTPUT);
}
void loop(){
  //Serial.println("prendido led");
  //digitalWrite(19, HIGH);
  values = Serial.read();
  //Serial.println("Hola mundo");
  if (values >= 40 and values <= 100){
    code[counter] = values;
    Serial.print(code[counter]);
    counter++;
  }
  else if (counter != 0){
    for(int i = 0; i < counter; i++){
      code[i] = '\0';
    }
    counter = 0;
    Serial.println(";");
  }
  delay(10);
  
}
