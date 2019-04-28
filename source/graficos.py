#!/usr/bin/python3
#coding: utf8

"""
+----------------------------------------+
| graficos v0.1                          |
| Autor: João Paulo F da Silva           |
| website: jpcompweb.com.br              |
+----------------------------------------+

graficos
========

O `graficos` é um módulo que contém componentes para visualização gráfica de dados.

"""

import tkinter as tk

class GraficoLinha(tk.Canvas):
    """Gráfico 2d que desenha os dados em linhas.

    Uso
    ===

    Antes de desenhar, deve-se definir os atributos da classe:
    - series:  lista contendo várias outras listas de valores do eixo y do gráfico.
    - x_init:  valor inicial do eixo x.
    - x_div:   valor de cada divisão de x.
    - x_label: rótulo do eixo x.
    - y_div:   lista contendo o valor de cada divisão relativa ao índice da série de valores
               definidos no atributo series.
    - labels:  lista contendo o rótulo de cada série de valores.
    - colors:  lista contendo a cor da linha de cada série de valores.
    - y_0:     deslocamento em divisões do eixo y.
    - x_0:     deslocamento em divisões do eixo x.

    """

    def __init__(self, *args, **keyargs):
        super().__init__(*args, **keyargs)
        self.series = []
        self.x_init = 0
        self.x_div = 0.1
        self.x_label = 's'
        self.y_div = []
        self.labels = []
        self.colors = []
        self.backcolor = '#1A1A1A'
        self.gridcolor = '#2D672D'
        self.y_0 = 0
        self.x_0 = 0
        w, h = 700, 540
        self.config(width=w, height=h)
        self.create_rectangle(0,0,w,h,fill=self.backcolor,outline='white')
        self.create_rectangle(20,20,w-200,h-20,fill=self.backcolor,outline='#2DD500')
        x = 30
        while x < w-200:
            if x % 20 == 0:
                self.create_line(x, 21, x, h-21, fill='#2E5922')
            else:
                self.create_line(x, 21, x, h-21, fill='#183318')
            x += 10
        y = 30
        while y < h-20:
            if y % 20 == 0:
                self.create_line(21, y, w-201, y, fill='#2E5922')
            else:
                self.create_line(21, y, w-201, y, fill='#183318')
            y += 10
        
    def draw(self):

        self.delete("series")

        w = int(self.cget('width'))
        h = int(self.cget('height'))

        f_0 = lambda i: 20 + 10 * (25+i)

        y_0 = f_0(-self.y_0)
        x_0 = f_0(self.x_0)

        self.create_line(20, y_0, w-200, y_0, fill='#2DD500',tags='series')
        self.create_line(x_0, 20, x_0, h-20, fill='#2DD500',tags='series')

        if len(self.series) == 0: return
        def len_max():
            m = 0
            for serie in self.series:
                if len(serie) > m: m = len(serie)
            return m
        
        N = len_max()
        if N == 0: return
            
                
        gtop = 21
        gleft = gtop
        gright = w - 201
        gbottom = h - 21
        gw = gright - gleft
        gh = gbottom - gtop
        
        g = lambda d: d + x_0
        dx = gw / N if N > 0 else 0
        x = self.x_init / self.x_div * 20
        xant = x
        f = lambda value, y_div: y_0 - (20/y_div) * value
        

        def get_limited_points(p1,p2):
            def _f(i1,i2,l1,l2):
                if i1 < l1 and i2 < l1: return None,None
                if i1 < l1 and i2 > l1: i1 = l1
                if i1 > l1 and i2 < l1: i2 = l1
                if i1 > l2 and i2 > l2: return None,None
                if i1 < l2 and i2 > l2: i1 = l2
                if i1 > l2 and i2 < l2: i2 = l2
                return i1,i2
            x1,y1 = p1
            x2,y2 = p2
            x1,x2 = _f(x1,x2,gleft,gright)
            if x1 is None: return None,None,None,None
            y1,y2 = _f(y1,y2,gtop,gbottom)
            if y1 is None: return None,None,None,None
            return x1,y1,x2,y2
        
        for i in range(0, N):
            if i > 0:
                for j, serie in enumerate(self.series):
                    if self.y_div[j] == 0: continue
                    x1,y1,x2,y2 = get_limited_points((g(xant),f(serie[i-1], self.y_div[j])), (g(x),f(serie[i], self.y_div[j])))
                    if x1 is None: continue
                    self.create_line(x1, y1, x2, y2, fill=self.colors[j], width=1, tags='series')
            xant = x
            x += dx
            
        labels = [(label, i) for i, label in enumerate(self.labels) if self.y_div[i] > 0]
        x0 = w - 180
        x1 = x0+5
        x2 = x1+20
        x3 = x2+5
        y0 = 0
        
        for label, i in labels:
            if self.y_div[i] == 0: continue
            y = y0 * 20 + 35
            y0+=1
            self.create_line(x1, y, x2, y, fill=self.colors[i], width=4, tags='series')
            self.create_text(x3, y - 10, text='%s (%0.2f/div)' % (label,self.y_div[i]), tags='series', anchor=tk.NW, fill='white')
        
        self.create_text(w-200,h-5, text='%0.2f%s' % (self.x_div * 25, self.x_label), anchor=tk.SW, tags='series', fill='white')
        
def get_graphico(title,series, x_max, x_div, x_label, colors, y_div, labels,x_0=0,y_0=0):
    win = tk.Tk()
    win.title(title)
    gr = GraficoLinha(win)
    gr.pack(fill=tk.BOTH)
    gr.series = series
    gr.x_label = x_label
    gr.x_max = x_max
    gr.x_div = x_div
    gr.y_div = y_div
    gr.colors = colors
    gr.labels = labels
    gr.x_0 = x_0
    gr.y_0 = y_0
    gr.draw()
    win.mainloop()
    return gr

if __name__ == "__main__":
    get_graphico('Gráfico',[],1,0.01,'s',('red',),(10,),('teste',))
        
