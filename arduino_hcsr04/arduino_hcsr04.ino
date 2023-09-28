//handshake
//send "ready?" from PC
//send "ok." from Arduino

#define BAUDRATE 115200
#define HANDSHAKE_FROM_PC "ready?\r\n"
#define HANDSHAKE_FROM_ARDUINO "ok.\r\n"


#define ECHO_PIN 2
#define TRIGGER_PIN 3

// [m/s]
double soundVelocity_mps=331.5 + 0.6 * 25;
// [s/us]
double us2s=1.0 / (1000.0 * 1000.0);
// [cm/m]
double m2cm=100.0;
// [mm/m]
double m2mm=1000.0;

enum HandshakeState{
  HandshakeState_Initializing,
  HandshakeState_Ready,
}handshakeState=HandshakeState_Initializing;

void setup() {
  Serial.begin(BAUDRATE);
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(ECHO_PIN,INPUT);
  pinMode(TRIGGER_PIN,OUTPUT);
}

void loopInitializing(){
  if(0<Serial.available()){
    String str=Serial.readStringUntil('\n');
    str+='\n';
    if(str==HANDSHAKE_FROM_PC){
      Serial.print(HANDSHAKE_FROM_ARDUINO);
      handshakeState=HandshakeState_Ready;
      digitalWrite(LED_BUILTIN, HIGH);
      
    }
  }
}

void loopReady(){
  digitalWrite(TRIGGER_PIN,LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN,HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN,LOW);
  double duration_us = pulseIn( ECHO_PIN, HIGH );
  uint16_t distance_cm=(duration_us * 0.5) * us2s * soundVelocity_mps * m2cm;
  uint16_t distance_mm=(duration_us * 0.5) * us2s * soundVelocity_mps * m2mm;
//  double distance_m=(duration_us * 0.5) * us2s * soundVelocity_mps;
  
//  Serial.print("Distance:");
//  Serial.print(distance_cm);
//  Serial.print("[cm]");
//  Serial.print(", ");
//  Serial.print(distance_mm);
//  Serial.print("[mm]");
//  Serial.print(", ");
//  Serial.print(distance_m);
//  Serial.print("[m]");
//  Serial.println("");

  Serial.write((distance_mm >> 8) & 0xff);
  Serial.write((distance_mm >> 0) & 0xff);

  delay(200);

}


void loop() {
  switch(handshakeState){
    case HandshakeState_Initializing:
    loopInitializing();
    break;
    case HandshakeState_Ready:
    loopReady();
    break;
  }

}
