#!/usr/bin/python3
#coding: utf8

"""
+----------------------------------------+
| graphics v0.3                          |
| Autor: João Paulo F da Silva           |
| website: jpcompweb.com.br              |
+----------------------------------------+

graphics
========

O `graphics` é um módulo que contém componentes para visualização gráfica de dados.

"""

import tkinter as tk


class GraphicLegend:
    def __init__(self,group,left=0,top=0,label='legend',lcolor='#0',ltext='',lfont=('Courier New', 9)):
        self.__group        = group
        self.__offsetLeft   = left
        self.__offsetTop    = top
        left                = self.__group.left + self.__offsetLeft        
        top                 = self.__group.top + self.__offsetTop
        self.__lcolor       = self.__group.canvas.create_line(left, top+10, left + 10, top+10, fill=lcolor, width=4)
        self.__label        = self.__group.canvas.create_text(left + 15, top, text=label, font=lfont, anchor=tk.NW)
        self.__ltext        = self.__group.canvas.create_text(left + 15, top + 15, text=ltext, font=lfont, anchor=tk.NW)
    
    @property
    def top(self):
        return self.__offsetTop
        
    @property
    def left(self):
        return self.__offsetLeft
    
    @property
    def color(self):
        return self.__group.canvas.itemcget(self.__lcolor, 'fill')
    
    @color.setter
    def color(self, value):
        self.__group.canvas.itemconfig(self.__lcolor, fill=value)
    
    @property
    def label(self):
        return self.__group.canvas.itemcget(self.__label, 'text')
    
    @label.setter
    def label(self, value):
        self.__group.canvas.itemconfig(self.__label, text=value)
    
    @property
    def text(self):
        return self.__group.canvas.itemcget(self.__ltext, 'text')
    
    @text.setter
    def text(self, value):
        self.__group.canvas.itemconfig(self.__ltext, text=value)
    
    @property
    def font(self):
        return self.__group.canvas.itemcget(self.__ltext, 'font')
    
    @font.setter
    def font(self, value):
        self.__group.canvas.itemconfig(self.__ltext, font=value)
    
    @property
    def width(self):
        return 150
    
    @property
    def height(self):
        return 40
    
    def update(self):
        left = self.__group.left + self.__offsetLeft        
        top  = self.__group.top + self.__offsetTop
        
        x1,y1,x2,y2 = self.__group.canvas.bbox(self.__lcolor)
        self.__group.canvas.move(self.__lcolor, x1-left, y1-top)
        
        self.__group.canvas.itemconfig(self.__llabel, x=left + 15, y=top)
        self.__group.canvas.itemconfig(self.__ltext , x=left + 15, y=top + 15)
    
    def destroy(self):
        self.__group.canvas.delete(self.__lcolor)
        self.__group.canvas.delete(self.__label)
        self.__group.canvas.delete(self.__ltext)
        
class GraphicLegendGroup:
    def __init__(self, canvas, left=0, top=0):
        self.__legends = []
        self.canvas = canvas
        self.__left = left
        self.__top = top
        
    @property
    def top(self):
        return self.__top
    
    @top.setter
    def top(self, value):
        if value == self.__top: return
        self.__top = value
        self.update()
    
    @property
    def left(self):
        return self.__left
    
    @left.setter
    def left(self, value):
        if value == self.__left: return
        self.__left = value
        self.update()
    
    @property
    def legends(self):
        return self.__legends
    
    def update(self):
        for legend in self.__legends:
            legend.update()
    
    def insert(self, label, color, text, font=('Courier New', 9)):
        if len(self.__legends) > 0:
            last = self.__legends[-1]
            top = last.top + last.height + 10
        else:
            top = 5
        gl = GraphicLegend(self,10,top,label,color,text,font)
        self.__legends.append(gl)
    
    def remove_all(self):
        for legend in self.__legends:
            legend.destroy()
        self.__legends = []
    
    def destroy(self):
        self.remove_all()

class GraphicSerie:
    def __init__(self,points=[(0,0)],x_div=1,y_div=1,x_label='X',y_label='Y',color='#FFFFFF',width=2):
        self.points = points
        self.x_div = x_div
        self.y_div = y_div
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.width = width

