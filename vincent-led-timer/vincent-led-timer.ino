/*
   LCD RS pin to digital pin 10
   LCD Enable pin to digital pin 9
   LCD D4 pin to digital pin 5
   LCD D5 pin to digital pin 4
   LCD D6 pin to digital pin 3
   LCD D7 pin to digital pin 2
   LCD R/W pin to ground
   LCD VSS pin to ground
   LCD VCC pin to 5V
   10K resistor:
   ends to +5V and ground
   wiper to LCD VO pin (pin 3)
*/

// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(10, 9, 7, 6, 5, 4);

const int buzzerPin = 13;
int led_ind = 0;
unsigned long beginning_time = millis(); // time at which the timer switched from start to stop or stop to switch

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Setup Complete!");

  // set up serial monitor
  Serial.begin(9600);
  while( ! Serial); //wait until serial is ready
  Serial.println("Ready!");

}


void start_timer(String name, unsigned long timer_beginning) {
  lcd.clear();
  // print name on first row
  lcd.setCursor(0,0);
  lcd.print(name);

  // print time on second row
  lcd.setCursor(0,1);
  unsigned long time_ms = millis();
  unsigned long duration_ms = time_ms - timer_beginning;
  int minutes = duration_ms / 60000;
  int seconds = (duration_ms / 1000) % 60;

  String time_msg = String(minutes) + ":" + String(seconds);
  lcd.print(time_msg);
  
  
  if ((seconds % 10) == 0) {
    tone(buzzerPin, 261, 300);
  }
}

void stop_timer(unsigned long timer_beginning) {
  lcd.clear();
  // print on first row
  lcd.setCursor(0,0);
  lcd.print("BRB!");

  // print time on second row
  lcd.setCursor(0,1);
  unsigned long time_ms = millis();
  unsigned long duration_ms = time_ms - timer_beginning;
  int minutes = duration_ms / 60000;
  int seconds = (duration_ms / 1000) % 60;

  String time_msg = String(minutes) + ":" + String(seconds);
  lcd.print(time_msg);
}

void loop() {
  // put your main code here, to run repeatedly:
  // start and stop timer depending on 
  if (Serial.available()) {
    char ch = Serial.read();
    if (ch == 'v') {
      if (led_ind == 0) {
        led_ind = 1;
        beginning_time = millis();
      }
    }
    if (ch == 'x') {
      if (led_ind == 1) {
        led_ind = 0;
        beginning_time = millis();
      }
    }
  }
  if (led_ind) {
    start_timer("Vincent", beginning_time);
  }
  else {
    stop_timer(beginning_time);
  }
}
