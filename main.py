"""
author: waliori
"""
# from machine import WDT

from setup import *
import _thread
from abutton import Pushbutton
import uasyncio
from time import time
import machine
# import math
print("==============")
print("imports done")

# wdt = WDT(timeout=8388)  # enable it with a timeout of 2s
# Motor Section
#TODO modifier go height to calculate current height + wanted height < max
#TODO add acceleration + position to know if impact        
current_m = ".."
menu_list = ["..", "WiFi","Configuration", "Lock Unlock", "Show Presets", "Show min/max", "Collision Reset", "Factory Reset"]
conf_menu = ["Go back","Sleep after","Set min/max", "Stand reminder","Vibration", "Sound"]
sound_menu = ["Back to Conf","On/Off","Melodies"]
menu = ["Back to Wifi","Connect","Forget"]
mm = ["Back to Conf","Min","Max"]
chosen_wf = ""



pb_up = Pushbutton(up_button, suppress=True)
pb_down = Pushbutton(down_button, suppress=True)
pb_switch = Pushbutton(button_pin, suppress = True)

pb_one = Pushbutton(one_button, suppress=True)
pb_two = Pushbutton(two_button, suppress=True)
pb_three = Pushbutton(three_button, suppress=True)

# timeo = 0
start_tm = time()
start_tm_rem = time()

button_pressed = False
current_melody_id = None

loop = asyncio.get_event_loop()

print("initial setup done -------")
def move_motor(button,calibration=False):
    motorO.move_motor(button,up_button,outA,outB,calibrationO.min_encoder, calibrationO.max_encoder, calibration )          
            
                       
# Menu handeling Section

def show_menu(menu):
    sLock.acquire()      
    menuO.menu_state = True
    menuO.reset_state = False
    menuO.presets_state = False
    calibrationO.system_idle = False
    line = 1
    displayO.show_menu(menu, line, menuO.highlight, menuO.shift,menuO.total_lines,"Menu",wifiO.wifi,wifiO.aps)
    sLock.release()
    
def disconnect():
    wifiO.disconnect()
    go_home()
    
def forget_wf(wifi):
    sLock.acquire()
    displayO.oled.fill(0)
    displayO.show_header(wifi,wifiO.wifi,wifiO.aps)
    displayO.show_frame()
    displayO.text_frame(f"Forget {wifi}, do you confirm?")
    menuO.forget_w_state = True
    menuO.wc_state = False
    menuO.wc_c_state = False
    sLock.release()
    
def forget_wifi(wifi):
#     print(wifi)
    wifiO.forget_wifi(wifi)
    go_home()
    
def connect_c_wifi(wifi):
#     sLock.acquire()
    connected = wifiO.connect(wifi,wifiO.saved_json[wifi])
#     sLock.release()
    if connected:
        toggle_server(loop,'start')
        go_home()
    else:
        displayO.oled.fill(0)
        displayO.show_frame()
        menuO.presets_state = True
        menuO.menu_state = False
        calibrationO.system_idle = False
        displayO.text_frame("Could not connect, try again")
        displayO.show_header("WiFi",wifiO.wifi,wifiO.aps)
        displayO.oled.show()
        asyncio.sleep(10)
        wifi_menu()

def set_sleep():
    sLock.acquire()
    menuO.slp_state = True
    menuO.rem_state =False
    preset_list = ["Turn KNOB to", "set time sleep"]
    displayO.show_static_frame(preset_list,len(preset_list))
    displayO.show_header("Sleep",wifiO.wifi,wifiO.aps)
    displayO.oled.show()
    sLock.release()
    
def stand_rem():
    sLock.acquire()
    menuO.rem_state = True
    menuO.slp_state =False
    preset_list = ["Turn KNOB to", "set posture reminder"]
    displayO.show_static_frame(preset_list,len(preset_list))
    displayO.show_header("Reminder",wifiO.wifi,wifiO.aps)
    displayO.oled.show()
    sLock.release()
    
def config_menu():
    global conf_menu
    menuO.highlight = 1
    menuO.menu_state = False
    calibrationO.system_idle = False
    sLock.acquire()    
    line = 1    
    displayO.oled.fill(0)
    displayO.show_frame()
    menuO.cf_state = True #mimic menustate
    menuO.cf_h_state = False
    menuO.cf_s_state = False
    menuO.wc_state = False
    menuO.wc_c_state = False
    menuO.s_w_state = False
    menuO.presets_state = False
    displayO.show_menu(conf_menu, line, menuO.highlight, menuO.shift,min(len(conf_menu),menuO.total_lines),"Config",wifiO.wifi,wifiO.aps)
    sLock.release()

def wifi_menu():
    menuO.highlight = 1
    menuO.menu_state = False
    calibrationO.system_idle = False
    sLock.acquire()    
    line = 1    
    displayO.oled.fill(0)
    displayO.show_frame()
    if wifiO.saved_json:
        menuO.wc_state = True #mimic menustate
        menuO.wc_c_state = False
        menuO.s_w_state = False
        menuO.cf_state = False
        menuO.presets_state = False
        wifiO.nearby_wifis()
        displayO.show_menu(wifiO.nearby, line, menuO.highlight, menuO.shift,min(len(wifiO.nearby),menuO.total_lines),"Wifi",wifiO.wifi,wifiO.aps)
    else:
        menuO.presets_state = True
        displayO.text_frame("Start AP, PicoW:waliori123 then visit 192.168.4.1")
        displayO.show_header("WiFi",wifiO.wifi,wifiO.aps)
        displayO.oled.show()
    sLock.release()

def connect_wifi():
    menuO.highlight = 1
    menuO.menu_state = False
    calibrationO.system_idle = False
    line = 1    
    displayO.oled.fill(0)
    displayO.show_frame()
    if wifiO.saved_json:
        menuO.wc_state = True #mimic menustate
        menuO.wc_c_state = False #mimic menustate
        menuO.cf_state = False
        menuO.s_w_state = False
        menuO.presets_state = False
        displayO.show_menu(wifiO.nearby, line, menuO.highlight, menuO.shift,min(len(wifiO.nearby),menuO.total_lines),"Wifi",wifiO.wifi,wifiO.aps)
    else:
        menuO.presets_state = True
        displayO.text_frame("Connect to PicoW:waliori123 then visit 192.168.4.1")
        displayO.show_header("WiFi",wifiO.wifi,wifiO.aps)
        displayO.oled.show()

#     menuO.wc_state = True #mimic menustate

#     menuO.presets_state = True


def c_wifi(wifi):
    global menu, chosen_wf
    menuO.highlight = 1
    menuO.wc_c_state = True #mimic menustate
    menuO.wc_state = False
    menuO.s_w_state = False
    menuO.cf_state = False
    menuO.presets_state = False
    chosen_wf = wifi
    line = 1  
    displayO.oled.fill(0)
    displayO.show_frame()  
    displayO.show_menu(menu, line, menuO.highlight, menuO.shift,min(len(menu),menuO.total_lines),wifi,wifiO.wifi,wifiO.aps)



