import random
import numpy as np 
import sys

BACKGROUND_COLOR = "green"
SQUARE_SIZE = 100
do_graphics = True
try:
    from tkinter import *
except ImportError:
    print("Warning: Could not find the tkinter module. Graphics disabled")
    do_graphics = False

try:
    from PIL import Image, ImageDraw, ImageTk
except ImportError:
    print("Warning: Could not find the tkinter module. Graphics disabled")
    do_graphics = False 

if do_graphics:
        class Window(Frame):
            def __init__(self, master=None):
                Frame.__init__(self, master)
                self.master = master

# initialize tkinter
root = Tk()
app = Window(root)

# set window title
root.wm_title("Tkinter window")

# show window
root.mainloop()

# if do_graphics:
#     app = Board()
#     app.mainloop()