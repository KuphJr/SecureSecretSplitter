import os.path
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import filedialog
from encoder import *
from decoder import *


# Creates the GUI in combine mode
def clickCombBtnSelected(self):
    global f
    f.destroy()
    f = tk.Frame(r, height=640, width=1024, bg="#262626")
    f.place(x=0, y=0)

    genBtnNotSelectedImg = tk.PhotoImage(file = r"GUIimages/genBtnNotSelected.ppm")
    genBtnNotSelected = tk.Label(f, width=512, height=48, image=genBtnNotSelectedImg, bd=-2, bg="#262626")
    genBtnNotSelected.place(x=0, y=0)
    genBtnNotSelected.bind("<Button-1>", clickGenBtnSelected)
    genBtnNotSelectedHoverImg = tk.PhotoImage(file = r"GUIimages/genBtnNotSelectedHover.ppm")
    genBtnNotSelected.bind("<Enter>", func=lambda e: genBtnNotSelected.config(image=genBtnNotSelectedHoverImg))
    genBtnNotSelected.bind("<Leave>", func=lambda e: genBtnNotSelected.config(image=genBtnNotSelectedImg))

    combBtnSelectedImg = tk.PhotoImage(file = r"GUIimages/combBtnSelected.ppm")
    combBtnSelected = tk.Label(f, width=512, height=48, image=combBtnSelectedImg, bd=-2, bg="#262626")
    combBtnSelected.place(x=512, y=0)

    combLabelImg = tk.PhotoImage(file = r"GUIimages/combLabel.ppm")
    combLabel = tk.Label(f, width=1024, height=26, image=combLabelImg, bd=-2)
    combLabel.place(x=0, y=72)

    loadBtnImg = tk.PhotoImage(file = r"GUIimages/loadBtn.ppm")
    loadBtn = tk.Label(f, width=388, height=36, image=loadBtnImg, bd=-2, bg="#262626")
    loadBtn.place(x=317, y=116)
    loadBtn.bind("<Button-1>", clickLoadBtn)
    loadBtnHoverImg = tk.PhotoImage(file = r"GUIimages/loadBtnHover.ppm")
    loadBtn.bind("<Enter>", func=lambda e: loadBtn.config(image=loadBtnHoverImg))
    loadBtn.bind("<Leave>", func=lambda e: loadBtn.config(image=loadBtnImg))

    global keyBox
    keyBoxFrame = tk.Frame(f, width=975, height=234)
    keyBoxFrame.pack_propagate(0)
    keyBox = scrolledtext.ScrolledText(keyBoxFrame, highlightbackground="#ffffff", highlightcolor="#ffffff", bg="#ffffff", fg="#000000", font=("Times New Roman", 14), insertbackground="#000000")
    keyBox.pack(fill=tk.BOTH, expand=1)
    keyBoxFrame.place(x=24, y=174)

    combBtnImg = tk.PhotoImage(file = r"GUIimages/combBtn.ppm")
    combBtn = tk.Label(f, width=390, height=38, image=combBtnImg, bd=-2, bg="#262626")
    combBtn.place(x=317, y=430)
    combBtn.bind("<Button-1>", clickCombBtn)
    combBtnHoverImg = tk.PhotoImage(file = r"GUIimages/combBtnHover.ppm")
    combBtn.bind("<Enter>", func=lambda e: combBtn.config(image=combBtnHoverImg))
    combBtn.bind("<Leave>", func=lambda e: combBtn.config(image=combBtnImg))

    global resultMsgBox
    resultMsgBoxFrame = tk.Frame(f, width=975, height=78)
    resultMsgBoxFrame.pack_propagate(0)
    resultMsgBox = scrolledtext.ScrolledText(resultMsgBoxFrame, highlightbackground="#bcbcbc", highlightcolor="#bcbcbc", bg="#bcbcbc", fg="#000000", font=("Times New Roman", 14), insertbackground="#000000")
    resultMsgBox.configure(state="disabled")
    resultMsgBox.pack(fill=tk.BOTH, expand=1)
    resultMsgBoxFrame.place(x=24, y=490)

    saveMsgBtnImg = tk.PhotoImage(file = r"GUIimages/saveMsgBtn.ppm")
    saveMsgBtn = tk.Label(f, width=388, height=36, image=saveMsgBtnImg, bd=-2, bg="#262626")
    saveMsgBtn.place(x=317, y=592)
    saveMsgBtn.bind("<Button-1>", clickSaveMsgBtn)
    saveMsgBtnHoverImg = tk.PhotoImage(file = r"GUIimages/saveMsgBtnHover.ppm")
    saveMsgBtn.bind("<Enter>", func=lambda e: saveMsgBtn.config(image=saveMsgBtnHoverImg))
    saveMsgBtn.bind("<Leave>", func=lambda e: saveMsgBtn.config(image=saveMsgBtnImg))

    r.mainloop()


