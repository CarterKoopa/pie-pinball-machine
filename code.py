import busio
import digitalio
import time
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_tlc5947

# Define Pins
FL_0 = board.GP0    # Flipper Left
FR_0 = board.GP1    # Flipper Right
SL_0 = board.GP2    # Slingshot Left
SR_0 = board.GP3    # Slingshot Right
FBL_0 = board.GP4   # Flipper Button Left
FBR_0 = board.GP5   # Flipper Button Right
SDU_IO_SDA = board.GP6
SDU_IO_SCL = board.GP7
SPI_MISO = board.GP8    # SPI MISO
LDR_ADC_CS = board.GP9  # MCP3008 Chip Select
SPI_CLK = board.GP10    # SPI Clock
SPI_MOSI = board.GP11   # SPI MOSI
LED_LAT = board.GP12    # LED Latch

spi = busio.SPI(clock=SPI_CLK, MOSI=SPI_MOSI, MISO=SPI_MISO)

# Set Up Rollovers
## Set Up MCP3008
ldr_adc_cs = digitalio.DigitalInOut(LDR_ADC_CS)
mcp3008 = MCP.MCP3008(spi, ldr_adc_cs)

## Calibrate LDRs
ldr_adc = []
for channel in range(8):
    ldr_adc.append(AnalogIn(mcp3008, channel))
### Create Default Light Voltages
ldr_adc_defaults = []
for channel in ldr_adc:
    ldr_adc_defaults.append(channel.voltage)
print("Default Voltages: " + str(ldr_adc_defaults))

# Set up LEDs
## Set Up TLC5947
led_lat = digitalio.DigitalInOut(LED_LAT)
tlc5947 = adafruit_tlc5947.TLC5947(spi, led_lat)

## Define LED Pins
red = tlc5947.create_pwm_out(0)
green = tlc5947.create_pwm_out(6)
blue = tlc5947.create_pwm_out(11)


# Code for controlling LEDs based on light levels
while True:
    if ldr_adc[0].voltage < 1:
        red.duty_cycle = 65535
        green.duty_cycle = 0
        blue.duty_cycle = 0
    elif ldr_adc[0].voltage > 2:
        red.duty_cycle = 0
        green.duty_cycle = 65535
        blue.duty_cycle = 0
    else:
        red.duty_cycle = 0
        green.duty_cycle = 0
        blue.duty_cycle = 65535
    time.sleep(1)
