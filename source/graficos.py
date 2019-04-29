#!/usr/bin/python3
#coding: utf8

"""
+----------------------------------------+
| graficos v0.2                          |
| Autor: João Paulo F da Silva           |
| website: jpcompweb.com.br              |
+----------------------------------------+

graficos
========

O `graficos` é um módulo que contém componentes para visualização gráfica de dados.

"""

import tkinter as tk

class GraphicSerie:
    def __init__(self,points=[(0,0)],x_div=1,y_div=1,x_label='X',y_label='Y',color='#FFFFFF'):
        self.points = points
        self.x_div = x_div
        self.y_div = y_div
        self.x_label = x_label
        self.y_label = y_label
        self.color = color

class LineGraphic(tk.Canvas):
    """Gráfico 2d que desenha os dados em linhas."""
    
    def __init__(self, master=None, series=[], w=740, h=560, *args, **keyargs):
        super().__init__(master, *args, **keyargs)
        self.__series = series
        self.__y_0 = 0
        self.__x_0 = 0
        self.config(width=w, height=h)
        self.set_colors('#232323','#E5E5E5','#175C17','#1A3E1A','#00A900')
    
    @property
    def series(self):
        return self.__series
    
    @series.setter
    def series(self, value):
        self.__series = value
        self.draw()
    
    @property
    def x_0(self):
        return self.__x_0
    
    @property
    def y_0(self):
        return self.__y_0
    
    def set_size(self, w, h):
        self.config(width=w, height=h)
        self.__draw_all()
    
    def set_axes(self, x_0, y_0):
        self.__x_0 = x_0
        self.__y_0 = y_0
        self.__draw_all()
    
    def set_colors(self, bg, fg, div, subdiv, axes):
        self.__bg = bg
        self.__fg = fg
        self.__dcolor = div
        self.__sdcolor = subdiv
        self.__xycolor = axes
        self.__draw_all()
    
    def __draw_base(self):
        self.delete('base')
        self.delete('series')

        w = int(self.cget('width'))
        h = int(self.cget('height'))
        
        gtop = 20
        gleft = 20
        gright = w - 200
        gbottom = h - 20
        gw = gright - gleft
        gh = gbottom - gtop
        
        f = lambda i: int(i/10)
        
        self.create_rectangle(0,0,w,h,fill=self.__bg,outline='white', tags='base')
        self.create_rectangle(gleft,gtop,gright,gbottom,fill=self.__bg,outline=self.__xycolor, tags='base')
        
        x = gleft + 10
        for i in range(1, f(gw)):
            if x % 20 == 0:
                self.create_line(x, gtop+1, x, gbottom-1, fill=self.__dcolor, tags='base')
            else:
                self.create_line(x, gtop+1, x, gbottom-1, fill=self.__sdcolor, tags='base')
            x += 10
        
        y = gtop + 10
        for i in range(1, f(gh)):
            if y % 20 == 0:
                self.create_line(gleft+1, y, gright-1, y, fill=self.__dcolor, tags='base')
            else:
                self.create_line(gleft+1, y, gright-1, y, fill=self.__sdcolor, tags='base')
            y += 10
    
    def __draw_all(self):
        self.__draw_base()
        self.draw()
        
    def draw(self):

        self.delete("series")

        w = int(self.cget('width'))
        h = int(self.cget('height'))
                
        gtop = 20
        gleft = gtop
        gright = w - 200
        gbottom = h - 20
        gw = gright - gleft
        gh = gbottom - gtop

        f_0 = lambda i, j: 20 + 10 * ((j/2)+i)

        y_0 = f_0(-self.y_0, gh / 10)
        x_0 = f_0(self.x_0, gw / 10)

        self.create_line(gleft, y_0, gright, y_0, fill=self.__xycolor,tags='series')
        self.create_line(x_0, gtop, x_0, gbottom, fill=self.__xycolor,tags='series')
                
        f = lambda value, y_div: y_0 - (20/y_div) * value
        g = lambda value, x_div: x_0 + (20/x_div) * value

        def get_limited_points(p1,p2):
            def _f(i1,i2,l1,l2):
                d1 = i1 - l1   #i1 = 20 L1 = 21
                d2 = i2 - l1   #
                if d1 <  0 and d2 <  0: return None,None
                if d1 <  0 and d2 >= 0: i1 = l1
                if d1 >= 0 and d2 <  0: i2 = l1
                d1 = l2 - i1
                d2 = l2 - i2
                if d1 <  0 and d2 <  0: return None,None
                if d1 <  0 and d2 >= 0: i1 = l2
                if d1 >= 0 and d2 <  0: i2 = l2
                return i1,i2
            x1,y1 = p1
            x2,y2 = p2
            x1,x2 = _f(x1,x2,gleft+1,gright-1)
            if x1 is None: return None,None,None,None
            y1,y2 = _f(y1,y2,gtop+1,gbottom-1)
            if y1 is None: return None,None,None,None
            return x1,y1,x2,y2
                   
        xl0 = w-180
        xl1 = xl0+5
        xl2 = xl1+20
        xl3 = xl2+5
        yl0 = 0
        
        def fleg(leg):
            result = ''
            for i in range(20):
                if i < len(leg):
                    result += leg[i]
                else:
                    result += ' '
            return result
        
        for serie in self.series:
            if not type(serie) is GraphicSerie: continue
            if 0 in (serie.y_div, serie.x_div): continue
            #== curva ==
            for i in range(1,len(serie.points)):
                x1, y1 = serie.points[i-1]
                x2, y2 = serie.points[i]
                x1,y1,x2,y2 = get_limited_points((g(x1, serie.x_div),f(y1, serie.y_div)), (g(x2, serie.x_div),f(y2, serie.y_div)))
                if x1 is None: continue
                self.create_line(x1, y1, x2, y2, fill=serie.color, width=1, tags='series')
                
            #== legenda ==
            y = yl0 * 60 + 35
            yl0 += 1
            self.create_line(xl1, y, xl2, y, fill=serie.color, width=4, tags='series')
            self.create_text(xl3, y - 10, font=('Courier New', 9), text='%s\nx=%0.2f/div\ny=%0.2f/div\n' % (fleg(serie.y_label),serie.x_div,serie.y_div), tags='series', anchor=tk.NW, fill=self.__fg)
        
def get_graphico(title,series,x_0=0,y_0=0):
    win = tk.Tk()
    win.title(title)
    gr = LineGraphic(win,series)
    gr.pack(fill=tk.BOTH)
    gr.set_axes(x_0,y_0)
    win.mainloop()
    return gr

if __name__ == "__main__":
    import math
    f = lambda i: i * 0.1
    g = lambda x: (x,x**2+x+1)
    h = lambda x: (x,math.tan(x))
    
    serie1 = GraphicSerie([g(f(i)) for i in range(-100,100)],1,1,'s','f(x)= x² + x + 1','#0000FF')
    serie2 = GraphicSerie([h(f(i)) for i in range(-10,10)],0.1,0.1,'s','g(x)= tan(x)','#FFFF00')
    
    get_graphico('Math Graphic',[serie1,serie2])
        
