import os

import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import filedialog

from clientsideServerFunctions import *
from encoder import *
from decoder import *

# Creates the GUI window in combine mode
def clickCombBtnSelected(f, r):
    f.destroy()
    f = tk.Frame(r, height=640, width=1024, bg="#262626")
    f.place(x=0, y=0)

    genBtnNotSelectedImg = tk.PhotoImage(file = r"GUIimages/genBtnNotSelected.ppm")
    genBtnNotSelected = tk.Label(f, width=512, height=48, image=genBtnNotSelectedImg,
                                 bd=-2, bg="#262626")
    genBtnNotSelected.place(x=0, y=0)
    genBtnNotSelected.bind("<Button-1>", func=lambda e: clickGenBtnSelected(f, r))
    genBtnNotSelectedHoverImg = tk.PhotoImage(file = r"GUIimages/genBtnNotSelectedHover.ppm")
    genBtnNotSelected.bind("<Enter>",
                           func=lambda e: genBtnNotSelected.config(image=
                                                                   genBtnNotSelectedHoverImg))
    genBtnNotSelected.bind("<Leave>",
                           func=lambda e: genBtnNotSelected.config(image=
                                                                   genBtnNotSelectedImg))

    combBtnSelectedImg = tk.PhotoImage(file = r"GUIimages/combBtnSelected.ppm")
    combBtnSelected = tk.Label(f, width=512, height=48, image=combBtnSelectedImg, bd=-2,
                               bg="#262626")
    combBtnSelected.place(x=512, y=0)

    combLabelImg = tk.PhotoImage(file = r"GUIimages/combLabel.ppm")
    combLabel = tk.Label(f, width=1024, height=26, image=combLabelImg, bd=-2)
    combLabel.place(x=0, y=72)

    keyBoxFrame = tk.Frame(f, width=975, height=234)
    keyBoxFrame.pack_propagate(0)
    keyBox = scrolledtext.ScrolledText(keyBoxFrame, highlightbackground="#ffffff",
                                       highlightcolor="#ffffff", bg="#ffffff", fg="#000000",
                                       font=("Times New Roman", 14),
                                       insertbackground="#000000")
    keyBox.pack(fill=tk.BOTH, expand=1)
    keyBoxFrame.place(x=24, y=174)

    resultMsgBoxFrame = tk.Frame(f, width=975, height=78)
    resultMsgBoxFrame.pack_propagate(0)
    resultMsgBox = scrolledtext.ScrolledText(resultMsgBoxFrame, highlightbackground="#bcbcbc",
                                             highlightcolor="#bcbcbc", bg="#bcbcbc",
                                             fg="#000000", font=("Times New Roman", 14),
                                             insertbackground="#000000")
    resultMsgBox.configure(state="disabled")
    resultMsgBox.pack(fill=tk.BOTH, expand=1)
    resultMsgBoxFrame.place(x=24, y=490)

    combBtnImg = tk.PhotoImage(file = r"GUIimages/combBtn.ppm")
    combBtn = tk.Label(f, width=390, height=38, image=combBtnImg, bd=-2, bg="#262626")
    combBtn.place(x=317, y=430)
    combBtn.bind("<Button-1>", func=lambda e: clickCombBtn(keyBox, resultMsgBox))
    combBtnHoverImg = tk.PhotoImage(file = r"GUIimages/combBtnHover.ppm")
    combBtn.bind("<Enter>", func=lambda e: combBtn.config(image=combBtnHoverImg))
    combBtn.bind("<Leave>", func=lambda e: combBtn.config(image=combBtnImg))

    loadBtnImg = tk.PhotoImage(file = r"GUIimages/loadBtn.ppm")
    loadBtn = tk.Label(f, width=388, height=36, image=loadBtnImg, bd=-2, bg="#262626")
    loadBtn.place(x=317, y=116)
    loadBtn.bind("<Button-1>", func=lambda e: clickLoadBtn(keyBox, resultMsgBox))
    loadBtnHoverImg = tk.PhotoImage(file = r"GUIimages/loadBtnHover.ppm")
    loadBtn.bind("<Enter>", func=lambda e: loadBtn.config(image=loadBtnHoverImg))
    loadBtn.bind("<Leave>", func=lambda e: loadBtn.config(image=loadBtnImg))

    saveMsgBtnImg = tk.PhotoImage(file = r"GUIimages/saveMsgBtn.ppm")
    saveMsgBtn = tk.Label(f, width=388, height=36, image=saveMsgBtnImg, bd=-2, bg="#262626")
    saveMsgBtn.place(x=317, y=592)
    saveMsgBtn.bind("<Button-1>", func=lambda e: clickSaveMsgBtn(resultMsgBox))
    saveMsgBtnHoverImg = tk.PhotoImage(file = r"GUIimages/saveMsgBtnHover.ppm")
    saveMsgBtn.bind("<Enter>", func=lambda e: saveMsgBtn.config(image=saveMsgBtnHoverImg))
    saveMsgBtn.bind("<Leave>", func=lambda e: saveMsgBtn.config(image=saveMsgBtnImg))

    r.mainloop()