# checks to ensure all input keys are valid
# if they are valid, replace the input keys with input keys in the proper format and return true
# else, do not modify the input keys and return false
# The "proper format" removes any beginning text before the key beginning. Each key must start with
# with either 'kXb62' or 'kXb92' where X is some number between 2 and 60.
# This beginning must be the same for every key entered.
def checkInputKeys(inputKeys):
    inputKeys = inputKeys.replace("\t", " ")
    while "  " in inputKeys:
        inputKeys = inputKeys.replace("  ", " ") 
    while "\n\n" in inputKeys:
        inputKeys = inputKeys.replace("\n\n", "\n")
    inputKeysList = inputKeys.split("\n")
    formattedInputKeys = []
    base = ""
    length = -1
    global resultMsgBox
    resultMsgBox.configure(state="normal")
    resultMsgBox.delete("1.0", tk.END)
    global numberOfInputKeys
    numberOfInputKeys = 0
    for inputKey in inputKeysList:
        if len(inputKey) > 0:
            numberOfInputKeys += 1
            hasValidBase = False
            for x in range(2, 61):
                chkStr62 = "k" + str(x) + "b62"
                chkStr94 = "k" + str(x) + "b94"
                global keyBase
                global numberOfRequiredKeys
                if chkStr62 in inputKey:
                    if base == "":
                        base = chkStr62
                        keyBase = 62
                        numberOfRequiredKeys = x
                    elif base != chkStr62:
                        resultMsgBox.insert(tk.INSERT, "ERROR: Invalid key format. Each key must begin " +
                            "with either 'kXb62' or 'kXb92' where X is some number between 2 and 60.\n" +
                            "This beginning must be the same for every key entered.")
                        resultMsgBox.configure(state="disabled")
                        return False
                    hasValidBase = True
                    inputKey = inputKey[inputKey.index(chkStr62):]
                    break
                if chkStr94 in inputKey:
                    if base == "":
                        base = chkStr94
                        keyBase = 94
                        numberOfRequiredKeys = x
                    elif base != chkStr94:
                        resultMsgBox.insert(tk.INSERT, "ERROR: Invalid key format. Each key must begin " +
                            "with either 'kXb62' or 'kXb92' where X is some number between 2 and 60.\n" +
                            "This beginning must be the same for every key entered.")
                        resultMsgBox.configure(state="disabled")
                        return False
                    hasValidBase = True
                    inputKey = inputKey[inputKey.index(chkStr94):]
                    break
            if not hasValidBase:
                resultMsgBox.insert(tk.INSERT, "ERROR: Invalid key format. Each key must begin " +
                    "with either 'kXb62' or 'kXb92' where X is some number between 2 and 60.")
                resultMsgBox.configure(state="disabled")
                return False
            if inputKey[-1:] == " ":
                inputKey = inputKey[:-1]
            if length == -1:
                length = len(inputKey.split(" "))
            elif length != len(inputKey.split(" ")):
                resultMsgBox.insert(tk.INSERT, "ERROR: The lengths of the input keys do not match.")
                resultMsgBox.configure(state="disabled")
                return []
            if inputKey in formattedInputKeys:
                resultMsgBox.insert(tk.INSERT, "ERROR: Duplicate key found. Each key must be unique.")
                resultMsgBox.configure(state="disabled")
                return []
            formattedInputKeys.append(inputKey)
    i = 1
    keyBox.delete("1.0", tk.END)
    for key in formattedInputKeys:
        if i == len(formattedInputKeys):
            keyBox.insert(tk.INSERT, key)
        else:
            keyBox.insert(tk.INSERT, key + "\n")
        i += 1
    resultMsgBox.configure(state="disabled")
    return True


