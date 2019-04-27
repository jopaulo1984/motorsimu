#!/usr/bin/python3
#coding: utf-8

from misc import *
import math

x2PI = 2 * math.pi
RAIZ_3 = math.sqrt(3)

def format_complex(value):
  x, y = value
  return ("%0.2f + j%0.2f" % (x, y)).replace('.',',')

class Motor3Ph:
    def __init__(self, polos=4, freq=60, perdas=100):
        
        self.__w_rotor = 0
        self.get_s = lambda: (self.__w_s - self.__w_rotor) / self.__w_s

        #componentes do circuito equivalente
        self.set_parametros(220,60,4,1,1,1,1,1)
    
    def set_parametros(self, Vn, freq, polos, r1, x1, xo, x2, r2, perdas=0,Mrotor=(10*0.1*0.1)/2):
        self.__Vn = Vn
        self.__Vf = self.get_tensao_fase(Vn)
        self.__freq = freq
        self.__polos = polos
        self.__perdas = perdas
        self.__r1 = r1
        self.__x1 = x1
        self.__xo = xo
        self.__x2 = x2
        self.__r2 = r2
        self.__rev_s = (2 * self.__freq) / self.__polos
        self.__rpm_sinc = self.__rev_s * 60
        self.__w_s = 2 * 3.14 * self.__rev_s
        self.__Mr = Mrotor
        r1jx1 = Vector2d(r1, x1)
        jxo = self.__jxo = Vector2d(0, xo)
        self.__R1jX1 = (r1jx1 * jxo) / (r1jx1 + jxo)
        self.__R1, self.__X1 = self.__R1jX1.get_complex()
        R1_2 = self.__R1 * self.__R1
        X1x2_2 = (self.__X1 + x2) ** 2
        self.__delta = math.sqrt(R1_2 + X1x2_2)
        self.__s_max = r2 / self.__delta
        self.__Tmax = (1/self.__w_s) * ((0.5*3*(self.__Vf**2))/(self.__R1 + self.__delta))
        self.__w_rotor = 0
        return
    
        
    def get_tensao_fase(self, tensao_linha):
        return tensao_linha
    
    def get_single_current(self, tensao, s):
        z, a = self.get_imped_equiv(s).get_polar()
        return self.get_tensao_fase(tensao) / z
    
    def get_line_current(self, fcurrent):
        return fcurrent * RAIZ_3
    
    def get_w_rotor(self):
        return self.__w_rotor
    
    def get_rpm(self):
        return (self.get_w_rotor() / x2PI) * 60
    
    def get_values(self, t, to, carga):
        values = dict()
        s = self.get_s()
        if s == 0: s = 0.01
        _s = 1 - s
        Zr = Vector2d(self.__r2 / s, self.__x2)
        Zf = (Zr * self.__jxo) / (Zr + self.__jxo)
        z, a = (Zf + self.__R1jX1).get_polar()
        I1 = self.__Vf / z
        I1xI1 = I1**2
        Pg1 = 3 * I1xI1 * Zf.get_complex()[0]
        I2 = self.__Vf / (self.__R1jX1 + Zr).get_mod()
        
        Cm = (1/self.__w_s) * 3 * (I2**2) * (self.__r2 / s)
        
        Tr_mot = self.__w_rotor * self.__Tmax * 0.01 / self.__w_s
        Tres = carga.get_torque(self.__w_rotor)
        a = (Cm - Tres - Tr_mot) / (self.__Mr + carga.I)
        self.__w_rotor += a * (t - to)

        """
        w_max = 0.98 * self.__w_s
        if w < w_max:
            self.__w_rotor = w
        else:
            self.__w_rotor = w_max
        """
        
        values['fp'] = math.cos(a)
        values['pot-mec'] = (Cm * self.__w_rotor) - self.__perdas
        if values['pot-mec'] < 0: values['pot-mec'] = 0
        values['rpm'] = self.get_rpm()
        values['Tres'] = Tres
        values['torque'] = Cm
        if values['torque'] > self.__Tmax: values['torque'] = self.__Tmax
        values['corrente'] = self.get_line_current(I1)
        values['pot-ele'] = values['pot-mec'] + (3 * I1xI1 * self.__r1) + (s * Pg1) + self.__perdas
        values['hp'] = values['pot-mec'] / 745.5

        return values
    
    def get_str_values(self, tensao, s):
        values = self.get_values(tensao, s)
        
        return """
        Motor de Indução Trifásico
        ===========   ================
        Tensão(V)     %0.2f
        Corrente(A)   %0.2f
        Potência(W)   %0.2f
        Potência(HP)  %0.2f
        Torque(N.m)   %0.2f
        FP            %0.4f
        RPM           %0.1f
        ===========   ================
        """ % (values['tensao'], values['corrente'], values['pot-ele'], 
               values['pot-mec'] / 745.7, values['torque'], values['fp'], values['rpm'])
    
    def execute(self, tensao, carga):
        pass

class Motor3PhD(Motor3Ph):
    
    def __init__(self, *args, **keyargs):
        super().__init__(*args, **keyargs)

class Motor3PhY(Motor3Ph):
    
    def __init__(self, *args, **keyargs):
        super().__init__(*args, **keyargs)
    
    def get_tensao_fase(self, tensao_linha):
        return tensao_linha / RAIZ_3
    
    def get_line_current(self, fcurrent):
        return fcurrent


#------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    
    def exit_():
        sys.exit(0)
        exit(0)
    
    print("""
==== MotorSimu ====
    """)
    
    while True:
        tipo = input("Fechamento(0=delta,1=Y)\n> ")
        if tipo == 'q': exit_()
        if tipo in ('0','1'):
            if tipo == '0':
                motor = Motor3PhD()
            elif tipo == '1':
                motor = Motor3PhY()
            break
        else:
            print('Entrada inválida.')
    
    while True:
        pars = input("Parâmetros(polos,frequência,perdas)\n> ")
        if pars == 'q': exit_()
        try:
            pars = pars.split(',')
            motor.polos   = int(pars[0])
            motor.freq    = int(pars[1])
            motor.perdas  = int(pars[2])
            break
        except:
            print('Entrada inválida.')

    while True:
        try:
            #0.294,0.503,13.25,0.209,0.144
            defs = input('Circuito equivalente(r1,x1,xo,x2,r2)\n> ').split(',')
            if(defs[0]=='q'): exit_()
            motor.r1 = float(defs[0])
            motor.x1 = float(defs[1])
            motor.xo = float(defs[2])
            motor.x2 = float(defs[3])
            motor.r2 = float(defs[4])
            break
        except Exception as ex:
            print('Definições inválidas.\nErr:%s\n' % ex)
    
    while True:
        try:
            values = input('tensão,escorregamento\n> ')
            if(values=='q'): break
            tensao, s = values.split(',')
            tensao = float(tensao)
            s = float(s)
            print(motor.get_str_values(tensao, s))
        except Exception as ex:
            print('Valor de escorregamento inválido.\nErr:%s\n' % ex)
    
    exit_()
            