# function to load split key from a text file 
def clickLoadBtn(keyBox, resultMsgBox):
    filename = filedialog.askopenfilename()
    if filename == "":
        return
    file = open(filename, "r")
    text = file.read()
    file.close()
    numberOfRequiredKeys, numberOfInputKeys, keyBase = checkInputKeys(
        keyBox.get("1.0", tk.END) + "\n" + text, resultMsgBox, keyBox)
    if numberOfRequiredKeys != 0:
        if numberOfRequiredKeys > numberOfInputKeys:
            resultMsgBox.configure(state="normal")
            resultMsgBox.delete("1.0", tk.END)
            if numberOfInputKeys > 1 and (numberOfRequiredKeys - numberOfInputKeys) > 1:
                resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) +
                                    " keys have been entered.\n" +
                    str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
                    "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
                    " more keys.")
            elif numberOfInputKeys == 1 and (numberOfRequiredKeys - numberOfInputKeys) == 1:
                resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) +
                                    " key has been entered.\n" +
                    str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
                    "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
                    " more key.")
            elif numberOfInputKeys == 1 and (numberOfRequiredKeys - numberOfInputKeys) > 1:
                resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) +
                                    " key has been entered.\n" +
                    str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
                    "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
                    " more keys.")
            elif numberOfInputKeys > 1 and (numberOfRequiredKeys - numberOfInputKeys) == 1:
                resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) +
                                    " keys have been entered.\n" +
                    str(numberOfRequiredKeys) + " keys are required to decode the message.\n"
                    "Please load or enter " + str(numberOfRequiredKeys - numberOfInputKeys) +
                    " more key.")
            resultMsgBox.configure(state="disabled")
        else:
            resultMsgBox.configure(state="normal")
            resultMsgBox.delete("1.0", tk.END)
            resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) +
                                " Keys successfully loaded.\n" +
                                "Click \"Combine Keys\" to decode the message.")
            resultMsgBox.configure(state="disabled")


