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

textArea.insert(1.0, "Scramble: \n\nSolution: ")

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

x = rubik.Algorithm('x')
y = rubik.Algorithm('y')
z = rubik.Algorithm('z')

abbreviations = {
        "222": "2x2x2",
        "2x2x2": "2x2x2",
        "2X2X2": "2x2x2",
        "2x2": "2x2x2",
        "2X2": "2x2x2",
        "sq": "Square",
        "SQ": "Square",
        "122": "Square",
        "1x2x2": "Square",
        "1X2X2": "Square",
        "square": "Square",
        "SQUARE": "Square",
        "221": "Square",
        "2x2x1": "Square",
        "2X2X1": "Square",
        "123": "1x2x3",
        "1x2x3": "1x2x3",
        "1X2X3": "1x2x3",
        "321": "1x2x3",
        "3x2x1": "1x2x3",
        "3X2X1": "1x2x3",
        "roux": "1x2x3",
        "ROUX": "1x2x3",
        "wall": "1x2x3",
        "WALL": "1x2x3",
        "223": "2x2x3",
        "322": "2x2x3",
        "2x2x3": "2x2x3",
        "2X2X3": "2x2x3",
        "3x2x2": "2x2x3",
        "3X2X2": "2x2x3",
        "petrus": "2x2x3",
        "PETRUS": "2x2x3",
        "F2L-1": "F2L-1",
        "f2l-1": "F2L-1",
        "xxxcross": "F2L-1",
        "XXXCROSS": "F2L-1",
        "eo": "EO",
        "EO": "EO",
        "p-": "Pseudo",
        "P-": "Pseudo",
        "ps": "Pseudo",
        "PS": "Pseudo",
        "p": "Pseudo",
        "P": "Pseudo",
        "ps-": "Pseudo",
        "PS-": "Pseudo",
        "dr": "Domino Reduction",
        "DR": "Domino Reduction",
        "domino": "Domino Reduction",
        "DOMINO": "Domino Reduction",
        "dom": "Domino Reduction",
        "DOM": "Domino Reduction",
        "pdr": "PDR",
        "PDR": "PDR",
        "diamond": "Diamond",
        "DIAMOND": "Diamond",
        "f2l-2": "Diamond",
        "F2L-2": "Diamond",
        "solved": "Solved",
        "SOLVED": "Solved",
        "FINISH": "Solved",
        "finish": "Solved",
        "finished": "Solved",
        "FINISHED": "Solved",
        "solve": "Solved",
        "done": "Solved",
        "DONE": "Solved",
        "f2l": "F2L",
        "F2L": "F2L",
        "skip": "Solved",
        "SKIP": "Solved",
        "cross": "Cross",
        "CROSS": "Cross"
    }


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
        "ps": pseudo,
        "PS": pseudo,
        "p": pseudo,
        "P": pseudo,
        "ps-": pseudo,
        "PS-": pseudo,
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
        "f2l": f2l,
        "F2L": f2l,
        "skip": solved,
        "SKIP": solved,
        "cross": cross,
        "CROSS": cross
    }

    func = steps.get(short, clear_tags)
    func()



def eo():
    c = rubik.Cube()
    c.apply_alg(movealg())

    is_solved = False

    if blockdefinitions.eosolved(c):
        is_solved = True

    c.apply_alg(x)
    if blockdefinitions.eosolved(c):
        is_solved = True

    c.apply_alg(y)
    if blockdefinitions.eosolved(c):
        is_solved = True

    if is_solved:
        colorgreen()
    else:
        colorred()


def pseudo():
    coloryellow()


def domino():
    c = rubik.Cube()
    c.apply_alg(movealg())

    is_solved = False

    if blockdefinitions.dominosolved(c):
        is_solved = True

    c.apply_alg(x)
    if blockdefinitions.dominosolved(c):
        is_solved = True

    c.apply_alg(z)
    if blockdefinitions.dominosolved(c):
        is_solved = True

    if is_solved:
        colorgreen()
    else:
        colorred()