async def a_c_melody(melody,melody_id):
    global button_pressed
    buzzvibO.play_tone(0, 0)
    if melody != "Back to Sounds":
        tune = RTTTL(songs.find(melody))
        try:
            buzzvibO.stop_flag = False
            button_pressed = False
            for freq, msec in tune.notes():
                if melody_id != current_melody_id or button_pressed or buzzvibO.stop_flag:
                    buzzvibO.play_tone(0, 0)  # Stop playing
                    break
                buzzvibO.play_tone(freq, msec)
                await asyncio.sleep(msec / 30000)  # Yield control to the event loop
        except KeyboardInterrupt:
            buzzvibO.play_tone(0, 0)


def c_melody(melody):
    global loop, current_melody_id
    melody = melody.replace("-> ", "")
    current_melody_id = id(melody)
    loop.create_task(a_c_melody(melody,current_melody_id))

    
def ch_melody(melody):    
    buzzvibO.set_song(melody)
    sound_m()                                                                                                                                                                               

    
def go_home():    
    sLock.acquire()
    buzzvibO.play_tone(0, 0)
    buzzvibO.stop()
    calibrationO.system_idle = True
    menuO.s_w_state = False
    menuO.wc_state = False
    menuO.wc_c_state = False
    menuO.cf_state = False
    menuO.cf_h_state=False
    menuO.cf_s_state = False
    menuO.cf_mel_state = False
    menuO.min_state = False
    menuO.max_state = False
    menuO.presets_state = False
    menuO.slp_state=False
    menuO.forget_w_state = False
    menuO.rem_state = False    
    menuO.go_home(wifiO.wifi,wifiO.aps,calibrationO.real_height,motorO.counter)
    sLock.release()

    
def go_back():
    global current_m, menu_list
#     print(current_m)
    if current_m in ["Show IP","Back to Wifi"]:
        current_m = "WiFi"
        wifi_menu()
    elif current_m in ["WiFi","Lock Unlock", "Show Presets", "Show min/max", "Collision Reset", "Factory Reset","Configuration","Go back"]:
        show_menu(menu_list)
    elif current_m in ["Sleep after","Back to Conf", "Vibration"]:
        current_m = "Configuration"
        config_menu()    
    elif current_m == "..":
        go_home()

def stop_ap():
    wifiO.stop()
    go_home()

def start_ap():#when up and restart cannot connect wifi 
    displayO.clear_frame()
    displayO.text_frame("Connect to PicoW:waliori123 then visit 192.168.4.1")
    utime.sleep(2)
    go_home()
    loop.create_task(wifiO.apserver(calibrationO.real_height,motorO.counter))

def list_saved_wifi():
    menuO.highlight = 1
    menuO.s_w_state = True
    menuO.wc_state = False
    menuO.wc_c_state = False
    saved_wifis = wifiO.saved_json
    w_l = list(saved_wifis.keys())
    print(w_l,wifiO.ssid)
    if wifiO.wlan.isconnected():
        w_l[w_l.index(wifiO.ssid)] = f"->{wifiO.ssid}"
    line = 1  
    displayO.oled.fill(0)
    displayO.show_frame()  
    displayO.show_menu(w_l, line, menuO.highlight, menuO.shift,min(len(w_l),menuO.total_lines),"Wifis",wifiO.wifi,wifiO.aps)
    
def set_minmax():
    sLock.acquire()
    global mm
    menuO.highlight = 1
    menuO.cf_h_state =True
    menuO.cf_state = False    
    line = 1  
    displayO.oled.fill(0)
    displayO.show_frame()  
    displayO.show_menu(mm, line, menuO.highlight, menuO.shift,min(len(mm),menuO.total_lines),"min/max",wifiO.wifi,wifiO.aps)
    sLock.release()

def min_m():
    sLock.acquire()
    menuO.min_state = True
    menuO.max_state = False
    preset_list = ["Turn KNOB to", "set min height"]
    displayO.show_static_frame(preset_list,len(preset_list))
    displayO.show_header("Min",wifiO.wifi,wifiO.aps)
    displayO.oled.show()
    sLock.release()
    
def set_min(height):
    menuO.min_state = False
    calibrationO.set_min(height)
    set_minmax()

def set_max(height):
    menuO.max_state = False
    calibrationO.set_max(height)
    set_minmax()
    
def max_m():
    sLock.acquire()
    menuO.max_state = True
    menuO.min_state = False
    preset_list = ["Turn KNOB to", "set max height"]
    displayO.show_static_frame(preset_list,len(preset_list))
    displayO.show_header("Max",wifiO.wifi,wifiO.aps)
    displayO.oled.show()
    sLock.release()

def toggle_vibration():
    sLock.acquire()
    buzzvibO.toggle_vibration()  # Toggle vibration state
    displayO.oled.fill(0)
    
    if buzzvibO.vibration:
        buzzvibO.vibrat.value(1)  # Vibrate when vibration is on
        lock = ["Vibration", "ON"]
    else:
        buzzvibO.vibrat.value(0)
        lock = ["Vibration", "OFF"]

    displayO.show_frame()
    displayO.show_static_frame(lock, len(lock))
    utime.sleep(1)
    buzzvibO.vibrat.value(0)
    sLock.release()
    displayO.oled.fill(0)
    config_menu()

def toggle_sound():
    sLock.acquire()
    menuO.cf_st_state =True 
    buzzvibO.toggle_sound()  # Toggle vibration state
    displayO.oled.fill(0)
    
    if buzzvibO.sound:
        buzzvibO.buzzer.duty_u16(440)  # Vibrate when vibration is on
        lock = ["Sound", "ON"]
    else:
        buzzvibO.buzzer.duty_u16(0)
        lock = ["Sound", "OFF"]

    displayO.show_frame()
    displayO.show_static_frame(lock, len(lock))
    utime.sleep(1)
    buzzvibO.buzzer.duty_u16(0)
    sLock.release()
    displayO.oled.fill(0)
    sound_m()
    
    
   
def sound_m():
#     sLock.acquire() 
    menuO.highlight = 1
    menuO.shift = 0
    menuO.cf_s_state =True
    menuO.cf_state = False
    menuO.cf_mel_state = False
    menuO.cf_st_state =False
    line = 1  
    displayO.oled.fill(0)
    displayO.show_frame()  
    displayO.show_menu(sound_menu, line, menuO.highlight, menuO.shift,min(len(sound_menu),menuO.total_lines),"Sound",wifiO.wifi,wifiO.aps)
#     sLock.release() 
#     toggle_sound()
   
   
def melodies_m():
    global button_pressed
    button_pressed = False
    menuO.highlight = 1
    menuO.shift = 0
    menuO.cf_mel_state =True   
    line = 1  
    displayO.oled.fill(0)
    displayO.show_frame()

    displayO.show_menu(buzzvibO.songs, line, menuO.highlight, menuO.shift,min(len(buzzvibO.songs),menuO.total_lines),"Melodies",wifiO.wifi,wifiO.aps)

