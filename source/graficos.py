import tkinter as tk

class GraficoLinha(tk.Canvas):
    def __init__(self, *args, **keyargs):
        super().__init__(*args, **keyargs)
        self.series = []
        self.x_init = 0
        self.x_max = 1
        self.x_div = 0.1
        self.x_label = 's'
        self.y_max = []
        self.labels = []
        self.colors = []
        self.backcolor = '#1A1A1A'
        self.gridcolor = '#2D672D'
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
        self.create_line(20, 400, w-200, 400, fill='#2DD500')
        
    def draw(self):
        #return
        self.delete("series")
        if len(self.series) == 0: return
        def len_max():
            m = 0
            for serie in self.series:
                if len(serie) > m: m = len(serie)
            return m
        N = len_max()
        if N == 0: return
        #dist = self.x_max - self.x_init
        w = int(self.cget('width'))
        h = int(self.cget('height'))
        dx = (w - 220) / N if N > 0 else 0
        x = 21
        xant = 20
        gtop = 21
        gleft = gtop
        gw = w - 201
        gh = h - 21
        f = lambda value, y_max: -(380 / y_max) * value + 400
        for i in range(0, N):
            if i > 0:
                for j, serie in enumerate(self.series):
                    if self.y_max[j] == 0: continue
                    y1 = f(serie[i-1], self.y_max[j])
                    y2 = f(serie[i], self.y_max[j])
                    if y1 < gtop and y2 < gtop: continue
                    if y1 < gtop and y2 > gtop: y1 = 21
                    if y1 > gtop and y2 < gtop: y2 = 21
                    if y1 > gh and y2 > gh: continue
                    if y1 < gh and y2 > gh: y1 = gh
                    if y1 > gh and y2 < gh: y2 = gh
                    self.create_line(xant, y1, x, y2, fill=self.colors[j], width=1, tags='series')
            xant = x
            x += dx
            
        labels = [(label, i) for i, label in enumerate(self.labels) if self.y_max[i] > 0]
        x0 = w - 180
        x1 = x0+5
        x2 = x1+20
        x3 = x2+5
        #self.create_rectangle(x0, 25, x0+155, len(labels) * 20 + 25, fill=self.backcolor, tags='series')
        y0 = 0
        for label, i in labels:
            if self.y_max[i] == 0: continue
            y = y0 * 20 + 35
            y0+=1
            self.create_line(x1, y, x2, y, fill=self.colors[i], width=4, tags='series')
            self.create_text(x3, y - 10, text="%s (Y:%0.1f/div)" % (label, self.y_max[i]/19), tags='series', anchor=tk.NW, fill='white')
        self.create_text(w-200,h-5, text='%0.2f%s' % (self.x_div * 25, self.x_label), anchor=tk.SW, tags='series', fill='white')
        
def get_graphico(series, x_max, x_div, x_label, colors, y_max, labels):
    win = tk.Tk()
    win.title('Curvas do motor')
    gr = GraficoLinha(win)
    gr.pack(fill=tk.BOTH)
    gr.series = series
    gr.x_max = x_max
    gr.x_div = x_div
    gr.x_label = x_label
    gr.y_max = y_max
    gr.colors = colors
    gr.labels = labels
    gr.draw()
    win.mainloop()
    return gr
    
if __name__ == "__main__":
    gr = get_graphico([i for i in range(100)],1,0.01,'s',['#0000FF'],[100],['teste'])
        
