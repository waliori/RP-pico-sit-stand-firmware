"""
author: waliori
""" 
import time, json
import uasyncio as asyncio
import songs
class Buzzer:
    def __init__(self, buzzer, vibrat,volume,sLock):
        self.buzzer = buzzer
        self.volume = volume
        self.vibrat = vibrat
        self.sLock = sLock
        self.buzzer.duty_u16(0)
        self.vibrat.value(0)
        self.stop_flag = False
        self.tsk = None
        try:
            with open("s_v.json", "r") as settings_file:
                settings_json = json.load(settings_file)
                self.vibration = settings_json.get("vibration", 0)
                self.sound = settings_json.get("sound", 0)
                self.melody = settings_json.get("melody", 0)
        except:
            self.sLock.acquire()
            with open("s_v.json", "w") as settings_file:
                self.vibration = True
                self.sound = True
                self.melody = "StarWars"
                settings_file.write(json.dumps({"sound": self.sound, "vibration": self.vibration, "melody": self.melody}))
            self.sLock.release()
        self.songs = ["Back to Sounds"]+[f"-> {song}" if song == self.melody else song for song in [self.melody] + [song for song in songs.list_s() if song != self.melody]]
#         self.songs.insert(0,"Back to Sounds")
        
    def set_song(self, melody):
#         if melody != "Back to Sounds":
        self.sLock.acquire()
        if melody != "Back to Sounds":
            self.melody = melody
            self.songs = ["Back to Sounds"]+[f"-> {song}" if song == self.melody else song for song in [self.melody] + [song for song in songs.list_s() if song != self.melody]]
            self.save_settings()
        self.sLock.release()  
        
    def play_tone(self,freq, msec):
#         print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
        if freq > 0:
            if self.sound:
                self.buzzer.freq( int(freq) )
                self.buzzer.duty_u16( int(self.volume) )
            if self.vibration:
                self.vibrat.value(1)
        time.sleep_ms( int(msec * 0.9 ) )
        self.buzzer.duty_u16(0)
        self.vibrat.value(0)
        time.sleep_ms( int(msec * 0.1 ) )

    def play(self,tune):
        try:
            self.stop_flag = False
            for freq, msec in tune.notes():
                if self.stop_flag:
                    self.play_tone(0, 0)  # Stop playing
                    break
                self.play_tone(freq, msec)
        except KeyboardInterrupt:#add stop when click on soemtinh
            self.play_tone(0, 0)
            
    def stop(self):
        self.stop_flag = True
        
    def save_settings(self):
        with open("s_v.json", "w") as settings_file:
            settings_file.write(json.dumps({"sound": self.sound, "vibration": self.vibration, "melody": self.melody}))
    def toggle_vibration(self):
        self.vibration = not self.vibration
        self.save_settings()
    def toggle_sound(self):
        self.sound = not self.sound
        self.save_settings()