def toggle_api():
    sLock.acquire()
    displayO.oled.fill(0)
    if wifiO.server:
        lock = ["API", "Off"]
        loop.create_task(wifiO.serve("stop"))
    else:
        lock = ["API", "On"]
        loop.create_task(wifiO.serve("start"))
    displayO.show_frame()
    displayO.show_static_frame(lock, len(lock))    
    utime.sleep(1)    
    sLock.release()
    displayO.oled.fill(0)
    wifi_menu()


def launch(item):
    global current_m, chosen_wf, button_pressed
    button_pressed = True
    current_m = item

    actions = {
        "..": go_home,
        "Show Presets": show_presets,
        "Factory Reset": confirm_reset,
        "Show min/max": show_calibration,
        "Show IP": show_ip,
        "Lock Unlock": lock_unlock,
        "WiFi": wifi_menu,
        "Collision Reset": confirm_reset_collision,
        "Disconnect": disconnect,
        "Scan again": wifi_menu,
        "Go back": go_back,
        "Back to Wifi": go_back,
        "Configuration": config_menu,
        "Sleep after": set_sleep,
        "Start AP": start_ap,
        "Stop AP": stop_ap,
        "Connect": connect_c_wifi,
        "Forget": forget_wf,
        "Saved WiFi": list_saved_wifi,
        "Set min/max": set_minmax,
        "Back to Conf": go_back,
        "Min": min_m,
        "Max": max_m,
        "Stand reminder": stand_rem,
        "Vibration": toggle_vibration,
        "Sound": sound_m,
        "On/Off": toggle_sound,
        "Melodies": melodies_m,
        "Toggle API": toggle_api
    }

    def extend_actions(prefix, keys, action):
        for key in keys:
            actions[prefix + key] = lambda item=key: action(item)

    if wifiO.saved_json:
        keys = list(wifiO.saved_json.keys())
        extend_actions("", keys, c_wifi)
        extend_actions("->", keys, c_wifi)

    extend_actions("", buzzvibO.songs, ch_melody)
    extend_actions("->", buzzvibO.songs, ch_melody)

    def default_action(): 
        print("No action defined for this item")

    action = actions.get(item, default_action)
    
    special_cases = ["Connect", "Forget"]
    if item in special_cases:
        action(chosen_wf)
    else:
        action()
    



# real height facilitator adding 10s and 100s when rotating the rotary encoder
def toggle_01():
    sLock.acquire()
    calibrationO._01 = False if calibrationO._01 else True
    calibrationO._100 = False
    calibrationO._10 = False
    sLock.release()

def toggle_10():
    sLock.acquire()
    calibrationO._10 = False if calibrationO._10 else True
    calibrationO._100 = False
    calibrationO._01 = False
    sLock.release()
        
def toggle_100():
    sLock.acquire()
    calibrationO._100 = False if calibrationO._100 else True
    calibrationO._10 = False
    calibrationO._01 = False
    sLock.release()

# presets

def go_to_preset(preset):
    if presetsO.get_preset(preset):
        p = presetsO.get_preset(preset)
        if p >= calibrationO.min_encoder and p <= calibrationO.max_encoder:
            presetsO.go_preset(outA, outB, p)
            return True
        return False
    return False

def set_preset(preset):
    presetsO.set_preset(preset)
    sLock.acquire()
    displayO.clear_frame()
    preset_list = [f"Preset {preset} set to", "",f"{str(calibrationO.real_height(motorO.counter))}"]
    displayO.show_static_frame(preset_list,len(preset_list))  
    displayO.oled.show()      
    utime.sleep(2)
    sLock.release()
                


        
# miscs

# @micropython.native    
def disable_button():
    pass

# @micropython.native  
def confirm_reset():
    sLock.acquire()
    displayO.oled.fill(0)
    displayO.show_header("F Reset",wifiO.wifi,wifiO.aps)
    displayO.show_frame()
    displayO.text_frame("All seetings and presets will be wiped, do you confirm?")
    menuO.reset_state = True
    menuO.menu_state = False
    calibrationO.system_idle = False
    sLock.release()

def confirm_reset_collision():
    sLock.acquire()
    displayO.oled.fill(0)
    displayO.show_header("C Reset",wifiO.wifi,wifiO.aps)
    displayO.show_frame()
    displayO.text_frame("Collision settings will be wiped, do you confirm?")
    menuO.collision_reset_state = True
    menuO.menu_state = False
    calibrationO.system_idle = False
    sLock.release()
    
def reset_collision():
    menuO.collision_reset_state = False
    menuO.menu_state = False
    calibrationO.system_idle = False
    calibrationO.collision_reset_state = True
    encoder_value = calibrationO.min_encoder+10
    motorO.move_motor_height("down",outA, outB, encoder_value)
    sLock.acquire()
    displayO.clear_frame()
    displayO.text_frame("Go to HIGHEST position then to LOWEST, then confirm")
    sLock.release()


        
        
        
# @micropython.native    
def factory_reset():
    sLock.acquire()
    try:
        os.remove("settings.json")
    except:
        print("File not found")
    try:
        os.remove("state.json")
    except:
        print("File not found")
    try:
        os.remove("presets.json")
    except:
        print("File not found")
    try:
        os.remove("saved_wifi.json")
    except:
        print("File not found")
    try:
        os.remove("s_v.json")
    except:
        print("File not found")
    machine.reset()
    sLock.release()


# @micropython.native
def show_presets():    
    sLock.acquire()
    menuO.presets_state = True
    menuO.menu_state = False
    calibrationO.system_idle = False
    motorO.api = False
    presets = presetsO.presets
    displayO.oled.fill(0)
    displayO.show_frame()
    if not presets:
        displayO.text_frame("There are no preset settings in place yet.")
    else:
        preset_list = ["{}: {}".format(k, calibrationO.real_height(v)) for k, v in presets.items()]
        displayO.show_static_frame(preset_list,len(preset_list))
        displayO.show_header("Presets",wifiO.wifi,wifiO.aps)
        displayO.oled.show()
    sLock.release()
    
# @micropython.native    
def show_calibration():    
    sLock.acquire()
    menuO.presets_state = True
    menuO.menu_state = False
    calibrationO.system_idle = False
    motorO.api = False
    min_max = ["Min: {}".format(calibrationO.min_real), "Max: {}".format(calibrationO.max_real)]
    displayO.oled.fill(0)
    displayO.show_frame()
    displayO.show_static_frame(min_max,len(min_max))
    displayO.show_header("Min/Max",wifiO.wifi,wifiO.aps)
    displayO.oled.show()
    sLock.release()
    
