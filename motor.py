import utime
import json
import uasyncio as asyncio

class Motor:
    def __init__(self, pwm1, pwm2, counter,sLock,accelO,curr_sens):
        self.pwm1 = pwm1
        self.pwm2 = pwm2
        self.counter = counter   # counter updates when encoder rotates
        self.last_counter = 0
        self.outA_last = 0 # registers the last state of outA pin / CLK pin
        self.outA_current = 0 # registers the current state of outA pin / CLK pin
        self.direction = 0 # 0 for stopped, 1 for clockwise, -1 for counterclockwise
        self.sLock = sLock
        self.curren_position = counter
        self.api = False
        self.rpm_up = 0
        self.rpm_down = 0
        self.sens_list_tresh = 9999999
        self.sens_tresh = 0
        self.block_err_cnt = 0
        self.last_pulse = 0
        self.ietrations = 0
        self.current_counter = self.counter
        self.srt = 0
        self.statesrota = 20 #encoder
        self.blocked = False
        self.rpm = 0
        self.avg_rpm=0
        self.rpm_running_sum = 0
        self.rpm_reading_count = 0
        self.current_direction = None
        self.current_duty = 0
        self.curr_sens = curr_sens
        self.curr = 0
        self.running_sum = 0
        self.reading_count = 0
        self.avg_current = 0
        self.peak_current = 0
        self.current_threshold = 0        
        self.accelO = accelO        
        self.accel = (0,0,0)
        self.avg_xyz = (0,0,0)
        self.xyz_running_sum = (0, 0, 0)
        self.xyz_reading_count = 0
        self.collision_count = 0
        
    def move_motor_forward(self,outA,outB,maxi):
        for duty in range(0,65025,5):
            if self.counter >= (maxi):
                self.stop_motor()
                break
            self.pwm1.duty_u16(duty)
            self.f_en(outA)
#             utime.sleep_us(1)
    
    def slow_motor_forward(self,outA,outB,maxi):
        for duty in range(65025, 0, -5):
            if self.counter >= (maxi - 15):
                self.stop_motor()
                break
            self.pwm1.duty_u16(duty)
            self.f_en(outA)
        self.rpm = 0
#             utime.sleep_us(1)

    def is_moving(self):
        return self.direction != 0
            
    def move_motor_backward(self,outA,outB,mini):
        for duty in range(0,65025,5):
            if self.counter <= (mini):
                self.stop_motor()
                break
            self.pwm2.duty_u16(duty)
            self.b_en(outA)
#             utime.sleep_us(1)
        
    def slow_motor_backward(self,outA,outB,mini):
        for duty in range(65025, 0, -5):
            if self.counter <= (mini):
                self.stop_motor()
                break
            self.pwm2.duty_u16(duty)
            self.b_en(outA)
        self.rpm = 0
