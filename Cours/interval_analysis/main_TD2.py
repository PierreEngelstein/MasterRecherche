import tkinter as tk
from interval.interval import Interval
from TD2.display_functions import *
from TD2.work2do import sivia_2d, inclusion_test

# size of the displayed area
gv.DOMAIN = [Interval(0, 15), Interval(0, 15)]

b1 = [Interval(0, 1), Interval(5, 10)]
b2 = [Interval(2, 7), Interval(1, 2)]
b3 = [Interval(2, 5), Interval(8, 9)]
b4 = [Interval(8, 10), Interval(5, 3)]
b5 = [Interval(7, 8), Interval(7, 8)]

gv.RED.append(b1)
gv.BLUE.append(b2)
gv.YELLOW.append(b3)
gv.BLUE.append(b4)
gv.YELLOW.append(b5)


def btn_test_event(event):
    print("SIVIA")
    sivia_2d(gv.DOMAIN, 0.2, gv.RED, gv.BLUE, gv.YELLOW, inclusion_test)
    draw()
    return event


# creation of the window
window = tk.Tk()
window.title("Display Boxes")  # define the name of the window
window.geometry("400x400+100+50")  # define the original size and position of the window
gv.DRAWING = tk.Canvas(window, background='white')  # define the background color
gv.DRAWING.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP)
gv.DRAWING.bind('<Configure>', resize_event)  # to get the size change
gv.DRAWING.bind("<Button-1>", mouse)  # get the mouse click position


btnTest = tk.Button(window, text="Test")  # creation of a start button
btnTest.pack(fill=tk.X, side=tk.BOTTOM)  # adding the start button in the window
btnTest.bind('<Button-1>', btn_test_event)

# call of the loop to display the window
window.mainloop()
