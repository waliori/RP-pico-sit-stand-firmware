from setup import *
import _thread
from abutton import Pushbutton
import uasyncio
calibrationO = calibration.Calibration(displayO,motorO,sLock)
menuO = menu.Menu(displayO,calibrationO,motorO)
presetsO = presets.Presets(motorO,calibrationO,sLock)

#NOTE no api params control implemented
#TODO http add response status codes
#TODO add qr code for profiles
#TODO add more presets in api/profile
#TODO add collision detection _ initial calibration done + handeling done - manual done , api not done
#TODO add standing alarm (goal sitting) + display timer to change position progress bar (if set)
#TODO set min max : api done, manual not done
#TODO measurement unit cm,inch
#TODO shutdown screen after x time
#TODO add wifi manager (WiFi show saved and open if open is true, else no open no saved show message to launch server) 
#TODO choose to by pass (smart) wifi etc
#TODO add support for open wifi with user choice (default no)
#TODO add "connecting" when first boot because no operation in table is possible why is connecting
#TODO add screen dim/black
#TODO forget wifi
#TODO add go back from sub to menu

# ----------- Functions

# Motor Section

def move_motor(button,calibration=False):
    motorO.move_motor(button,up_button,outA,outB,calibrationO.min_encoder, calibrationO.max_encoder, calibration )          
            
                       
# Menu handeling Section

def show_menu(menu):
    sLock.acquire()      
    menuO.menu_state = True
    menuO.reset_state = False
    menuO.presets_state = False
    calibrationO.idle_state = False
    line = 1
    displayO.show_menu(menu, line, menuO.highlight, menuO.shift,menuO.total_lines,"Main menu")
    sLock.release()
    
def disconnect():
    wifiO.disconnect()
    go_home()

def connect_c_wifi(wifi):
#     sLock.acquire()
    connected = wifiO.connect(wifi,wifiO.saved_json[wifi])
#     sLock.release()
    if connected:
        go_home()
    else:
        displayO.oled.fill(0)
        displayO.show_frame()
        menuO.presets_state = True
        menuO.menu_state = False
        calibrationO.idle_state = False
        displayO.text_frame("Could not connect, try again")
        displayO.show_header("WiFi")
        displayO.oled.show()
        asyncio.sleep(10)
        connect_wifi()    
def connect_wifi():
    menuO.menu_state = False
    calibrationO.idle_state = False
    sLock.acquire()    
    line = 1    
    displayO.oled.fill(0)
    displayO.show_frame()
    if wifiO.saved_json:
        print("if")
        menuO.wc_state = True #mimic menustate
        wifiO.nearby_wifis()
        displayO.show_menu(wifiO.nearby, line, menuO.highlight, menuO.shift,min(len(wifiO.nearby),menuO.total_lines),"Wifi")
    else:
        print("else")
        menuO.presets_state = True
        displayO.text_frame("Connect to PicoW:waliori123 then visit 192.168.4.1")
        displayO.show_header("WiFi")
        displayO.oled.show()
    sLock.release()
        
        
current_m = ".."
menu_list = ["..", "WiFi", "Lock Unlock", "Show Presets", "Show min/max", "Collision Reset", "Factory Reset"]

def go_home():
    sLock.acquire()
    menuO.menu_state = False
    menuO.reset_state = False
    menuO.presets_state = False
    calibrationO.idle_state = True
    menuO.go_home()
    sLock.release()
    
def go_back():
    global current_m, menu_list
    print(f"current menu {current_m}")
    if current_m in ["Show IP"]:
        connect_wifi()
    elif current_m in ["WiFi","Lock Unlock", "Show Presets", "Show min/max", "Collision Reset", "Factory Reset"]:
        show_menu(menu_list)
    elif current_m == "..":
        go_home()

def launch(item):
  global current_m
  current_m = item
#   sLock.acquire()
  actions = {
    "..": go_home,
    "Show Presets": show_presets,
    "Factory Reset": confirm_reset,
    "Show min/max": show_calibration,
    "Show IP" : show_ip,
    "Lock Unlock": lock_unlock,
    "WiFi" : connect_wifi,
    "Collision Reset": confirm_reset_collision,
    "Disconnect": disconnect,
    "Scan again": connect_wifi,
    "Go back": go_back
  }
  if wifiO.saved_json:
      for wf in wifiO.saved_json.keys():
          actions[wf] = connect_c_wifi
