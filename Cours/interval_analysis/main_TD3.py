from TD3.work2do import *
from interval.ifunctions import *
import tkinter as tk
import tkinter.messagebox
import random


# initialisation of the problem
E_val = Interval(23, 26)
I_val = Interval(4, 8)
U1_val = Interval(10, 11)
U2_val = Interval(14, 17)
P_val = Interval(124, 130)

R1_val = Interval(-float('Inf'), float('Inf'))
R2_val = Interval(-float('Inf'), float('Inf'))

# variables for the monte carlo
mcR1 = []
mcR2 = []


# function to draw the monte carlo results
def draw_monte_carlo():
    global R1_val, R2_val, mcR1, mcR2
    step = 60

    if R1_val.inf >= 0 and R1_val.sup <= 5:
        drawing.create_rectangle(R1_val.inf * 60 + 70, 330, R1_val.sup * 60 + 70, 370, fill="green", outline="green",
                                 width=2)
    else:
        drawing.create_rectangle(70, 330, 370, 370, fill="green", outline="green", width=2)
    if R2_val.inf >= 0 and R2_val.sup <= 5:
        drawing.create_rectangle(R2_val.inf * 60 + 70, 380, R2_val.sup * 60 + 70, 420, fill="green", outline="green",
                                 width=2)
    else:
        drawing.create_rectangle(70, 380, 370, 420, fill="green", outline="green", width=2)

    drawing.create_line(70, 350, 370, 350, fill="black", width=1)
    drawing.create_text(40, 350, text="R1", font=("Arial", 20))

    drawing.create_line(70, 400, 370, 400, fill="black", width=1)
    drawing.create_text(40, 400, text="R2", font=("Arial", 20))

    drawing.create_text(70, 320, text="0", font=("Arial", 15))
    drawing.create_text(370, 320, text="5", font=("Arial", 15))

    for i in range(0, 6):
        drawing.create_line(i * step + 70, 330, i * step + 70, 370, fill="black", width=1)
        drawing.create_line(i * step + 70, 380, i * step + 70, 420, fill="black", width=1)

    for v in mcR1:
        drawing.create_line(v * step + 70, 330, v * step + 70, 370, fill="red", width=1)
    for v in mcR2:
        drawing.create_line(v * step + 70, 380, v * step + 70, 420, fill="red", width=1)


# function to draw system
def draw_schema():
    global drawing
    drawing.create_rectangle(100, 50, 300, 250, fill="white", outline="black", width=2)
    drawing.create_oval(80, 130, 120, 170, outline="black", fill="white", width=2)
    drawing.create_rectangle(280, 70, 320, 120, fill="white", outline="black", width=2)
    drawing.create_rectangle(280, 180, 320, 230, fill="white", outline="black", width=2)
    drawing.create_line(70, 130, 70, 170, fill="black", width=2)
    drawing.create_line(70, 130, 65, 140, fill="black", width=2)
    drawing.create_text(50, 150, text="E", font=("Arial", 20))

    drawing.create_line(270, 70, 270, 120, fill="black", width=2)
    drawing.create_line(270, 70, 265, 80, fill="black", width=2)
    drawing.create_text(240, 100, text="U1", font=("Arial", 20))
    drawing.create_text(345, 100, text="R1", font=("Arial", 20))

    drawing.create_line(270, 170, 270, 230, fill="black", width=2)
    drawing.create_line(270, 170, 265, 180, fill="black", width=2)
    drawing.create_text(240, 210, text="U2", font=("Arial", 20))
    drawing.create_text(345, 210, text="R2", font=("Arial", 20))

    drawing.create_line(200, 50, 190, 45, fill="black", width=2)
    drawing.create_text(195, 30, text="I", font=("Arial", 20))


# main drawing function
def draw(): 
    global drawing
    drawing.delete("all")
    draw_schema()
    draw_monte_carlo()


# function to generate the monte carlo values
def rand_r():
    global E_val, U1_val, U2_val, I_val, P_val, R1_val, R2_val, mcR1, mcR2

    del mcR1[:]
    del mcR2[:]

    for i in range(0, 300):
        re = random.uniform(E_val.inf, E_val.sup)
        ru1 = random.uniform(U1_val.inf, U1_val.sup)
        ri = random.uniform(I_val.inf, I_val.sup)
        ru2 = re-ru1
        rp = re*ri
        if(U2_val.inf <= ru2 <= U2_val.sup) and (P_val.inf <= rp <= P_val.sup):
            mcR1.append(ru1/ri)
            if mcR1[len(mcR1)-1] < R1_val.inf or mcR1[len(mcR1)-1] > R1_val.sup:
                tk.messagebox.showerror("R1 - Lost of solution!", str(mcR1[len(mcR1)-1]) + " not in " + str(R1_val))
                break
            mcR2.append(ru2/ri)
            if mcR2[len(mcR2)-1] < R2_val.inf or mcR2[len(mcR2)-1] > R2_val.sup:
                tk.messagebox.showerror("R2 - Lost of solution!", str(mcR2[len(mcR2)-1]) + " not in " + str(R2_val))
                break


# function to generate the monte carlo values
def btn_contract_event(event):
    global U1_val, U2_val, R1_val, R2_val, E_val, P_val, I_val
    print("***********")
    print("before contraction:")
    print('\tR1:' + str(R1_val))
    print('\tR2:' + str(R2_val))
    print('\tE:' + str(E_val))
    print('\tI:' + str(I_val))
    print('\tU1:' + str(U1_val))
    print('\tU2:' + str(U2_val))
    print('\tP:' + str(P_val))

    E_val, U1_val, U2_val, R1_val, R2_val, I_val, P_val = c_system(E_val, U1_val, U2_val, R1_val, R2_val, I_val, P_val)

    print("-----")
    print("after contraction:")
    print('\tR1:' + str(R1_val))
    print('\tR2:' + str(R2_val))
    print('\tE:' + str(E_val))
    print('\tI:' + str(I_val))
    print('\tU1:' + str(U1_val))
    print('\tU2:' + str(U2_val))
    print('\tP:' + str(P_val))
    print("***********")
    draw()
    return event


# function to generate the monte carlo values
def btn_test_event(event):
    rand_r()
    draw()
    return event


# creation of the window
window = tk.Tk()
window.title("System")
window.geometry("400x500+150+100")
window.resizable(width=False, height=False)

drawing = tk.Canvas(window, background="white")
drawing.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP)

btnTest = tk.Button(window, text="Test values")
btnTest.pack(fill=tk.X, side=tk.BOTTOM)
btnTest.bind("<Button-1>", btn_test_event)

btnContract = tk.Button(window, text="Contract")
btnContract.pack(fill=tk.X, side=tk.BOTTOM)
btnContract.bind("<Button-1>", btn_contract_event)

draw()

window.mainloop()