# TODO: Test this.  DR was broken, this might be too.
def partialdomino():
    c = rubik.Cube()
    c.apply_alg(movealg())

    is_solved = False

    if blockdefinitions.pdrsolved(c):
        is_solved = True

    c.apply_alg(x)
    if blockdefinitions.pdrsolved(c):
        is_solved = True

    c.apply_alg(z)
    if blockdefinitions.pdrsolved(c):
        is_solved = True

    if is_solved:
        colorgreen()
    else:
        colorred()


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
    try:
        if word in rubik.FACE_MOVES:
            move = word + "'"
        elif len(word) == 2:
            if word[1] == "'":
                move = word[0:len(word) - 1]
            elif word[1] == "2":
                move = word
        return move
    except UnboundLocalError:
        return ""

# TODO: Make this just go up until the start marker
def movealg():
    short = textArea.get("start", INSERT)
    pos = textArea.search(short, '0.0', stopindex=END)
    return rubik.Algorithm(movestring(textArea.get(2.0, pos))[0] + movestring(textArea.get(1.0, 2.0))[1] + movestring(textArea.get(2.0, pos))[1])


# must be passed text that only contains moves
def lengthaftercancel(moves):
    try:
        split_moves = moves.split()
    except AttributeError:
        split_moves = moves
    moves_canceled = 1
    while moves_canceled != 0:
        moves_canceled = 0
        temp = []
        skipmove = False

        for i in range(len(split_moves)):
            # print(i)
            if skipmove:
                # print("skipped:", split_moves[i])
                skipmove = False
                continue
            # print(split_moves[i])
            try:
                if split_moves[i][0] != split_moves[i+1][0]:
                    temp.append(split_moves[i])
                    continue
                skipmove = True
                moves_canceled += 1
                # print("this move + next move: ", split_moves[i], split_moves[i+1])
                if split_moves[i] == split_moves[i+1]:
                    # print("moves are the same")
                    if split_moves[i] in blockdefinitions.movestwo:
                            # print("moves cancel fully")
                            moves_canceled += 1
                            continue
                    temp.append(split_moves[i][0] + "2")
                elif len(split_moves[i]) == len(split_moves[i+1]):
                    # print("moves are ' and 2")
                    temp.append(split_moves[i][0])
                elif split_moves[i] in blockdefinitions.movestwo or split_moves[i+1] in blockdefinitions.movestwo:
                    # print("moves are move and 2")
                    temp.append(split_moves[i][0] + "'")
                else:
                    # print("moves cancel fully")
                    moves_canceled += 1
                    continue
            except IndexError:
                temp.append(split_moves[i])
                continue
        # print(temp)
        split_moves = list(temp)
    return len(split_moves)


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


def openfile():
    file = filedialog.askopenfile(parent=root, mode='rb', title='Select a text file')

    if file is not None:
        contents = file.read()
        textArea.delete(1.0, END)
        textArea.insert('1.0', contents)
        file.close()


def savefileproxy():
    savefile("e")


def savefile(e):
    file = filedialog.asksaveasfile(mode='w')

    if file is not None:
        # removes last character, which is extra return
        data = textArea.get('1.0', END+'-1c')
        file.write(data)
        file.close()


def quitprogram():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()


