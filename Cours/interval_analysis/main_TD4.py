import tkinter as tk
import tkinter.messagebox
from interval.interval import Interval
from TD4.work2do import *


# domain for the drawing [x][y]
domain = [Interval(0, 30), Interval(0, 30)]

# default values for the window size
width = 1
height = 3

# domain for the drawing [x][y]
b1 = [Interval(2, 4), Interval(3, 5)]
b2 = [Interval(5, 20), Interval(9, 20)]
dst = Interval(5.5, 6.5)
x_test = -1
y_test = -1


# Main drawing function, it is called each time the window needs to be redraw
def draw(): 
    global drawing, b1, b2, dst, x_test, y_test
    drawing.delete("all")
    draw_box(b1, "green")
    draw_box(b2, "blue")
    draw_test_circles(x_test, y_test, dst)
    draw_axes(1)


# function to draw the "test circles"
def draw_test_circles(x, y, border):
    global drawing
    # circle inf
    drawing.create_oval(real2draw_x(x - border.inf), real2draw_y(y + border.inf), real2draw_x(x + border.inf),
                        real2draw_y(y - border.inf))
    # circle sup
    drawing.create_oval(real2draw_x(x - border.sup), real2draw_y(y + border.sup), real2draw_x(x + border.sup),
                        real2draw_y(y - border.sup))


# to convert an X value from the world to the window frame
def real2draw_x(x):
    global domain, width
    step = width/(domain[0].sup-domain[0].inf)
    x_draw = (x-domain[0].inf)*step
    return x_draw


# to convert an Y value from the world to the window frame
def real2draw_y(y):
    global domain, height
    step = height/(domain[1].sup-domain[1].inf)
    y_draw = (y-domain[1].inf)*step
    return height-y_draw


# to convert an X value from the window frame to the world
def draw2real_x(x):
    global domain, width
    step = abs(domain[0].sup-domain[0].inf)/float(width)
    x_real = x*step+domain[0].inf
    return x_real


# to convert an Y value from the world to the window frame
def draw2real_y(y):
    global domain, height
    step = abs(domain[1].sup-domain[1].inf)/float(height)
    y_real = (height-y)*step+domain[1].inf
    return y_real


# to get the pointed coordinates of the window
def mouse(event):
    global x_test, y_test
    x_test = draw2real_x(event.x)
    y_test = draw2real_y(event.y)
    draw()


# function to draw the origin axes
def draw_axes(step=1.0, color="grey"):
    global domain, drawing
    i = domain[0].inf
    while i < domain[0].sup+step:
        if i % 5 == 0:
            val_width = 2
        else:
            val_width = 1
        drawing.create_line(real2draw_x(i), real2draw_y(domain[1].inf), real2draw_x(i), real2draw_y(domain[1].sup),
                            fill=color, width=val_width)
        i = i+step
    i = domain[1].inf
    while i < domain[1].sup+step:
        if i % 5 == 0:
            val_width = 2
        else:
            val_width = 1
        drawing.create_line(real2draw_x(domain[0].inf), real2draw_y(i), real2draw_x(domain[0].sup), real2draw_y(i),
                            fill=color, width=val_width)
        i = i+step


# function to draw a box
def draw_box(box, color="white"):
    global drawing
    x1 = real2draw_x(box[0].sup)
    y1 = real2draw_y(box[1].inf)
    x2 = real2draw_x(box[0].inf)
    y2 = real2draw_y(box[1].sup)
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 < 0:
        x2 = 0
    if y2 < 0:
        y2 = 0
    drawing.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)


# function to get the new size of the window
def resize_event(event):
    global width, height
    width = event.width
    height = event.height
    draw()


# function to update the values of the labels
def update_labels():
    global b1, b2, dst, domain, label_b1, label_b2, label_dst, label_domain
    label_b1.config(text="[b1]: " + str(b1[0]) + ", " + str(b1[1]))
    label_b2.config(text="[b2]: " + str(b2[0]) + ", " + str(b2[1]))
    label_dst.config(text="[dst]: " + str(dst))
    label_domain.config(text="[domain]: " + str(domain[0]) + ", " + str(domain[1]))