#   sLock.release()
  print(f"current menu: {current_m}, and chosen menu item: {item}")
  default_action = lambda: print("No action defined for this item")
  action = actions.get(item, default_action)
  if wifiO.saved_json and item in wifiO.saved_json:
    action(item)
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
            return "Ok"
        return "preset outside limits"
    return "no preset"

def set_preset(preset):
    presetsO.set_preset(preset)


        
# miscs

# @micropython.native    
def disable_button():
    pass

# @micropython.native  
def confirm_reset():
    sLock.acquire()
    displayO.oled.fill(0)
    displayO.show_header("Factory Reset")
    displayO.show_frame()
    displayO.text_frame("All seetings and presets will be wiped, do you confirm?")
    menuO.reset_state = True
    menuO.menu_state = False
    calibrationO.idle_state = False
    sLock.release()

def confirm_reset_collision():
    sLock.acquire()
    displayO.oled.fill(0)
    displayO.show_header("Collision Reset")
    displayO.show_frame()
    displayO.text_frame("Collision settings will be wiped, do you confirm?")
    menuO.collision_reset_state = True
    menuO.menu_state = False
    calibrationO.idle_state = False
    sLock.release()
    
def reset_collision():
    menuO.collision_reset_state = False
    menuO.menu_state = False
    calibrationO.idle_state = False
    calibrationO.semi_collision_state = True
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
    machine.reset()
    sLock.release()


# @micropython.native
def show_presets():    
    sLock.acquire()
    menuO.presets_state = True
    menuO.menu_state = False
    calibrationO.idle_state = False
    motorO.api = False
    presets = presetsO.presets
    displayO.oled.fill(0)
    displayO.show_frame()
    if not presets:
        displayO.text_frame("There are no preset settings in place yet.")
    else:
        preset_list = ["preset {}: {}cm".format(k, calibrationO.real_height(v)) for k, v in presets.items()]
        displayO.show_static_frame(preset_list,len(preset_list))
        displayO.show_header("Presets")
        displayO.oled.show()
    sLock.release()
    
# @micropython.native    
def show_calibration():    
    sLock.acquire()
    menuO.presets_state = True
    menuO.menu_state = False
    calibrationO.idle_state = False
    motorO.api = False
    min_max = ["Min: {}cm".format(calibrationO.min_real), "Max: {}cm".format(calibrationO.max_real)]
    displayO.oled.fill(0)
    displayO.show_frame()
    displayO.show_static_frame(min_max,len(min_max))
    displayO.show_header("Table min/max")
    displayO.oled.show()
    sLock.release()
    
# @micropython.native
def show_ip():
    sLock.acquire()
    menuO.presets_state = True
    menuO.menu_state = False
    calibrationO.idle_state = False
    motorO.api = False
    if wifiO.wlan.isconnected():
        ip = ["IP address: ",wifiO.wlan.ifconfig()[0]]
    else:
        ip = ["IP address: ","Not connected!"]
    displayO.oled.fill(0)
    displayO.show_frame()
    displayO.show_static_frame(ip,len(ip))
    displayO.show_header("IP Address")
    displayO.oled.show()
    sLock.release()
    

# @micropython.native   
def lock_unlock():
    sLock.acquire()
    menuO.presets_state = True
    menuO.menu_state = False
    calibrationO.idle_state = False
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
    displayO.show_header("(Un)Lock")
    displayO.oled.show()
    sLock.release()   

pb_up = Pushbutton(up_button, suppress=True)
pb_down = Pushbutton(down_button, suppress=True)
pb_switch = Pushbutton(button_pin, suppress = True)

pb_one = Pushbutton(one_button, suppress=True)
pb_two = Pushbutton(two_button, suppress=True)
pb_three = Pushbutton(three_button, suppress=True)

