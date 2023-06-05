import json
class Presets:
    def __init__(self, motorO,calibrationO,sLock):
        self.motorO = motorO
        self.calibrationO = calibrationO
        self.sLock = sLock
        self.sLock.acquire()
        try:    
            presetsf = open("presets.json","r")
            presets_json = json.loads(presetsf.read())
            self.presets = presets_json
#             print(presets_json)
        except:
            self.presets = {}
            file=open("presets.json","w")
            file.write(json.dumps({}))
        self.sLock.release()
    
    def get_preset(self,preset):
        presets = open("presets.json","r")
        prestes_json = json.loads(presets.read())
        if not prestes_json:
            return False
        return prestes_json[preset]
    
    def set_preset(self,preset):
        self.sLock.acquire()
        presets = open("presets.json","r")
        prestes_json = json.loads(presets.read())
        prestes_json[preset] = self.motorO.counter
        self.presets = prestes_json
        file=open("presets.json","w")
        file.write(json.dumps(prestes_json))
        print("saved presets file with", str(self.motorO.counter), ' in ', preset)
        self.sLock.release()
    
    def go_preset(self, outA, outB, preset):
        if self.motorO.curren_position > preset:
            self.motorO.move_motor_height("down",outA, outB, preset)
        else:
            self.motorO.move_motor_height("up",outA, outB, preset)

        
