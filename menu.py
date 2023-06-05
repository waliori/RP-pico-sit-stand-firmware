class Menu:
    def __init__(self,displayO,calibrationO,motorO):
        self.menu_state = False
        self.displayO = displayO
        self.calibrationO = calibrationO
        self.motorO = motorO
        self.line = 1 
        self.highlight = 1
        self.shift = 0
        self.list_length = 0
        self.total_lines = 5
        self.previous_value = True
        self.button_down = False
        self.reset_state = False
        self.collision_reset_state = False
        self.presets_state = False
        self.wc_state= False
        
#     def show_menu(self,menu):
#         self.displayO.show_menu(menu)
        
    def go_home(self):        
        self.displayO.oled.fill(0)
        self.displayO.show_header("Home")
        self.displayO.show_frame()
        self.displayO.show_height_frame(str(self.calibrationO.real_height(self.motorO.counter)))
        
    def move_menu_encoder(self,step_pin,direction_pin,menu_list,header):
        list_length = len(menu_list)
        tot = min(list_length,self.total_lines)
        if self.previous_value != step_pin.value():
            if step_pin.value() == False:

                # Turned Left 
                if direction_pin.value() == False:
                    if self.highlight > 1:
                        self.highlight -= 1  
                    else:
                        if self.shift > 0:
                            self.shift -= 1  
                # Turned Right
                else:
                    if self.highlight < tot:
                        self.highlight += 1
                    else: 
                        if self.shift+tot < list_length:
                            self.shift += 1
                self.displayO.show_menu(menu_list,self.line, self.highlight, self.shift,tot,header)
            self.previous_value = step_pin.value()
            
    def move_menu_buttons(self, direction, menu_list,header):
        list_length = len(menu_list)
        tot = min(list_length,self.total_lines)
        if direction == "up":
            if self.highlight > 1:
                self.highlight -= 1  
            else:
                if self.shift > 0:
                    self.shift -= 1
        else:
            if self.highlight < tot:
                self.highlight += 1
            else: 
                if self.shift+tot < list_length:
                    self.shift += 1
        self.displayO.show_menu(menu_list,self.line, self.highlight, self.shift,tot,header)
    
#     def move_menu_buttons(self,button,up_button,menu_list): 
#         list_length = len(menu_list)
#         self.button_down = True
#         if button == up_button:
#             self.highlight, self.shift = self.displayO.move_menu("up",self.highlight, self.shift, menu_list, self.total_lines, list_length)
#         else:
#             self.highlight, self.shift = self.displayO.move_menu("down",self.highlight, self.shift, menu_list, self.total_lines, list_length)
#         self.displayO.show_menu(menu_list,self.line, self.highlight, self.shift, list_length,self.total_lines)
