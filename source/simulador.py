#!/usr/bin/python3
#coding: utf8

"""
+----------------------------------------+
| MotorSimu v0.2                         |
| Autor: João Paulo F da Silva           |
| website: jpcompweb.com.br              |
+----------------------------------------+

MotorSimu
=========

O MotorSimu é um simulador de curvas de partida e regime de motores de indução.

"""

import tkinter as tk
import graficos as gr
import motorinducao as mi
import carga as cg
import ast
import math

class SimuAppWindow(tk.Tk):
    def __init__(self, *args, **keyargs):
        super().__init__(*args, **keyargs)
        
        self.__scalex = 1.0
        self.__scaley = 1.0
        
        panesq      = tk.Frame(self, padx=5, pady=5)
        mainpan     = tk.Frame(self)
        panmot      = tk.Frame(panesq, bd=1)
        pancarg     = tk.Frame(panesq, bd=1)
        pansimu     = tk.Frame(panesq, bd=1)        
        panbuttons  = tk.Frame(panesq, bd=1, pady=10)
        
        self.grafic = gr.LineGraphic(mainpan)
        self.grafic.set_axes(-20,-20)
        
        #== motor ==
        self.m_r1 = tk.Entry(panmot)
        self.m_r1.insert(0,'0.294')
        self.m_r1.bind('<KeyRelease>',self.__valida_num)
        
        self.m_x1 = tk.Entry(panmot)
        self.m_x1.insert(0,'0.503')
        self.m_x1.bind('<KeyRelease>',self.__valida_num)
        
        self.m_xo = tk.Entry(panmot)
        self.m_xo.insert(0,'13.25')
        self.m_xo.bind('<KeyRelease>',self.__valida_num)
        
        self.m_r2 = tk.Entry(panmot)
        self.m_r2.insert(0,'0.144')
        self.m_r2.bind('<KeyRelease>',self.__valida_num)
        
        self.m_x2 = tk.Entry(panmot)
        self.m_x2.insert(0,'0.209')
        self.m_x2.bind('<KeyRelease>',self.__valida_num)
        
        self.v_n  = tk.Entry(panmot)
        self.v_n .insert(0,'220')
        self.v_n .bind('<KeyRelease>',self.__valida_num)
        
        self.freq = tk.Entry(panmot)
        self.freq.insert(0,'60')
        self.freq.bind('<KeyRelease>',self.__valida_num)
        
        self.pols = tk.Entry(panmot)
        self.pols.insert(0,'6')
        self.pols.bind('<KeyRelease>',self.__valida_num)
        
        #== carga ===
        self.c_I    = tk.Entry(pancarg)
        self.c_I.bind('<Return>', self.__simular)
        self.c_I.bind('<KeyRelease>',self.__valida_num)
        self.c_I.insert(0,'0.4')
        
        self.c_func = tk.Entry(pancarg)
        self.c_func.bind('<Return>', self.__simular)
        self.c_func.insert(0,'(50/125) * w')
        
        #== simulação ==
        self.dt = tk.Entry(pansimu,width=6)
        self.dt.bind('<Return>', self.__simular)
        self.dt.bind('<KeyRelease>',self.__valida_num)
        self.dt.insert(0,'0.04')
        
        self.divtorque = tk.Entry(pansimu,width=6)
        self.divtorque.bind('<Return>', self.__simular)
        self.divtorque.bind('<KeyRelease>',self.__valida_num)        
        self.divtorque.insert(0,'10')
        
        self.divpot = tk.Entry(pansimu,width=6)
        self.divpot.bind('<Return>', self.__simular)
        self.divpot.bind('<KeyRelease>',self.__valida_num)        
        self.divpot.insert(0,'0')
        
        self.divcorr = tk.Entry(pansimu,width=6)
        self.divcorr.bind('<Return>', self.__simular)
        self.divcorr.bind('<KeyRelease>',self.__valida_num)
        self.divcorr.insert(0,'0')
        
        self.divrpm = tk.Entry(pansimu,width=6)
        self.divrpm.bind('<Return>', self.__simular)
        self.divrpm.bind('<KeyRelease>',self.__valida_num)
        self.divrpm.insert(0,'100')
        
        self.divcr = tk.Entry(pansimu,width=6)
        self.divcr.bind('<Return>', self.__simular)
        self.divcr.bind('<KeyRelease>',self.__valida_num)
        self.divcr.insert(0,'10')
        
        panesq.grid(row=0,column=0, sticky=tk.N)
        mainpan.grid(row=0,column=1, sticky=tk.N)
        
        self.grafic.pack(fill=tk.BOTH)
        
        tk.Label(panesq,text='------ Motor ------').pack()
        panmot.pack(anchor=tk.W)
        
        tk.Label(panesq,text='\n------ Carga ------').pack()
        pancarg.pack(anchor=tk.W)
        
        tk.Label(panesq,text='\n---- Simulação ----').pack()
        pansimu.pack(anchor=tk.W)
        
        panbuttons.pack()
        
        tk.Button(panesq,text='Simular',command=self.__simular).pack()
        
        #== panmot ==
        self.__v = tk.IntVar()
        self.__v.set(1)
        
        pan = tk.Frame(panmot)        
        pan.grid(row=0,column=0,columnspan=2,sticky=tk.W)
        
        tk.Label(pan,text='Fechamento').grid(row=0,column=0,sticky=tk.W)
        tk.Radiobutton(pan,text='Estrela', variable=self.__v, value=1).grid(row=0,column=1,sticky=tk.W)
        tk.Radiobutton(pan,text='Delta', variable=self.__v, value=2).grid(row=0,column=2,sticky=tk.W)
        
        tk.Label(panmot,text='Circuito equivalente').grid(row=1,column=0,columnspan=2,sticky=tk.W,ipady=5)
        
        tk.Label(panmot,text='r1').grid(row=2,column=0,sticky=tk.W)
        self.m_r1.grid(row=2,column=1,sticky=tk.W)
        
        tk.Label(panmot,text='x1').grid(row=3,column=0,sticky=tk.W)
        self.m_x1.grid(row=3,column=1,sticky=tk.W)
        
        tk.Label(panmot,text='xo').grid(row=4,column=0,sticky=tk.W)
        self.m_xo.grid(row=4,column=1,sticky=tk.W)
        
        tk.Label(panmot,text='r2').grid(row=5,column=0,sticky=tk.W)
        self.m_r2.grid(row=5,column=1,sticky=tk.W)
        
        tk.Label(panmot,text='x2').grid(row=6,column=0,sticky=tk.W)
        self.m_x2.grid(row=6,column=1,sticky=tk.W)
        
        tk.Label(panmot,text='V').grid(row=7,column=0,sticky=tk.W)
        self.v_n.grid(row=7,column=1,sticky=tk.W)
        
        tk.Label(panmot,text='f').grid(row=8,column=0,sticky=tk.W)
        self.freq.grid(row=8,column=1,sticky=tk.W)
        
        tk.Label(panmot,text='P').grid(row=9,column=0,sticky=tk.W)
        self.pols.grid(row=9,column=1,sticky=tk.W)
        
        #== pancarg ==
        tk.Label(pancarg,text='M').grid(row=0,column=0,sticky=tk.W)
        self.c_I.grid(row=0,column=1)
        
        tk.Label(pancarg,text='Cr(w)').grid(row=1,column=0,sticky=tk.W)
        self.c_func.grid(row=1,column=1)
        
        #== panbuttons ==
        tk.Button(panbuttons,text='Y+',command=self.y_up).grid(row=0,column=0)
        tk.Button(panbuttons,text='Y0',command=self.y_reset).grid(row=1,column=0)
        tk.Button(panbuttons,text='Y-',command=self.y_down).grid(row=2,column=0)
        
        tk.Label(panbuttons,text='|').grid(row=1,column=1)
        
        tk.Button(panbuttons,text='X-',command=self.x_down).grid(row=1,column=3)
        tk.Button(panbuttons,text='X0',command=self.x_reset).grid(row=1,column=4)
        tk.Button(panbuttons,text='X+',command=self.x_up).grid(row=1,column=5)
        
        #== pansimu ==
        tk.Label(pansimu,text='Tempo(s)').grid(row=0,column=0,sticky=tk.W)
        self.dt.grid(row=0,column=1,sticky=tk.W)
        tk.Label(pansimu,text='/div').grid(row=0,column=2)
        
        tk.Label(pansimu,text='Conjugado motor').grid(row=3,column=0, sticky=tk.W)
        self.divtorque.grid(row=3,column=1)
        tk.Label(pansimu,text='/div').grid(row=3,column=2)
        
        tk.Label(pansimu,text='Potência(HP)').grid(row=4,column=0, sticky=tk.W)
        self.divpot.grid(row=4,column=1)
        tk.Label(pansimu,text='/div').grid(row=4,column=2)
        
        tk.Label(pansimu,text='Corrente').grid(row=5,column=0, sticky=tk.W)
        self.divcorr.grid(row=5,column=1)
        tk.Label(pansimu,text='/div').grid(row=5,column=2)
        
        tk.Label(pansimu,text='Rotação').grid(row=6,column=0, sticky=tk.W)
        self.divrpm.grid(row=6,column=1)
        tk.Label(pansimu,text='/div').grid(row=6,column=2)
        
        tk.Label(pansimu,text='Conjugado resistente').grid(row=7,column=0, sticky=tk.W)
        self.divcr.grid(row=7,column=1)
        tk.Label(pansimu,text='/div').grid(row=7,column=2)
        
        self.__simular()
        
        self.title('Curvas Motor 3ph')
        
        self.mainloop()
        
    def __valida_num(self, evt):
        pts = 0
        for i, c in enumerate(evt.widget.get()):
            if not c in ('0','1','2','3','4','5','6','7','8','9','.',',','-'):
                evt.widget.delete(i)
            elif c == '.':
                if pts > 0:
                    evt.widget.delete(i)
                pts += 1
            elif c == ',':
                evt.widget.delete(i)
                if pts == 0:
                    evt.widget.insert(i,'.')
                    pts += 1
            elif c in '-' and i > 0:
                evt.widget.delete(i)
        self.__simular()
    
    def y_up(self):
        if self.__scaley > 0.2:
            self.__scaley -= 0.1
        self.__simular()
            
    def y_down(self):
        if self.__scaley < 10:
            self.__scaley += 0.1
        self.__simular()
    
    def y_reset(self):
        self.__scaley = 1.0
        self.__simular()
    
    def x_up(self):
        if self.__scalex > 0.2:
            self.__scalex -= 0.1
        self.__simular()
            
    def x_down(self):
        if self.__scalex < 10:
            self.__scalex += 0.1
        self.__simular()
    
    def x_reset(self):
        self.__scalex = 1.0
        self.__simular()
    
    def __scale(self, value, scale):
        if type(value) in (int, float):
            return scale * value
        elif type(value) in (tuple, list):
            result = []
            for v in value:
                result.append(self.__scale(v))
            return result
        return value
        
    def __simular(self, *args):
            
        f = lambda x: float(x.get()) if x.get()!='' else 0
        g = lambda x: self.__scale(f(x), self.__scalex)
        h = lambda y: self.__scale(f(y), self.__scaley)
        
        pars = (f(self.v_n),f(self.freq),
                f(self.pols),f(self.m_r1),
                f(self.m_x1),f(self.m_xo),
                f(self.m_r2),f(self.m_x2))
        
        if self.__v.get() == 1:
          motor = mi.Motor3PhY()
        else:
          motor = mi.Motor3PhD()
          
        motor.set_parametros(*pars)
        
        carga = cg.CargaRotativa()
        carga.I = f(self.c_I)
        
        try:
            carga.f_torque = eval('lambda w: %s' %  self.c_func.get().lower().replace('^','**').replace('sqrt','math.sqrt'))
        except:
            carga.f_torque = None
        
        divt = h(self.dt)
        
        tf = divt * 25
        dt = 0.005
        
        t = 0
        to = t - dt
        
        divrpm = self.__scale(100, self.__scalex)
        
        Tserie = gr.GraphicSerie([],divrpm,h(self.divtorque),'w','Cm(w)','#6D87FF')
        Tpoten = gr.GraphicSerie([],divrpm,h(self.divpot)   ,'w','Pm(w)','#F24F4F')
        Tcorre = gr.GraphicSerie([],divrpm,h(self.divcorr)  ,'w','I(w)' ,'#F24FB7')
        Ttempo = gr.GraphicSerie([],divrpm,divt             ,'w','t(w)' ,'#FDFD36')
        
        while dt > 0 and t < tf:
            mvalues = motor.get_values(t, to, carga)
            Tserie.points.append((mvalues['rpm'],mvalues['torque']))
            Tpoten.points.append((mvalues['rpm'],mvalues['hp']))
            Tcorre.points.append((mvalues['rpm'],mvalues['corrente']))
            Ttempo.points.append((mvalues['rpm'],t))
            to = t
            t += dt
        
        self.grafic.series = [Tserie,Tpoten,Tcorre,Ttempo]

if __name__ == "__main__":
    win = SimuAppWindow()
    exit(0)