# @micropython.native
def show_ip():
#     sLock.acquire()
    menuO.presets_state = True
    menuO.wc_state = False
    menuO.wc_c_state = False
    menuO.menu_state = False
    calibrationO.system_idle = False
    motorO.api = False
    if wifiO.wlan.isconnected():
        ip = ["IP address: ",wifiO.wlan.ifconfig()[0]]
    else:
        ip = ["IP address: ","Not connected!"]
    displayO.oled.fill(0)
    displayO.show_frame()
    displayO.show_static_frame(ip,len(ip))
    displayO.show_header("IP",wifiO.wifi,wifiO.aps)
    displayO.oled.show()
#     sLock.release()
    

# @micropython.native   
def lock_unlock():
    sLock.acquire()
    menuO.presets_state = True
    menuO.menu_state = False
    calibrationO.system_idle = False
    motorO.api = False
    if not displayO.lock_state:
        displayO.lock_state = True
        lock = ["Table Locked!"]
    else:
        displayO.lock_state = False
        lock = ["Table Unlocked!"]
    displayO.oled.fill(0)
    displayO.show_frame()
    displayO.show_static_frame(lock,len(lock))
    displayO.show_header("(Un)Lock",wifiO.wifi,wifiO.aps)
    displayO.oled.show()
    sLock.release()   



def awake():
    sLock.acquire()
    global start_tm
    displayO.wake()
    start_tm = time()
    if time() - start_tm >= calibrationO.sleep_time:
        go_home()
    sLock.release()                                                                                                                                              

def stp_rem():
    buzzvibO.stop()
    sLock.acquire()
    global start_tm_rem
    displayO.stp_alarm()
    displayO.start_time = utime.ticks_ms()
    start_tm_rem = time()
    if time() - start_tm_rem >= calibrationO.reminder_time:
        go_home()
    sLock.release()
    
def handle_button(fc,args):
    awake()
    stp_rem()
    fc(*args)
    global start_tm, start_tm_rem
    start_tm = time()
    start_tm_rem = time()
    

def set_sleep_value(sleep_value):
    menuO.slp_state=False
    if sleep_value == 0 or sleep_value == 86400:
        sleep_value = sys.maxsize
    calibrationO.sleep_time = sleep_value
    sLock.acquire()
    with open("settings.json","r") as file:
        settings_json = json.loads(file.read())
        settings_json["sleep_time"] = sleep_value
    with open("settings.json","w") as file:
        file.write(json.dumps(settings_json))
    sLock.release()
    displayO.clear_frame()
    preset_list = ["Done!", "Table will sleep", f"after: {displayO.seconds_to_timestamp(sleep_value)}"]
    displayO.show_static_frame(preset_list,len(preset_list))  
    displayO.oled.show()      
    utime.sleep(2)
    displayO.oled.fill(0)
    config_menu()

def set_rem_value(rem_value):
    menuO.rem_state=False
    if rem_value == 0 or rem_value == 86400:
        rem_value = sys.maxsize
    calibrationO.reminder_time = rem_value
    displayO.reminder_time = rem_value
    sLock.acquire()
    with open("settings.json","r") as file:
        settings_json = json.loads(file.read())
        settings_json["reminder_time"] = rem_value
    with open("settings.json","w") as file:
        file.write(json.dumps(settings_json))
    sLock.release()
    displayO.clear_frame()
    preset_list = ["Done!", "Change Posture", f"in: {displayO.seconds_to_timestamp(rem_value)}"]
    displayO.show_static_frame(preset_list,len(preset_list))  
    displayO.oled.show()      
    utime.sleep(2)
    displayO.oled.fill(0)
    config_menu()
    


async def alarm():
    tune = RTTTL(songs.find(buzzvibO.melody))
    try:
        x=True
        buzzvibO.stop_flag = False
        
        for freq, msec in tune.notes():
            displayO.show_reminder_frame()
            displayO.oled.invert(x)
            x=not x
            if buzzvibO.stop_flag:
                buzzvibO.play_tone(0, 0)
                break
            buzzvibO.play_tone(freq, msec)
    except KeyboardInterrupt:
        buzzvibO.play_tone(0, 0)


# @micropython.native
def task_display_navigation():
    global menu_list, start_tm, start_tm_rem, conf_menu, menu, chosen_wf, mm
    height_value = 0
    height_previousValue = 1
    min_height_value = calibrationO.min_real
    min_height_previousValue = calibrationO.min_real+1
    max_height_value = calibrationO.max_real
    max_height_previousValue = calibrationO.max_real+1
    speed_value = 0
    speed_previousValue = 1
    sleep_value = calibrationO.sleep_time
    sleep_previousValue = calibrationO.sleep_time+1
    rem_value = calibrationO.reminder_time
    rem_previousValue = calibrationO.reminder_time+1    
#     x=True
    while True:
        
        sLock.acquire()

        # not calibrated and not semi calibrated and not idle (AKA first boot of the system)
        if not calibrationO.enc_calib and not calibrationO.max_enc_set and not calibrationO.system_idle and not calibrationO.speed_calib:
            if motorO.is_moving():                
                motorO.update_pca()
            pb_up.press_func(move_motor, (up_button,True))
            pb_down.press_func(move_motor, (down_button,True))#TODO mayber remove ability to go down            
            pb_switch.release_func(calibrationO.set_max_enc, ())            
#             motorO.update_pca()
        # not calibrated but semi calibrated and not idle (highest point set) 
        elif not calibrationO.enc_calib and  calibrationO.max_enc_set and not calibrationO.system_idle and not calibrationO.speed_calib:
            # not real semi calibrated ()
            if not calibrationO.max_real_set:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_one.press_func(toggle_01, ())
                pb_two.press_func(toggle_10, ())
                pb_three.press_func(toggle_100, ())
                pb_switch.release_func(calibrationO.set_max_real, (height_value,))                
                if height_previousValue != step_pin.value():
                    if step_pin.value() == False:
                        if direction_pin.value() == True:
                            if height_value > 0:
                                if calibrationO._01:
                                    height_value = max(height_value-0.1, 0)
                                elif calibrationO._10:
                                   height_value = max(height_value - 10, 0)
                                elif calibrationO._100:
                                    height_value = max(height_value - 100, 0)
                                else:
                                    height_value  = max(height_value - 1, 0)
                        else:
                            if calibrationO._01:
                                height_value +=0.1
                            elif calibrationO._10:
                               height_value +=10
                            elif calibrationO._100:
                                height_value +=100
                            else:
                                height_value +=1
                        displayO.show_height_frame(str(round(height_value,1)),0)
                    height_previousValue = step_pin.value()
                    utime.sleep_ms(1)
            # real semi calibrated done
            # TODO verify if else works
            elif calibrationO.max_real_set:
                if motorO.is_moving():
                    motorO.update_pca()
                pb_up.press_func(move_motor, (up_button,True))
                pb_down.press_func(move_motor, (down_button,True))
                pb_switch.release_func(calibrationO.set_min_enc, ())
                #motorO.update_pca()
        # if calibrated and max_enc_set and not idle (Highest point Done, starting lower)
        elif calibrationO.enc_calib and  calibrationO.max_enc_set and not calibrationO.system_idle and not calibrationO.speed_calib:
            # calibrated but not real calibrated 
            if not calibrationO.real_calib:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_one.press_func(toggle_01, ())
                pb_two.press_func(toggle_10, ())
                pb_three.press_func(toggle_100, ())
                pb_switch.release_func(calibrationO.set_min_real, (height_value,))
                if height_previousValue != step_pin.value():
                    if step_pin.value() == False:
                        if direction_pin.value() == True:
                            if height_value > 0:
                                if calibrationO._01:
                                    height_value = max(height_value-0.1, 0)
                                elif calibrationO._10:
                                   height_value = max(height_value - 10, 0)
                                elif calibrationO._100:
                                    height_value = max(height_value - 100, 0)
                                else:
                                    height_value  = max(height_value - 1, 0)
                        else:
                            if calibrationO._01:
                                height_value +=0.1
                            elif calibrationO._10:
                               height_value +=10
                            elif calibrationO._100:
                                height_value +=100
                            else:
                                height_value +=1
                        displayO.show_header("Setup",wifiO.wifi,wifiO.aps)
                        displayO.show_height_frame(str(round(height_value,1)),0)
                    height_previousValue = step_pin.value()
                    utime.sleep_ms(1)
                    
        if motorO.is_moving() and not motorO.slowing:
            print(f"{collisionO.detect_obstacle(motorO.direction,[motorO.avg_xyz[0],motorO.avg_xyz[1],motorO.avg_xyz[2],motorO.avg_rpm,motorO.current_threshold])}")
