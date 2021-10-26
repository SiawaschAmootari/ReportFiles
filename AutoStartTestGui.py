
from tkinter import font
from tkinter.constants import COMMAND
import TestGui
import os, time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile 

def start_watchdog():
    path_to_watch = "C:\\Users\\samootari\\OneDrive\\Desktop\\Python"
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    done = True
    while done:
        time.sleep (10)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added: print ("Added: ", ", ".join (added)) 
        if removed: print ("Removed: ", ", ".join (removed))
  

        print(type(added))
  
        if len(added)>0:
            if ".xml" in added[-1]:
                print("i´m in")
                TestGui.start(added)
                before = dict ([(f, None) for f in os.listdir (path_to_watch)])
                done = False




def start_report_analyse():
    start.destroy()
    button_text.set("started")
    start_watchdog()

def close_window():
    exit()    
    
start = tk.Tk()

canvas = tk.Canvas(start,width=426, height=188, background="blue")
canvas.grid(columnspan=3, rowspan=3)


logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column =1 , row=0)

button_text = tk.StringVar()
button_btn = tk.Button(start, textvariable= button_text, font="Raleway", command= lambda:start_report_analyse() )
button_text.set("Start Report Analyse")
button_btn.grid(column=1, row=2)

button_text_two = tk.StringVar()
button_btn_two = tk.Button(start, textvariable= button_text_two, font="Raleway", command= lambda:close_window() )
button_text_two.set("Exit")
button_btn_two.grid(column=2, row=2)


        

start.mainloop()



