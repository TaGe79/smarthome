import Adafruit_PWM_Servo_Driver
import time

class Redony(object):
    def __init__(self):
        self.nappali_fel = 4
        self.nappali_le = 5
        self.konyha_fel = 7
        self.konyha_le = 6
        self.pwm = self.setup_pwm()

    @staticmethod
    def setup_pwm(freq=1000):
        pwm = Adafruit_PWM_Servo_Driver.PWM()
        pwm.setPWMFreq(freq)
        return pwm

    def redony(self, port, value):
        if value > 0:
            self.pwm.setPWM(port, 4096, 0)
        else:
            self.pwm.setPWM(port, 0, 4096)

#    def redony_nappali_le(self, be_ki):
#        self.pwm.setPWM(self.nappali_le, 0, be_ki)
#
#    def redony_nappali_fel(self, be_ki):
#        self.pwm.setPWM(self.nappali_fel, 0, be_ki)
#
#    def redony_konyha_le(self, be_ki):
#        self.pwm.setPWM(self.konyha_le, 0, be_ki)
#
#    def redony_konyha_fel(self, be_ki):
#        self.pwm.setPWM(self.konyha_fel, 0, be_ki)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='konyha nappali')

    parser.add_argument('-p','--port', type=int,choices=range(4,8), default=0, help="4: nappali le, 5: nappali fel, 6: konyha le, 7 konyha fel")
    # parser.add_argument('-v','--value',nargs=4, type=int,choices=range(0,2), default=[0,0,0,0])
    parser.add_argument('-v','--value', type=int,choices=range(0,2), default=0)
    #parser.add_argument('-kl', '--konyha_le',  type=int, choices=range(0,2), default=1, help="Ki:1,be:0")
    #parser.add_argument('-kf', '--konyha_fel', type=int, choices=range(0,2), default=1, help="Ki:1,be:0")
    #parser.add_argument('-nl', '--nappali_le', type=int, choices=range(0,2), default=0, help="Ki:0,be:1")
    #parser.add_argument('-nf', '--nappali_fel',type=int, choices=range(0,2), default=0, help="Ki:0,be:1")

    args = parser.parse_args()

    driver = Redony()
    #driver.redony(4,0)
    #driver.redony(5,0)
    #driver.redony(6,0)
    #driver.redony(7,0)
    
    #for p in range(4,8):
    driver.redony(args.port, args.value)
    
    #driver.redony_nappali_le(args.nappali_le*4095)
    #driver.redony_nappali_fel(args.nappali_fel*4095)
    #driver.redony_konyha_le(args.konyha_le*4095)
    #driver.redony_konyha_fel(args.konyha_fel*4095)    
