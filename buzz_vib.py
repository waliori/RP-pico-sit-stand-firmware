# TinyPICO RTTTL Player
# This should also work with any ESP32  
import time

class Buzzer:
    def __init__(self, buzzer, vibrat,volume=2000):
        self.buzzer = buzzer
        self.pwm = volume
        self.vibrat = vibrat
        self.buzzer.duty_u16(0)
        self.vibrat.value(0)
        self.vibration = True
        self.sound = True
    
    def play_tone(self,freq, msec):
#         print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
        if freq > 0:
            if self.sound:
                self.buzzer.freq( int(freq) )
                self.buzzer.duty_u16( int(self.pwm) )
            if self.vibration:
                self.vibrat.value(1)
        time.sleep_ms( int(msec * 0.9 ) )
        self.buzzer.duty_u16(0)
        self.vibrat.value(0)
        time.sleep_ms( int(msec * 0.1 ) )

    def play(self,tune):
        try:
            for freq, msec in tune.notes():
                self.play_tone(freq, msec)
        except KeyboardInterrupt:#add stop when click on soemtinh
            self.play_tone(0, 0)
            
    def stop(self):
        self.buzzer.duty_u16(0)
        self.vibrat.value(0)

