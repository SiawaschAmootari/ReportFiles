from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import *
from fpdf import FPDF
import win32api 

def btn_clicked():
    print("Button Clicked")

def open_file():
    
    report_file = askopenfile(parent = window, mode ="r", title= "Choose a file" ,filetypes=[("XML file", "*.xml"),("Text file","*.txt")])
    
    if report_file:
        entry0.delete('1.0', END)
        entry1.delete('1.0', END)
        entry2.delete('1.0', END)
        entry3.delete('1.0', END)
        xml_file =[]
        error_bool = False

        for line in report_file:
            
            stripped_line = line.strip()
            xml_file.append(stripped_line)

        report_file.close()
        #Allgemein Start/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        
        generall_line = xml_file[2].split("\"")
        generall_line_two = xml_file[3].split("\"")
        date ="Date: "+ generall_line[1]+"\n"
        time="Time: "+ generall_line[3]+"\n"

        measurement_unit ="Measurement Unit: "+generall_line[9]+"\n"
        no_of_tools = "Number of tools: "+ generall_line_two[1]+"\n"
        nr_of_tools_int = int(generall_line_two[1])
        no_of_blocks ="Number of blocks: "+ generall_line_two[3]+"\n"
        tmp_counter =0

        for line in xml_file:
            tmp_counter +=1
            if "</operations>" in line:
                tmp_counter+=1
                break
        
        time_info = xml_file[tmp_counter-1].replace("timeInfo ","")
        time_info = time_info.replace(" ","\n")
        time_info= time_info.replace("<","")
        time_info= time_info.replace("/>","")
        time_info= "Operation time information: "+ time_info

        generall_information =date+time+measurement_unit + no_of_tools + no_of_blocks + time_info
        gen_list.append(date)
        gen_list.append(time)
        gen_list.append(measurement_unit)
        gen_list.append(no_of_tools)
        gen_list.append(no_of_blocks)
        gen_list.append(time_info)
        # Allgemein End//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


        # Tools Liste////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        tmp_counter = 0
        #tool_list = []
        for line in xml_file:
            tmp_counter +=1
            if "<tools count=" in line:
                break
        for i in range(0,nr_of_tools_int):
            one_tool = xml_file[tmp_counter+i].split("&quot;")
            tool_list.append(one_tool[1])

        one_tool = xml_file[tmp_counter+1].split("&quot;")
        
        # End Tools Liste////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        #Operation Information///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #operation_list=[]
        tmp_counter=0 
        reached_operations= False
        operation_lines = []
        for line in xml_file:            
            if "</operations>" in line:
                break
            tmp_counter +=1
            if "<operations count=" in line:
                reached_operations = True
            if reached_operations:
                operation_lines.append(tmp_counter)
        operation = []
        time_operation = []
        operation_string= ""
        valuable_operation = False
        operation_count = xml_file[operation_lines[0]-1]
        operation_count = operation_count.replace("<","")
        operation_count = operation_count.replace(">","")
        
        operation_list.append(operation_count)
        for i in range(operation_lines[0],operation_lines[-1]):
            if "<operation id=" in xml_file[i]:
                if "TOOLCHANGE" in xml_file[i] or "INITIAL" in xml_file[i]:
                    pass
                else :
                    valuable_operation = True
                    operation = xml_file[i].split(" ")

                    for line in operation:
                          line = line.replace("\'","")
                          line = line.replace("&quot;","")
                          line = line.replace(">","")
                          line = line.replace("<","")
                          if "toolId" in line:
                              line = line.replace("\"","")
                              line = line.replace("toolId=","")
                              line = "tool="+tool_list[int(line)-1]
                          if "no_simulated_moves" in line:
                              line = ""    
                          operation_string += line + " "
                    operation_list.append(operation_string)
                    operation_string=""

            if "<timeInfo"  in xml_file[i] and valuable_operation == True:
                valuable_operation = False
                time_operation = xml_file[i].split(" ")
                for line in time_operation:
                    line = line.replace("\'","")
                    line = line.replace(">","")
                    line = line.replace("<","")
                    line = line.replace("/","")
                    if "0h:00m:00,0s" in line:
                        line = ""
                    operation_string += line + " "
                if len(operation_string) > 10:        
                    operation_list.append(operation_string+"\n")
                operation_string="" 
        
        #End of Operation information //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        # ErrorList
        tmp_counter=0
        #error_list = []
        tmp_list=[]
        line_nr_list=[]

        line_prior =""
        line_next = line_prior
        nci_prior= 0
        nci_next= nci_prior
        last_nci= 0


        for line in xml_file:
            tmp_counter+=1

            if "<operation id=" in line and "toolId" in line and "description" not in line:
                    error_list.extend(tmp_list)
                    line_nr_list.append("Zeile: "+str(tmp_counter)+" ")
                    error_list.append(tool_list[int(line.split("\"")[3])-1])
            
            if "nci number=" in line and "blk=" in line and "custom_information" in line and "completion_factor=":
                last_nci = nci_next
                nci_prior = line.split("\"")[1]
                if nci_prior != nci_next:
                    nci_next = nci_prior
                    error_list.append("nci= "+line.split("\"")[1])
                    #line_nr_list.append("Zeile: "+str(tmp_counter)+" ")

            if "simulator_out_of_range" in line or "simulator_collision" in line:
                error_bool = True
                line_prior = line
                if last_nci != nci_next:
                    line_next = line_prior 
                    error_list.append(line)
                   # line_nr_list.append("Zeile: "+str(tmp_counter)+" ")
                else:
                    if line_prior != line_next:
                        line_next = line_prior       
                        error_list.append(line)
                       # line_nr_list.append("Zeile: "+str(tmp_counter)+" ")

       

        print("file loaded")
        entry0.insert("end",generall_information)
       
        for line in tool_list:
            entry1.insert("end",line+"\n")
        for line in tool_list:
            print(line)

        for line in operation_list:
            entry3.insert("end",line+"\n")
        
        for i in range(0,len(error_list)):
            entry2.insert("end", error_list[i]+"\n")
            tmp_counter=+1
        
        #if error_bool is True:
        #    img = Image.open('thumbs_down.png')
        #else: 
        #    img = Image.open('thumbs_up.png')

        #img = ImageTk.PhotoImage(img)
        #img_label = Label(new_window,image=img)
        #img_label.image = img
        #img_label.grid(column=1,row=0)
        
        #browse_text.set("Browse")
