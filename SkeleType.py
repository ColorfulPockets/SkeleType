from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import rubik
import blockdefinitions

# root for main window
root = Tk(className=" SkeleType")
textArea = Text(root, width=100, height=20)
textArea.grid(row=0, column=0, sticky=NSEW)
scroll = Scrollbar(root)
scroll.grid(row=0, column=1, sticky=NS)
scroll.config(command=textArea.yview)
textArea.config(yscrollcommand=scroll.set)
output_area = Text(root, width=100, height=20)
output_area.grid(row=1, column=0, sticky=NSEW)
output_scroll = Scrollbar(root)
output_scroll.grid(row=1, column=1, sticky=NS)
output_scroll.config(command=output_area.yview)
output_area.config(yscrollcommand=output_scroll.set)

textArea.insert(1.0, "Scramble: ")

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

x = rubik.Algorithm('x')
y = rubik.Algorithm('y')
z = rubik.Algorithm('z')


# Creates a mark "start" at the start of the last word typed, runs run(), unmarks "start"
def checklastword(event):
    textArea.mark_set("start", textArea.index(INSERT) + "-1c wordstart")

    # checks for special case where word has hyphen, forces marker to start of word
    if textArea.get(textArea.index("start") + "-1c", textArea.index("start")) == "-":
        textArea.mark_unset("start")
        textArea.mark_set("start", textArea.index(INSERT) + "-1c wordstart -4c")

    textArea.mark_gravity("start", LEFT)
    run()
    textArea.mark_unset("start")


# In textArea, detect every time space or return is pressed
textArea.bind('<space>', checklastword)
textArea.bind('<Return>', checklastword)

#
# FUNCTIONS
#


def run():
    short = textArea.get("start", INSERT)

# The dictionary "steps" contains all different steps in the solve that can be highlighted.
# Keys are the abbreviations used in the skeleton, dict values are function names
    steps = {
        "222": twobytwo,
        "2x2x2": twobytwo,
        "2X2X2": twobytwo,
        "2x2": twobytwo,
        "2X2": twobytwo,
        "sq": square,
        "SQ": square,
        "122": square,
        "1x2x2": square,
        "1X2X2": square,
        "square": square,
        "SQUARE": square,
        "221": square,
        "2x2x1": square,
        "2X2X1": square,
        "123": roux,
        "1x2x3": roux,
        "1X2X3": roux,
        "321": roux,
        "3x2x1": roux,
        "3X2X1": roux,
        "roux": roux,
        "ROUX": roux,
        "wall": roux,
        "WALL": roux,
        "223": twobytwobythree,
        "322": twobytwobythree,
        "2x2x3": twobytwobythree,
        "2X2X3": twobytwobythree,
        "3x2x2": twobytwobythree,
        "3X2X2": twobytwobythree,
        "petrus": twobytwobythree,
        "PETRUS": twobytwobythree,
        "F2L-1": f2lminusone,
        "f2l-1": f2lminusone,
        "xxxcross": f2lminusone,
        "XXXCROSS": f2lminusone,
        "eo": eo,
        "EO": eo,
        "p-": pseudo,
        "P-": pseudo,
        "dr": domino,
        "DR": domino,
        "domino": domino,
        "DOMINO": domino,
        "dom": domino,
        "DOM": domino,
        "pdr": partialdomino,
        "PDR": partialdomino,
        "diamond": diamond,
        "DIAMOND": diamond,
        "f2l-2": diamond,
        "F2L-2": diamond,
        "solved": solved,
        "SOLVED": solved,
        "FINISH": solved,
        "finish": solved,
        "finished": solved,
        "FINISHED": solved,
        "solve": solved,
        "done": solved,
        "DONE": solved,
        "Scramble:": scramble,
        "SCRAMBLE:": scramble,
        "scramble:": scramble,
        "Solution:": solution,
        "SOLUTION:": solution,
        "solution:": solution,
        "f2l": f2l,
        "F2L": f2l,
        "skip": solved,
        "SKIP": solved,
        "cross": cross,
        "CROSS": cross
    }

    func = steps.get(short, clear_tags)
    func()


def solution():
    colorgreen()


def scramble():
    colorgreen()


def eo():
    coloryellow()


def pseudo():
    coloryellow()


def domino():
    coloryellow()


def partialdomino():
    coloryellow()


def diamond():
    c = rubik.Cube()
    c.apply_alg(movealg())

    if blockdefinitions.check12positions(blockdefinitions.diamondsolved, c):
        colorgreen()
    else:
        colorred()


def solved():
    c = rubik.Cube()
    c.apply_alg(movealg())

    if c.solved():
        colorgreen()
    else:
        colorred()