def about():
    messagebox.showinfo("About", "This is an assistant to help you type and format your FMC skeletons and solutions"
                                 " quickly. After you type them in the upper box, press \"Run\" or control + R to get "
                                 "a nicely formatted solution in the lower box.\n\nCopy the scramble onto the first "
                                 "line, write your skeleton in between, and type your solution on the last line. Use"
                                 " \"//\"  to label parts of your"
                                 " skeleton. SkeleType will automatically check if your solution is correct while you "
                                 "are typing it (be sure to add a space after each move and after \"//\" or else it"
                                 " will not work properly)."
                                 "\n\nSkeleType will also format your solution with a movecount and "
                                 "expand abbreviations for blocks and other steps in the skeleton.  \n\nIf "
                                 "you have any questions or suggestions, tweet me "
                                 "@AndrewNathenson\n\nWARNING: DO NOT "
                                 "DELETE \"Scramble: \" OR \"Solution: \" -- it will break. \n\nThe following shortcuts"
                                 " can be used and will be detected and color-coded (green = it "
                                 "works!, red = it doesn't work) "
                                 "along with some variations of these phrases:\n\nSquare: sq, 122, 221\n\n1x2x3: "
                                 "roux, 123,"
                                 " 321\n\n2x2x2: 222, 2x2\n\n2x2x3: 223, 322, petrus\n\nDomino Reduction: dr, dom, "
                                 "domino\n\nOther abbreviations and labels are also detected. Try typing different"
                                 " things to see what works, or check the source code or something for the full list.")


def transcribeproxy():
    transcribe("e")


def transcribe(e):
    c = rubik.Cube()
    try:
        solvestart = textArea.search("Solution: ", END, stopindex=1.0, backwards=TRUE)

        c.apply_alg(rubik.Algorithm(movestring(textArea.get(1.0, 2.0))[1] + movestring(
            textArea.get(solvestart, END))[1]))

        output_area.delete(1.0, END)

        movecount = len(textArea.get(solvestart, END).split()) - 1

        if not c.solved():
            messagebox.showwarning("Solution Does Not Work", "Warning: the solution written after \"Solution:\" does "
                                                             "not work for the provided scramble.\n\nThe skeleton has"
                                                             " been formatted anyway, but it may not work.")

        split_text = textArea.get(1.0, END).split("\n")
        formatted_text = ""
        linecount = 0.0

        for line in split_text:
            insertion = False
            if ":" in line:
                insertion = True
            linecount = linecount + 1
            split_line = line.split()
            for word in split_line:
                if word is "//":
                    formatted_text = formatted_text + "\n"
                elif word in abbreviations:
                    formatted_text = formatted_text + abbreviations.get(word) + " "
                else:
                    formatted_text = formatted_text + word + " "
            # Adds the running movecount, but also detects any cancellations in the moves, even with previous lines
            if "//" in split_line and not insertion:
                formatted_text = formatted_text + "(" + str(lengthaftercancel(movestring(textArea.get(linecount, (
                        linecount + 1)))[0]) + lengthaftercancel(movestring(textArea.get(linecount, linecount + 1))[(
                            1)])) + "/" + str(lengthaftercancel(movestring(textArea.get(2.0, linecount + 1))[0]) + (
                                 lengthaftercancel(movestring(textArea.get(2.0, linecount + 1))[1]))) + ")"
            formatted_text = formatted_text + "\n"

        output_area.insert(1.0, formatted_text + str(movecount) + " Moves.")
    except TclError:
        messagebox.showerror("Solution: deleted or modified", "Error: The word \"Solution: \" has been deleted or "
                                                              "modified. Please type \"Solution: \" at the start "
                                                              "of your solution (with a space before the first move of"
                                                              " your solution).")


# create the menu
menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(label="Run", command=transcribeproxy)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New")
fileMenu.add_command(label="Open", command=openfile)
fileMenu.add_command(label="Save", command=savefileproxy)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=quitprogram)

menu.add_cascade(label="About", command=about)


def select_all_1(e):
    textArea.tag_add("sel", '1.0', 'end')

def select_all_2(e):
    output_area.tag_add("sel", '1.0', 'end')


def testfunction(e):
    print(lengthaftercancel("U U U U U U U U U U U"))


root.bind('<Control-s>', savefile)
root.bind('<Control-r>', transcribe)
root.bind('<Control-S>', savefile)
root.bind('<Control-R>', transcribe)
textArea.bind('<Control-a>', select_all_1)
textArea.bind('<Control-A>', select_all_1)
output_area.bind('<Control-a>', select_all_2)
output_area.bind('<Control-A>', select_all_2)
root.bind('<Control-t>', testfunction)  # TODO: Delete this binding and function

# keep window open
root.mainloop()