#             print(f"{motorO.avg_xyz}")
#             sensor_data = [motorO.avg_xyz[0],motorO.avg_xyz[1],motorO.avg_xyz[2],motorO.avg_rpm,motorO.current_threshold]
#             direction = motorO.direction
#             print(f"{motorO.direction}")
#             print(f"{[motorO.avg_xyz[0],motorO.avg_xyz[1],motorO.avg_xyz[2],motorO.avg_rpm,motorO.current_threshold]}")
#             if collisionO.detect_obstacle(motorO.direction,[motorO.avg_xyz[0],motorO.avg_xyz[1],motorO.avg_xyz[2],motorO.avg_rpm,motorO.current_threshold]):
#                 print("collision")
#             else:
#                 print("ok")
#                 print(f" x,y,z,rpm, current:  {[motorO.avg_xyz[0],motorO.avg_xyz[1],motorO.avg_xyz[2],motorO.avg_rpm,motorO.current_threshold]}")
            #print(f"{motorO.projected_mean_down}, {motorO.projected_mean_up}")
            #motorO.blocked = True
            #if motorO.direction == 1:
#                 print(f"rpm: {motorO.avg_rpm < calibrationO.rpm_up}, avg:{motorO.avg_rpm}, tresh:{calibrationO.rpm_up}")
#                 print(f"current: {motorO.current_threshold > calibrationO.curr_up}, avg:{motorO.current_threshold}, tresh:{calibrationO.curr_up}")
            #   print("---------------------------")
#             elif motorO.direction == -1:
#                 print(f"x_sens:{motorO.avg_xyz[0]}, y_sens:{motorO.avg_xyz[1]}, z_sens:{motorO.avg_xyz[2]}")
#                 print(f"x_tresh:{calibrationO.accel_down[0]}, y_tresh:{calibrationO.accel_down[1]}, z_tresh:{calibrationO.accel_down[2]}")
#                 print(f"rpm_sens:{motorO.avg_rpm}, rpm_tresh:{calibrationO.rpm_down}")
#                 print(f"current_sens:{motorO.current_threshold}, current_tresh:{calibrationO.curr_down}")
#                 print("---------------------------")

        if menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            menuO.move_exec_menu_encoder(step_pin,direction_pin,menu_list,"Menu",wifiO.wifi,wifiO.aps)                                  
            pb_up.press_func(handle_button, (menuO.move_menu_buttons,("up",menu_list,"Menu",wifiO.wifi,wifiO.aps,)))
            pb_down.press_func(handle_button, (menuO.move_menu_buttons,("down",menu_list,"Menu",wifiO.wifi,wifiO.aps,)))
            pb_switch.release_func(handle_button, (launch, (menu_list[(menuO.highlight-1) + menuO.shift],)))
            pb_switch.long_func(handle_button, (go_home, ()))
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        elif menuO.reset_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(factory_reset, ())
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        #enter collision reset menu
        elif menuO.collision_reset_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(reset_collision, ())
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        # confirm reset
        #TODO should be separated into 2 phases UP then DOwn for cleaner code and better ux
        elif calibrationO.collision_reset_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            if motorO.counter <= calibrationO.min_encoder+10 and motorO.direction == -1:
                pb_up.press_func(move_motor, (up_button,True))
                pb_down.press_func(disable_button, ())
                motorO.stop_motor()
                calibrationO.set_avg_vals("down")
            elif motorO.counter >= calibrationO.max_encoder-10 and motorO.direction == 1:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(move_motor, (down_button,True))
                motorO.stop_motor()
                calibrationO.set_avg_vals("up")
            if motorO.direction == -1:
                pb_up.press_func(move_motor, (up_button,True))
                pb_down.press_func(disable_button, ())
            elif motorO.direction == 1:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(move_motor, (down_button,True))
            elif motorO.direction == 0:
                pb_up.press_func(move_motor, (up_button,True))
                pb_down.press_func(move_motor, (down_button,True))
            if motorO.is_moving():
                motorO.update_pca()
            pb_switch.release_func(calibrationO.reset_collision, ())
            pb_switch.long_func(disable_button, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())

            if up_button.value() == 0 or down_button.value() == 0:
                displayO.show_height_frame(str(calibrationO.real_height(motorO.counter)),motorO.rpm)
        # Show message when clik on menu item
        elif menuO.presets_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(go_back, ())
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        # Show list of wifis
        elif menuO.wc_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            menuO.move_exec_menu_encoder(step_pin,direction_pin,wifiO.nearby,"Wifi",wifiO.wifi,wifiO.aps)                                  
            pb_up.press_func(menuO.move_menu_buttons, ("up",wifiO.nearby,"Wifi",wifiO.wifi,wifiO.aps,))
            pb_down.press_func(menuO.move_menu_buttons, ("down",wifiO.nearby,"Wifi",wifiO.wifi,wifiO.aps,))
            pb_switch.release_func(launch, (wifiO.nearby[(menuO.highlight-1) + menuO.shift],))
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        elif menuO.wc_c_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            menuO.move_exec_menu_encoder(step_pin,direction_pin,menu,chosen_wf,wifiO.wifi,wifiO.aps)                                  
            pb_up.press_func(menuO.move_menu_buttons, ("up",menu,chosen_wf,wifiO.wifi,wifiO.aps,))
            pb_down.press_func(menuO.move_menu_buttons, ("down",menu,chosen_wf,wifiO.wifi,wifiO.aps,))
            pb_switch.release_func(launch, (menu[(menuO.highlight-1) + menuO.shift],))
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        elif menuO.forget_w_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(forget_wifi, (chosen_wf,))
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        elif menuO.s_w_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            saved_wifis = wifiO.saved_json
            w_l = list(saved_wifis.keys())
            if wifiO.wlan.isconnected():
                w_l[w_l.index(wifiO.ssid)] = f"->{wifiO.ssid}"
            menuO.move_exec_menu_encoder(step_pin,direction_pin,w_l,"Wifis",wifiO.wifi,wifiO.aps)                                  
            pb_up.press_func(menuO.move_menu_buttons, ("up",w_l,"Wifis",wifiO.wifi,wifiO.aps,))
            pb_down.press_func(menuO.move_menu_buttons, ("down",w_l,"Wifis",wifiO.wifi,wifiO.aps,))
            pb_switch.release_func(launch, (w_l[(menuO.highlight-1) + menuO.shift],))
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        elif menuO.cf_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            if menuO.slp_state:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_one.press_func(toggle_01, ())
                pb_two.press_func(toggle_10, ())
                pb_three.press_func(toggle_100, ())
                pb_switch.long_func(go_home, ())
                pb_switch.release_func(set_sleep_value,(sleep_value,))