# function to combine split keys    
def clickCombBtn(self):
    global keyBox
    # check input keys
    if not checkInputKeys(keyBox.get("1.0", tk.END)):
        return
    global numberOfRequiredKeys
    global numberOfInputKeys
    # ensure the correct number of keys have been entered
    if numberOfRequiredKeys > numberOfInputKeys:
        global resultMsgBox
        resultMsgBox.configure(state="normal")
        resultMsgBox.delete("1.0", tk.END)
        resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) + " key(s) have been entered.\n" +
            str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
            "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
            " more key(s).")
        resultMsgBox.configure(state="disabled")
        return
    inputKeys = keyBox.get("1.0", tk.END)
    inputKeysList = inputKeys.split("\n")
    if len(inputKeysList[0]) < 2:
        return
    keyPairsList = [["" for w in range(len(inputKeysList[0].split(" "))-1)]
                    for k in range(numberOfRequiredKeys)]
    for keyNum in range(numberOfRequiredKeys):
        keyPairsList[keyNum] = inputKeysList[keyNum].split(" ")[1:]        
    global keyBase
    # place input keys into the result message scrolled textbox
    combineResult = splitKeyDecoder(numberOfRequiredKeys, keyPairsList, keyBase)
    resultMsgBox.configure(state="normal")
    resultMsgBox.delete("1.0", tk.END)
    resultMsgBox.insert(tk.INSERT, combineResult)
    resultMsgBox.configure(state="disabled")
    

# function to load split key from a text file 
def clickLoadBtn(self):
    filename = filedialog.askopenfilename()
    if filename == "":
        return
    file = open(filename, "r")
    text = file.read()
    file.close()
    global keyBox
    if checkInputKeys(keyBox.get("1.0", tk.END) + "\n" + text):
        global numberOfRequiredKeys
        global numberOfInputKeys
        if numberOfRequiredKeys > numberOfInputKeys:
            global resultMsgBox
            resultMsgBox.configure(state="normal")
            resultMsgBox.delete("1.0", tk.END)
            if numberOfInputKeys > 1 and (numberOfRequiredKeys - numberOfInputKeys) > 1:
                resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) + " keys have been entered.\n" +
                    str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
                    "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
                    " more keys.")
            elif numberOfInputKeys == 1 and (numberOfRequiredKeys - numberOfInputKeys) == 1:
                resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) + " key has been entered.\n" +
                    str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
                    "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
                    " more key.")
            elif numberOfInputKeys == 1 and (numberOfRequiredKeys - numberOfInputKeys) > 1:
                resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) + " key has been entered.\n" +
                    str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
                    "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
                    " more keys.")
            elif numberOfInputKeys > 1 and (numberOfRequiredKeys - numberOfInputKeys) == 1:
                resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) + " keys have been entered.\n" +
                    str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
                    "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
                    " more key.")
            resultMsgBox.configure(state="disabled")
        else:
            resultMsgBox.configure(state="normal")
            resultMsgBox.delete("1.0", tk.END)
            resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) + " Keys successfully loaded.\n" +
                                "Click \"Combine Keys\" to decode the message.")
            resultMsgBox.configure(state="disabled")


# function to save combined message to a text file
def clickSaveMsgBtn(self):
    filename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"),))
    if filename == "":
        return
    try:
        if filename[-4:] != ".txt":
            filename += ".txt"
    except:
        return
    file = open(filename, "w")
    global resultMsgBox
    resultMsg = resultMsgBox.get("1.0", tk.END)
    file.write(resultMsg)
    file.close()


def checkBoxClicked():
    pass


def selectAllKeys(self):
    global selectedKeys
    for key in selectedKeys:
        key.set(True)