# @micropython.native
def task_display_navigation():
    global menu_list
    
    height_value = 0
    height_previousValue = 1
    speed_value = 0
    speed_previousValue = 1
    while True:
        sLock.acquire()
        # not calibrated and not semi calibrated and not idle (AKA first boot of the system)
        if not calibrationO.calibrated and not calibrationO.semi_calibrated and not calibrationO.idle_state and not calibrationO.speed_calibrated:
            pb_up.press_func(move_motor, (up_button,True))
            pb_down.press_func(move_motor, (down_button,True))
            pb_switch.long_func(calibrationO.semi_calibrate, ())
        # not calibrated but semi calibrated and not idle (highest point set) 
        elif not calibrationO.calibrated and  calibrationO.semi_calibrated and not calibrationO.idle_state and not calibrationO.speed_calibrated:
            # not real semi calibrated ()
            if not calibrationO.real_semi_calibrated:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_one.press_func(toggle_01, ())
                pb_two.press_func(toggle_10, ())
                pb_three.press_func(toggle_100, ())
                pb_switch.long_func(calibrationO.real_semi_calibrate, (height_value,))
                
                if height_previousValue != step_pin.value():
                    if step_pin.value() == False:
                        if direction_pin.value() == False:
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
            elif calibrationO.real_semi_calibrated:
                pb_up.press_func(move_motor, (up_button,True))
                pb_down.press_func(move_motor, (down_button,True))
                pb_switch.long_func(calibrationO.calibrate, ())
        # if calibrated and semi_calibrated and not idle (Highest point Done, starting lower)
        elif calibrationO.calibrated and  calibrationO.semi_calibrated and not calibrationO.idle_state and not calibrationO.speed_calibrated:
            # calibrated but not real calibrated 
            if not calibrationO.real_calibrated:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(disable_button, ())
                pb_one.press_func(toggle_01, ())
                pb_two.press_func(toggle_10, ())
                pb_three.press_func(toggle_100, ())
                pb_switch.long_func(calibrationO.real_calibrate, (height_value,))
                if height_previousValue != step_pin.value():
                    if step_pin.value() == False:
                        if direction_pin.value() == False:
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
                        displayO.show_header("Calibration")
                        displayO.show_height_frame(str(round(height_value,1)),0)
                    height_previousValue = step_pin.value()
                    utime.sleep_ms(1)    
        if menuO.menu_state and not calibrationO.idle_state and not motorO.api and calibrationO.speed_calibrated:
            menuO.move_menu_encoder(step_pin,direction_pin,menu_list,"Main menu")                                  
            pb_up.press_func(menuO.move_menu_buttons, ("up",menu_list,"Main menu",))
            pb_down.press_func(menuO.move_menu_buttons, ("down",menu_list,"Main menu",))
            pb_switch.release_func(launch, (menu_list[(menuO.highlight-1) + menuO.shift],))
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        elif menuO.reset_state and not menuO.menu_state and not calibrationO.idle_state and not motorO.api and calibrationO.speed_calibrated:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(factory_reset, ())
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        #enter collision reset menu
        elif menuO.collision_reset_state and not menuO.menu_state and not calibrationO.idle_state and not motorO.api and calibrationO.speed_calibrated:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(reset_collision, ())
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        # confirm reset
        elif calibrationO.semi_collision_state and not menuO.menu_state and not calibrationO.idle_state and not motorO.api and calibrationO.speed_calibrated:
            if motorO.counter <= calibrationO.min_encoder+10 and motorO.direction == -1:
                pb_up.press_func(move_motor, (up_button,True))
                pb_down.press_func(disable_button, ())
                motorO.stop_motor()
            elif motorO.counter >= calibrationO.max_encoder-10 and motorO.direction == 1:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(move_motor, (down_button,True))
                motorO.stop_motor()
                
            if motorO.direction == -1:
                pb_up.press_func(move_motor, (up_button,True))
                pb_down.press_func(disable_button, ())
            elif motorO.direction == 1:
                pb_up.press_func(disable_button, ())
                pb_down.press_func(move_motor, (down_button,True))
            elif motorO.direction == 0:
                pb_up.press_func(move_motor, (up_button,True))
                pb_down.press_func(move_motor, (down_button,True))
            pb_switch.release_func(calibrationO.collision_semi_calibrate, ())
            pb_switch.long_func(disable_button, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())

            if up_button.value() == 0 or down_button.value() == 0:
                displayO.show_height_frame(str(calibrationO.real_height(motorO.counter)),motorO.rpm)

        # Show message when clik on menu item
        elif menuO.presets_state and not menuO.menu_state and not calibrationO.idle_state and not motorO.api and calibrationO.speed_calibrated:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(go_back, ())
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        # Show list of wifis
        elif menuO.wc_state and not menuO.menu_state and not calibrationO.idle_state and not motorO.api and calibrationO.speed_calibrated:
            menuO.move_menu_encoder(step_pin,direction_pin,wifiO.nearby,"Wifi")                                  
            pb_up.press_func(menuO.move_menu_buttons, ("up",wifiO.nearby,"Wifi",))
            pb_down.press_func(menuO.move_menu_buttons, ("down",wifiO.nearby,"Wifi",))
            pb_switch.release_func(launch, (wifiO.nearby[(menuO.highlight-1) + menuO.shift],))
            pb_switch.long_func(go_home, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        # subMenu
#         elif menuO.sub_state and not menuO.menu_state and not calibrationO.idle_state and not motorO.api and calibrationO.speed_calibrated:
#             pb_up.press_func(disable_button, ())
#             pb_down.press_func(disable_button, ())
#             pb_switch.release_func(show_menu, (menu_list,))
#             pb_switch.long_func(go_home, ())
#             pb_one.release_func(disable_button, ())
#             pb_two.release_func(disable_button, ())
#             pb_three.release_func(disable_button, ())
        elif motorO.api and not menuO.presets_state and not menuO.menu_state and not calibrationO.idle_state and calibrationO.speed_calibrated:
            pb_up.press_func(disable_button, ())
            pb_down.press_func(disable_button, ())
            pb_switch.release_func(disable_button, ())
            pb_switch.long_func(disable_button, ())
            pb_one.release_func(disable_button, ())
            pb_two.release_func(disable_button, ())
            pb_three.release_func(disable_button, ())
        else:
            #if idle show height and handle motor stoping if reach lowest or heighest point (calibration result)
            if calibrationO.idle_state:                                               
                if motorO.counter <= calibrationO.min_encoder+10 and motorO.direction == -1:
                    pb_up.press_func(move_motor, (up_button,))
                    pb_down.press_func(disable_button, ())
                    motorO.stop_motor()
                elif motorO.counter >= calibrationO.max_encoder-10 and motorO.direction == 1:
                    pb_up.press_func(disable_button, ())
                    pb_down.press_func(move_motor, (down_button,))
                    motorO.stop_motor()
                    
                if motorO.direction == -1:
                    pb_up.press_func(move_motor, (up_button,))
                    pb_down.press_func(disable_button, ())
                elif motorO.direction == 1:
                    pb_up.press_func(disable_button, ())
                    pb_down.press_func(move_motor, (down_button,))
                elif motorO.direction == 0:
                    pb_up.press_func(move_motor, (up_button,))
                    pb_down.press_func(move_motor, (down_button,))
                    
                #addig to that, we display current real height and handle buttons
                if not menuO.menu_state and not displayO.lock_state and calibrationO.speed_calibrated:
                    displayO.show_height_frame(str(calibrationO.real_height(motorO.counter)),motorO.rpm)
                    pb_up.press_func(move_motor, (up_button,))
                    pb_down.press_func(move_motor, (down_button,))
                    pb_switch.release_func(show_menu, (menu_list,))
                    pb_switch.long_func(show_menu, (menu_list,)) # maybe set presets                    
                    pb_one.release_func(go_to_preset, ('1',))
                    pb_two.release_func(go_to_preset, ('2',))
                    pb_three.release_func(go_to_preset, ('3',))
                    pb_one.long_func(set_preset, ('1',))
                    pb_two.long_func(set_preset, ('2',))
                    pb_three.long_func(set_preset, ('3',))
                
                else:
                    pb_up.press_func(disable_button, ())
                    pb_down.press_func(disable_button, ())
                    displayO.show_height_frame(str(calibrationO.real_height(motorO.counter)),motorO.rpm)                      
                    pb_switch.release_func(show_menu, (menu_list,))
                    pb_switch.long_func(show_menu, (menu_list,)) # maybe set presets
                    pb_one.release_func(disable_button, ())
                    pb_two.release_func(disable_button, ())
                    pb_three.release_func(disable_button, ())
        sLock.release()

       



# loop = asyncio.get_event_loop()
loop = asyncio.get_event_loop()


# @micropython.native
def toggle_server(loop,operation):
    if not wifiO.wlan.isconnected():
        print("nothing to do")
        return
    loop.create_task(wifiO.serve(operation))
    if operation == "start":
        current_task = None
        # ######### controllers
        async def a_go_to_preset(preset):
            go_to_preset(preset)

        async def a_get_height():
            return str(calibrationO.real_height(motorO.counter))

        async def a_get_minmax():
            string = "Min: {}cm".format(calibrationO.min_real)+' - '+"Max: {}cm".format(calibrationO.max_real)
            return string

        async def a_get_presets():
            presets = presetsO.presets
            if not presets:
                string = "no presets yet."
            else:
                preset_list = ["{}: {}cm".format(k, calibrationO.real_height(v)) for k, v in presets.items()]        
                string = ' - '.join(preset_list)
            return string            

        async def a_forward():
            motorO.api = True
            await asyncio.create_task(motorO.move_motor_api("up",outA,outB,calibrationO.min_encoder, calibrationO.max_encoder ))
        
        async def a_backward():
            motorO.api = True
            await asyncio.create_task(motorO.move_motor_api("down",outA,outB,calibrationO.min_encoder, calibrationO.max_encoder ))
        
        async def a_stop():            
            motorO.api = False
            await asyncio.create_task(motorO.stop_motor_api())
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
            return 'Hello world'

        @wifiO.app.route('/go_preset')#TODO change for cors
        async def preset(request):
#             global current_task
            current_task = asyncio.create_task(a_go_to_preset(request.args['preset']))
            return 'Ok'

        @wifiO.app.route('/get_height',methods=['GET', 'OPTIONS'])
        async def get_height(request):            
#             global current_task
            current_task = await asyncio.create_task(a_get_height())
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"height": str(current_task)+'cm'})              
            return res
            
        @wifiO.app.route('/get_minmax')#TODO change for cors
        async def get_minmax(request):