#                 if sleep_value <= 86400:
                if sleep_previousValue != step_pin.value():
                    if step_pin.value() == False:
                        if direction_pin.value() == True:
                            if sleep_value > 0:
                                if calibrationO._01:
                                    sleep_value = max(sleep_value - 10, 0)
                                elif calibrationO._10:
                                   sleep_value = max(sleep_value - 60, 0)
                                elif calibrationO._100:
                                    sleep_value = max(sleep_value - 3600, 0)
                                else:
                                    sleep_value  = max(sleep_value - 1, 0)
                                
                        else:
                            if sleep_value <= 86400:
                                if calibrationO._01:
                                    sleep_value +=10
                                elif calibrationO._10:
                                   sleep_value +=60
                                elif calibrationO._100:
                                    sleep_value +=3600
                                else:
                                    sleep_value +=1
                        displayO.show_header("Sleep",wifiO.wifi,wifiO.aps)
                        displayO.show_time_frame(sleep_value)
                    sleep_previousValue = step_pin.value()
                    utime.sleep_ms(1)
            elif menuO.rem_state:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_one.press_func(toggle_01, ())
                pb_two.press_func(toggle_10, ())
                pb_three.press_func(toggle_100, ())
                pb_switch.long_func(go_home, ())
                pb_switch.release_func(set_rem_value,(rem_value,))
