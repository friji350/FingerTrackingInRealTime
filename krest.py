import time
from tkinter import *
import math
import krest_trest

class Paint(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.color = "black"
        self.brush_size = 2
        self.setUI()
        self.points = []

    def set_color(self, new_color):
        self.color = new_color

    def set_brush_size(self, new_size):
        self.brush_size = new_size

    def draw(self, event):
        if event.x < 400 and event.y < 400:

            self.canv.create_oval(event.x - self.brush_size,
                                  event.y - self.brush_size,
                                  event.x + self.brush_size,
                                  event.y + self.brush_size,
                                  fill=self.color, outline=self.color)

            self.points.append([event.x, event.y])

    def delete_all(self):
        self.canv.delete("all")
        self.points = []
        self.canv.create_rectangle(0, 400, 2000, 2000,
                           fill='yellow')
        self.canv.create_rectangle(400, 0, 2000, 2000,
                                   fill='yellow')

    def points_add(self):
        new_points = []
        for i in range(0 , len(self.points)-1):
            new_points.append(self.points[i])
            new_point = []
            new_x = math.fabs(self.points[i][0] + self.points[i+1][0])/2
            new_y = math.fabs(self.points[i][1] + self.points[i+1][1])/2

            new_point.append(new_x)
            new_point.append(new_y)

            new_points.append(new_point)

        return new_points


    def send_robot(self):
        man = []
        a_max = 0
        print(self.points)
        time.sleep(3)
        print(len(self.points))
        for j in range(0, len(self.points)-1):
            i = self.points[j]

            dis = math.sqrt((self.points[j][0] - self.points[j+1][0]) ** 2 + (self.points[j][1] - self.points[j+1][1]) ** 2)
            x = i[0]*4
            y = i[1]*4
            rxox = 600
            rxoy = 0

            trox = x
            troy = y
            try:
                angle = math.atan((rxoy - troy) / (rxox - trox))
            except:
                angle = 90
            x1 = rxox  # начало
            x2 = trox  # конец
            if x1 > x2:
                angle += math.pi

            angle = round(math.degrees(angle))

            print(i)

            x_robot = -round(((math.fabs(math.sqrt((x - 600) ** 2 + (y - 0) ** 2)))/40), 2)
            x_robot += 0.02

            if a_max < dis:
                a_max = dis

            y_robot = 2.1

            print(x)

            man.append([x_robot, y_robot, angle])

            if angle < 180:
                krest_trest.go_to([x_robot, y_robot], angle,False)

        print(a_max)


        print(man)

        self.canv.delete("all")
        self.points = []
        self.canv.create_rectangle(0, 400, 2000, 2000,
                                       fill='yellow')
        self.canv.create_rectangle(400, 0, 2000, 2000,
                                       fill='yellow')


    def setUI(self):

        self.parent.title("Pythonicway PyPaint")  # Устанавливаем название окна
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне

        self.columnconfigure(6, weight=1) # Даем седьмому столбцу возможность растягиваться, благодаря чему кнопки не будут разъезжаться при ресайзе
        self.rowconfigure(2, weight=1) # То же самое для третьего ряда

        self.canv = Canvas(self, bg="white")  # Создаем поле для рисования, устанавливаем белый фон
        self.canv.grid(row=2, column=0, columnspan=7,
                       padx=5, pady=5, sticky=E+W+S+N)  # Прикрепляем канвас методом grid. Он будет находится в 3м ряду, первой колонке, и будет занимать 7 колонок, задаем отступы по X и Y в 5 пикселей, и заставляем растягиваться при растягивании всего окна
        self.canv.bind("<B1-Motion>", self.draw) # Привязываем обработчик к канвасу. <B1-Motion> означает "при движении зажатой левой кнопки мыши" вызывать функцию draw

        color_lab = Label(self, text="Color: ") # Создаем метку для кнопок изменения цвета кисти
        color_lab.grid(row=0, column=0, padx=6) # Устанавливаем созданную метку в первый ряд и первую колонку, задаем горизонтальный отступ в 6 пикселей

        red_btn = Button(self, text="Red", width=10,
                         command=lambda: self.set_color("red")) # Создание кнопки:  Установка текста кнопки, задание ширины кнопки (10 символов), функция вызываемая при нажатии кнопки.
        red_btn.grid(row=0, column=1) # Устанавливаем кнопку

        # Создание остальных кнопок повторяет ту же логику, что и создание
        # кнопки установки красного цвета, отличаются лишь аргументы.

        green_btn = Button(self, text="Green", width=10,
                           command=lambda: self.set_color("green"))
        green_btn.grid(row=0, column=2)

        blue_btn = Button(self, text="Blue", width=10,
                          command=lambda: self.set_color("blue"))
        blue_btn.grid(row=0, column=3)

        black_btn = Button(self, text="Black", width=10,
                           command=lambda: self.set_color("black"))
        black_btn.grid(row=0, column=4)

        white_btn = Button(self, text="Send", width=10,
                           command=lambda: self.send_robot())
        white_btn.grid(row=0, column=5)

        clear_btn = Button(self, text="Clear all", width=10,
                           command=lambda: self.delete_all())
        clear_btn.grid(row=0, column=6, sticky=W)

        size_lab = Label(self, text="Brush size: ")
        size_lab.grid(row=1, column=0, padx=5)
        one_btn = Button(self, text="Two", width=10,
                         command=lambda: self.set_brush_size(2))
        one_btn.grid(row=1, column=1)

        two_btn = Button(self, text="Five", width=10,
                         command=lambda: self.set_brush_size(5))
        two_btn.grid(row=1, column=2)

        five_btn = Button(self, text="Seven", width=10,
                          command=lambda: self.set_brush_size(7))
        five_btn.grid(row=1, column=3)

        seven_btn = Button(self, text="Ten", width=10,
                           command=lambda: self.set_brush_size(10))
        seven_btn.grid(row=1, column=4)

        ten_btn = Button(self, text="Twenty", width=10,
                         command=lambda: self.set_brush_size(20))
        ten_btn.grid(row=1, column=5)

        twenty_btn = Button(self, text="Fifty", width=10,
                            command=lambda: self.set_brush_size(50))
        twenty_btn.grid(row=1, column=6, sticky=W)

        self.canv.create_rectangle(0, 300, 2000, 2000,
                           fill='yellow')
        self.canv.create_rectangle(300, 0, 2000, 2000,
                                   fill='yellow')


def main():
    root = Tk()
    root.geometry("850x500+300+300")
    app = Paint(root)
    root.mainloop()


if __name__ == '__main__':
    main()