#TODO add file.close()
import json
import utime
import math
import sys
class Calibration:
    def __init__(self,displayO,motorO,sLock,wifi,aps):
        self.idle_state = False
        self.calibrated = False
        self.real_calibrated = False
        self.semi_calibrated = False
        self.real_semi_calibrated = False
        self.speed_calibrated = False
        self.displayO = displayO
        self.motorO = motorO
        self.wifi = wifi
        self.aps = aps
        self.max_encoder = 0
        self.min_encoder = 0
        self.max_real = 0
        self.min_real = 0
        self.sLock = sLock
        self._01 = False
        self._10 = False
        self._100 = False
        self.semi_collision_state = False
#         self.height_value = 0
#         self.height_previousValue = 1
#         self.min_height = 0
#         print(self.wifi)
        try:    
            settings = open("settings.json","r")
            settings_json = json.loads(settings.read())
            self.max_encoder = settings_json["max_encoder"]
            self.min_encoder = settings_json["min_encoder"]
            self.max_real = settings_json["max_real"]
            self.min_real = settings_json["min_real"]
            self.motorO.max_speed = settings_json["max_speed"]
            self.motorO.min_speed = settings_json["min_speed"]
            self.sleep_time = settings_json["sleep_time"]
            if settings_json["sleep_time"] > 86400:
                self.sleep_time = 86400
            self.idle_state = True
            self.semi_calibrated = True
            self.real_semi_calibrated = True        
            self.calibrated = True
            self.real_calibrated = True
            self.speed_calibrated = True
            self.displayO.oled.fill(0)
            self.displayO.show_header("Home",self.wifi,self.aps)
            self.displayO.show_frame()
        except:
            self.idle_state = False
            self.sLock.acquire()
            file=open("settings.json","w")
            self.sleep_time = 30
            file.write(json.dumps({"sleep_time":30}))
            self.sLock.release()
            self.displayO.oled.fill(0)
            self.displayO.show_header("Calibration",self.wifi,self.aps)
            self.displayO.show_frame()
            self.displayO.text_frame("Go to HIGHEST position (UP), to confirm long clik (KNOB)")
            
            
    def real_height(self,current_encoder):
        value = (current_encoder - self.min_encoder)* (self.max_real - self.min_real) / (self.max_encoder - self.min_encoder) + self.min_real
        if isinstance(value,float):
            return round(value,1)        
        return value
    
    def encoder_height(self,real):
        value = (real - self.min_real) * (self.max_encoder - self.min_encoder) / (self.max_real - self.min_real) + self.min_encoder
        if isinstance(value,float):
            return round(value,1)
        return value
    
    def real_to_encoder(self,real):
        value = (self.min_real - real) * (self.max_encoder - self.min_encoder) / (self.max_real - real) + self.min_encoder
        if isinstance(value,float):
            return round(value,1)
        return value
    def semi_calibrate(self):
        self.semi_calibrated = True
#         print(str(self.motorO.counter))
        self.max_encoder = self.motorO.counter
        self.displayO.clear_frame()
        self.displayO.text_frame("Turn KNOB to set your table's highest height")
    
    def real_semi_calibrate(self,real_heigh):
        self.real_semi_calibrated = True
#         print(str(real_heigh))
        self.max_real = real_heigh
        self.displayO.clear_frame()
        self.displayO.text_frame("Go to LOWEST position (DOWN), to confirm long clik (KNOB)")
    
    def calibrate(self):
        self.calibrated = True
#         print(str(self.motorO.counter))
        self.min_encoder = self.motorO.counter
        self.displayO.clear_frame()
        self.displayO.text_frame("Turn KNOB to set your table's lowest height")
    
    def real_calibrate(self,real_heigh):
        self.real_calibrated = True
        self.idle_state = True
        self.speed_calibrated = True
#         print(str(real_heigh))
        self.min_real = real_heigh        
        self.sLock.acquire()
        settings = open("settings.json","r")
        settings_json = json.loads(settings.read())
        settings_json["min_encoder"] = self.min_encoder
        settings_json["max_encoder"] = self.max_encoder
        settings_json["min_real"] = self.min_real
        settings_json["max_real"] = self.max_real
        settings_json["min_speed"] = self.motorO.min_speed
        settings_json["max_speed"] = self.motorO.max_speed
        file=open("settings.json","w")
        file.write(json.dumps(settings_json))
        self.displayO.clear_frame()
        self.displayO.oled.show()
        self.displayO.text_frame("Done! Exiting to Main Screen...")        
        utime.sleep(1)
        self.displayO.oled.fill(0)
        self.displayO.show_header("Home",self.wifi,self.aps)
        self.displayO.show_height_frame(str(self.real_height(self.motorO.counter)),0)
        self.sLock.release()
    
    def collision_semi_calibrate(self):
        self.semi_collision_state = False
        self.sLock.acquire()
        settings = open("settings.json","r")
        settings_json = json.loads(settings.read())
        settings_json["min_speed"] = self.motorO.min_speed
        settings_json["max_speed"] = self.motorO.max_speed
        settings.close()
        print(self.motorO.min_speed,self.motorO.max_speed)
        file=open("settings.json","w")
        file.write(json.dumps(settings_json))
        file.close()
        self.displayO.clear_frame()
        self.displayO.oled.show()
        self.displayO.text_frame("Done! Exiting to Main Screen...")        
        utime.sleep(1)
        self.displayO.oled.fill(0)
        self.displayO.show_header("Home",self.wifi,self.aps)
#         self.displayO.show_height_frame(str(self.real_height(self.motorO.counter),0))
        self.sLock.release()
        self.idle_state = True
        
#     def collision_calibrate(self):
#              
#         self.collision_state = False
#         self.idle_state = True
    
    def set_min(self,real_min):
        self.sLock.acquire()
        settings = open("settings.json","r")
        settings_json = json.loads(settings.read())
        print(settings_json["min_real"],settings_json["min_encoder"])        
        encoder_min = self.real_to_encoder(real_min)        
        settings_json["min_real"] = real_min
        settings_json["min_encoder"] = encoder_min
        self.min_real = real_min
        self.min_encoder = encoder_min
        file=open("settings.json","w")
        file.write(json.dumps(settings_json))
        print(settings_json["min_real"],settings_json["min_encoder"])
        self.sLock.release()
        
    def set_max(self,real_max):
        self.sLock.acquire()
        settings = open("settings.json","r")
        settings_json = json.loads(settings.read())        
        encoder_max = self.real_to_encoder(real_max)
        self.max_real = real_max
        self.max_encoder = encoder_max
        settings_json["max_real"] = real_max
        settings_json["max_encoder"] = encoder_max
        file=open("settings.json","w")
        file.write(json.dumps(settings_json))
        self.sLock.release()
        
        