#                 if sleep_value <= 86400:
                if rem_previousValue != step_pin.value():
                    if step_pin.value() == False:
                        if direction_pin.value() == True:
                            if rem_value > 0:
                                if calibrationO._01:
                                    rem_value = max(rem_value - 10, 0)
                                elif calibrationO._10:
                                   rem_value = max(rem_value - 60, 0)
                                elif calibrationO._100:
                                    rem_value = max(rem_value - 3600, 0)
                                else:
                                    rem_value  = max(rem_value - 1, 0)
                                
                        else:
                            if rem_value <= 86400:
                                if calibrationO._01:
                                    rem_value +=10
                                elif calibrationO._10:
                                   rem_value +=60
                                elif calibrationO._100:
                                    rem_value +=3600
                                else:
                                    rem_value +=1
                        displayO.show_header("Reminder",wifiO.wifi,wifiO.aps)
                        displayO.show_time_frame(rem_value)
                    rem_previousValue = step_pin.value()
                    utime.sleep_ms(1)
            else:
                menuO.move_exec_menu_encoder(step_pin,direction_pin,conf_menu,"Config",wifiO.wifi,wifiO.aps)                                  
                pb_up.press_func(menuO.move_menu_buttons, ("up",conf_menu,"Config",wifiO.wifi,wifiO.aps,))
                pb_down.press_func(menuO.move_menu_buttons, ("down",conf_menu,"Config",wifiO.wifi,wifiO.aps,))
                pb_switch.release_func(launch, (conf_menu[(menuO.highlight-1) + menuO.shift],))
                pb_switch.long_func(go_home, ())
                pb_one.release_func(disable_button, ())
                pb_two.release_func(disable_button, ())
                pb_three.release_func(disable_button, ())
        elif menuO.cf_h_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            if menuO.min_state:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_one.press_func(toggle_01, ())
                pb_two.press_func(toggle_10, ())
                pb_three.press_func(toggle_100, ())
                pb_switch.release_func(set_min, (min_height_value,))
                if min_height_previousValue != step_pin.value():
                    if step_pin.value() == False:
                        if direction_pin.value() == True:
                            if min_height_value > 0:
                                if calibrationO._01:
                                    min_height_value = max(min_height_value-0.1, 0)
                                elif calibrationO._10:
                                   min_height_value = max(min_height_value - 10, 0)
                                elif calibrationO._100:
                                    min_height_value = max(min_height_value - 100, 0)
                                else:
                                    min_height_value  = max(min_height_value - 1, 0)
                        else:
                            if calibrationO._01:
                                min_height_value +=0.1
                            elif calibrationO._10:
                               min_height_value +=10
                            elif calibrationO._100:
                                min_height_value +=100
                            else:
                                min_height_value +=1
                        displayO.show_header("Min",wifiO.wifi,wifiO.aps)
                        displayO.show_height_frame(str(round(min_height_value,1)),0)
                    min_height_previousValue = step_pin.value()
                    utime.sleep_ms(1)
            elif menuO.max_state:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_one.press_func(toggle_01, ())
                pb_two.press_func(toggle_10, ())
                pb_three.press_func(toggle_100, ())
                pb_switch.release_func(set_max, (max_height_value,))
                if max_height_previousValue != step_pin.value():
                    if step_pin.value() == False:
                        if direction_pin.value() == True:
                            if max_height_value > 0:
                                if calibrationO._01:
                                    max_height_value = max(max_height_value-0.1, 0)
                                elif calibrationO._10:
                                   max_height_value = max(max_height_value - 10, 0)
                                elif calibrationO._100:
                                    max_height_value = max(max_height_value - 100, 0)
                                else:
                                    max_height_value  = max(max_height_value - 1, 0)
                        else:
                            if calibrationO._01:
                                max_height_value +=0.1
                            elif calibrationO._10:
                               max_height_value +=10
                            elif calibrationO._100:
                                max_height_value +=100
                            else:
                                max_height_value +=1
                        displayO.show_header("Min",wifiO.wifi,wifiO.aps)
                        displayO.show_height_frame(str(round(max_height_value,1)),0)
                    max_height_previousValue = step_pin.value()
                    utime.sleep_ms(1)
            else:
                menuO.move_exec_menu_encoder(step_pin,direction_pin,mm,"min/max",wifiO.wifi,wifiO.aps)                                  
                pb_up.press_func(menuO.move_menu_buttons, ("up",mm,"min/max",wifiO.wifi,wifiO.aps,))
                pb_down.press_func(menuO.move_menu_buttons, ("down",mm,"min/max",wifiO.wifi,wifiO.aps,))
                pb_switch.release_func(launch, (mm[(menuO.highlight-1) + menuO.shift],))
                pb_switch.long_func(go_home, ())
                pb_one.release_func(disable_button, ())
                pb_two.release_func(disable_button, ())
                pb_three.release_func(disable_button, ())
        elif menuO.cf_s_state and not menuO.menu_state and not calibrationO.system_idle and not motorO.api and calibrationO.speed_calib:
            if menuO.cf_mel_state:
                menuO.move_exec_menu_encoder(step_pin,direction_pin,buzzvibO.songs,"Melodies",wifiO.wifi,wifiO.aps,c_melody)                                  
                pb_up.press_func(menuO.move_menu_buttons, ("up",buzzvibO.songs,"Melodies",wifiO.wifi,wifiO.aps,c_melody,))
                pb_down.press_func(menuO.move_menu_buttons, ("down",buzzvibO.songs,"Melodies",wifiO.wifi,wifiO.aps,c_melody))
                pb_switch.release_func(launch, (buzzvibO.songs[(menuO.highlight-1) + menuO.shift],))
                pb_switch.long_func(go_home, ())
                pb_one.release_func(disable_button, ())
                pb_two.release_func(disable_button, ())
                pb_three.release_func(disable_button, ())
            elif menuO.cf_st_state:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_switch.release_func(disable_button, ())
                pb_switch.long_func(disable_button, ())
                pb_one.release_func(disable_button, ())
                pb_two.release_func(disable_button, ())
                pb_three.release_func(disable_button, ())
            else:
                menuO.move_exec_menu_encoder(step_pin,direction_pin,sound_menu,"Sound",wifiO.wifi,wifiO.aps)                                  
                pb_up.press_func(menuO.move_menu_buttons, ("up",sound_menu,"Sound",wifiO.wifi,wifiO.aps,))
                pb_down.press_func(menuO.move_menu_buttons, ("down",sound_menu,"Sound",wifiO.wifi,wifiO.aps,))
                pb_switch.release_func(launch, (sound_menu[(menuO.highlight-1) + menuO.shift],))
                pb_switch.long_func(go_home, ())
                pb_one.release_func(disable_button, ())
                pb_two.release_func(disable_button, ())
                pb_three.release_func(disable_button, ())
        elif motorO.api and not menuO.presets_state and not menuO.menu_state and not calibrationO.system_idle and calibrationO.speed_calib:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(disable_button, ())
            pb_switch.long_func(disable_button, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        else:
            #if idle show height and handle motor stoping if reach lowest or heighest point (calibration result)
            if calibrationO.system_idle:                                               
                if motorO.counter <= calibrationO.min_encoder+10 and motorO.direction == -1:
                    pb_up.press_func(handle_button, (move_motor, (up_button,)))
                    pb_down.press_func(disable_button, ())
                    motorO.stop_motor()
                elif motorO.counter >= calibrationO.max_encoder-10 and motorO.direction == 1:
                    pb_up.press_func(disable_button, ())
                    pb_down.press_func(handle_button, (move_motor, (down_button,)))
                    motorO.stop_motor()
                    
                if motorO.direction == -1:
                    pb_up.press_func(handle_button, (move_motor, (up_button,)))
                    pb_down.press_func(disable_button, ())
                elif motorO.direction == 1:
                    pb_up.press_func(disable_button, ())
                    pb_down.press_func(handle_button, (move_motor, (down_button,)))
                elif motorO.direction == 0:
                    pb_up.press_func(handle_button, (move_motor, (up_button,)))
                    pb_down.press_func(handle_button, (move_motor, (down_button,)))
                #addig to that, we display current real height and handle buttons
                if (not displayO.sleep_state and not displayO.rem_state) and not menuO.menu_state and not displayO.lock_state and calibrationO.speed_calib:
                    elapsed_time = (utime.ticks_ms() - displayO.start_time) / 1000.0  # Convert to seconds
                    remaining_ratio = min(1, elapsed_time / displayO.reminder_time)  # Calculate the remaining time ratio
                    displayO.progress_fill = int(remaining_ratio * 97)  # Calculate fill amount, scale it according to the length of the progress bar
                    displayO.show_header("Home",wifiO.wifi,wifiO.aps)
                    displayO.show_height_frame(str(calibrationO.real_height(motorO.counter)),motorO.rpm)
                    pb_up.press_func(handle_button, (move_motor, (up_button,)))
                    pb_down.press_func(handle_button, (move_motor,(down_button,)))
                    pb_switch.release_func(show_menu, (menu_list,))
                    pb_switch.long_func(show_menu, (menu_list,)) # maybe set presets                    
                    pb_one.release_func(handle_button,(go_to_preset, ('1',)))
                    pb_two.release_func(handle_button,(go_to_preset, ('2',)))
                    pb_three.release_func(handle_button,(go_to_preset, ('3',)))
                    pb_one.long_func(set_preset, ('1',))
                    pb_two.long_func(set_preset, ('2',))
                    pb_three.long_func(set_preset, ('3',))
                    if time() - start_tm_rem >= calibrationO.reminder_time and calibrationO.reminder_time < 86401:
                        displayO.alarm()
                    if time() - start_tm >= calibrationO.sleep_time:
                        displayO.dim()
                elif displayO.rem_state and not menuO.menu_state and not displayO.lock_state and calibrationO.speed_calib:
                    pb_up.press_func(stp_rem, ())
                    pb_down.press_func(stp_rem, ())
                    pb_switch.release_func(stp_rem, ())
                    pb_switch.long_func(stp_rem, ())                   
                    pb_one.release_func(stp_rem, ())
                    pb_two.release_func(stp_rem, ())
                    pb_three.release_func(stp_rem, ())
                    pb_one.long_func(stp_rem, ())
                    pb_two.long_func(stp_rem, ())
                    pb_three.long_func(stp_rem, ())
                    loop.run_until_complete(alarm())
                elif displayO.sleep_state and not menuO.menu_state and not displayO.lock_state and calibrationO.speed_calib:
                    pb_up.press_func(awake, ())
                    pb_down.press_func(awake, ())
                    pb_switch.release_func(awake, ())
                    pb_switch.long_func(awake, ())                   
                    pb_one.release_func(awake, ())
                    pb_two.release_func(awake, ())
                    pb_three.release_func(awake, ())
                    pb_one.long_func(awake, ())
                    pb_two.long_func(awake, ())
                    pb_three.long_func(awake, ())
                    if time() - start_tm_rem >= calibrationO.reminder_time:
                        displayO.alarm()
                else:
                    pb_up.press_func(disable_button, ())
                    pb_down.press_func(disable_button, ())
                    displayO.show_height_frame(str(calibrationO.real_height(motorO.counter)),motorO.rpm)                      
                    pb_switch.release_func(show_menu, (menu_list,))
                    pb_switch.long_func(show_menu, (menu_list,)) # maybe set presets
                    pb_one.release_func(disable_button, ())
                    pb_two.release_func(disable_button, ())
                    pb_three.release_func(disable_button, ())
        
        utime.sleep_ms(10)
        sLock.release()
        

       



# loop = asyncio.get_event_loop()



# @micropython.native
def toggle_server(loop,operation):
    if not wifiO.wlan.isconnected():
        return
    loop.create_task(wifiO.serve(operation))
    if operation == "start":
        current_task = None
        # ######### controllers
        async def a_go_to_preset(preset):
            return go_to_preset(preset)

        async def a_get_height():
            return str(calibrationO.real_height(motorO.counter))

        async def a_get_minmax():
            d= {"min": calibrationO.min_real, "max":calibrationO.max_real}
            return json.dumps(d)

        async def a_get_presets():
            presets = presetsO.presets
            if not presets:
                preset_list = []
            else:
                preset_list = ["{}: {}".format(k, calibrationO.real_height(v)) for k, v in presets.items()]
            return json.dumps(preset_list)            

        async def a_forward():
            motorO.api = True
            await asyncio.create_task(motorO.move_motor_api("up",outA,outB,calibrationO.min_encoder, calibrationO.max_encoder ))
        
        async def a_backward():
            motorO.api = True
            await asyncio.create_task(motorO.move_motor_api("down",outA,outB,calibrationO.min_encoder, calibrationO.max_encoder ))
        
        async def a_stop():            
            motorO.api = False
            await asyncio.create_task(motorO.stop_motor_api(outA,outB))
            
        async def a_lock():#refresh display header? requires get current header
            displayO.lock_state = True
        async def a_unlock():
            displayO.lock_state = False
            
        async def a_islocked():
            return displayO.lock_state
        
        async def a_go(height):
            if height >= calibrationO.min_real and height <= calibrationO.max_real:
                encoder_value = calibrationO.encoder_height(height)
                if encoder_value >= motorO.counter:
                    motorO.move_motor_height("up",outA, outB, encoder_value)
                else:
                    motorO.move_motor_height("down",outA, outB, encoder_value)
        
        async def a_set_min(real_min):
            calibrationO.set_min(real_min)
        
        async def a_set_max(real_max):
            calibrationO.set_max(real_max)
                
        # ######## routes
        
        @wifiO.app.before_request
        async def pre_request_handler(request):
            if current_task:
                current_task.cancel()
        
        @wifiO.app.route('/')#TODO change for cors
        async def hello(request):
            return 'waliori smart sit/stand table'

        @wifiO.app.route('/go_preset')#TODO change for cors
        async def preset(request):
#             global current_task
            current_task = asyncio.create_task(a_go_to_preset(request.args['preset']))
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            if current_task:
                res.body = json.dumps({"status": "ok"})
            else:
                res.body = json.dumps({"status": "nok"})
            return res

        @wifiO.app.route('/get_height',methods=['GET', 'OPTIONS'])
        async def get_height(request):            
#             global current_task
            current_task = await asyncio.create_task(a_get_height())
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"height": str(current_task)})              
            return res
            
        @wifiO.app.route('/get_minmax')#TODO change for cors
        async def get_minmax(request):