#             global current_task
            current_task = await asyncio.create_task(a_get_minmax())
            return current_task

        @wifiO.app.route('/get_presets')#TODO change for cors
        async def get_presets(request):
            current_task = await asyncio.create_task(a_get_presets())
            return current_task
        
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
                     
        
        @wifiO.app.route('/stop')
        async def stop(request):
            current_task = await asyncio.create_task(a_stop())
            res= None
            res = Response(res)
            res.status_code = 200
            res.headers["Access-Control-Allow-Origin"] = '*'
            res.headers["Access-Control-Allow-Methods"] = '*'
            res.body = json.dumps({"status":  "ok"})              
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


    






#     ip = ["Connected to: ",wifiO.ssid]
#     menuO.presets_state = True
#     menuO.menu_state = False
#     calibrationO.idle_state = False
#     sLock.acquire()
#     displayO.oled.fill(0)
#     displayO.show_frame()
#     displayO.text_frame("Connecting to "+ wifiO.ssid)
#     displayO.show_header("WiFi")
#     displayO.oled.show()
#     sLock.release()
#     if not wifiO.wlan.isconnected():
#         sLock.acquire()    
#         wifiO.connect()
#         if not wifiO.wlan.isconnected():
#             ip = ["Error: ","Try Again!"]
#         displayO.oled.fill(0)
#         displayO.show_frame()
#         displayO.show_static_frame(ip,len(ip))
#         displayO.show_header("WiFi")
#         displayO.oled.show()
#         toggle_server(loop,"start")
#         sLock.release()
#     else:
#         sLock.acquire()
#         displayO.oled.fill(0)
#         displayO.show_frame()
#         displayO.show_static_frame(ip,len(ip))
#         displayO.show_header("WiFi")
#         displayO.oled.show()
#         sLock.release()     
       
        
if wifiO.wlan.isconnected():
    wifiO.stop()
    toggle_server(loop,'start')
else:
    loop.create_task(wifiO.start_connection())
    

_thread.start_new_thread(task_display_navigation, ())

try: 
    loop.run_forever()
except KeyboardInterrupt:
    print("closing")
    loop.close()