# function to save keys to text files 
def clickSaveBtn(self):
    global keys
    global resultKeysBox
    textInResultKeysBox = resultKeysBox.get("1.0", tk.END)
    print(textInResultKeysBox)
    print(str(len(textInResultKeysBox)))
    if len(resultKeysBox.get("1.0", tk.END)) > 1:
        keySelectWindow = tk.Toplevel()
        keySelectWindow.title("Select keys to save")
        keySelectWindow.geometry("480x480")
        keySelectWindow.resizable(0, 0)
        keySelectWindow["bg"]="#262626"
        btnImg = tk.PhotoImage(file = r"GUIimages/keyBtn.ppm")
        global selectedKeys
        selectedKeys = []
        keyNum = 0
        style = ttk.Style()
        style.configure("TCheckbutton", foreground="#ffffff", background="#262626", font=("Arial", 14))
        for key in keys:
            btnText = "Key #" + str(keyNum+1)
            col = keyNum % 3
            row = keyNum // 3
            selectedKeys.append(tk.BooleanVar())
            ttk.Checkbutton(keySelectWindow, text=btnText,
                            variable=selectedKeys[keyNum]).place(x=col*160+24, y=row*48+8)
            print(keyNum)
            print(selectedKeys[keyNum].get())
            keyNum += 1
        selectAllBtnImg = tk.PhotoImage(file = r"GUIimages/selectAllKeys.ppm")
        selectAllBtn = tk.Label(keySelectWindow, width=260, height=36, image=selectAllBtnImg,
                           bd=-2, bg="#262626")
        selectAllBtn.bind("<Button-1>", selectAllKeys)
        selectAllBtnHoverImg = tk.PhotoImage(file = r"GUIimages/selectAllKeysHover.ppm")
        selectAllBtn.bind("<Enter>", func=lambda e: selectAllBtn.config(image=selectAllBtnHoverImg))
        selectAllBtn.bind("<Leave>", func=lambda e: selectAllBtn.config(image=selectAllBtnImg))
        selectAllBtn.place(x=112, y=388)
        okayBtnImg = tk.PhotoImage(file = r"GUIimages/selectSaveLocation.ppm")
        okayBtn = tk.Label(keySelectWindow, width=260, height=36, image=okayBtnImg,
                           bd=-2, bg="#262626")
        okayBtn.bind("<Button-1>", saveKeys)
        okayBtnHoverImg = tk.PhotoImage(file = r"GUIimages/selectSaveLocationHover.ppm")
        okayBtn.bind("<Enter>", func=lambda e: okayBtn.config(image=okayBtnHoverImg))
        okayBtn.bind("<Leave>", func=lambda e: okayBtn.config(image=okayBtnImg))
        okayBtn.place(x=112, y=432)
        keySelectWindow.mainloop()
    else:
        messagebox.showerror("Error", "Keys must be generated before they can be saved.")


def saveKeys(self):
    global selectedKeys
    isAtLeastOneKeySelected = False
    for selectedKey in selectedKeys:
        if selectedKey.get():
            isAtLeastOneKeySelected = True
            break
    if not isAtLeastOneKeySelected:
        messagebox.showerror("Error", "Select at least one key to save.")
        return
    global keys
    directory = filedialog.askdirectory()
    j = 0
    isConflictingFileName = True
    while isConflictingFileName:
        isConflictingFileName = False
        if j > 0:
            endOfFileName = " (" + str(j) + ").txt"
        else:
            endOfFileName = ".txt"
        for i in range(len(keys)):
            fileName = "key" + str(i+1) + endOfFileName
            filePath = directory + "/" + fileName
            if os.path.isfile(filePath):
                isConflictingFileName = True
                break
        j += 1
    k = 1
    for key in keys:
        if selectedKeys[k-1].get():
            fileName = directory + "/key" + str(k) + endOfFileName
            file = open(fileName,"w")
            file.write(key)
            file.close()
        k += 1


