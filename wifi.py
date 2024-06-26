"""
author: waliori
"""
import time
import network
import json
import uasyncio as asyncio
from microdot_asyncio import redirect
import machine
# import socket

#wifi logo
y_ico = bytearray(b'\xff\xff\xff\xff\xf8\x1f\xe3\xc7\xcf\xf3\xfe\x7f\xf8\x1f\xf7\xef\xff\xff\xfe\x7f\xfe\x7f\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00')
n_ico = bytearray(b'\xff\xff\x98\x1f\xc1\x87\xf7\xf1\xbb\xfd\xfc\x1f\xf6\x0f\xe7\x27\xff\xdf\xfe\x67\xfe\x73\xfe\x79\xff\xff\x00\x00\x00\x00\x00\x00')

#ap logo
y_a_ico = bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xcf\xf3\xdf\xfb\xd3\xcb\x96\x69\x96\x69\xd3\xcb\xdf\xfb\xcf\xf3\xff\xff\xff\xff\xff\xff\xff\xff')
n_a_ico = bytearray(b'\xff\xff\xff\xff\xdf\xff\xef\xff\xe7\xe7\xe3\xf7\xc9\x93\xd8\xdb\xdb\x5b\xc9\xb3\xef\xd7\xe7\xef\xff\xf7\xff\xfb\xff\xff\xff\xff')
class Wifi:    
    def __init__(self,app,sLock,displayO,menuO):
        self.sLock = sLock
        self.displayO = displayO
        self.menuO = menuO
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.config(pm = 0xa11140)
        self.apssid = "PicoW"
        self.appassword = "waliori123"
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(False)
        self.aps = n_a_ico
        self.ap.config(essid=self.apssid, password=self.appassword)
        self.string = ""
        self.app = app
        self.server = False
        self.connected = False
        self.apmode = False
        self.open = False # to True if we want open wifi suport
        self.nearby = []
        if self.wlan.isconnected():
            self.wifi = y_ico
            self.ssid = self.wlan.config("ssid")
            self.ip = self.wlan.ifconfig()[0]
        else:
            self.wifi = n_ico
            self.ip = ""
            self.ssid = ""

            
           
