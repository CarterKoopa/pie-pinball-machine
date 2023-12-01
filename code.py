import busio
import digitalio
import pwmio
import time
import board
import random
from adafruit_motor import servo
from adafruit_mcp230xx.mcp23017 import MCP23017
import adafruit_mcp3xxx.mcp3008 as MCP3
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import sdcardio
import storage
import adafruit_tlc5947
import audiomp3
import audiomixer
import audiobusio

# Define Pins
FL_0 = board.GP0    # Flipper Left
FR_0 = board.GP1    # Flipper Right
SL_0 = board.GP2    # Slingshot Left
SR_0 = board.GP3    # Slingshot Right
FBL_0 = board.GP4   # Flipper Button Left
FBR_0 = board.GP5   # Flipper Button Right
DD1_PWM = board.GP15    # Dropdown Target 1
DD2_PWM = board.GP14    # Dropdown Target 2

I2C_SDA = board.GP6 # I2C In-Out SDA
I2C_SCL = board.GP7 # I2C In-Out SCL

SPI_0_MISO = board.GP8  # SPI_0 MISO
SPI_0_CLK = board.GP10  # SPI_0 Clock
SPI_0_MOSI = board.GP11 # SPI_0 MOSI

SPI_1_CLK = board.GP18  # SPI 1 Clock
SPI_1_MOSI = board.GP19 # SPI 1 MOSI
SPI_1_MISO = board.GP20 # SPI 1 MISO

LDR_ADC_CS = board.GP9  # MCP3008 Chip Select for Rollover LDRs
SD_CS = board.GP17  # MicroSD Chip Select
LED_LAT = board.GP22    # TLC5947 Latch for LEDs

AMP_DIN = board.GP26    # Amp Data In
AMP_BCLK = board.GP27   # Amp Bit Clock
AMP_LRC = board.GP28    # Amp Left/Right Clock

# Define I2C and SPI
i2c = busio.I2C(I2C_SCL, I2C_SDA)
spi_0 = busio.SPI(clock=SPI_0_CLK, MOSI=SPI_0_MOSI, MISO=SPI_0_MISO)
spi_1 = busio.SPI(clock=SPI_1_CLK, MOSI=SPI_1_MOSI, MISO=SPI_1_MISO)

def cross_lights(speed=0.2):
    led_tlc[0] = 0
    led_tlc[5] = 0
    time.sleep(speed)
    led_tlc[1] = 0
    led_tlc[6] = 0
    led_tlc[0] = 4095
    led_tlc[5] = 4095
    time.sleep(speed)
    led_tlc[2] = 0
    led_tlc[1] = 4095
    led_tlc[6] = 4095
    time.sleep(speed)
    led_tlc[3] = 0
    led_tlc[7] = 0
    led_tlc[2] = 4095
    time.sleep(speed)
    led_tlc[4] = 0
    led_tlc[8] = 0
    led_tlc[3] = 4095
    led_tlc[7] = 4095
    time.sleep(speed)
    led_tlc[4] = 4095
    led_tlc[8] = 4095

# Set Up Dropdowns
dd1_pwm = pwmio.PWMOut(DD1_PWM, duty_cycle=2 ** 15, frequency=50)
dd1_servo = servo.Servo(dd1_pwm)
dd2_pwm = pwmio.PWMOut(DD2_PWM, duty_cycle=2 ** 15, frequency=50)
dd2_servo = servo.Servo(dd2_pwm)

dd1_servo.angle = 70
dd2_servo.angle = 70

# Set Up Rollovers
ldr_adc_mcp = MCP3.MCP3008(spi_0, digitalio.DigitalInOut(LDR_ADC_CS))
ldr_adcs = []
ldr_adc_defaults = []
for channel in range(4):
    ldr_adcs.append(AnalogIn(ldr_adc_mcp, channel))
    ldr_adc_defaults.append(ldr_adcs[channel].voltage)
print(ldr_adc_defaults)

# Set up LEDs
led_tlc = adafruit_tlc5947.TLC5947(spi_1, digitalio.DigitalInOut(LED_LAT))
for i in range(19):
    led_tlc[i] = 0
for i in range(19):
    time.sleep(0.5)
    led_tlc[i] = 4095
for i in range(19):
    led_tlc[i] = 0
time.sleep(0.1)
for i in range(19):
    led_tlc[i] = 4095

# Code for using rollovers to calculate score
score = 0
while True:
    for i,ldr in enumerate(ldr_adcs):
        if ldr.voltage > ldr_adc_defaults[i] + 0.75:
            score += 100
            print(i,ldr.voltage)
            print(score)
            cross_lights()
            if i == 0:
                if dd2_servo.angle == 10:
                    time.sleep(1)
                    dd1_servo.angle = 70
                    dd2_servo.angle = 70
                elif dd1_servo.angle == 10:
                    dd2_servo.angle = 10

                else:
                    dd1_servo.angle = 10
