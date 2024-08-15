#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        4 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 24 // Popular NeoPixel ring size

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
#define TRIG_PIN 23 // ESP32 pin GIOP23 connected to Ultrasonic Sensor's TRIG pin
#define ECHO_PIN 22 // ESP32 pin GIOP22 connected to Ultrasonic Sensor's ECHO pin
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define TRIG_PIN 23 // ESP32 pin GIOP23 connected to Ultrasonic Sensor's TRIG pin
#define ECHO_PIN 22 // ESP32 pin GIOP22 connected to Ultrasonic Sensor's ECHO pin
float duration_us, distance_cm;
int   stopdistance=40; //parking position from sensor (CENTIMETERS)
int startdistance=280;   //distance from sensor to begin scan as car pulls in(CENTIMETERS) 
int increment=((startdistance-stopdistance)/NUMPIXELS);

void setup() {
  // begin serial port
  Serial.begin (115200);

  // configure the trigger pin to output mode
  pinMode(TRIG_PIN, OUTPUT);
  // configure the echo pin to input mode
  pinMode(ECHO_PIN, INPUT);

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
}

void loop() {
  // generate 10-microsecond pulse to TRIG pin
  pixels.setBrightness(16);
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // measure duration of pulse from ECHO pin
  duration_us = pulseIn(ECHO_PIN, HIGH);

  // calculate the distance
  //distance_cm = (float)duration_us * 0.034 / 2;
  int currentdistance = duration_us * 0.034 / 2;

  // print the value to Serial Monitor
  Serial.println(currentdistance);
  //Serial.print("distance: ");
  //Serial.print(distance_cm);
  //Serial.println(" cm");

  delay(100);
  
  if(currentdistance > 240)
  {
    colorWipe(pixels.Color(0, 0, 0) , NUMPIXELS);
  }

  if(currentdistance <= stopdistance)
  {
    colorWipe(pixels.Color(255, 0, 0) , NUMPIXELS);
  }
  else
  {
    for(int i = 1 ; i <= NUMPIXELS ; i++)
    {
      if(currentdistance < stopdistance + increment * i && i >= 7 && i <= NUMPIXELS)
      {
        swap_to_green(i);
        break;
      }
      if(currentdistance<stopdistance+increment*i && i>=1 && i<=6)
      {
        swap_to_yellow(i);
        break;
      }
    }
  }

}

void colorWipe(uint32_t c , int j) {
  for(uint16_t i=0; i < j; i++) {
    pixels.setPixelColor(i, c);
    pixels.show();
  }
}

void swap_to_green(int i)
{
  colorWipe(pixels.Color(0, 255, 0) , NUMPIXELS - i + 1);
  for(int j = NUMPIXELS - i + 1; j < NUMPIXELS ; j++)
  {
    pixels.setPixelColor(j, pixels.Color(0, 0, 0));
    pixels.show();
  }
}

void swap_to_yellow(int i)
{
  for (int   j = 0; j < NUMPIXELS - 6; j++)
  {
    pixels.setPixelColor(j, pixels.Color(0, 255, 0));
    pixels.show();
  }
  for (int   c = NUMPIXELS - 6; c < NUMPIXELS - i + 1; c++)
  {
    pixels.setPixelColor(c, pixels.Color(255, 255, 0));
    pixels.show();
  }
  for (int   a = NUMPIXELS - i + 1; a < NUMPIXELS; a++)
  {
    pixels.setPixelColor(a, pixels.Color(0, 0, 0));
    pixels.show();
  }
}