#         self.saved                
        try:
            print("try")
            self.sLock.acquire()
            saved = open("saved_wifi.json","r")
            self.saved_json = json.loads(saved.read())
            print(self.saved_json)
            self.sLock.release()
        except:
            print("except")
            self.sLock.release()
            self.sLock.acquire()
            file=open("saved_wifi.json","w")
            file.write(json.dumps({}))
            self.saved_json = {}
            self.sLock.release()
        
    def go_home(self,real_height,counter):
        self.sLock.acquire()
        self.menuO.go_home(self.wifi,self.aps,real_height,counter)
        self.sLock.release()
        
    def nearby_wifis(self):
        networks = self.wlan.scan()
        self.nearby = ["Go back"]
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            if encrypted:
                if self.saved_json:
                    if ssid in self.saved_json:
                        self.nearby.append(ssid)
            else:  # open
                if self.open:
                    self.nearby.append(ssid)
        self.nearby.append("Scan again")
        if self.wlan.isconnected() and self.wlan.config("ssid") in self.nearby:
            self.nearby.remove(self.wlan.config("ssid"))
            self.nearby.insert(len(self.nearby)-1,"Show IP")
            self.nearby.insert(len(self.nearby)-1,"Disconnect")
            self.nearby.insert(len(self.nearby)-1,"Toggle API")
        else:
            print("AP state")
            print(self.ap.active())
            if self.apmode: #self.ap.active():
                self.nearby.insert(len(self.nearby)-1,"Stop AP")
            else:
                self.nearby.insert(len(self.nearby)-1,"Start AP")
        
        self.nearby.insert(len(self.nearby)-1,"Saved WiFi")
    

    
    async def start_connection(self,real_height,counter):
        if self.wlan.isconnected():
            self.connected = True
            self.wifi = y_ico
            self.aps = n_a_ico
            print("already connected to ", self.wlan.ifconfig())
            self.go_home(real_height,counter)
        try:
            networks = self.wlan.scan()
            for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
                ssid = ssid.decode('utf-8')
                print(ssid,hidden)
                encrypted = authmode > 0
                if encrypted:
                    if self.saved_json:
                        if ssid in self.saved_json:
                            password = self.saved_json[ssid]
                            self.connected = self.connect(ssid, password)
                        else:
                            print("skipping unknown encrypted network")
                else:  # open
                    if self.open:
                        self.connected = self.connect(ssid, None)
                if self.connected:
                    print("connected to ", self.wlan.ifconfig())
                    self.wifi = y_ico
                    self.aps = n_a_ico
                    self.go_home(real_height,counter)
                    break                   
        except Exception as e:
            print("Error here MF:", str(e))
        if not self.connected:
            self.connected = await self.apserver(real_height,counter)
            if self.connected:
                self.stop()
                self.go_home(real_height,counter)
            else:
                self.go_home(real_height,counter)
                return False

    
    #<style>.center{display:flex;justify-content:center;align-items:center;flex-direction:column}body{display:flex;flex-direction:column;min-height:100vh;position:relative;font-family:Arial,sans-serif;padding:20px}form{width:80%;max-width:600px;margin:0 auto;padding:20px;border-radius:10px;background-color:#f5f5f5}legend{font-size:1.2em;font-weight:700;margin-bottom:10px}input[type=radio]{display:inline-block;margin-right:10px}label{display:inline-block;padding-bottom:5px}hr{border:none;height:1px;background-color:#ccc;margin:10px 0}input[type=submit]{background-color:#4caf50;color:#fff;padding:12px 20px;border:none;border-radius:4px;cursor:pointer;margin-top:20px}input[type=submit]:hover{background-color:#45a049}ul{list-style:none;padding:0;margin:0;text-align:center}li{display:inline-block;margin:20px}a{color:#333;text-decoration:none;font-size:1.2em}a:hover{color:#4caf50}.label-radio-container{display: flex;align-items: center;}</style>
    def htmlssid(self):
        def generate_html():
            yield """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Title Example</title></head><body><h3>WiFi Setup by <a href="https://walior.it" target="_blank">waliori</a></h3><p>if the connection is successful the pico will soft reboot</p><form action="/save" method="post" class="center"><fieldset><legend>Choose your new ssid and enter your password </legend><i id="error" style="color:red;" hidden>Error connecting, try again</i><div><div class="center"><div id="ssids" style="display: inline-grid;"><hr>"""
            ssids = sorted(ssid.decode('utf-8') for ssid, *_ in self.wlan.scan())
            ssids_near=[]
            while len(ssids):            
                ssid = ssids.pop(0)
                if ssid != "" and ssid not in self.saved_json:                    
                    yield """<div class="label-radio-container"><input type="radio" id="{0}" name="ssid" value="{0}"><label for="{0}">{0}</label></div>""".format(ssid)
                if ssid in self.saved_json:
                    ssids_near.append(ssid)
            yield """<hr></div><div class="center"><label for="password">Password:</label><input type="password" id="password" name="password"></div></fieldset><div class="center"><input type="submit" value="Submit"><button type="button" onclick="window.location.href = window.location.href.split('?')[0]">Can't see your wifi, Refresh the list</button></div></form><div class="center"><form action="/connect" method="post" class="center"><fieldset><legend>Already saved wifi near you</legend>"""
            while len(ssids_near):
                ssid = ssids_near.pop(0)
                password = self.saved_json[ssid]
                yield """<input type="radio" id="{0}" name="ssid2" value="{0}"><label for="{0}">{0}</label><input type="password" id="password2" name="password2" value="{1}">""".format(ssid,password)
            yield  """</fieldset><input type="submit" value="Connect"></form></div><script>if(window.location.search != ""){document.getElementById("error").hidden = false}</script>"""
        return ''.join(generate_html())
    
    def forget_wifi(self,ssid):
        self.sLock.acquire()
        wifis = open("saved_wifi.json","r")
        wifis_json = json.loads(wifis.read())
        wifis.close()
        print(wifis_json)
        del wifis_json[ssid]
        print(wifis_json)
        file=open("saved_wifi.json","w")
        file.write(json.dumps(wifis_json))
        file.close()
        self.saved_json = wifis_json
        self.sLock.release()
    
    async def savewifi(self,ssid,password):
        if self.connect(ssid,password):            
            self.sLock.acquire()
            wifis = open("saved_wifi.json","r")
            wifis_json = json.loads(wifis.read())
            wifis.close()
            print(wifis_json)
            wifis_json[ssid] = password
            file=open("saved_wifi.json","w")
            file.write(json.dumps(wifis_json))
            file.close()
            self.saved_json = wifis_json
            self.sLock.release()
            return True
        else:
            return False
        
            
            
        @app.route('/connect',methods=['POST'])
        def connect(request):
            connected = self.connect(request.form.get("ssid2"), request.form.get("password2"))
            if connected:
                self.stop()
                self.go_home(real_height,counter)
                try:
                    return "Success, restarting...", 200
                finally:
                    print("restarting")
            else:
                return redirect('/?error=true')
            
        
        app.run(port=80,debug=True)
        self.app = app
        
        
    async def apserver(self,real_height,counter):
        if self.wlan.isconnected():
            self.stop()
            self.go_home(real_height,counter)
        self.apmode = True
        self.ap.active(True)
        self.aps = y_a_ico
        if self.server:#TODO check diff between server and apmode
            self.app.shutdown()
            self.server = False
        app = self.app
        print('Connect to WiFi ssid ' + self.apssid + ',password: ' + self.appassword)
        print('and access 192.168.4.1 with a web browser')
                
        html = self.htmlssid
        @app.route('/')
        async def hello(request):
            return html(), 200, {'Content-Type': 'text/html'}


        @app.route('/save', methods=['POST'])
        async def save(request):
            correct = await self.savewifi(request.form.get("ssid"), request.form.get("password"))
            print(correct)
            if correct:
                success = """ <html><center><br><br><h1><span>successfully connected to WiFi network {0}.</span></h1><br><br></center></html> """.format(request.form.get("ssid"))
                self.stop()
                self.go_home(real_height,counter)
                return success, 200, {'Content-Type': 'text/html'}
            else:
                self.go_home(real_height,counter)
                return redirect('/?error=true')
            
            
        @app.route('/connect',methods=['POST'])
        async def connect(request):
            connected = self.connect(request.form.get("ssid2"), request.form.get("password2"))
            if connected:
#                 try:
#                     return "Success, restarting...", 200
#                 finally:
#                     print("restarting")
                self.stop()
                self.go_home(real_height,counter)
            else:
                self.go_home(real_height,counter)
                return redirect('/?error=true')
            
        app.run(port=80,debug=True)
        self.app = app
        self.server = True
    
    
    
    def stop(self):
        if self.apmode:
            self.app.shutdown()
            self.server = False
        self.ap.active(False)
        print(self.ap.active())
        self.apmode = False
        self.aps = n_a_ico
                
        
    def disconnect(self):
        self.wlan.disconnect()
        self.wifi = n_ico        
        self.ip = ""
        self.ssid = ""
        self.connected = False
        
    def connect(self, ssid, password, retries=100, verbose = True):        
        self.sLock.acquire()
        if ssid != self.ssid:
            self.wlan.disconnect()
            print(self.wlan.isconnected())
            self.wifi = n_ico        
            self.ip = ""
            self.ssid = ""
        else:
            if self.wlan.isconnected():
                self.wifi = y_ico
                self.stop()
                self.sLock.release()
                return True                
        self.string = ""
        self.wlan.connect(ssid, password)
        if verbose:
            self.string ='Connecting to ' + ssid
            print('Connecting to ' + ssid, end=' ')
        
        self.displayO.oled.fill(0)
        self.displayO.show_frame()
        self.displayO.show_header("Wifi",self.wifi,self.aps)
        dots=""            
        while retries > 0 and self.wlan.status() != network.STAT_GOT_IP:
            retries -= 1
            dots += "."
            s = ["Connecting to", ssid,dots]
            self.displayO.show_static_frame(s,len(s))        
            self.displayO.oled.show()
            if retries %3 == 0:
                dots=""
            if verbose:
                self.string += '.'
                print('.', end='')
            time.sleep(0.1)
        if self.wlan.status() == network.STAT_GOT_IP:
            self.ip = self.wlan.ifconfig()[0]
            self.ssid = ssid
            self.wifi = y_ico
            self.stop()
        self.sLock.release()
        return self.wlan.isconnected()
    
    async def serve(self,operation):
        if operation == "start":
            if self.wlan.isconnected():
                print('Starting microdot app')
                try:
                    self.server = True
                    self.aps = y_a_ico
                    self.app.run(port=80, debug=True)                    
                except:
                    self.server = False
                    self.aps = n_a_ico
                    self.app.shutdown()                    
                else:
                    print("not connected to wifi")
        else:
            self.aps = n_a_ico
            self.app.shutdown()
            self.server = False
            
    #rewrite
#     def connect(self, retries=50, verbose = True):
#         self.string = ""
# #         self.wlan.active(True)
#           # Disable power-save mode
#         self.wlan.connect(self.ssid, self.password)
#         if verbose:
#             self.string ='Connecting to ' + self.ssid
#             print('Connecting to ' + self.ssid, end=' ')
#             
#         while retries > 0 and self.wlan.status() != network.STAT_GOT_IP:
#             retries -= 1
#             if verbose:
#                 self.string += '.'
#                 print('.', end='')
#             time.sleep(1)    
#             
#         if self.wlan.status() == network.STAT_GOT_IP:
#             self.ip = self.wlan.ifconfig()[0]
#             print('\nConnected. Network config: ', self.wlan.ifconfig())
#         else:
#             print('\nFailed. Not Connected to: ' + ssid)
#         return self.wlan.isconnected()

    
    