# function to generate split keys
def clickGenBtn(self):
    global msgBox
    global resultKeysBox
    global totalNumKeys
    global reqNumKeys
    resultKeysBox.configure(state = "normal")
    resultKeysBox.delete("1.0", tk.END)
    message = msgBox.get("1.0", tk.END)
    # check that the input message is valid
    if len(message) > 0:
        message = message.replace("\n", " ")
        message = message.replace("\t", " ")
        while "  " in message:
            message = message.replace("  ", " ")
        if message == " " or message == "":
            return
        if message[0] == " ":
            message = message[1:]
        if message[-1:] == " ":
            message = message[:-1]
        for letter in message:
            if letter > "~" or letter < " ":
                resultKeysBox.insert(tk.INSERT, "ERROR: Invalid input character(s) detected. \nOnly standard ASCII letters, numbers and symbols are accepted.")
                resultKeysBox.configure(state = "disabled")
                return
        msgBox.delete("1.0", tk.END)
        msgBox.insert(tk.INSERT, message)
        global includeSymbols
        global keys
        # generate keys and place keys in the result scrolling textbox
        if includeSymbols:
            keys = splitKeyCreator(94, reqNumKeys.get(), totalNumKeys.get(), message)
        else:
            keys = splitKeyCreator(62, reqNumKeys.get(), totalNumKeys.get(), message)
        k=1
        for key in keys:
            insertKey = "Key #" + str(k) + ": " + key + "\n\n"
            resultKeysBox.insert(tk.INSERT, insertKey)
            k += 1
        resultKeysBox.configure(state = "disabled")


# function for the toggle button to include symbols in the resulting split keys or not
def clickToggle(self):
    global includeSymbols
    global toggle
    if includeSymbols == True:
        includeSymbols = False
        toggleImg = tk.PhotoImage(file = r"GUIimages/toggleNo.ppm")
        toggle.config(image=toggleImg)
        toggle.image = toggleImg
    else:
        includeSymbols = True
        toggleImg = tk.PhotoImage(file = r"GUIimages/toggleYes.ppm")
        toggle.config(image=toggleImg)
        toggle.image = toggleImg


# Function to ensure the number of required keys required to recreate the message
# is <= the total number of keys generated.
# If not, the function will automatically set the requiredNumKeys slider value
# to the totalNumKeys that are to be generated
def updateReqNumKeys(self):
    if reqNumKeys.get() > totalNumKeys.get():
        reqNumKeys.set(totalNumKeys.get())


# Function to ensure the number of total keys is >= the required number
# of keys to recreate the message.
# If not, the function will automatically set the totalNumKeys slider value to the
# required number of keys to recreate the message as set by the reqNumKeys slider
def updateTotalNumKeys(self):
    if reqNumKeys.get() > totalNumKeys.get():
        totalNumKeys.set(reqNumKeys.get())


