from tkinter import font
from tkinter.constants import COMMAND
import os, time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile 
import WatchDog

class ReportApp:
    
    def __init__(self):
        self.root = tk.Tk()

        canvas = tk.Canvas(self.root,width=426, height=188, background="blue")
        canvas.grid(columnspan=3, rowspan=3)

        
        logo = Image.open('logo.png')
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo)
        logo_label.image = logo
        logo_label.grid(column =1 , row=0)

        button_text = tk.StringVar()
        button_btn = tk.Button(self.root, textvariable= button_text, font="Raleway",height= 1, width= 18, command= lambda:[self.root.destroy(), WatchDog()])
        button_text.set("Start Report Analyse")
        button_btn.grid(column=1, row=2)

        button_text_two = tk.StringVar()
        button_btn_two = tk.Button(self.root, textvariable= button_text_two, font="Raleway",command=lambda:exit(), height= 1, width= 18)
        button_text_two.set("Exit  Report Analyse")
        button_btn_two.grid(column=1, row=3)
        self.root.mainloop()

app = ReportApp()

def startApp():
    app = ReportApp()