#             global current_task
            current_task = await asyncio.create_task(a_get_minmax())
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = current_task              
            return res
#             return current_task

        @wifiO.app.route('/get_presets')#TODO change for cors
        async def get_presets(request):
            current_task = await asyncio.create_task(a_get_presets())
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = current_task              
            return res
        
        @wifiO.app.route('/forward',methods=['GET', 'OPTIONS'])
        async def forward(request):
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            if not displayO.lock_state:
                current_task = await asyncio.create_task(a_forward())                                
                res.body = json.dumps({"status": "ok"})              
                return res
            res.body = json.dumps({"status": "nok"})              
            return res
        
        @wifiO.app.route('/backward',methods=['GET', 'OPTIONS'])
        async def backward(request):            
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            if not displayO.lock_state:
                current_task = await asyncio.create_task(a_backward())
                res.body = json.dumps({"status": "ok"})              
                return res
            res.body = json.dumps({"status": "nok"})              
            return res
                     
        
        @wifiO.app.route('/stop',methods=['GET', 'OPTIONS'])
        async def stop(request):
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            if not displayO.lock_state:
                current_task = await asyncio.create_task(a_stop())
                res.body = json.dumps({"status": "ok"})              
                return res
            res.body = json.dumps({"status": "nok"})              
            return res
        
        @wifiO.app.route('/lock')
        async def lock(request):
            current_task = await asyncio.create_task(a_lock())
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"status":  "ok"})              
            return res
        
        @wifiO.app.route('/unlock')
        async def unlock(request):
            current_task = await asyncio.create_task(a_unlock())
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"status":  "ok"})              
            return res
        
        @wifiO.app.route('/islocked')
        async def islocked(request):
            current_task = await asyncio.create_task(a_islocked())
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"locked":  current_task})              
            return res
        
        @wifiO.app.route('/go')
        async def go(request):
            current_task = await asyncio.create_task(a_go(round(float(request.args['height']),1)))
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"status":  "ok"})              
            return res
        
        @wifiO.app.route('/set_min')
        async def set_min(request):
            current_task = await asyncio.create_task(a_set_min(round(float(request.args['min']),1)))
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"status":  "ok"})              
            return res
        
        @wifiO.app.route('/set_max')
        async def set_max(request):
            current_task = await asyncio.create_task(a_set_max(round(float(request.args['max']),1)))
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"status":  "ok"})              
            return res 
print("-----------")    
print("staarting main loop")       
_thread.start_new_thread(task_display_navigation, ())

if wifiO.wlan.isconnected():
    wifiO.stop()
    wifiO.wifi = bytearray(b'\xff\xff\xff\xff\xf8\x1f\xe3\xc7\xcf\xf3\xfe\x7f\xf8\x1f\xf7\xef\xff\xff\xfe\x7f\xfe\x7f\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00')
    toggle_server(loop,'start')
else:
    loop.create_task(wifiO.start_connection(calibrationO.real_height,motorO.counter))
    wifiO.wifi = bytearray(b'\xff\xff\x98\x1f\xc1\x87\xf7\xf1\xbb\xfd\xfc\x1f\xf6\x0f\xe7\x27\xff\xdf\xfe\x67\xfe\x73\xfe\x79\xff\xff\x00\x00\x00\x00\x00\x00')




try: 
    loop.run_forever()
except KeyboardInterrupt:
    print("closing")
    loop.close()



# wdt.feed()










