from microdot_asyncio import Microdot, Response
from machine import Pin, Timer, I2C, PWM, ADC
import display, motor, wifi, calibration, menu, presets, buzz_vib, songs, accelerometer, acs712, dev.collision as collision
from rtttl import RTTTL
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

#current sensor
#TODO 2.29 for usb (dev) and 1.65 for pico (prod)
# 66 for 30A, 100 for 25A and 185 for 5A sensor
curr_sens = acs712.ACS712(adc_pin=28, sensitivity=66, aref=3.3, default_output_voltage=2.29, error=0.12)
print("initi current ")
#collision detection
# cd_i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
# detector  = collision.CollisionDetector(cd_i2c)
# print("initi collision detection")
#accelerometer
accelO = accelerometer.Accelerometer(sda=Pin(6),scl=Pin(7),freq=400000)
print("initi accelerometer")

#bridge for motor
r_pwm_pin = 0
l_pwm_pin = 1
pwm1 = PWM(Pin(r_pwm_pin, Pin.OUT)) #R_PWM SDA
pwm2 = PWM(Pin(l_pwm_pin, Pin.OUT)) #L_PWM SCL


duty = 0
pwm1.freq(16000)
pwm1.duty_u16(duty)
pwm2.freq(16000)
pwm2.duty_u16(duty)
motorO = motor.Motor(pwm1, pwm2,current_encoder,sLock,accelO,curr_sens)
motorO.stop_motor()
print("initi motor")



app = Microdot()



#buttons
down_button = Pin(26, Pin.IN, Pin.PULL_UP)#down
up_button = Pin(27, Pin.IN, Pin.PULL_UP)#up
one_button = Pin(9, Pin.IN, Pin.PULL_UP)#1
two_button = Pin(10, Pin.IN, Pin.PULL_UP)#2
three_button = Pin(11, Pin.IN, Pin.PULL_UP)#3

#rotary encoders
#encoder 1 (interface)
button_pin = Pin(13, Pin.IN, Pin.PULL_UP) #scl
direction_pin = Pin(15, Pin.IN, Pin.PULL_UP) #SCL clk
step_pin  = Pin(14, Pin.IN, Pin.PULL_UP) # sdda dt
#encoder 2 (motor position) - no need for switch
outA = Pin(20, mode=Pin.IN) # Pin CLK of encoder 2 #sda
outB = Pin(21, mode=Pin.IN) # Pin DT of encoder 2 #scl

#buzzer + vibrator
buzzer = PWM(Pin(22))
volume=1000
vibrat = Pin(16, Pin.OUT)

buzzvibO = buzz_vib.Buzzer(buzzer, vibrat, volume, sLock)
print("initi buzzvibO")






# oled display init
sLock.acquire()
displayO = display.Display(128,64,0,5,4,buzzvibO)
sLock.release()
print("initi displayO")
menuO = menu.Menu(displayO)
print("initi menuO")
wifiO = wifi.Wifi(app,sLock,displayO,menuO)
print("initi wifiO")
calibrationO = calibration.Calibration(displayO,motorO,sLock,wifiO.wifi,wifiO.aps)
print("initi calibrationO")
collisionO = collision.Collision(motorO,calibrationO)
print("initi collisionO")
displayO.reminder_time = calibrationO.reminder_time
displayO.start_time = utime.ticks_ms()
presetsO = presets.Presets(motorO,calibrationO,sLock)
print("initi presetsO")
# led = Pin("LED", Pin.OUT)
# led.off()
# led.on()
# print("initi all done")