# function to call the contractor
def btn_contract_event(event):
    global b1, b2, dst, label_b1, label_b2, label_dst
    dst, b1, b2 = c_dst(dst, b1, b2)
    update_labels()
    draw()
    return event


# function to test is a text is a float
def isfloat(txt):
    try:
        float(txt)
        return True
    except ValueError:
        return False


# function to modify the parameters
def btn_set_param_event(event):
    global b1, b2, dst, domain, entry_b1, entry_b2, entry_dst, entry_domain, label_b1, label_b2, label_dst, label_domain
    b1text = entry_b1.get()
    b2text = entry_b2.get()
    dst_text = entry_dst.get()
    domain_text = entry_domain.get()

    if b1text != "":
        tab = [float(f) for f in b1text.split() if isfloat(f)]
        if len(tab) != 4:
            tk.messagebox.showerror("Error", "The value of [b1] should be 4 floats separated by spaces")
        else:
            b1 = [Interval(tab[0], tab[1]), Interval(tab[2], tab[3])]
    if b2text != "":
        tab = [float(f) for f in b2text.split() if isfloat(f)]
        if len(tab) != 4:
            tk.messagebox.showerror("Error", "The value of [b2] should be 4 floats separated by spaces")
        else:
            b2 = [Interval(tab[0], tab[1]), Interval(tab[2], tab[3])]
    if dst_text != "":
        tab = [float(f) for f in dst_text.split() if isfloat(f)]
        if len(tab) != 2:
            tk.messagebox.showerror("Error", "The value of [dst] should be 2 floats separated by spaces")
        else:
            dst = Interval(tab[0], tab[1])
    if domain_text != "":
        tab = [float(f) for f in domain_text.split() if isfloat(f)]
        if len(tab) != 4:
            tk.messagebox.showerror("Error", "The value of [domain] should be 4 floats separated by spaces")
        else:
            domain = [Interval(tab[0], tab[1]), Interval(tab[2], tab[3])]
    update_labels()
    draw()
    return event


# function to close both windows at the same time
def on_closing_window():
    global window, form
    window.destroy()
    form.destroy()


# creation of the window
window = tk.Tk()
window.title("Distance contraction")  # define the name of the window
window.geometry("400x400+150+100")  # define the original size and position of the window
drawing = tk.Canvas(window, background='white')  # define the background color
drawing.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP)
drawing.bind('<Configure>', resize_event)  # to get the resize event
drawing.bind("<Button-1>", mouse)  # get the mouse click position


btnTest = tk.Button(window, text="Contract")  # creation of the start button
btnTest.pack(fill=tk.X, side=tk.BOTTOM)  # add the button to the window
btnTest.bind("<Button-1>", btn_contract_event)  # event for the contract button

window.protocol("WM_DELETE_WINDOW", on_closing_window)

# creation of the window with the text boxes
form = tk.Tk()
form.title("Contraction parameters")  # define the name of the window
form.geometry("460x120+100+50")  # define the original size and position of the window

entry_b1 = tk.Entry(form)
label_b1 = tk.Label(form, text="[b1]: " + str(b1))
entry_b2 = tk.Entry(form)
label_b2 = tk.Label(form, text="[b2]: " + str(b2))
entry_dst = tk.Entry(form)
label_dst = tk.Label(form, text="[dst]: " + str(dst))
entry_domain = tk.Entry(form)
label_domain = tk.Label(form, text="[domain]: " + str(domain))

entry_b1.grid(row=0, column=0, sticky="W")
label_b1.grid(row=0, column=1, sticky="W")
entry_b2.grid(row=1, column=0, sticky="W")
label_b2.grid(row=1, column=1, sticky="W")
entry_dst.grid(row=2, column=0, sticky="W")
label_dst.grid(row=2, column=1, sticky="W")
entry_domain.grid(row=3, column=0, sticky="W")
label_domain.grid(row=3, column=1, sticky="W")

form.columnconfigure(1, weight=1)

btnSetParam = tk.Button(form, text="Modify parameters")
btnSetParam.grid(row=4, column=0, columnspan=2, sticky="N,S,E,W")

btnSetParam.bind("<Button-1>", btn_set_param_event)  # to get the resize event

form.protocol("WM_DELETE_WINDOW", on_closing_window)
update_labels()
# call of the loop to display the window
window.mainloop()