# checks to ensure all input keys are valid
# if they are valid, replace the input keys with input keys in the proper format
# else, do not modify the input keys and return false
# The "proper format" removes any beginning text before the key beginning.
# Each key must start with either 'kXb62' or 'kXb92' where X is some number between 2 and 60.
# This beginning must be the same for every key entered.
def checkInputKeys(inputKeys, resultMsgBox, keyBox):
    inputKeys = inputKeys.replace("\t", " ")
    while "  " in inputKeys:
        inputKeys = inputKeys.replace("  ", " ") 
    while "\n\n" in inputKeys:
        inputKeys = inputKeys.replace("\n\n", "\n")
    inputKeysList = inputKeys.split("\n")
    formattedInputKeys = []
    base = ""
    length = -1
    resultMsgBox.configure(state="normal")
    resultMsgBox.delete("1.0", tk.END)
    numberOfInputKeys = 0
    for inputKey in inputKeysList:
        if len(inputKey) > 0:
            numberOfInputKeys += 1
            hasValidBase = False
            for x in range(2, 61):
                chkStr62 = "k" + str(x) + "b62"
                chkStr94 = "k" + str(x) + "b94"
                if chkStr62 in inputKey:
                    if base == "":
                        base = chkStr62
                        keyBase = 62
                        numberOfRequiredKeys = x
                    elif base != chkStr62:
                        resultMsgBox.insert(tk.INSERT,
                            "ERROR: Invalid key format. Each key must begin " +
                            "with either 'kXb62' or 'kXb92' where X is some number " +
                            " between 2 and 60.\n" +
                            "This beginning must be the same for every key entered.")
                        resultMsgBox.configure(state="disabled")
                        return 0, 0, 0
                    hasValidBase = True
                    inputKey = inputKey[inputKey.index(chkStr62):]
                    break
                if chkStr94 in inputKey:
                    if base == "":
                        base = chkStr94
                        keyBase = 94
                        numberOfRequiredKeys = x
                    elif base != chkStr94:
                        resultMsgBox.insert(tk.INSERT,
                            "ERROR: Invalid key format. Each key must begin " +
                            "with either 'kXb62' or 'kXb92' where X is some number " +
                            "between 2 and 60.\n" +
                            "This beginning must be the same for every key entered.")
                        resultMsgBox.configure(state="disabled")
                        return 0, 0, 0
                    hasValidBase = True
                    inputKey = inputKey[inputKey.index(chkStr94):]
                    break
            if not hasValidBase:
                resultMsgBox.insert(tk.INSERT,
                    "ERROR: Invalid key format. Each key must begin " +
                    "with either 'kXb62' or 'kXb92' where X is some number between 2 and 60.")
                resultMsgBox.configure(state="disabled")
                return 0, 0, 0
            if inputKey[-1:] == " ":
                inputKey = inputKey[:-1]
            if length == -1:
                length = len(inputKey.split(" "))
            elif length != len(inputKey.split(" ")):
                resultMsgBox.insert(tk.INSERT,
                                    "ERROR: The lengths of the input keys do not match.")
                resultMsgBox.configure(state="disabled")
                return 0, 0, 0
            if inputKey in formattedInputKeys:
                resultMsgBox.insert(tk.INSERT,
                                    "ERROR: Duplicate key found. Each key must be unique.")
                resultMsgBox.configure(state="disabled")
                return 0,0, 0
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
    return numberOfRequiredKeys, numberOfInputKeys, keyBase


