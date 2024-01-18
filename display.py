from machine import Pin, I2C
from sh1106 import SH1106_I2C
import framebuf
import freesans20
import firacodeBold30
import writer
import base64
import math

#display
# logo = bytearray(b'\x00\x00\xc0\x80\x00\x00\x00\x40\xc0\x00\x00\xc0\x00\x00\x00\x00\x80\xc0\x00\x00\x80\xc0\x40\x40\x40\xc0\x80\x00\x00\x00\x00\xfc\x00\x00\x00\x00\x00\xcc\x00\x00\x00\x00\x80\xc0\x40\x40\x40\xc0\x80\x00\x00\x00\x00\xc0\xc0\x00\x80\xc0\x40\x00\x00\xcc\x00\x00\x00\x00\x00\x03\x1c\x70\xc0\xc0\x71\x1e\x1f\xe1\x80\xc0\x38\x0e\x03\x00\x00\xf0\x98\x08\x08\x08\x08\x88\xff\xff\x00\x00\x00\xff\x80\x00\x00\x00\x00\xff\x00\x00\x1c\x7f\xc1\x80\x00\x00\x00\x00\x81\xe3\x3e\x00\x00\xff\xff\x01\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x08\x08\x08\x08\x09\x09\x08\x08\x08\x08\x09\x09\x08\x08\x08\x08\x08\x08\x09\x09\x09\x09\x09\x08\x08\x09\x08\x08\x88\x09\x09\x09\x09\x08\x08\x89\x08\x08\x08\x08\x08\x09\x09\x09\x09\xc9\x09\x08\x08\x08\x08\x09\xc9\x08\x08\x08\x08\x08\x08\x09\x00\x00\x00\x00\x06\x49\x49\x3a\x00\x00\x3e\x02\x01\x02\x7e\x02\x00\x02\x3e\x00\x10\x6a\x49\x09\x3e\x00\x00\x3e\x02\x01\x00\x00\x3f\x40\x00\x00\x00\x00\x00\x3f\x41\x00\x30\x6a\x49\x09\x3e\x00\x00\x3f\x22\x40\x40\x3e\x00\x00\x3f\x00\x18\x3e\x48\x49\x0a\x2c\x00\x00')
sit = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x1f\x80\x00\x00\x00\x1f\x80\x02\x00\x00\x1f\x80\x03\x80\x00\x0f\x00\x03\x70\x00\x30\x00\x00\x0c\x00\x78\x00\x00\x02\x00\xbc\x00\x00\x02\x20\xfc\x00\x00\x00\x31\xfe\x38\x00\x04\x31\xfd\xfc\x00\x04\x39\xff\xf8\x00\x08\x39\xf7\xfc\x00\x08\x19\xf1\xf3\x80\x08\x1d\xf0\x3f\xff\xf8\x1d\xff\xcf\xff\xe0\x09\xff\xc0\x38\x00\x08\xff\xc0\x30\x00\x00\x01\xc0\x30\x00\x07\xfd\xc0\x38\x00\x01\xe1\xc0\x38\x00\x00\x41\xe0\x38\x00\x00\x41\xe0\x38\x00\x00\x41\xe0\x38\x00\x01\xf1\xe0\x38\x00\x04\x45\xe0\x38\x00\x04\x44\xe7\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
stand = bytearray(b"\x00\x00\x00\x00\x00\x01\xe0\x00\x00\x00\x03\xf0\x00\x00\x00\x03\xf8\x00\x80\x00\x03\xf8\x00\x80\x00\x03\xf0\x00\x80\x00\x01\xf0\x00\xc0\x00\x00\xc0\x00\xf8\x00\x07\x00\x00\xc6\x00\x0d\x80\x00\x80\x80\x0f\x80\x00\x80\x40\x1f\x00\x00\x80\x40\x1f\x80\x00\x80\x40\x1f\x80\x00\x00\x80\x1f\x80\x00\x00\x80\x1f\xff\x00\x01\x00\x1e\xff\x00\x01\x00\x1f\xff\x00\x01\x00\x1f\x00\x00\x00\x00\x1f\x07\xff\xfe\x00\x0f\x10\xff\xf0\x00\x07\x00\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x07\x80\x06\x00\x00\x03\x83\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
alarm = bytearray(b"\x00\x00\x0c\x00\x1e\x00\x3e\x00\x3f\x00\x3f\x00\x3f\x00\x3f\x00\x0c\x00\x00\x00")
s_and_v = bytearray(b"\xff\xff\xff\xff\xff\xff\xef\xe7\xde\x6f\xe8\x3b\xfb\xdf\xf7\xdf\xf7\xdf\xf7\xdf\xf7\xdf\xf3\xdf\xe0\x0f\xfe\x7f\xff\xff\xff\xff")
v=bytearray(b"\xff\xfc\xff\xf4\x9c\xe4\xcc\xcc\xe6\xe4\x83\xe4\x81\xcc\x80\xcc\x80\x64\xf0\x24\xf8\xcc\xfc\xec\xff\xf4\xff\xfc")
s=bytearray(b"\xff\xfc\xff\xfc\xff\x34\xfe\x0c\xf8\x1c\xc0\x3c\xc0\x7c\xc0\x3c\xc0\x3c\xe0\x3c\xec\x3c\xdf\x3c\xff\xfc\xff\xfc")
s_no_v = bytearray(b"\xff\xfc\xff\xfc\xf9\xec\xf1\xbc\xe1\x54\x01\xa4\x00\xac\x00\xac\x01\xa4\xe1\x54\xf1\xbc\xf9\xec\xff\xfc\xff\xfc")
# logo_buffer = framebuf.FrameBuffer(logo, 64, 32, framebuf.MONO_HLSB)
sit_fb = framebuf.FrameBuffer(sit, 40, 38, framebuf.MONO_HLSB)
stand_fb = framebuf.FrameBuffer(stand, 40, 38, framebuf.MONO_HLSB)
alarm_fb = framebuf.FrameBuffer(alarm, 10, 10, framebuf.MONO_HLSB)
s_and_v_fb = framebuf.FrameBuffer(s_and_v, 14, 14, framebuf.MONO_HLSB)
s_fb = framebuf.FrameBuffer(s, 11, 14, framebuf.MONO_HLSB)
v_fb = framebuf.FrameBuffer(v, 14, 14, framebuf.MONO_HLSB)
s_no_v_fb = framebuf.FrameBuffer(s_no_v, 14, 14, framebuf.MONO_HLSB)

def get_center_x(text, area_width,avg_char_width):
    text_width = len(text)*avg_char_width
    if area_width > text_width:
        return int((area_width - text_width) / 2)
    return 0
def get_center_y(area_height,char_height):
    if area_height > char_height:
        return int((area_height - char_height) / 2)
    return 0

def get_avg_char_width_height(text,font=False):
    if not font:
        return 5,8
    l_w = []
    for l in text:
        _,h,w = font.get_ch(l)
        l_w.append(w)
    return h,math.floor(sum(l_w )/len(l_w ))

def divide_phrase(phrase, max_width, avg_char_width):
    words = phrase.split()
    parts = []
    part = ''
    for i,word in enumerate(words) :
        width = avg_char_width * (len(part) + len(word))
        if width > max_width:
            parts.append(part)
            part = word
        else:
            if i > 0:
                part += ' '
            part += word
    parts.append(part)
    return parts



class Display:
    def __init__(self,width,height,i2c_id,scl,sda,buzzvibO,freq=400000):
        self.width = width
        self.height = height
        self.i2c_id = i2c_id
        self.scl = scl
        self.sda = sda
        self.freq = freq
        self.buzzvibO = buzzvibO
        i2c = I2C(self.i2c_id, scl=Pin(scl), sda=Pin(sda), freq=freq)
        self.oled = SH1106_I2C(width, height, i2c, rotate=180)
        self.oled.invert(False)
        self.font_writer_20 = writer.Writer(self.oled, freesans20)
        self.font_writer_30 = writer.Writer(self.oled, firacodeBold30)
#         self.show_boot()
        self.title_height = 12
        self.menu_line = 1 
        self.menu_highlight = 1
        self.menu_shift = 0
        self.menu_list_length = 0
        self.menu_total_lines = 5
        self.lock_state = False
        self.sleep_state = False        
        self.rem_state = False
        self.reminder_time = 0
        self.start_time = 0
        self.progress_fill = 0
    
        
    def init(self):        
        return self.oled
    
    def seconds_to_timestamp(self,seconds):
        if seconds == 0:
            return "Never"
        days = seconds // 86400
        seconds %= 86400
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60    
        if days > 0:
            return "Never"
        elif hour > 0:
            return "{}h {}m".format(hour, minutes)
        else:
            return "{}m {}s".format(minutes, seconds)
        
    def show_boot(self):
#         self.oled.init_display()
#         self.oled.blit(logo_buffer, 20, 10)
        self.font_writer_30.set_textpos(2, 5)
        self.font_writer_30.printstring("WALIORI")
        self.font_writer_20.set_textpos(2, 40)
        self.font_writer_20.printstring("sit/stand desk")
        self.oled.show()
        
    def show_menu(self,menu,line, highlight, shift,total_lines,header,wifi,ap):
        item = 1
        line = 1
        line_height = 10

        # clear the display
        self.oled.fill_rect(0,(line*line_height)+6,self.width,self.height,0)

        # Shift the list of files so that it shows on the display
        list_length = len(menu)
        short_list = menu[shift:shift+total_lines]

        for item in short_list:
            if highlight == line:
                self.oled.fill_rect(0,(line*line_height)+5, self.width,line_height+1,1)
                self.oled.text(">",0, (line*line_height)+6,0)
                self.oled.text(item, 10, (line*line_height)+6,0)
                self.oled.show()
            else:
                self.oled.text(item, 10, (line*line_height)+6,1)
            line += 1
        self.show_header(header,wifi,ap)
        self.show_frame()
        self.oled.show()
    
    def show_static_frame(self,presets,total_lines):
        item = 1
        line = 1
        line_height = 12
        shift = 0
        # clear the display
        self.oled.fill_rect(0,(line*line_height),self.width,self.height,0)

        # Shift the list of files so that it shows on the display
        short_list = presets[shift:shift+total_lines]
        for item in short_list:
            self.oled.text(item, 2, (line*line_height)+10,1)
#             print(item)
            line += 1        
        self.show_frame()
        
            
    def move_menu(self, direction, highlight, shift, menu_list, total_lines, list_length):
        if direction == "up":
            if highlight > 1:
                highlight -= 1  
            else:
                if shift > 0:
                    shift -= 1
        else:
            if highlight < total_lines:
                highlight += 1
            else: 
                if shift+total_lines < list_length:
                    shift += 1
        return highlight, shift
    
    def hide_menu(self,counter):
        self.oled.init_display()
        self.font_writer_30.set_textpos(35, 20)
        self.font_writer_30.printstring(str(counter))
        self.oled.show()
        
    def show_height(self,height):
        self.oled.fill(0)
        h,w = get_avg_char_width_height(height,firacodeBold30)
        x=get_center_x(height,self.width,w)
        y=get_center_y(self.height,h)
        self.font_writer_30.set_textpos(x, y)
        self.font_writer_30.printstring(height)
        self.oled.show()
        
    def show_height_frame(self,height,rpm=0):
        self.clear_frame()
        h,w = get_avg_char_width_height(height,firacodeBold30)
        x=get_center_x(height,self.width,w)
        y=get_center_y(self.height-1+ self.title_height+3,h)
        self.font_writer_30.set_textpos(x, y)
        self.font_writer_30.printstring(height)
        if rpm != 0:
            self.oled.text('RPM: '+str(int(rpm)),60,55)
        if self.reminder_time <= 86400:
            self.oled.blit(alarm_fb, 5, 17)
            self.draw_frame(18,18,100,7)
            self.oled.fill_rect(20,20,self.progress_fill,4,1)
        self.oled.show()
    
    def show_reminder_frame(self):
        self.oled.fill(0)
        self.clear_frame()
        text= ">>>"
        header = "Reminder"
        self.draw_frame(0,0,self.width-1,self.title_height+1)
        self.oled.fill_rect(0,0,self.width-1,self.title_height+1,1)
        h,w = get_avg_char_width_height(text,freesans20)
        x=get_center_x(text,self.width,w)
        y=get_center_y(self.height-1+ self.title_height+3,h)
        self.font_writer_20.set_textpos(x, y)
        self.font_writer_20.printstring(text)
        h,w = get_avg_char_width_height(header)
        x=get_center_x(header,self.width,w)
        y=get_center_y(self.title_height,h)
        self.oled.text(header, x, y,0)        
        y=get_center_y(self.height-1+ self.title_height+3,38)
        self.oled.blit(sit_fb, 5, y)
        self.oled.blit(stand_fb, 83, y)
        self.oled.show()
        
    def show_time_frame(self,time):
        if time > 86400:
            text = "Never"
        else:
            text= self.seconds_to_timestamp(time)
        self.clear_frame()
        h,w = get_avg_char_width_height(text,firacodeBold30)
        x=get_center_x(text,self.width,w)
        y=get_center_y(self.height-1+ self.title_height+3,h)
        self.font_writer_30.set_textpos(x, y)
        self.font_writer_30.printstring(text)
        self.oled.show()
        
    def draw_frame(self, x,y, width, height):
        self.oled.hline(x, y, width, 1)
        self.oled.vline(x, y, height, 1)
        self.oled.hline(x, y+height, width, 1)
        self.oled.vline(x+width, y, height, 1)

    def show_header(self,header,wifi,ap):             
        fb = framebuf.FrameBuffer(wifi, 14, 14, framebuf.MONO_HLSB)
        ap_fb = framebuf.FrameBuffer(ap, 14, 14, framebuf.MONO_HLSB)
        self.draw_frame(0,0,self.width-1,self.title_height+1)
        self.oled.fill_rect(0,0,self.width-1,self.title_height+1,1)
        if self.lock_state:
            lock = bytearray(b'\xff\xfc\xf0\x3c\xe7\x1c\xe7\x9c\xe7\x9c\xc0\x0c\x80\x04\x80\x04\x80\x04\x80\x04\x80\x04\x80\x04\x80\x04\xff\xfc')
        else:
            lock = bytearray(b'\xff\xdc\xff\x04\xfe\x74\xfe\x70\xfe\x70\xfe\x78\x80\x1c\x80\x1c\x80\x1c\x80\x1c\x80\x1c\x80\x1c\x80\x1c\x80\x3c')
        if self.buzzvibO.sound and self.buzzvibO.vibration:
            p = s_and_v_fb
        elif self.buzzvibO.sound and not self.buzzvibO.vibration:
            p= s_no_v_fb
        elif self.buzzvibO.vibration and not self.buzzvibO.sound:
            p = v_fb
        elif not self.buzzvibO.vibration and not self.buzzvibO.sound:
            p = s_fb
        #try to add self.wifi here   
        l_fb = framebuf.FrameBuffer(lock, 14, 14, framebuf.MONO_HLSB)
        self.oled.blit(p, 99, 0)
        self.oled.blit(l_fb, 112, 0)        
        self.oled.blit(fb, 0, 1)
        self.oled.blit(ap_fb, 15, 0)
        h,w = get_avg_char_width_height(header)
        x=get_center_x(header,self.width,w)
        y=get_center_y(self.title_height,h)
        self.oled.text(header, x, y,0)        
        self.oled.show()
        
    def show_frame(self):
        self.draw_frame(0,self.title_height+3,self.width-1,self.height-self.title_height-4)
        self.oled.show()
        
    def clear_frame(self):
        self.oled.fill_rect(2,self.title_height+4,self.width-3,self.width-3,0)
        self.draw_frame(0,self.title_height+3,self.width-1,self.height-self.title_height-4)
#         self.oled.show()

    def text_frame(self, message):
        parts = divide_phrase(message, self.width-4, 8)
        c = 8
        for part in parts:
            self.oled.text(part,2, self.title_height+c )
            c = c + 10
        self.oled.show()
    
    def dim(self):
        self.sleep_state = True
        self.oled.init_display()
    def wake(self):
        self.sleep_state = False
    
    def alarm(self):
        self.sleep_state = False
        self.rem_state = True
    
    def stp_alarm(self):
        self.rem_state = False
        self.progress_fill = 0
        self.oled.invert(False)        
        