def save_file():
    filename = asksaveasfilename( defaultextension='.pdf', filetypes=[("PDF file","*.pdf")])
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('arial','',4.0)

    pdf.cell(200,3,txt="General information:",ln=1)
    for line in gen_list:
        pdf.cell(200,3,txt=line,ln=2)
    pdf.cell(200,3,txt="Tool information:",ln=1)
    for line in tool_list:
        pdf.cell(200,3,txt=line,ln=1)
    pdf.cell(200,3,txt="Operation information:",ln=2)
    for line in operation_list:
        pdf.cell(200,3,txt=line,ln=1)
    pdf.cell(200,3,txt="Error information:",ln=1)
    for line in error_list:
        pdf.cell(200,3,txt=line,ln=2)
    pdf.output("ReportNeu.pdf")
    

def print_file():
    file_to_print = filedialog.askopenfilename( 
    initialdir="/", title="Select file",  
    filetypes=(("Text files", "*.txt"), ("all files", "*.*"))) 
      
    if file_to_print: 
        win32api.ShellExecute(0, "print", file_to_print, None, ".", 0) 
    #file = pdf

    #FileName = filedialog.askopenfilename(parent = window ,filetypes=["Text files", "*.txt"])
    #filetext = str(entry0.get(1.0,END))
    #file.write(filetext)
    #filetext = str(entry1.get(1.0,END))
    #file.write(filetext)
    #filetext = str(entry3.get(1.0,END))
    #file.write(filetext)
    #filetext = str(entry2.get(1.0,END))
    #file.write(filetext)
    #file.close()
    #FileName.writelines(entry0)
    #for line in entry1:
    #    FileName.writelines(line)
   # for line in entry3:
     #   FileName.writelines(line)
    #for line in entry2:
      #  FileName.writelines(line)
    #FileName.close()        
        
window = Tk()
generall_information=""
tool_list =[]
operation_list=[]
error_list=[]
gen_list=[]
window.geometry("1440x1074")
window.configure(bg = "#ffffff")
canvas = Canvas(window,bg = "#ffffff",height = 1074,width = 1440,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(720.0, 537.0,image=background_img)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(391.0, 414.0,image = entry0_img)

entry0 = Text(bd = 0,bg = "#ffffff",highlightthickness = 0)

entry0.place(x = 89.0, y = 325,width = 604.0,height = 176)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(1060.5, 414.0,image = entry1_img)

entry1 = Text(bd = 0,bg = "#ffffff",highlightthickness = 0)

entry1.place(x = 770.0, y = 325,width = 581.0,height = 176)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(720.0, 876.0,image = entry2_img)

entry2 = Text(bd = 0,bg = "#ffffff",highlightthickness = 0)

entry2.place(x = 89.0, y = 787,width = 1262.0,height = 176)

entry3_img = PhotoImage(file = f"img_textBox3.png")
entry3_bg = canvas.create_image(720.0, 645.0,image = entry3_img)

entry3 = Text(bd = 0,bg = "#ffffff",highlightthickness = 0)

entry3.place(x = 89.0, y = 556,width = 1262.0,height = 176)

canvas.create_text(145.5, 311.0,text = "Generall ",fill = "#000000",font = ("None", int(24.0)))

canvas.create_text(800.5, 307.5,text = "Tools",fill = "#000000",font = ("None", int(24.0)))

canvas.create_text(145.5, 538.5,text = "Operation",fill = "#000000",font = ("None", int(24.0)))

canvas.create_text(125.5, 769.5,text = "Errors",fill = "#000000",font = ("None", int(24.0)))

img0 = PhotoImage(file = f"img0.png")
b0 = Button(image = img0,borderwidth = 0,highlightthickness = 0,command = lambda:open_file(),relief = "flat")

b0.place(x = 81, y = 203,width = 140,height = 39)
img1 = PhotoImage(file = f"img1.png")
b1 = Button(image = img1,borderwidth = 0,highlightthickness = 0,command = lambda:save_file(),relief = "flat")

b1.place(x = 312, y = 203,width = 140,height = 39)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(image = img2,borderwidth = 0,highlightthickness = 0,command = lambda:print_file(),relief= "flat")

b2.place(x = 555, y = 203,width = 140,height = 39)

window.resizable(False, False)
window.mainloop()
