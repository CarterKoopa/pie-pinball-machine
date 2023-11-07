import busio
import digitalio
import time
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Define Pins
FL_0 = board.GP0    # Flipper Left
FR_0 = board.GP1    # Flipper Right
LDR_ADC_CLK = board.GP2   # MCP3008 Clock
LDR_ADC_MOSI = board.GP3    # MCP3008 MOSI
LDR_ADC_MISO = board.GP4    # MCP3008 MISO
LDR_ADC_CS = board.GP5  # MCP3008 Chip Select
SL_0 = board.GP6    # Slingshot Left
SR_0 = board.GP7    # Slingshot Right
FBL_0 = board.GP8   # Flipper Button Left
FBL_0= board.GP9    # Flipper Button Right

# Set Up Rollovers

## Set Up MCP3008
ldr_adc_spi = busio.SPI(clock=LDR_ADC_CLK, MOSI=LDR_ADC_MOSI, MISO=LDR_ADC_MISO)
ldr_adc_cs = digitalio.DigitalInOut(LDR_ADC_CS)
mcp3008 = MCP.MCP3008(ldr_adc_spi, ldr_adc_cs)

## Calibrate LDRs
ldr_adc = []
for channel in range(8):
    ldr_adc.append(AnalogIn(mcp3008, channel))
### Create Default Light Voltages
ldr_adc_defaults = []
for channel in ldr_adc:
    ldr_adc_defaults.append(channel.voltage)
print("Default Voltages: " + str(ldr_adc_defaults))