def twobytwo():
    c = rubik.Cube()
    c.apply_alg(movealg())

    if blockdefinitions.check8positions(blockdefinitions.twobytwosolved, c):
        colorgreen()
    else:
        colorred()


def square():
    c = rubik.Cube()
    c.apply_alg(movealg())

    if blockdefinitions.check24positions(blockdefinitions.square_solved, c):
        colorgreen()
    else:
        colorred()


def roux():
    c = rubik.Cube()
    c.apply_alg(movealg())
    if blockdefinitions.check24positions(blockdefinitions.rouxsolved, c):
        colorgreen()
    else:
        colorred()


def twobytwobythree():
    c = rubik.Cube()
    c.apply_alg(movealg())

    if blockdefinitions.check12positions(blockdefinitions.twobytwobythreesolved, c):
        colorgreen()
    else:
        colorred()


def f2lminusone():
    c = rubik.Cube()
    c.apply_alg(movealg())

    if blockdefinitions.check24positions(blockdefinitions.f2lminus1solved, c):
        colorgreen()
    else:
        colorred()


def f2l():
    c = rubik.Cube()
    c.apply_alg(movealg())

    if blockdefinitions.check6positions(blockdefinitions.f2lsolved, c):
        colorgreen()
    else:
        colorred()


def cross():
    c = rubik.Cube()
    c.apply_alg(movealg())

    if blockdefinitions.check6positions(blockdefinitions.cross_solved, c):
        colorgreen()
    else:
        colorred()


# TODO Make this way simpler with a stack based system
def movestring(text):
    split_text = text.split()
    moves = ""
    invmoves = ""
    inverse = False
    for word in split_text:
        if word in rubik.FACE_MOVES and not inverse:
            moves = moves + " " + word
        elif len(word) == 2 and not inverse and word[0] in rubik.FACE_MOVES and word[1] in ["'", "2"]:
                moves = moves + " " + word
        elif word[0] == "(" and word[len(word) - 1] == ")":
            invword = word[1:len(word) - 1]
            invmoves = invstring(invword) + " " + invmoves
        elif word[0] == "(":
            invword = word[1:len(word)]
            if invword in rubik.FACE_MOVES:
                invmoves = invstring(invword) + " " + invmoves
            elif len(invword) == 2:
                if invword[0] in rubik.FACE_MOVES and invword[1] in ["'", "2"]:
                    invmoves = invstring(invword) + " " + invmoves
            inverse = True
        elif (inverse and not word[len(word) - 1] == ")" and len(word) == 2 and word[0] in rubik.FACE_MOVES and word[1] in ["'", "2"]) or word in rubik.FACE_MOVES:
            invmoves = invstring(word) + " " + invmoves
        elif word[len(word) - 1] == ")":
            invword = word[0:len(word) - 1]
            if invword in rubik.FACE_MOVES or (len(invword) == 2 and invword[0] in rubik.FACE_MOVES and invword[1] in ["'", "2"]):
                invmoves = invstring(invword) + " " + invmoves
            inverse = False
    return [invmoves, moves]


def invstring(word):
    if word in rubik.FACE_MOVES:
        move = word + "'"
    elif len(word) == 2:
        if word[1] == "'":
            move = word[0:len(word) - 1]
        elif word[1] == "2":
            move = word
    return move

def movealg():
    short = textArea.get("start", INSERT)
    pos = textArea.search(short, '0.0', stopindex=END)
    return rubik.Algorithm(movestring(textArea.get(2.0, pos))[0] + movestring(textArea.get(1.0, 2.0))[1] + movestring(textArea.get(2.0, pos))[1])


def clear_tags():
    short = textArea.get("start", INSERT)

    textArea.tag_configure("none", foreground="black")

    textArea.delete("start", INSERT)
    textArea.insert(INSERT, short, "none")


def colorgreen():
    short = textArea.get("start", INSERT)

    textArea.tag_configure("green", foreground="green")

    textArea.delete("start", INSERT)
    textArea.insert(INSERT, short, "green")


def coloryellow():
    short = textArea.get("start", INSERT)

    textArea.tag_configure("yellow", foreground="orange")

    textArea.delete("start", INSERT)
    textArea.insert(INSERT, short, "yellow")


def colorred():
    short = textArea.get("start", INSERT)

    textArea.tag_configure("red", foreground="red")

    textArea.delete("start", INSERT)
    textArea.insert(INSERT, short, "red")


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
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()


def about():
    messagebox.showinfo("About", "If you're seeing this message, I forgot to update this message")


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
