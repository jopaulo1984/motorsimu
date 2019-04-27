
import tkinter as tk
import graficos as gr
import motor_inducao as mi
import carga as cg
import ast
import math

class SimuApp(tk.Tk):
    def __init__(self, *args, **keyargs):
        super().__init__(*args, **keyargs)
        
        self.__scalex = 1.0
        self.__scaley = 1.0
        self.__dx = 0
        self.__dy = 0
        
        #self.motor = mi.Motor3PhY()
        #self.carga = cg.CargaRotativa()
        
        panesq      = tk.Frame(self, padx=5, pady=5)
        mainpan     = tk.Frame(self)
        panmot      = tk.Frame(panesq, bd=1)
        pancarg     = tk.Frame(panesq, bd=1)
        pansimu     = tk.Frame(panesq, bd=1)
        #pansimuvisu = tk.Frame(pansimu, bd=1)
        panbuttons  = tk.Frame(panesq, bd=1, pady=10)
        
        self.grafic = gr.GraficoLinha(mainpan)
        
        def valida_num(evt):
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
        
        #== motor ==
        self.m_r1 = tk.Entry(panmot)
        self.m_x1 = tk.Entry(panmot)
        self.m_xo = tk.Entry(panmot)
        self.m_r2 = tk.Entry(panmot)
        self.m_x2 = tk.Entry(panmot)        
        self.v_n  = tk.Entry(panmot)
        self.freq = tk.Entry(panmot)
        self.pols = tk.Entry(panmot)
        self.m_r1.insert(0,'0.294')
        self.m_x1.insert(0,'0.503')
        self.m_xo.insert(0,'13.25')
        self.m_r2.insert(0,'0.144')
        self.m_x2.insert(0,'0.209')        
        self.v_n .insert(0,'220')
        self.freq.insert(0,'60')
        self.pols.insert(0,'6')
        self.m_r1.bind('<KeyRelease>',valida_num)
        self.m_x1.bind('<KeyRelease>',valida_num)
        self.m_xo.bind('<KeyRelease>',valida_num)
        self.m_r2.bind('<KeyRelease>',valida_num)
        self.m_x2.bind('<KeyRelease>',valida_num)      
        self.v_n .bind('<KeyRelease>',valida_num)
        self.freq.bind('<KeyRelease>',valida_num)
        self.pols.bind('<KeyRelease>',valida_num)
        
        #== carga ===
        self.c_I    = tk.Entry(pancarg)
        self.c_func = tk.Entry(pancarg)
        self.c_I.bind('<Return>', self.__simular)
        self.c_I.insert(0,'0.4')
        self.c_I.bind('<KeyRelease>',valida_num)
        self.c_func.bind('<Return>', self.__simular)
        self.c_func.insert(0,'(50/125) * w')
        
        #== simulação ==
        #self.tf = tk.Entry(pansimu)
        self.dt = tk.Entry(pansimu,width=6)
        #self.tf.bind('<Return>', self.__simular)
        self.dt.bind('<Return>', self.__simular)
        self.dt.bind('<KeyRelease>',valida_num)
        #self.tf.insert(0,'1')
        self.dt.insert(0,'0.04')             
        #self.chktorque = tk.Checkbutton(pansimu,text='Torque motor')
        self.divtorque = tk.Entry(pansimu,width=6)
        self.divtorque.bind('<Return>', self.__simular)
        self.divtorque.bind('<KeyRelease>',valida_num)
        #self.chktorque.toggle()
        self.divtorque.insert(0,'12')
        #self.chkpot = tk.Checkbutton(pansimu,text='Potência')
        self.divpot = tk.Entry(pansimu,width=6)
        self.divpot.bind('<Return>', self.__simular)
        self.divpot.bind('<KeyRelease>',valida_num)
        #self.chkpot.toggle()
        self.divpot.insert(0,'0')
        #self.chkcorr = tk.Checkbutton(pansimu,text='Corrente')
        self.divcorr = tk.Entry(pansimu,width=6)
        self.divcorr.bind('<Return>', self.__simular)
        self.divcorr.bind('<KeyRelease>',valida_num)
        #self.chkcorr.toggle()
        self.divcorr.insert(0,'0')
        #self.chkrpm = tk.Checkbutton(pansimu,text='Rotação')
        self.divrpm = tk.Entry(pansimu,width=6)
        self.divrpm.bind('<Return>', self.__simular)
        self.divrpm.bind('<KeyRelease>',valida_num)
        #self.chkrpm.toggle()
        self.divrpm.insert(0,'100')
        #self.chkcr = tk.Checkbutton(pansimu,text='Torque carga')
        self.divcr = tk.Entry(pansimu,width=6)
        self.divcr.bind('<Return>', self.__simular)
        self.divcr.bind('<KeyRelease>',valida_num)
        #self.chkcr.toggle()
        self.divcr.insert(0,'12')
        
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
        
        """
        tk.Label(panesq,text='\n---- Comandos ----').pack()
        """
        
        tk.Label(panmot,text='r1').grid(row=0,column=0)
        self.m_r1.grid(row=0,column=1)
        tk.Label(panmot,text='x1').grid(row=1,column=0)
        self.m_x1.grid(row=1,column=1)
        tk.Label(panmot,text='xo').grid(row=2,column=0)
        self.m_xo.grid(row=2,column=1)
        tk.Label(panmot,text='r2').grid(row=3,column=0)
        self.m_r2.grid(row=3,column=1)
        tk.Label(panmot,text='x2').grid(row=4,column=0)
        self.m_x2.grid(row=4,column=1)
        tk.Label(panmot,text='V').grid(row=5,column=0)
        self.v_n.grid(row=5,column=1)
        tk.Label(panmot,text='f').grid(row=6,column=0)
        self.freq.grid(row=6,column=1)
        tk.Label(panmot,text='P').grid(row=7,column=0)
        self.pols.grid(row=7,column=1)
        
        tk.Label(pancarg,text='M').grid(row=0,column=0)
        self.c_I.grid(row=0,column=1)
        tk.Label(pancarg,text='Cr(w)').grid(row=1,column=0)
        self.c_func.grid(row=1,column=1)        
        
        #tk.Label(pansimu,text='tf').grid(row=0,column=0,sticky=tk.W)
        #self.tf.grid(row=0,column=1,sticky=tk.W)
        #pansimuvisu.grid(row=2,column=0,columnspan=2)
        
        tk.Button(panbuttons,text='Y+',command=self.y_up).grid(row=0,column=0)
        tk.Button(panbuttons,text='Y0',command=self.y_reset).grid(row=1,column=0)
        tk.Button(panbuttons,text='Y-',command=self.y_down).grid(row=2,column=0)
        
        tk.Label(panbuttons,text='|').grid(row=1,column=1)
        
        tk.Button(panbuttons,text='X-',command=self.x_down).grid(row=1,column=3)
        tk.Button(panbuttons,text='X0',command=self.x_reset).grid(row=1,column=4)
        tk.Button(panbuttons,text='X+',command=self.x_up).grid(row=1,column=5)
        
        
        tk.Label(pansimu,text='Tempo(s)').grid(row=0,column=0,sticky=tk.W)
        self.dt.grid(row=0,column=1,sticky=tk.W)
        tk.Label(pansimu,text='/div').grid(row=0,column=2)
        #tk.Label(pansimu,text='--- Visualizar ---', pady=5).grid(row=0,column=0,columnspan=3)
        #self.chktorque.grid(row=1,column=0, sticky=tk.W)
        tk.Label(pansimu,text='Conjugado motor').grid(row=3,column=0, sticky=tk.W)
        self.divtorque.grid(row=3,column=1)
        tk.Label(pansimu,text='/div').grid(row=3,column=2)
        #self.chkpot.grid(row=2,column=0, sticky=tk.W)
        tk.Label(pansimu,text='Potência(HP)').grid(row=4,column=0, sticky=tk.W)
        self.divpot.grid(row=4,column=1)
        tk.Label(pansimu,text='/div').grid(row=4,column=2)
        #self.chkcorr.grid(row=3,column=0, sticky=tk.W)
        tk.Label(pansimu,text='Corrente').grid(row=5,column=0, sticky=tk.W)
        self.divcorr.grid(row=5,column=1)
        tk.Label(pansimu,text='/div').grid(row=5,column=2)
        #self.chkrpm.grid(row=4,column=0, sticky=tk.W)
        tk.Label(pansimu,text='Rotação').grid(row=6,column=0, sticky=tk.W)
        self.divrpm.grid(row=6,column=1)
        tk.Label(pansimu,text='/div').grid(row=6,column=2)
        #self.chkcr.grid(row=5,column=0, sticky=tk.W)
        tk.Label(pansimu,text='Conjugado resistente').grid(row=7,column=0, sticky=tk.W)
        self.divcr.grid(row=7,column=1)
        tk.Label(pansimu,text='/div').grid(row=7,column=2)
                
        self.__simular()
        
        self.title('Curvas Motor 3ph')
                
        self.mainloop()
    
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
    
    def scale(self, value):
        if type(value) in (int, float):
            return self.__scaley * value
        elif type(value) in (tuple, list):
            result = []
            for v in value:
                result.append(self.scale(v))
            return result
        return value
        
    def __simular(self, *args):
            
        f = lambda x: float(x.get()) if x.get()!='' else 0
        g = lambda x: f(x) * 19
        
        pars = (f(self.v_n),f(self.freq),
                f(self.pols),f(self.m_r1),
                f(self.m_x1),f(self.m_xo),
                f(self.m_r2),f(self.m_x2))
        
        motor = mi.Motor3PhY()
        motor.set_parametros(*pars)
        #fcr = '(lambda w: %s)' % self.c_func.get()
        carga = cg.CargaRotativa()
        carga.I = f(self.c_I)
        try:
            carga.f_torque = eval('lambda w: %s' %  self.c_func.get().lower().replace('^','**').replace('sqrt','math.sqrt'))
        except:
            carga.f_torque = None
    
        #tf = self.__scalex * f(self.tf)
        divt = self.__scalex * f(self.dt)
        tf = divt * 25
        AMOSTRAS = 200
        dt = tf / AMOSTRAS
        t = 0
        to = 0
        values = [],[],[],[],[]
        k = 0
        while dt > 0 and t < tf:
            mvalues = motor.get_values(t, to, carga)
            values[0].append(mvalues['torque'])
            values[1].append(mvalues['hp'])
            values[2].append(mvalues['corrente'])
            values[3].append(mvalues['rpm'])
            values[4].append(mvalues['Tres'])
            to = t
            t += dt
        
        self.grafic.series = values
        self.grafic.x_max = tf
        self.grafic.x_div = divt
        self.grafic.x_label = 's'
        self.grafic.y_max = self.scale((g(self.divtorque),g(self.divpot),g(self.divcorr),g(self.divrpm),g(self.divcr)))
        self.grafic.colors = '#7D90FB','#FBB461','#FF96E8','#B4FBF8','#F44D49'
        self.grafic.labels = 'Conjugado','Potência(HP)','Corrente','RPM','Cr'
        self.grafic.draw()

if __name__ == "__main__":
    try:
        win = SimuApp()
    except Exception as ex:
        print(ex)
        input('<Enter>')
    exit(0)
