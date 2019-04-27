
from motor_inducao import Motor3PhY
from carga import CargaRotativa
from fonte import Fonte3Ph
from graficos import get_graphico
from threading import Timer

class MotorSimu:
    class States:
        STOPPED  = 0
        RUNNING  = 1
        PAUSED   = 2
        STOPPING = 3
    
    def __init__(self):
        self.motor = Motor3PhY()
        self.carga = CargaRotativa()
        self.fonte = Fonte3Ph()
        self.__state = MotorSimu.States.STOPPED
        self.__timestamp = 0
        self.__dt = 0.01
        self.__t1 = 0
        self.__t2 = 1
    
    def simular(self, t2=1, dt=0.1):
        self.__t2 = t2
        self.__dt = dt
        t = self.__t1
        s = 1
        rpm = 0
        wo = 0
        w = 0
        values = [[],[],[],[]]
        while t < self.__t2:            
            to = t
            mvalues = self.motor.get_values(s)
            values[0].append(mvalues['torque'])
            values[1].append(mvalues['hp'])
            values[2].append(mvalues['corrente'])
            values[3].append(mvalues['rpm'])
            t += self.__dt
            wo = w
            w = self.carga.get_rpm(mvalues['torque'], to, t, wo, mvalues['w-max'])
            s = (mvalues['w-sinc'] - w) / mvalues['w-sinc']
            if s > 1: s = 1
        
        gr = get_graphico(values, self.__t2, self.__dt, 's',
                ['blue','red','#33DDFF','#8B6914'], [250,50,300,2000], 
                ['Conjugado','Potência(HP)','Corrente','RPM'])
    
    def __next_step(self):
        if self.__state == MotorSimu.States.STOPPING:
            self.__state = MotorSimu.States.STOPPED
        else:
            if self.__state == MotorSimu.States.RUNNING:
                pass
            Timer(self.__next_step, 0.1).start()
    
    def start(self):
        if self.__state == MotorSimu.States.STOPPING:
            return
        if self.__state == MotorSimu.States.STOPPED:
            self.__timestamp = 0
            Timer(self.__next_step, 0.1).start()
        self.__state = MotorSimu.States.RUNNING
        print('Simulação rodando...')
    
    def pause(self):
        if self.__state != MotorSimu.States.RUNNING:
            return
        self.__state = MotorSimu.States.PAUSED
        print('Simulação pausada.')

    def stop(self):
        if self.__state in (MotorSimu.States.STOPPED, MotorSimu.States.STOPPING):
            return
        self.__state = MotorSimu.States.STOPPING
        while self.__state ==  MotorSimu.States.STOPPING: pass
        print('Simulação parada.')


if __name__ == "__main__":
    simu = MotorSimu()
    simu.motor.set_paramentros(220,60,6,0.294,0.503,13.25,0.209,0.144,403)
    while True:
        try:
            m = float(input('massa da carga: '))
            simu.carga.I = (m*0.2*0.2) / 2 #momento de inércia de um disco de massa de m e raio de 0.2m.
            Tr = float(input('torque da carga: '))
            simu.carga.f_torque = lambda w: Tr
            config = input('Tempos(t2, dt): ').split(',')
            simu.simular(float(config[0]), float(config[1]))
        except Exception as ex:
            print(ex)
        if input('Continuar?(s/n): ') == 'n': break