# function to combine split keys    
def clickCombBtn(keyBox, resultMsgBox):
    if len(keyBox.get("1.0", tk.END)) > 1:
        # check input keys
        numberOfRequiredKeys, numberOfInputKeys, keyBase = checkInputKeys(
            keyBox.get("1.0", tk.END), resultMsgBox, keyBox)
        if numberOfRequiredKeys == 0:
            return
        # ensure the correct number of keys have been entered
        if numberOfRequiredKeys > numberOfInputKeys:
            resultMsgBox.configure(state="normal")
            resultMsgBox.delete("1.0", tk.END)
            resultMsgBox.insert(tk.INSERT, str(numberOfInputKeys) +
                " key(s) have been entered.\n" +
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
        # place input keys into the result message scrolled textbox
        combineResult = splitKeyDecoder(numberOfRequiredKeys, keyPairsList, keyBase)
        resultMsgBox.configure(state="normal")
        resultMsgBox.delete("1.0", tk.END)
        resultMsgBox.insert(tk.INSERT, combineResult)
        resultMsgBox.configure(state="disabled")


# function to save combined message to a text file
def clickSaveMsgBtn(resultMsgBox):
    filename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"),))
    if filename == "":
        return
    try:
        if filename[-4:] != ".txt":
            filename += ".txt"
    except:
        return
    file = open(filename, "w")
    resultMsg = resultMsgBox.get("1.0", tk.END)
    file.write(resultMsg)
    file.close()


# Creates the GUI in generate mode
def clickGenBtnSelected(f, r):
    f.destroy()
    f = tk.Frame(r, height=640, width=1024, bg="#262626")
    f.place(x=0, y=0)
    
    genBtnSelectedImg = tk.PhotoImage(file = r"GUIimages/genBtnSelected.ppm")
    genBtnSelected = tk.Label(f, width=512, height=48, image=genBtnSelectedImg, bd=-2,
                              bg="#262626")
    genBtnSelected.place(x=0, y=0)

    combBtnNotSelectedImg = tk.PhotoImage(file = r"GUIimages/combBtnNotSelected.ppm")
    combBtnNotSelected = tk.Label(f, width=512, height=48, image=combBtnNotSelectedImg,
                                  bd=-2, bg="#6c6c6c")
    combBtnNotSelected.place(x=512, y=0)
    combBtnNotSelected.bind("<Button-1>",
                            func=lambda e: clickCombBtnSelected(f, r))
    combBtnNotSelectedHoverImg = tk.PhotoImage(file = r"GUIimages/combBtnNotSelectedHover.ppm")
    combBtnNotSelected.bind("<Enter>",
                            func=lambda e: combBtnNotSelected.config(image=
                                                                     combBtnNotSelectedHoverImg))
    combBtnNotSelected.bind("<Leave>",
                            func=lambda e: combBtnNotSelected.config(image=
                                                                     combBtnNotSelectedImg))

    toggleLabelImg = tk.PhotoImage(file = r"GUIimages/toggleLabel.ppm")
    toggleLabel = tk.Label(f, image=toggleLabelImg, bd=-2, bg="#262626")
    toggleLabel.place(x=0, y=70)

    global includeSymbols
    if includeSymbols == True:
        toggleImg = tk.PhotoImage(file = r"GUIimages/toggleYes.ppm")
    else:
        toggleImg = tk.PhotoImage(file = r"GUIimages/toggleNo.ppm")
    toggle = tk.Label(f, width=68, height=30, image=toggleImg, bd=-2, bg="#262626")
    toggle.place(x=630, y=70)
    toggle.bind("<Button-1>", func=lambda e: clickToggle(toggle))

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

    msgBoxFrame = tk.Frame(f, width=975, height=64)
    msgBoxFrame.pack_propagate(0)
    msgBox = scrolledtext.ScrolledText(msgBoxFrame, highlightbackground="#ffffff",
                                       highlightcolor="#ffffff", bg="#ffffff", fg="#000000",
                                       font=("Times New Roman", 14),
                                       insertbackground="#000000")
    msgBox.pack(fill=tk.BOTH, expand=1)
    msgBoxFrame.place(x=24, y=208)

    resultKeysBoxFrame = tk.Frame(f, width=975, height=216)
    resultKeysBoxFrame.pack_propagate(0)
    resultKeysBox = scrolledtext.ScrolledText(resultKeysBoxFrame,
                                              highlightbackground="#bcbcbc",
                                              highlightcolor="#bcbcbc", bg="#bcbcbc",
                                              fg="#000000", font=("Times New Roman", 14),
                                              insertbackground="#000000")
    resultKeysBox.configure(state="disabled")
    resultKeysBox.pack(fill=tk.BOTH, expand=1)
    resultKeysBoxFrame.place(x=24, y=354)

    genBtnImg = tk.PhotoImage(file = r"GUIimages/genBtn.ppm")
    genBtn = tk.Label(f, width=390, height=38, image=genBtnImg, bd=-2, bg="#262626")
    genBtn.place(x=317, y=294)
    genBtn.bind("<Button-1>", func=lambda e: clickGenBtn(msgBox, resultKeysBox))
    genBtnHoverImg = tk.PhotoImage(file = r"GUIimages/genBtnHover.ppm")
    genBtn.bind("<Enter>", func=lambda e: genBtn.config(image=genBtnHoverImg))
    genBtn.bind("<Leave>", func=lambda e: genBtn.config(image=genBtnImg))

    saveBtnImg = tk.PhotoImage(file = r"GUIimages/saveBtn.ppm")
    saveBtn = tk.Label(f, width=388, height=36, image=saveBtnImg, bd=-2, bg="#262626")
    saveBtn.place(x=92, y=592)
    saveBtn.bind("<Button-1>", func=lambda e: clickSaveBtn(resultKeysBox))
    saveBtnHoverImg = tk.PhotoImage(file = r"GUIimages/saveBtnHover.ppm")
    saveBtn.bind("<Enter>", func=lambda e: saveBtn.config(image=saveBtnHoverImg))
    saveBtn.bind("<Leave>", func=lambda e: saveBtn.config(image=saveBtnImg))

    serverSaveBtnImg = tk.PhotoImage(file = r"GUIimages/saveKeysToServer.ppm")
    serverSaveBtn = tk.Label(f, width=388, height=36, image=serverSaveBtnImg, bd=-2,
                             bg="#262626")
    serverSaveBtn.place(x=544, y=592)
    serverSaveBtn.bind("<Button-1>", func=lambda e: getLoginInfo(resultKeysBox))
    serverSaveBtnHoverImg = tk.PhotoImage(file = r"GUIimages/saveKeysToServerHover.ppm")
    serverSaveBtn.bind("<Enter>",
                       func=lambda e: serverSaveBtn.config(image=serverSaveBtnHoverImg))
    serverSaveBtn.bind("<Leave>", func=lambda e: serverSaveBtn.config(image=serverSaveBtnImg))
    
    r.mainloop()


# function for the toggle button to include symbols in the resulting split keys or not
def clickToggle(toggle):
    global includeSymbols
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


# function to generate split keys
def clickGenBtn(msgBox, resultKeysBox):
    global keys
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
                resultKeysBox.insert(tk.INSERT, "ERROR: Invalid input character(s) detected.\n"
                                     + "Only use standard ASCII letters, numbers and symbols.")
                resultKeysBox.configure(state = "disabled")
                return
        msgBox.delete("1.0", tk.END)
        msgBox.insert(tk.INSERT, message)
        global includeSymbols
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


# function to save keys to text files 
def clickSaveBtn(resultKeysBox):
    global keys
    textInResultKeysBox = resultKeysBox.get("1.0", tk.END)
    if len(resultKeysBox.get("1.0", tk.END)) > 1:
        keySelectWindow = tk.Toplevel()
        keySelectWindow.title("Select keys to save to text files")
        keySelectWindow.geometry("480x480")
        keySelectWindow.resizable(0, 0)
        keySelectWindow["bg"]="#262626"
        selectedKeys = []
        keyNum = 0
        style = ttk.Style()
        style.configure("TCheckbutton", foreground="#ffffff", background="#262626",
                        font=("Arial", 14))
        for key in keys:
            btnText = "Key #" + str(keyNum+1)
            col = keyNum % 3
            row = keyNum // 3
            selectedKeys.append(tk.BooleanVar())
            ttk.Checkbutton(keySelectWindow, text=btnText,
                            variable=selectedKeys[keyNum]).place(x=col*160+24, y=row*48+8)
            keyNum += 1
        selectAllBtnImg = tk.PhotoImage(file = r"GUIimages/selectAllKeys.ppm")
        selectAllBtn = tk.Label(keySelectWindow, width=260, height=36, image=selectAllBtnImg,
                           bd=-2, bg="#262626")
        selectAllBtn.bind("<Button-1>", func=lambda e: selectAllKeys(selectedKeys))
        selectAllBtnHoverImg = tk.PhotoImage(file = r"GUIimages/selectAllKeysHover.ppm")
        selectAllBtn.bind("<Enter>",
                          func=lambda e: selectAllBtn.config(image=selectAllBtnHoverImg))
        selectAllBtn.bind("<Leave>",
                          func=lambda e: selectAllBtn.config(image=selectAllBtnImg))
        selectAllBtn.place(x=112, y=388)
        okayBtnImg = tk.PhotoImage(file = r"GUIimages/selectSaveLocation.ppm")
        okayBtn = tk.Label(keySelectWindow, width=260, height=36, image=okayBtnImg,
                           bd=-2, bg="#262626")
        okayBtn.bind("<Button-1>", func=lambda e: saveKeys(keySelectWindow, selectedKeys))
        okayBtnHoverImg = tk.PhotoImage(file = r"GUIimages/selectSaveLocationHover.ppm")
        okayBtn.bind("<Enter>", func=lambda e: okayBtn.config(image=okayBtnHoverImg))
        okayBtn.bind("<Leave>", func=lambda e: okayBtn.config(image=okayBtnImg))
        okayBtn.place(x=112, y=432)
    else:
        messagebox.showerror("Error", "Keys must be generated before they can be saved.")


def selectAllKeys(selectedKeys):
    for key in selectedKeys:
        key.set(True)


# function to save keys to text files
def saveKeys(keySelectWindow, selectedKeys):
    global keys
    keySelectWindow.destroy()
    isAtLeastOneKeySelected = any(key.get() for key in selectedKeys)
    if not isAtLeastOneKeySelected:
        messagebox.showerror("Error", "Select at least one key to save.")
        return
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


# function to close any open server connections if a window is closed
def closeServer(window):
    window.destroy()
    #sendMsgToServer("close")
    print("closed server connection")


# creates window to gather login information from the user and logs into the server
def getLoginInfo(resultKeysBox):
    if len(resultKeysBox.get("1.0", tk.END)) > 1:
        global keys
        if any(len(key) > 250 for key in keys):
            messagebox.showerror("Error", "The message has a word that is too long to be " +
                                 "properly saved to the server.")
        # includes for connecting to the server. Not required if server functionality is not used
        # so these includes are not included until the "save keys to server" button is clicked
        loginWindow = tk.Toplevel()
        loginWindow.protocol("WM_DELETE_WINDOW", lambda: closeServer(loginWindow))
        loginWindow.title("Login to the server")
        loginWindow.geometry("320x240")
        loginWindow.resizable(0, 0)
        loginWindow["bg"]="#262626"
        userLbl = tk.Label(loginWindow, text="Username: ", font=("Arial", 16), fg="#ffffff",
                           bg="#262626", bd=-2)
        userLbl.place(x=24, y=24)
        username = tk.Entry(loginWindow, font=("Arial", 14), width = 14, bg="#ffffff",
                            fg="#000000")
        username.place(x=136, y=25)
        pwLbl = tk.Label(loginWindow, text="Password: ", font=("Arial", 16), fg="#ffffff",
                         bg="#262626", bd=-2)
        pwLbl.place(x=24, y=80)
        password = tk.Entry(loginWindow, font=("Arial", 14), show="*", width = 14, bg="#ffffff",
                            fg="#000000")
        password.place(x=136, y=79)
        createAccountBtnImg = tk.PhotoImage(file = r"GUIimages/createAccountBtn.ppm")
        createAccountBtn = tk.Label(loginWindow, image=createAccountBtnImg, bd=-2, bg="#262626",
                                    width=260, height=36)
        createAccountBtn.place(x=30,y=148)
        createAccountBtn.bind("<Button-1>", func=lambda e: createAccount(username.get(),
                                password.get()))
        createAccountBtnHoverImg = tk.PhotoImage(file = r"GUIimages/createAccountBtnHover.ppm")
        createAccountBtn.bind("<Enter>", func=lambda e: createAccountBtn.config(
                                image=createAccountBtnHoverImg))
        createAccountBtn.bind("<Leave>", func=lambda e: createAccountBtn.config(
                                image=createAccountBtnImg))
        loginBtnImg = tk.PhotoImage(file = r"GUIimages/loginBtn.ppm")
        loginBtn = tk.Label(loginWindow, image=loginBtnImg, bd=-2, bg="#262626", width=260,
                            height=36)
        loginBtn.place(x=30,y=192)
        loginBtn.bind("<Button-1>", func=lambda e: login(username.get(), password.get(),
                        loginWindow, resultKeysBox))
        loginBtnHoverImg = tk.PhotoImage(file = r"GUIimages/loginBtnHover.ppm")
        loginBtn.bind("<Enter>", func=lambda e: loginBtn.config(image=loginBtnHoverImg))
        loginBtn.bind("<Leave>", func=lambda e: loginBtn.config(image=loginBtnImg))
    else:
        messagebox.showerror("Error", "Keys must be generated before they can be saved.")


def createAccount(username, password):
    import hashlib
    if len(password) > 32 or len(username) > 32:
        messagebox.showerror("Error", "The username or password is too long. " +
                             "The maximum length is 32 characters.")
        return
    if len(username) < 4:
        messagebox.showerror("Error", "The password is too short. " +
                             "The minimum length is 4 characters.")
        return
    if len(password) < 8:
        messagebox.showerror("Error", "The password is too short. " +
                             "The minimum length is 8 characters.")
        return
    if not all(" " < char <= "~" for char in password):
        messagebox.showerror("Error", "The username can only contain standard ASCII " +
                                "letters, numbers and symbols without any spaces.")
        return
    if not all(" " < char <= "~" for char in password):
        messagebox.showerror("Error", "The password can only contain standard ASCII " +
                                "letters, numbers and symbols without any spaces.")
        return
    syms = r"!@#$%^&*()_+{}|:\"<>?-=[];',./`~" + chr(92)
    if not all([any(char in password for char in syms),
                any("a" <= char <= "z" for char in password),
                any("A" <= char <= "Z" for char in password),
                any("0" <= char <= "9" for char in password)]):
        messagebox.showerror("Error", "The password must contain at least 1 symbol, 1 number, " +
                             "1 lowercase letter and 1 uppercase letter.")
        return
    if establishServerConnection:
        # salt and hash password before sending to the server
        salt = os.urandom(32)
        hashedPassword = hashlib.pbkdf2_hmac("sha256", password.encode("ascii"), salt, 100000)
        print("salt")
        print(salt)
        print("hashedPassword")
        print(hashedPassword)
        sendMsgToServer("create")
        sendMsgToServer(username)
        sendMsgToServer(salt)
        sendMsgToServer(hashedPassword)
        serverMsg = recvMsgFromServer()
        if serverMsg == "created":
            selectKeys(resultKeysBox, password)
        elif serverMsg == "exists":
            messagebox.showerror("Error", "An account with that username already exists.")
        else:
            messagebox.showerror("Error", "Failed to create an account.")
            

# function to handle logging into the server
def login(username, password, loginWindowl, resultKeysBox):
    import hashlib
    if len(password) > 32 or len(username) > 32:
        messagebox.showerror("Error", "The username or password is too long. " +
                             "The maximum length is 32 characters.")
        return
    for char in username:
        if char <= " " or char > "~":
            messagebox.showerror("Error", "The username can only contain standard ASCII " +
                                 "letters, numbers and symbols without any spaces.")
            return
    for char in password:
        if char <= " " or char > "~":
            messagebox.showerror("Error", "The password can only contain standard ASCII " +
                                 "letters, numbers and symbols without any spaces.")
            return
    # salt and hash password before sending to the server
    salt = os.urandom(32)
    hashedPassword = hashlib.pbkdf2_hmac("sha256", password.encode("ascii"), salt, 100000)
    print("salt")
    print(salt)
    print("hashedPassword")
    print(hashedPassword)
    # establish connection to the server
    if establishServerConnection():
        sendMsgToServer("login")
        sendMsgToServer(username)
        sendBytesToServer(salt)
        sendBytesToServer(hashedPassword)
        serverMsg = recvMsgFromServer()
        if serverMsg == "success":
            selectKeys(resultKeysBox)
        elif serverMsg == "fail":
            messagebox.showerror("Error", "The username or password was incorrect.\n" +
                                 "Try again or create a new account.")


# function to select which keys should be uploaded to the server
def selectKeys(resultKeysBox, password):
    global keys
    textInResultKeysBox = resultKeysBox.get("1.0", tk.END)
    if len(resultKeysBox.get("1.0", tk.END)) > 1:
        keySelectWindow = tk.Toplevel()
        keySelectWindow.protocol("WM_DELETE_WINDOW", lambda: closeServer(keySelectWindow))
        keySelectWindow.title("Select keys to save to the server")
        keySelectWindow.geometry("480x480")
        keySelectWindow.resizable(0, 0)
        keySelectWindow["bg"]="#262626"
        serverSelectedKeys = []
        keyNum = 0
        style = ttk.Style()
        style.configure("TCheckbutton", foreground="#ffffff", background="#262626",
                        font=("Arial", 14))
        for key in keys:
            btnText = "Key #" + str(keyNum+1)
            col = keyNum % 3
            row = keyNum // 3
            serverSelectedKeys.append(tk.BooleanVar())
            ttk.Checkbutton(keySelectWindow, text=btnText,
                            variable=serverSelectedKeys[keyNum]).place(x=col*160+24,
                                                                       y=row*48+8)
            keyNum += 1
        okayBtnImg = tk.PhotoImage(file = r"GUIimages/saveKeysToServerBlue.ppm")
        okayBtn = tk.Label(keySelectWindow, width=260, height=36, image=okayBtnImg,
                           bd=-2, bg="#262626")
        okayBtn.bind("<Button-1>",func=lambda e: saveKeysToServer(keySelectWindow,
                                                                  serverSelectedKeys, password))
        okayBtnHoverImg = tk.PhotoImage(file = r"GUIimages/saveKeysToServerBlueHover.ppm")
        okayBtn.bind("<Enter>", func=lambda e: okayBtn.config(image=okayBtnHoverImg))
        okayBtn.bind("<Leave>", func=lambda e: okayBtn.config(image=okayBtnImg))
        okayBtn.place(x=112, y=432)
    else:
        messagebox.showerror("Error", "Keys must be generated before they can be saved.")
    

# function to upload keys to server
def saveKeysToServer(keySelectWindow, serverSelectedKeys, password):
    global keys
    numKeysSelected = 0
    for selectedKey in serverSelectedKeys:
        if selectedKey.get():
            numKeysSelected += 1
    if numKeysSelected < 1:
        messagebox.showerror("Error", "Select at least one key to save.")
        return
    global reqNumKeys
    if numKeysSelected >= reqNumKeys.get():
        messagebox.showerror("Error", "For security, the number of keys saved "+
                             "to the server must be less than the number of keys " +
                             "required to recreate the message.")
        return
    keySelectWindow.destroy()
    # Before a key is sent to the server, it is encrypted using the user's password
    # The password is only stored locally * and is required to decrypt any key which
    # is saved on the server. This means that even if the server is hacked, any information
    # gained is useless because it is encrypted based on the user's local password.
    #
    # * (The password is never sent to the server for authentication, only a hash of the
    #    password is used to authenticate.)
    #
    sendMsgToServer("save")
    j = 0
    for key in keys:
        if serverSelectedKeys[j].get():
            sendMsgToServer("startkey")
            i = 0
            # encrypt key
            encryptedKey = ""
            for s in key:
                if i == len(password):
                    i = 0
                p = ord(password[i]) - ord("!")
                k = ord(s) - ord("!")
                e = (k + p) % 94
                c = chr(e + ord("!"))
                encryptedKey += c
                i += 1
            numSends = len(encryptedKey) // 256 + 1
            start = 0
            for n in numSends:
                if start + 255 > len(encryptedKey):
                    keyPacket = encryptedKey[start:]
                else:
                    end = start + 255
                    keyPacket = encryptedKey[start:end]
                    start += 256
                sendMsgToServer(keyPacket)
            sendMsgToServer("endkey")
        j += 1
    sendMsgToServer("endall")
    if recvMsgFromServer() != "success":
        messagebox.showerror("Error", "Failed to save keys to the server.")


if __name__ == "__main__":
    # tkinter GUI
    r = tk.Tk()
    # method to handle closing the application to close any potentially opened sockets
    r.protocol("WM_DELETE_WINDOW", lambda: closeServer(r))
    r.title("Secure Secret Splitter")
    r.geometry("1024x640")
    r.resizable(0, 0)
    r["bg"]="#262626"
    f = tk.Frame(r, height=640, width=1024, bg="#262626")
    # variables set by tkinter GUI
    # defined as global variables to make them easier to acess since they are
    # used by multiple functions
    global includeSymbols
    includeSymbols = True
    global reqNumKeys
    reqNumKeys = tk.IntVar()
    global totalNumKeys
    totalNumKeys = tk.IntVar()
    # initalize the GUI
    clickGenBtnSelected(f, r)
