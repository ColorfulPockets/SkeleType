from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# root for main window
root = Tk(className=" SkeleType")
textArea = Text(root, width = 100, height = 20)
textArea.grid(row=0,column=0)
scroll = Scrollbar(root)
scroll.grid(row=0,column=1, sticky=NS)
scroll.config(command=textArea.yview)
textArea.config(yscrollcommand=scroll.set)
output_area = Text(root, width = 100, height = 20)
output_area.grid(row=1,column=0)
output_scroll = Scrollbar(root)
output_scroll.grid(row=1,column=1, sticky = NS)
output_scroll.config(command=output_area.yview)
output_area.config(yscrollcommand=output_scroll.set)

# set up initial mark in textArea
textArea.mark_set("start", INSERT)
textArea.mark_gravity("start", LEFT)

def checklastword(event):
    run()
    textArea.mark_unset("start")
    textArea.mark_set("start", INSERT)
    textArea.mark_gravity("start", LEFT)

# In textArea, detect every time space or return is pressed
textArea.bind('<space>', checklastword)
textArea.bind('<Return>', checklastword)

#
# FUNCTIONS
#

#TODO: make run function take all the text and split it up


def run():
    print(textArea.get("start", INSERT))

def openFile():
    file = filedialog.askopenfile(parent=root, mode='rb', title='Select a text file')

    if file != None:
        contents = file.read()
        textArea.insert('1.0', contents)
        file.close()

def saveFile():
    file = filedialog.asksaveasfile(mode='w')

    if file != None:
        # removes last character, which is extra return
        data = textArea.get('1.0', END+'-1c')
        file.write(data)
        file.close()

def quitProgram():
    if messagebox.askyesno("Quit","Are you sure you want to quit?"):
        root.destroy()

def about():
    messagebox.showinfo("About","If you're seeing this message, I forgot to update this message")
# create the menu
menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(label="Run", command=run)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New")
fileMenu.add_command(label="Open", command=openFile)
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=quitProgram)

menu.add_cascade(label="About", command=about)

# keep window open
root.mainloop()