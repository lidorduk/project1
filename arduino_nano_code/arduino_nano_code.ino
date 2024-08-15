
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(4);

char message[]="You are parking in private parking, please move your car";
int x, minX;
const int buzzer = 9;
unsigned long prevTime_activate = millis();
unsigned long prevTime_no_activate = millis();

void setup()
{
  Serial.begin(9600);
  pinMode(buzzer , OUTPUT);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setTextWrap(false);
  display.clearDisplay();
  display.display();
  x = display.width();
  minX = -12 * strlen(message);  // 12 = 6 pixels/character * text size 2
}

void loop()
{
  if (Serial.available() > 0)
  {
    String data = Serial.readStringUntil('\n');
    if (data == "active")
    {
      Lcd_Show_Text();
      Buzzer_alarm_active();
      Buzzer_alarm_no_active();
    }
    else
    {
      noTone(buzzer);
      display.clearDisplay();
      display.display();
    }
  }
  // Lcd_Show_Text();
  // Buzzer_alarm_active();
  // Buzzer_alarm_no_active();
}

void Buzzer_alarm_active()
{
  unsigned long currentTime = millis();
  if (currentTime - prevTime_activate > 1000)
  {
    tone(buzzer , 10000);
    prevTime_activate = currentTime;
  }
}

void Buzzer_alarm_no_active()
{
  unsigned long currentTime = millis();
  if (currentTime - prevTime_no_activate > 2000)
  {
    noTone(buzzer);
    prevTime_no_activate = currentTime;
  }
}

void Lcd_Show_Text()
{
  display.clearDisplay();
  display.setCursor(0,0);
  display.setTextSize(2);
  display.setCursor(x,10);
  display.print(message);
  display.setCursor(x,28);
  display.setCursor(x,38);
  display.setCursor(x,48);
  display.display();
  x=x-8; // scroll speed, make more positive to slow down the scroll
  if(x < minX) x= display.width();
}
