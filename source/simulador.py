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
        def insert_simu_entry(label, value, line):
            entry = tk.Entry(pansimu,width=6)
            entry.bind('<Return>', self.__simular)
            entry.bind('<KeyRelease>',self.__valida_num)
            entry.insert(0, value)
            tk.Label(pansimu,text=label).grid(row=line,column=0,sticky=tk.W)
            entry.grid(row=line,column=1,sticky=tk.W)
            tk.Label(pansimu,text='/div').grid(row=line,column=2)
            return entry
        
        panaxex = tk.Frame(pansimu)
        panaxex.grid(row=0,column=0,columnspan=3,ipady=5)
        self.__axex = tk.IntVar()
        self.__axex.set(0)
        tk.Label(panaxex,text='Eixo x').grid(row=0,column=0)
        tk.Radiobutton(panaxex, variable=self.__axex, value=0, text='Rotação(RPM)', command=self.__simular).grid(row=0,column=1)
        tk.Radiobutton(panaxex, variable=self.__axex, value=1, text='Tempo(s)', command=self.__simular).grid(row=0,column=2)
        
        self.dt         = insert_simu_entry('Tempo(s)', '0.04', 1)
        self.divtorque  = insert_simu_entry('Conjugado M.(N.m)', '10', 2)
        self.divpot     = insert_simu_entry('Potência(HP)', '0', 3)
        self.divcorr    = insert_simu_entry('Corrente(A)', '0', 4)
        self.divrpm     = insert_simu_entry('Rotação(RPM)', '100', 5)
        self.divcr      = insert_simu_entry('Conjugado R.(N.m)', '10', 6)
        
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
        self.__motortype = tk.IntVar()
        self.__motortype.set(1)
        
        pan = tk.Frame(panmot)        
        pan.grid(row=0,column=0,columnspan=2,sticky=tk.W)
        
        tk.Label(pan,text='Fechamento').grid(row=0,column=0,sticky=tk.W)
        tk.Radiobutton(pan,text='Estrela', variable=self.__motortype, value=1, command=self.__simular).grid(row=0,column=1,sticky=tk.W)
        tk.Radiobutton(pan,text='Delta', variable=self.__motortype, value=2, command=self.__simular).grid(row=0,column=2,sticky=tk.W)
        
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
        
        if self.__motortype.get() == 1:
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
        to = -dt
        
        #divr = 
        divx = g(self.divrpm) if self.__axex.get() == 0 else self.__scale(divt, self.__scalex)
        
        Tserie = gr.GraphicSerie([],divx,h(self.divtorque),'','Conjugado M.(N.m)','#6D87FF')
        Tpoten = gr.GraphicSerie([],divx,h(self.divpot)   ,'','Potência(HP)','#F24F4F')
        Tcorre = gr.GraphicSerie([],divx,h(self.divcorr)  ,'','Corrente(A)' ,'#F24FB7')
        Tconjr = gr.GraphicSerie([],divx,h(self.divcr)    ,'','Conjugado R.(N.m)','#885AE1')
        
        Tvar = gr.GraphicSerie([],divx,divt,'','t(w)' ,'#FDFD36') if  self.__axex.get() == 0 else gr.GraphicSerie([],divx,h(self.divrpm),'','w(t)' ,'#FFB340')
        
        while dt > 0 and t < tf:
            mvalues = motor.get_values(t, to, carga)
            x_ = mvalues['rpm'] if self.__axex.get() == 0 else t
            Tserie.points.append((x_,mvalues['torque']))
            Tpoten.points.append((x_,mvalues['hp']))
            Tcorre.points.append((x_,mvalues['corrente']))
            Tconjr.points.append((x_,mvalues['Tres']))
            if self.__axex.get() == 0:                
                Tvar.points.append((mvalues['rpm'],t))
            else:
                Tvar.points.append((t,mvalues['rpm']))
            to = t
            t += dt
        
        self.grafic.series = [Tserie,Tpoten,Tcorre,Tconjr,Tvar]

if __name__ == "__main__":
    win = SimuAppWindow()
    exit(0)
