from machine import Pin, I2C
from sh1106 import SH1106_I2C
import framebuf
import freesans20
import firacodeBold30
import writer
import base64
import math

#display

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
    def __init__(self,width,height,i2c_id,scl,sda,freq=400000):
        self.width = width
        self.height = height
        self.i2c_id = i2c_id
        self.scl = scl
        self.sda = sda
        self.freq = freq
        i2c = I2C(1, scl=Pin(scl), sda=Pin(sda), freq=freq)
        self.oled = SH1106_I2C(width, height, i2c)
        self.font_writer_20 = writer.Writer(self.oled, freesans20)
        self.font_writer_30 = writer.Writer(self.oled, firacodeBold30)
        self.title_height = 12
        self.show_boot()
        self.menu_line = 1 
        self.menu_highlight = 1
        self.menu_shift = 0
        self.menu_list_length = 0
        self.menu_total_lines = 5
        self.lock_state = False
        self.sleep_state = False

    
        
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
        def custom_to_buff(data):
            width = data[0]
            height = data[1]
            fbuff = framebuf.FrameBuffer(data[2:],width,height, framebuf.MONO_HLSB)
            return fbuff
              
        def show_image(image):
            oled.blit(image, 0, 0)
            oled.show()
            
        logo_base64="gCIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP+AAAAAAAAAAAAAAAAAAAA/gPAAAAAAAB4AAAAAAAAAP4P4AAAAAAA/AAAAAAAAAD+D+AAAAAAAP4AAAAAAAAA/g/gAAAAAAD+AAAAAAAAAP4P4AAAAAAA/gAAAAAAAAD+B+AAAAAAAPwAAAAAAAAA/gOAAAAAAAB4AAAAAAAAAP4AAAAAAAAAAAAAAAAAAAD+AAAAAAAAAAAAAAAAAbwA/gAAB+AAAeAAB/A/AQ8fAP4P4B48B/Lw/gfwP4EfH4D+D+B8Pgf0eP4H+D+AH5/A/g/g/D8H+Pj+A/g/gh+fwP4P4Pw/h/H4/gP4P4Ifn8D+D+H8P4fx+P4D/D/CH5/A/g/h/D+H8fD+Afw/wA4fwP4P4fw/x/Bg/gH8D8QAH8D+D+H8P8fwAP4B/E/EAB/A/g/h/D/H8AD+AP5P4A/fwP4P4fw/x/AA/gD+D+gfj8D+D+H8P4fwAP4A/ofoP5/A/g/h/D+H8AD+AH+H+D+PwP4P4fw/h/AA/gB/h/A/n8D+D+D8P4fwAP4AfwPwP5/A/g/g/D8H8AD+AD8D8D+f6P4P4Hw+B/AA/gA/A/Af7/D+D+AePAfwAP4AAAAAB4PgAAAAA+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        logo_buffer = custom_to_buff(bytearray(base64.b64decode(logo_base64)))
        self.oled.init_display()
        self.oled.blit(logo_buffer, -3, 0)
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
        list_length = len(presets)
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
        x=get_center_x(height,128,w)
        y=get_center_y(64,h)
        self.font_writer_30.set_textpos(x, y)
        self.font_writer_30.printstring(height)
        self.oled.show()
        
    def show_height_frame(self,height,rpm=0):
        text= height
        self.clear_frame()
        h,w = get_avg_char_width_height(height,firacodeBold30)
        x=get_center_x(text,128,w)
        y=get_center_y(self.height-1+ self.title_height+3,h)
        self.font_writer_30.set_textpos(x, y)
        self.font_writer_30.printstring(text)
        if rpm != 0:
            self.oled.text('RPM: '+str(int(rpm)),60,55)
        self.oled.show()

    def show_sleep_frame(self,time):
        if time > 86400:
            text = "Never"
        else:
            text= self.seconds_to_timestamp(time)
        self.clear_frame()
        h,w = get_avg_char_width_height(text,firacodeBold30)
        x=get_center_x(text,128,w)
        y=get_center_y(self.height-1+ self.title_height+3,h)
        self.font_writer_30.set_textpos(x, y)
        self.font_writer_30.printstring(text)
        self.oled.show()
        
    def draw_frame(self, x,y, width, height):
        self.oled.hline(x, y, width, 1)
        self.oled.vline(x, y, height, 1)
        self.oled.hline(x, height, width, 1)
        self.oled.vline(width, y, height+1, 1)

    def show_header(self,header,wifi,ap):             
        fb = framebuf.FrameBuffer(wifi, 14, 14, framebuf.MONO_HLSB)
        ap_fb = framebuf.FrameBuffer(ap, 16, 16, framebuf.MONO_HLSB)
        self.draw_frame(0,0,self.width-1,self.title_height+1)
        self.oled.fill_rect(0,0,self.width-1,self.title_height+1,1)
        if self.lock_state:
            lock = bytearray(b'\xff\xfc\xf0\x3c\xe7\x1c\xe7\x9c\xe7\x9c\xc0\x0c\x80\x04\x80\x04\x80\x04\x80\x04\x80\x04\x80\x04\x80\x04\xff\xfc')
        else:
            lock = bytearray(b'\xff\xdc\xff\x04\xfe\x74\xfe\x70\xfe\x70\xfe\x78\x80\x1c\x80\x1c\x80\x1c\x80\x1c\x80\x1c\x80\x1c\x80\x1c\x80\x3c')
        #try to add self.wifi here   
        l_fb = framebuf.FrameBuffer(lock, 14, 14, framebuf.MONO_HLSB)
        self.oled.blit(l_fb, 112, 0)
        self.oled.blit(fb, 0, 1)
        self.oled.blit(ap_fb, 15, 0)
        h,w = get_avg_char_width_height(header)
        x=get_center_x(header,self.width,w)
        y=get_center_y(self.title_height,h)
        self.oled.text(header, x, y,0)        
        self.oled.show()
        
    def show_frame(self):
        self.draw_frame(0,self.title_height+3,self.width-1,self.height-1)
        self.oled.show()
        
    def clear_frame(self):
        self.oled.fill_rect(2,self.title_height+4,self.width-3,self.width-3,0)
        self.draw_frame(0,self.title_height+3,self.width-1,self.height-1)
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
        
    