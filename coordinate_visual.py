from tkinter import Tk, Canvas, Frame, BOTH, IntVar, LEFT,Button, Entry
from tkinter.ttk import Frame, Label, Scale, Style
import math 
import serial
import time

class Example(Frame):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.master.title("Рисуем х")
        self.pack(fill=BOTH, expand=1)

        self.a1 = 186
        self.a2 = 172

        scale1 = Scale(self, from_=70, to=180, command=self.onScale)
        scale1.pack(padx=15)

        scale2 = Scale(self, from_=-180, to=30, command=self.onScale2)
        scale2.pack(padx=45)
 
        self.var1 = 90
        self.var2 = 90
 
        self.canvas = Canvas(self)


        self.b1 = 20-float(self.a1*math.cos(math.radians(self.var1)))
        self.b2 = 400-float(self.a1*math.sin(math.radians(self.var1)))



        print(float(self.a1*math.cos(math.radians(self.var1))))
        self.canvas.create_line(20, 400, self.b1, self.b2)
        self.canvas.create_line(self.b1, self.b2, self.b1+float(self.a2*math.cos(math.radians(self.var2+self.var1))), self.b2+float(self.a2*math.sin(math.radians(self.var2+self.var1))))

        self.g1 = IntVar()
        self.g2 = IntVar()
        self.entryg1 = Entry(width=20, textvariable=self.g1)
        self.entryg1.pack(padx=15, pady=20)
        self.entryg2 = Entry(width=20, textvariable=self.g2)
        self.entryg2.pack(padx=45, pady=20)

        self.resultButton = Button(text = 'Get Result',
                         command=self.res)

        self.resultButton.pack(padx=65, pady=20)
        

 
        self.canvas.pack(fill=BOTH, expand=1)

    def res(self):
        self.var1 = int(self.g1.get())
        self.var2 = int(self.g2.get())
        self.b1 = 20-float(self.a1*math.cos(math.radians(self.var1)))
        self.b2 = 400-float(self.a1*math.sin(math.radians(self.var1)))
        self.canvas.delete("all")
        self.canvas.create_line(20, 400, self.b1, self.b2)
        self.canvas.create_line(self.b1, self.b2, self.b1+float(self.a2*math.cos(math.radians(self.var2+self.var1))), self.b2+float(self.a2*math.sin(math.radians(self.var2+self.var1))))
        self.canvas.pack(fill=BOTH, expand=1)
        self.var2 = 180 - abs(self.var2)
        
        print('#####################################')
        print(self.b1+float(self.a2*math.cos(math.radians(self.var2+self.var1))))
        print(self.b2+float(self.a2*math.sin(math.radians(self.var2+self.var1))))

        
        ser = serial.Serial("COM4", baudrate = 9600, timeout = 1)

        ser.write(f'A0 B{self.var1} C{self.var2}'.encode('utf-8'))

        print('#####################################')

    def onScale(self, val):
        v = int(float(val))
        self.var1 = v
        self.b1 = float(self.a1*math.cos(math.radians(self.var1)))
        self.b2 = float(self.a1*math.sin(math.radians(self.var1)))
        self.canvas.delete("all")
        self.canvas.create_line(20, 400, 20-self.b1, 400-self.b2)
        self.canvas.create_line(20-self.b1, 400-self.b2, 20-self.b1+float(self.a2*math.cos(math.radians(self.var2+self.var1))), self.b2+float(self.a2*math.sin(math.radians(self.var2+self.var1))))
        
        self.canvas.pack(fill=BOTH, expand=1)
        self.var2 = 180 - abs(self.var2)

        print(self.b1+float(self.a2*math.cos(math.radians(self.var2+self.var1))))
        print(self.b2+float(self.a2*math.sin(math.radians(self.var2+self.var1))))

        print('#####################################')
    
    def onScale2(self, val):
        v = int(float(val))
        self.var2 = v
        self.b1 = float(self.a1*math.cos(math.radians(self.var1)))
        self.b2 = float(self.a1*math.sin(math.radians(self.var1)))
        self.canvas.delete("all")
        self.canvas.create_line(20, 400, 20-self.b1, 400-self.b2)
        self.canvas.create_line(20-self.b1, 400-self.b2, (20-self.b1)+float(self.a2*math.cos(math.radians(self.var2+self.var1))), (400-self.b2)+float(self.a2*math.sin(math.radians(self.var2+self.var1))))
        
        self.canvas.pack(fill=BOTH, expand=1)
        self.var2 = 180 - abs(self.var2)

        print(self.b1+float(self.a2*math.cos(math.radians(self.var2+self.var1))))
        print(self.b2+float(self.a2*math.sin(math.radians(self.var2+self.var1))))

        print('#####################################')
 
 
def main():
    root = Tk()
    ex = Example()
    root.geometry("800x650+300+300")
    root.mainloop()
 
 
if __name__ == '__main__':
    main()