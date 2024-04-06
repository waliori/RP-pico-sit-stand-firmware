#TODO add file.close()
import json
import utime
import math
import sys

class Calibration:
    def __init__(self,displayO,motorO,sLock,wifi,aps):
        self.system_idle = False
        self.enc_calib = False
        self.real_calib = False
        self.max_enc_set = False
        self.max_real_set = False
        self.speed_calib = False
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
        self.collision_reset_state = False
        self.curr_up = 0
        self.curr_down = 0
        self.rpm_down = 0
        self.rpm_up = 0
        self.accel_up = (0,0,0)
        self.accel_down = (0,0,0)
        try:    
            settings = open("settings.json","r")
            settings_json = json.loads(settings.read())
            settings.close()
            self.max_encoder = settings_json["max_encoder"]
            self.min_encoder = settings_json["min_encoder"]
            self.max_real = settings_json["max_real"]
            self.min_real = settings_json["min_real"]
            self.rpm_up = settings_json["rpm_up"]
            self.rpm_down = settings_json["rpm_down"]
            self.curr_down = settings_json["current_down"] 
            self.curr_up = settings_json["current_up"]
            self.accel_up = settings_json["accel_up"] 
            self.accel_down = settings_json["accel_down"] 
            self.sleep_time = settings_json["sleep_time"]
            self.reminder_time = settings_json["reminder_time"]
            if settings_json["sleep_time"] > 86400:
                self.sleep_time = 86401
            if settings_json["reminder_time"] > 86400:
                self.reminder_time = 86401 #TODO change this causing alarm to go on after 24h
            self.system_idle = True
            self.max_enc_set = True
            self.max_real_set = True        
            self.enc_calib = True
            self.real_calib = True
            self.speed_calib = True
            self.displayO.oled.fill(0)
            self.displayO.show_header("Home",self.wifi,self.aps)
            self.displayO.show_frame()
        except:
            self.system_idle = False
            self.sLock.acquire()
            file=open("settings.json","w")
            self.sleep_time = 30
            self.reminder_time = 5400 #90min
            file.write(json.dumps({"sleep_time":30,"reminder_time":5400}))
            file.close()
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
    
    def get_reminder(self):
        return self.reminder_time
    
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
    
    def set_max_enc(self):
        self.max_enc_set = True
        self.max_encoder = self.motorO.counter
        self.curr_up = self.motorO.current_threshold
        self.rpm_up = self.motorO.avg_rpm
        self.accel_up = self.motorO.avg_xyz
        self.displayO.clear_frame()
        self.displayO.text_frame("Turn KNOB to set your table's highest height")
    
    def set_max_real(self,real_heigh):
        self.max_real_set = True
        self.max_real = real_heigh
        self.displayO.clear_frame()
        self.displayO.text_frame("Go to LOWEST position (DOWN), to confirm long clik (KNOB)")
    
    def set_min_enc(self):
        self.enc_calib = True
        self.min_encoder = self.motorO.counter
        self.curr_down = self.motorO.current_threshold
        self.rpm_down = self.motorO.avg_rpm
        self.accel_down = self.motorO.avg_xyz
        self.displayO.clear_frame()
        self.displayO.text_frame("Turn KNOB to set your table's lowest height")
    
    def set_min_real(self,real_heigh):
        self.real_calib = True
        self.system_idle = True
        self.speed_calib = True
        self.min_real = real_heigh        
        self.sLock.acquire()
        settings = open("settings.json","r")
        settings_json = json.loads(settings.read())
        settings_json["min_encoder"] = self.min_encoder
        settings_json["max_encoder"] = self.max_encoder
        settings_json["min_real"] = self.min_real
        settings_json["max_real"] = self.max_real
        settings_json["rpm_down"] = self.rpm_down
        settings_json["rpm_up"] = self.rpm_up
        settings_json["current_down"] = self.curr_down
        settings_json["current_up"] = self.curr_up
        settings_json["accel_down"] = self.accel_down
        settings_json["accel_up"] = self.accel_up
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
    
    def reset_collision(self):#TODO to review all the logic of up and down
        self.collision_reset_state = False
        self.sLock.acquire()
        settings = open("settings.json","r")
        settings_json = json.loads(settings.read())
        settings_json["rpm_down"] = self.rpm_down
        settings_json["rpm_up"] = self.rpm_up
        settings.close()
        file=open("settings.json","w")
        file.write(json.dumps(settings_json))
        file.close()
        self.displayO.clear_frame()
        self.displayO.oled.show()
        self.displayO.text_frame("Done! Exiting to Main Screen...")        
        utime.sleep(1)
        self.displayO.oled.fill(0)
        self.displayO.show_header("Home",self.wifi,self.aps)
        self.sLock.release()
        self.system_idle = True
        
    
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
