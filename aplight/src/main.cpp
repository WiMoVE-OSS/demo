#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN 3

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 12

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 30 // Time (in milliseconds) to pause between pixels

#define BUFLEN (6 + 1) * NUMPIXELS + 1

char input[BUFLEN];
int charsRead;
int offset = 0;

uint32_t colors[NUMPIXELS];

uint32_t StrToHex(char str[])
{
  char buf[7];
  strncpy(buf, str, 6);
  buf[6] = '\0';
  return (uint32_t)strtoul(buf, 0, 16);
}

void parseSerial()
{
  if (Serial.available() > 0)
  {
    charsRead = Serial.readBytesUntil('\n', input, BUFLEN - 1);
    if (charsRead == BUFLEN - 1)
    {
      input[charsRead] = '\0';
      for (int i = 0; i < NUMPIXELS; i++)
      {
        colors[i] = StrToHex(input + i * 7);
      }
    }
  }
}

void displayPixels() {
  for (int i = 0; i < NUMPIXELS; i++)
  {
    pixels.setPixelColor((i + offset) % NUMPIXELS, colors[i]);
  }
  offset = (offset + 1) % NUMPIXELS;
  pixels.show();
}

void setup()
{
  pixels.begin();
  Serial.begin(9600);
}

void loop()
{
  parseSerial();
  displayPixels();
  delay(DELAYVAL);
}
