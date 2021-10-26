import tkinter as tk
from tkinter import Label, filedialog , Text
import os 
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk


def start_app(added):
    
        root = tk.Tk()

        root.configure(background='white')

            
        report_file = open(added[-1], 'r', encoding= "cp1252") 

        xml_file =[]
        error_bool = False
        for line in report_file:
            stripped_line = line.strip()
            #line_list = stripped_line.split()
            xml_file.append(stripped_line)

        report_file.close()
        errorList =[]
        operationList =[]
        counterList =[]
        for line in xml_file:
            if "description='&quot;" in line:
                line = line.split("&quot;")
                operationList.append(line[1])

        for line in xml_file:
            if line.find("simulator_out_of_range") == 1 or line.find("simulator_collision") ==1 or line.find("operation id=")==1:
                if "operation id=" in line :
                    line = line.split('"')
                    counterList.append(line[1])
                    
                    errorList.append(operationList[int(line[1])-1])
                
                elif not (len(errorList)>1 and line == errorList[-1]):
                    errorList.append(line)
                    error_bool = True

            
        t = Text(root, width = 100, height = 10, wrap = "none", background= "white", foreground="black")
        ys = tk.Scrollbar(root, orient = 'vertical', command = t.yview)
        xs = tk.Scrollbar(root, orient = 'horizontal', command = t.xview)
        t['yscrollcommand'] = ys.set
        t['xscrollcommand'] = xs.set
        for line in errorList:
            t.insert('end', line+"\n")
        t.grid(column = 0, row = 0, sticky = 'nwes')
        xs.grid(column = 0, row = 1, sticky = 'we')
        ys.grid(column = 1, row = 0, sticky = 'ns')

        if error_bool is True:
            img = Image.open('thumbs_down.png')
        else: 
            img = Image.open('thumbs_up.png')

        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(image=img)
        img_label.image = img
        img_label.grid(column=3,row=0)
        
        close_btn_text = tk.StringVar()
        close_btn = tk.Button(root, textvariable= close_btn_text, font="Raleway", command= lambda:[exit()])
        close_btn_text.set("Close Report")
        close_btn.grid(column=1, row=2)
        #root.grid_columnconfigure(0, weight = 1)
        #root.grid_rowconfigure(0, weight = 1)


        root.mainloop()