# Creates the GUI in generate mode
def clickGenBtnSelected(self):
    global f
    f.destroy()
    f = tk.Frame(r, height=640, width=1024, bg="#262626")
    f.place(x=0, y=0)
    
    genBtnSelectedImg = tk.PhotoImage(file = r"GUIimages/genBtnSelected.ppm")
    genBtnSelected = tk.Label(f, width=512, height=48, image=genBtnSelectedImg, bd=-2, bg="#262626")
    genBtnSelected.place(x=0, y=0)

    combBtnNotSelectedImg = tk.PhotoImage(file = r"GUIimages/combBtnNotSelected.ppm")
    combBtnNotSelected = tk.Label(f, width=512, height=48, image=combBtnNotSelectedImg, bd=-2, bg="#6c6c6c")
    combBtnNotSelected.place(x=512, y=0)
    combBtnNotSelected.bind("<Button-1>", clickCombBtnSelected)
    combBtnNotSelectedHoverImg = tk.PhotoImage(file = r"GUIimages/combBtnNotSelectedHover.ppm")
    combBtnNotSelected.bind("<Enter>", func=lambda e: combBtnNotSelected.config(image=combBtnNotSelectedHoverImg))
    combBtnNotSelected.bind("<Leave>", func=lambda e: combBtnNotSelected.config(image=combBtnNotSelectedImg))

    toggleLabelImg = tk.PhotoImage(file = r"GUIimages/toggleLabel.ppm")
    toggleLabel = tk.Label(f, image=toggleLabelImg, bd=-2, bg="#262626")
    toggleLabel.place(x=0, y=70)

    global includeSymbols
    global toggle
    if includeSymbols == True:
        toggleImg = tk.PhotoImage(file = r"GUIimages/toggleYes.ppm")
    else:
        toggleImg = tk.PhotoImage(file = r"GUIimages/toggleNo.ppm")
    toggle = tk.Label(f, width=68, height=30, image=toggleImg, bd=-2, bg="#262626")
    toggle.place(x=630, y=70)
    toggle.bind("<Button-1>", clickToggle)

    totalNumKeysSlider = tk.Scale(f, variable=totalNumKeys, from_=2, to=24, bd=4, fg="#ffffff",
                                  bg="#262626", highlightthickness=0, troughcolor="#6c6c6c",
                                  length=464, orient=tk.HORIZONTAL, font=("Arial", 14),
                                  command=updateReqNumKeys)
    totalNumKeysSlider.place(x=24, y=104)

    reqNumKeysSlider = tk.Scale(f, variable=reqNumKeys, from_=2, to=12, bd=4, fg="#ffffff",
                                bg="#262626", highlightthickness=0, troughcolor="#6c6c6c",
                                length=464, orient=tk.HORIZONTAL, font=("Arial", 16),
                                command=updateTotalNumKeys)
    reqNumKeysSlider.place(x=536, y=104)

    sliderLabelsImg = tk.PhotoImage(file = r"GUIimages/sliderLabels.ppm")
    sliderLabels = tk.Label(f, image=sliderLabelsImg, bd=-2, bg="#262626")
    sliderLabels.place(x=0, y=160)

    global msgBox
    msgBoxFrame = tk.Frame(f, width=975, height=64)
    msgBoxFrame.pack_propagate(0)
    msgBox = scrolledtext.ScrolledText(msgBoxFrame, highlightbackground="#ffffff", highlightcolor="#ffffff", bg="#ffffff", fg="#000000", font=("Times New Roman", 14), insertbackground="#000000")
    msgBox.pack(fill=tk.BOTH, expand=1)
    msgBoxFrame.place(x=24, y=208)

    genBtnImg = tk.PhotoImage(file = r"GUIimages/genBtn.ppm")
    genBtn = tk.Label(f, width=390, height=38, image=genBtnImg, bd=-2, bg="#262626")
    genBtn.place(x=317, y=294)
    genBtn.bind("<Button-1>", clickGenBtn)
    genBtnHoverImg = tk.PhotoImage(file = r"GUIimages/genBtnHover.ppm")
    genBtn.bind("<Enter>", func=lambda e: genBtn.config(image=genBtnHoverImg))
    genBtn.bind("<Leave>", func=lambda e: genBtn.config(image=genBtnImg))

    global resultKeysBox
    resultKeysBoxFrame = tk.Frame(f, width=975, height=216)
    resultKeysBoxFrame.pack_propagate(0)
    resultKeysBox = scrolledtext.ScrolledText(resultKeysBoxFrame, highlightbackground="#bcbcbc", highlightcolor="#bcbcbc", bg="#bcbcbc", fg="#000000", font=("Times New Roman", 14), insertbackground="#000000")
    resultKeysBox.configure(state="disabled")
    resultKeysBox.pack(fill=tk.BOTH, expand=1)
    resultKeysBoxFrame.place(x=24, y=354)

    saveBtnImg = tk.PhotoImage(file = r"GUIimages/saveBtn.ppm")
    saveBtn = tk.Label(f, width=388, height=36, image=saveBtnImg, bd=-2, bg="#262626")
    saveBtn.place(x=317, y=592)
    saveBtn.bind("<Button-1>", clickSaveBtn)
    saveBtnHoverImg = tk.PhotoImage(file = r"GUIimages/saveBtnHover.ppm")
    saveBtn.bind("<Enter>", func=lambda e: saveBtn.config(image=saveBtnHoverImg))
    saveBtn.bind("<Leave>", func=lambda e: saveBtn.config(image=saveBtnImg))    
    
    r.mainloop()


if __name__ == "__main__":
    # tkinter GUI
    global r
    r = tk.Tk()
    r.title("Secure Secret Splitter")
    r.geometry("1024x640")
    r.resizable(0, 0)
    r["bg"]="#262626"
    global f
    f = tk.Frame(r, height=640, width=1024, bg="#262626")
    # variables set by tkinter GUI
    global includeSymbols
    includeSymbols = True
    global inputMsg
    inputMsg = tk.StringVar()
    global outputMsg
    outputMsg = tk.StringVar()
    global inputKeys
    inputKeys = tk.StringVar()
    global outputKeys
    outputKeys = tk.StringVar()
    global reqNumKeys
    reqNumKeys = tk.IntVar()
    global totalNumKeys
    totalNumKeys = tk.IntVar()
    # initalize the GUI
    clickGenBtnSelected(0)