class LineGraphic(tk.Canvas):
    """Gráfico 2d que desenha os dados em linhas."""
    
    def __init__(self, master=None, series=[], w=740, h=560, *args, **keyargs):
        super().__init__(master, *args, **keyargs)
        self.__series = series
        self.__y_0 = 0
        self.__x_0 = 0
        self.__divsize = 20
        self.__leg_group = GraphicLegendGroup(self, w - 200, 20)
        self.__inst = -1
        self.config(width=w, height=h)
        self.bind("<Motion>", self.__canvas_mouse_move)
        self.set_colors('#FFFFFF','#1A1A1A','#D5D5D5','#F5F5F5','#1A1A1A')
    
    @property
    def legendsgroup(self):
        return self.__leg_group
    
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
    
    @property
    def divsize(self):
        return self.__divsize
    
    @divsize.setter
    def divsize(self, value):
        self.__divsize = value
        self.__draw_all()
    
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
    
    def __canvas_mouse_move(self, event):
        if event.x < 20: return
        if event.x > int(self['width']) - 200: return
        self.delete(self.__inst)
        self.__inst = self.create_line(event.x, 20, event.x, int(self['height'])-20, fill=self.__xycolor, width=1, tags='base') 
        gw = int(self['width']) - 220
        offx = event.x - 20
        k = offx / gw
        cdivs = gw / self.__divsize
        subdivw = self.__divsize / 2
        f_0 = lambda i, j: subdivw * ((j / 2) + i)        
        g_0 = lambda i, n, i_0: i - ((n + i_0) / 2)    
        x_0 = f_0(self.x_0, gw / subdivw)     
        
        i = 0
        for serie in self.series:
            
            if serie is None or 0 in (serie.x_div, serie.y_div): continue
            
            def get_pt(x):
                vx = serie.x_div * (x - x_0) / self.__divsize
                for px, py in serie.points:
                    if vx != 0:
                        dx = px / vx
                        if 0.98 < dx and dx < 1.02:
                            return px, py
                    else:
                        if -0.02 < px and px < 0.02:
                            return px, py
                        
            pt = get_pt(offx)
            if pt is None: continue
            self.legendsgroup.legends[i].text = 'x <- %0.2f\ny <- %0.2f' % pt
            i += 1
        
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
        
        subdivw = self.__divsize / 2
        
        f   = lambda i: int(i / subdivw)        
        f_0 = lambda i, j: 20 + subdivw * ((j / 2) + i)        
        g_0 = lambda i, n, i_0: i - ((n + i_0) / 2)
        
        x_0 = f_0(self.x_0, gw / subdivw)
        y_0 = f_0(-self.y_0, gh / subdivw)
        ndivx = gw / self.__divsize
        ndivy = gh / self.__divsize
        xvalues = []
        yvalues = []
        
        self.create_rectangle(0,0,w,h,fill=self.__bg,outline='white', tags='base')
        self.create_rectangle(gleft,gtop,gright,gbottom,fill=self.__bg,outline=self.__xycolor, tags='base')        
        
        x = gleft + subdivw
        j = 1
        nx = f(gw)
        for i in range(1, nx):
            if x % self.__divsize == 0:
                self.create_line(x, gtop+1, x, gbottom-1, fill=self.__dcolor, tags='base')
                xvalues.append(g_0(j,ndivx,self.x_0))
                j += 1
            else:
                self.create_line(x, gtop+1, x, gbottom-1, fill=self.__sdcolor, tags='base')
            x += subdivw
        
        y = gtop + subdivw
        ny = f(gh)
        j = 1
        for i in range(1, ny):
            if y % self.__divsize == 0:
                self.create_line(gleft+1, y, gright-1, y, fill=self.__dcolor, tags='base')
                yvalues.append(-g_0(j,ndivy,-self.y_0))
                j += 1
            else:
                self.create_line(gleft+1, y, gright-1, y, fill=self.__sdcolor, tags='base')
            y += subdivw   
        
        x = gleft + self.__divsize
        for i in xvalues:
            if i % 2 == 0:
                self.create_text(x, y_0, text='%i' % i, font=('Courier New', 9), anchor=tk.NE, tags='base')
            x += self.__divsize
        
        y = gleft + self.__divsize
        for i in yvalues:
            if i % 2 == 0:
                self.create_text(x_0, y, text='%i' % i, font=('Courier New', 9), anchor=tk.NE, tags='base')
            y += self.__divsize
        
        self.__inst = self.create_line(gleft, gtop, gleft, gbottom, fill=self.__xycolor, width=1, tags='base')
    
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
        
        subdivw = self.__divsize / 2

        f_0 = lambda i, j: 20 + subdivw * ((j / 2) + i)

        y_0 = f_0(-self.y_0, gh / subdivw)
        x_0 = f_0(self.x_0, gw / subdivw)

        self.create_line(gleft, y_0, gright, y_0, fill=self.__xycolor,tags='series')
        self.create_line(x_0, gtop, x_0, gbottom, fill=self.__xycolor,tags='series')
                
        f = lambda value, y_div: y_0 - (self.__divsize/y_div) * value
        g = lambda value, x_div: x_0 + (self.__divsize/x_div) * value

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
        
        self.__leg_group.remove_all()
        for serie in self.series:
            if not type(serie) is GraphicSerie: continue
            if 0 in (serie.y_div, serie.x_div): continue
            #== curva ==
            for i in range(1,len(serie.points)):
                x1, y1 = serie.points[i-1]
                x2, y2 = serie.points[i]
                x1,y1,x2,y2 = get_limited_points((g(x1, serie.x_div),f(y1, serie.y_div)), (g(x2, serie.x_div),f(y2, serie.y_div)))
                if x1 is None: continue
                self.create_line(x1, y1, x2, y2, fill=serie.color, width=serie.width, tags='series')
                
            #== legenda ==
            self.__leg_group.insert(fleg(serie.y_label),serie.color,'x <- x%0.2f\ny <- x%0.2f\n' % (serie.x_div,serie.y_div))
            
def get_graphico(title,series,x_0=0,y_0=0,divsize=20):
    win = tk.Tk()
    win.title(title)
    gr = LineGraphic(win,series)
    gr.pack(fill=tk.BOTH)
    gr.set_axes(x_0,y_0)
    gr.divsize = divsize
    """
    gl = GraphicLegendGroup(gr, 100, 100)
    gl.insert('teste de legenda', 'red', 'teste de legenda\nlinha2')
    """
    win.mainloop()
    return gr

if __name__ == "__main__":
    import math
    f = lambda i: i * 0.1
    g = lambda x: (x,x**2+x+1)
    h = lambda x: (x,math.tan(x))
    
    serie1 = GraphicSerie([g(f(i)) for i in range(-100,100)],1,1,'s','f(x)= x² + x + 1','#000075')
    serie2 = GraphicSerie([h(f(i)) for i in range(-100,100)],0.1,0.1,'s','g(x)= tan(x)','#A52A2A')
    
    get_graphico('Math Graphic',[serie1,serie2],divsize=20)
    
        