#             utime.sleep_us(1)
        
    def stop_motor(self):
        self.pwm1.duty_u16(0)
        self.pwm2.duty_u16(0)
        self.rpm = 0
        
    def save_position(self):
        self.sLock.acquire()
        self.curren_position = self.counter
        file=open("state.json","w")
        file.write(json.dumps({"current_encoder":self.counter}))
        self.sLock.release()
        
    def set_curr_tresh(self):            
        current = self.curr
        self.running_sum += current
        self.reading_count += 1
        self.avg_current = self.running_sum / self.reading_count
        self.peak_current = max(self.peak_current, current)
        self.current_threshold = self.avg_current + 0.2*(self.peak_current - self.avg_current)
    
    def set_rpm_tresh(self):
        rpm = self.rpm
        self.rpm_running_sum += rpm
        self.rpm_reading_count += 1
        self.avg_rpm = self.rpm_running_sum / self.rpm_reading_count
    
    def set_accel_tresh(self):
        accel = self.accel
        self.xyz_running_sum = tuple(map(sum, zip(self.xyz_running_sum, accel)))
        self.xyz_reading_count += 1
        self.avg_xyz = tuple(x / self.xyz_reading_count for x in self.xyz_running_sum)
        
    def rpm_updt(self):
        if self.current_counter != self.counter:
            self.curr = self.curr_sens.read_current()
            self.accel = self.accelO.read_accel_data()
            self.set_curr_tresh()
            self.set_rpm_tresh()
            self.set_accel_tresh()
            self.current_counter = self.counter            
            self.last_pulse += 1
            timediff = round((utime.ticks_us() - self.srt)/1_000,2)
            if timediff >= 100:
                rps = round((self.last_pulse/timediff)*self.statesrota,1)
                self.rpm = round(rps*60,1)               
                self.last_pulse=0
                self.ietrations= 0
                self.srt = utime.ticks_us()
                
                
                
    def f_en(self,outA):
        self.outA_current = outA.value()
        if self.outA_current != self.outA_last:
            self.counter += 1
        self.outA_last = self.outA_current
        self.rpm_updt()
        
    def b_en(self,outA):
        self.outA_current = outA.value()
        if self.outA_current != self.outA_last:
            self.counter -= 1
        self.outA_last = self.outA_current
        self.rpm_updt()

    def encoder(self,outA,outB,collision=False):
        self.outA_current = outA.value()
        if self.outA_current != self.outA_last:
            if outB.value() != self.outA_current:
                self.counter -= 1
            else:
                self.counter += 1
        self.outA_last = self.outA_current
        self.rpm_updt()
        utime.sleep_us(1)
        
    def move_motor(self, button, up_button,outA, outB, mini ,maxi, collision=False):
        debounce_time = 50  # Debounce time in milliseconds
        debounce_start = 0  # Timestamp of debounce start
        debounce_duration = debounce_time * 1000  # Debounce duration in microseconds        
        self.last_pulse=0       
        self.running_sum = 0
        self.reading_count = 0
        self.last_counter= 0
        self.avg_rpm=0
        self.rpm_running_sum = 0
        self.rpm_reading_count = 0
        self.avg_xyz = (0,0,0)
        self.xyz_running_sum = (0, 0, 0)
        self.xyz_reading_count = 0
        self.srt= utime.ticks_us()
        if not mini or not maxi:
            mini=-9999999
            maxi=9999999        
        self.block_err_cnt = 0
        self.current_readings = []
        while True:            
            if button.value() == 0:
                if self.blocked:
                    self.stop_motor()
                if debounce_start == 0:
                    debounce_start = utime.ticks_us()
                elif utime.ticks_diff(utime.ticks_us(), debounce_start) > debounce_duration:
                    if(button == up_button):
                        if self.direction == 0 and not self.counter >= maxi:
                            if self.counter >= (maxi - 15):
                                self.stop_motor()                            
                            self.move_motor_forward(outA,outB,maxi - 15)
                            self.direction = 1                                
                    else:
                        if self.direction == 0 and not self.counter <= mini:
                            if self.counter <= (mini + 15):
                                self.stop_motor()
                            self.move_motor_backward(outA,outB,mini + 15)
                            self.direction = -1
                    debounce_start = 0
            if button.value() != 0:
                if self.blocked:
                    self.stop_motor()
                if (self.counter >= (mini + 30) and self.counter <= (maxi -30)) and not self.blocked:
                    if button == up_button:
                        self.slow_motor_forward(outA,outB,maxi -30)
                    else:
                        self.slow_motor_backward(outA,outB,mini + 30)
                else:
                    self.stop_motor()
                self.direction = 0
                self.ietrations = 0
                self.save_position()
                debounce_start = 0
                break
            self.encoder(outA,outB,collision)
            
    def move_motor_height(self, direction,outA, outB, height):
        self.pwm1.duty_u16(0)  # Start with both motor channels stopped.
        self.pwm2.duty_u16(0)
        duty = 0
        while True:
            if direction == "up":
                if self.counter >= height:
                    for duty in range(duty, -1, -3):
                        self.pwm1.duty_u16(duty)
                        utime.sleep_us(1)
                    self.save_position()
                    self.rpm=0
                    break
                elif duty < 65025:  # Ramp up to full speed.
                    duty += 10
                    self.pwm1.duty_u16(duty)
                    self.f_en(outA)
                self.f_en(outA)  # Update encoder readings
            else:
                if self.counter <= height:
                    for duty in range(duty, -1, -3):
                        self.pwm2.duty_u16(duty)
                        utime.sleep_us(1)
                    self.save_position()
                    self.rpm=0
                    break
                elif duty < 65025:  # Ramp up to full speed.
                    duty += 10
                    self.pwm2.duty_u16(duty)
                    self.b_en(outA)
                self.b_en(outA)  # Update encoder readings
            utime.sleep_us(1)
            
    #TODO change api to be like non-api        
    async def encoder_api(self,outA,outB):
        self.outA_current = outA.value()
        if self.outA_current != self.outA_last:
            if outB.value() != self.outA_current:
                self.counter -= 1
            else:
                self.counter += 1 
        self.outA_last = self.outA_current
        await asyncio.sleep_ms(1)
        
    async def move_motor_api(self, direction,outA, outB, mini, maxi):
        self.pwm1.duty_u16(0)  # Start with both motor channels stopped.
        self.pwm2.duty_u16(0)      
        duty = 0
        while self.api:
            if(direction == "up"):
                if self.counter >= maxi-10:
                    self.api = False
                    # Gradual stop
                    for duty in range(duty, -1, -50):
                        self.pwm1.duty_u16(duty)
                        await asyncio.sleep_ms(1)
                    self.save_position()
                    break
                elif duty < 65025:  # Ramp up to full speed.
                    duty += 50  # Increase step size for faster ramp-up.
                    self.pwm1.duty_u16(duty)  # Assuming PWM1 controls 'up' direction.
                self.f_en(outA)  # Update the encoder counter
            else:
                if self.counter <= mini+10:
                    self.api = False
                    for duty in range(duty, -1, -50):
                        self.pwm2.duty_u16(duty)
                        await asyncio.sleep_ms(1)
                    self.save_position()
                    break
                elif duty < 65025:  # Ramp up to full speed.
                    duty += 50  # Increase step size for faster ramp-up.
                    self.pwm2.duty_u16(duty)  # Assuming PWM2 controls 'down' direction.
                self.b_en(outA)  # Update the encoder counter
            self.current_direction = direction  
            self.current_duty = duty
            await asyncio.sleep_ms(1)
            
    async def stop_motor_api(self,outA, outB):
        self.api = False
        # Gradual stop
        if self.current_direction == "up":
            for duty in range(self.current_duty, -1, -50):
                self.pwm1.duty_u16(duty)
                self.f_en(outA)  # Update the encoder counter while slowing down
                await asyncio.sleep_ms(1)
        else: 
            for duty in range(self.current_duty, -1, -50):
                self.pwm2.duty_u16(duty)
                self.b_en(outA)  # Update the encoder counter while slowing down
                await asyncio.sleep_ms(1)
        self.save_position()