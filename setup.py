from microdot_asyncio import Microdot, Response
from machine import Pin, Timer, I2C
import display, motor, wifi, calibration, menu, presets
import utime
import os, sys
import uasyncio as asyncio
# import writer
# import freesans20
# import firacodeBold30
import json
import _thread
sLock = _thread.allocate_lock()

print("====================================")
print(sys.implementation[0], os.uname()[3],
      "\nrun on", os.uname()[4])
print("====================================")

try:    
    state = open("state.json","r")
    state_json = json.loads(state.read())
    current_encoder = state_json["current_encoder"]
#     print(current_encoder)
except:
    file=open("state.json","w")
    file.write(json.dumps({"current_encoder":0}))
    current_encoder = 0
  
#relay for motor
relay1 = Pin(0, Pin.OUT)
relay2 = Pin(1, Pin.OUT)
  
motorO = motor.Motor(relay1, relay2,current_encoder,sLock)
motorO.stop_motor()

app = Microdot()



#buttons
up_button = Pin(14, Pin.IN, Pin.PULL_UP)#up
down_button = Pin(15, Pin.IN, Pin.PULL_UP)#down
one_button = Pin(10, Pin.IN, Pin.PULL_UP)#1
two_button = Pin(11, Pin.IN, Pin.PULL_UP)#2
three_button = Pin(13, Pin.IN, Pin.PULL_UP)#3

#rotary encoders
#encoder 1 (interface)
button_pin = Pin(21, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(17, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(18, Pin.IN, Pin.PULL_UP)
#encoder 2 (motor position) - no need for switch
outA = Pin(26, mode=Pin.IN) # Pin CLK of encoder 2
outB = Pin(27, mode=Pin.IN) # Pin DT of encoder 2




# oled display init

displayO = display.Display(128,64,1,7,6)
asyncio.sleep(2)
print("initi displayO")
menuO = menu.Menu(displayO)
print("initi menuO")
wifiO = wifi.Wifi(app,sLock,displayO,menuO)
print("initi wifiO")
calibrationO = calibration.Calibration(displayO,motorO,sLock,wifiO.wifi)
print("initi calibrationO")
presetsO = presets.Presets(motorO,calibrationO,sLock)
print("initi presetsO")

# oled = displayO.init()
# font_writer = writer.Writer(oled, freesans20)


#TODO change here 
# wifiO.start_connection()



#display
# line = 1 
# highlight = 1
# shift = 0
# list_length = 0
# total_lines = 5
# line_height = 10
# # for tracking the direction and button state
# previous_value = True
# button_down = False
# value = 0
# 
# #for entering min max table height

# min_height = 0
# _10 = False
# _100 = False
# #state to enable/disable motor
# disable_motor = False

# Read the last state of CLK pin in the initialisaton phase of the program 
# outA_last = outA.value()