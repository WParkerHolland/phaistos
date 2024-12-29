# Phaistos Disc Project
# Declaration of processor function and calling of it
# Uses cltk, Fran did most of this
import tkinter as tk
from tkinter import filedialog
import os

#---------------------- Scansion making -------------------------------------------------------------
def greekToScansion(file_path):
    from cltk.prosody.grc import Scansion
    from cltk import NLP
    import sys
    sys.path.append("/cltk")

    with open(file_path, 'r', encoding="utf8") as file:
        file_content = file.read()

    # https://github.com/cltk/cltk/issues/1247
    # Including this here just in case
    cltk_nlp = NLP(language="grc", suppress_banner=True)
    cltk_doc = cltk_nlp.analyze(file_content)
    tokens = cltk_doc.tokens
    clean_accents = Scansion()._clean_accents(tokens)

    syllables = Scansion()._make_syllables(clean_accents, True)
    condensed = Scansion()._syllable_condenser(syllables, splitByLine=True)
    scanned = Scansion()._scansion(condensed)
    return scanned, condensed, clean_accents, syllables

def makePresentable(scansion):
    # This function is used to make the scansion output more presentable
    newScansion = ""
    for line in scansion:
        for foot in line:
            for syllable in foot:
                match syllable:
                    case "¯":
                        newScansion += "- "
                    case "˘":
                        newScansion += "u "
                    case "|":
                        if newScansion[len(newScansion) - 1] != "\n":
                            newScansion += "| "
                    case _:
                        newScansion += "x\n"
    return newScansion

def centerText(text, length):
    while len(text) < length:
        if(len(text) % 2 == 0):
            text = " " + text
        else:
            text = text + " "
    return text

def makeMorePresentable(scansion, syllables, preview=False, lineNumeration=False):
    # Combine syllables into proper format
    tempList = []
    for grouping in syllables:
        for i in range(len(grouping)):
            for j in range(len(grouping[i])):
                grouping[i][j] = grouping[i][j].replace("\n", "")
        tempList += grouping
    syllables = tempList

    # This function will make the scansion output more presentable while also displaying how each syllable was classified
    lineOffset = 0
    finString = "\n"
    for line in scansion:
        if(preview and lineOffset > 10):
            break

        scanLine = ""
        syllLine = ""
        if('?' in line):
            for i in range(len(line)):
                if(line[i] == '?'):
                    scanLine += centerText('?', len(syllables[lineOffset][i])) + " "
                    syllLine += syllables[lineOffset][i] + " "
                else:
                    scanLine += centerText(line[i], len(syllables[lineOffset][i])) + " "
                    syllLine += syllables[lineOffset][i] + " "
        else:
            for i in range(len(line)):
                if(line[i:i+2] == ['¯', '¯']):
                    scanLine += centerText('¯', len(syllables[lineOffset][i])) + " " + centerText('¯', len(syllables[lineOffset][i+1])) + " | "
                    syllLine += syllables[lineOffset][i] + " " + syllables[lineOffset][i+1] + " | "
                elif(line[i:i+2] == ['¯', 'X']):
                    scanLine += centerText('¯', len(syllables[lineOffset][i])) + " " + centerText('x', len(syllables[lineOffset][i+1]))
                    syllLine += syllables[lineOffset][i] + " " + syllables[lineOffset][i+1]
                elif(line[i:i+3] == ['¯', '˘', '˘']):
                    scanLine += centerText('¯', len(syllables[lineOffset][i])) + " " + centerText('˘', len(syllables[lineOffset][i+1])) + " " + centerText('˘', len(syllables[lineOffset][i+2])) + " | "
                    syllLine += syllables[lineOffset][i] + " " + syllables[lineOffset][i+1] + " " + syllables[lineOffset][i+2] + " | "
        
        if(lineNumeration):
            finString += "Line {}: \n".format(lineOffset + 1)
        finString += scanLine + "\n" + syllLine + "\n\n"
        lineOffset += 1
    return finString

def makeSyllablesPresentable(syllables):
    # This function is used solely for presentation in displayMatches function
    finString = ""
    for character in syllables:
        finString += character + " "
    return finString

def makePrologPresentable(scansion):
    # This function translates scansion so it doesn't use prolog operator symbols
    newScansion = []
    for sentence in scansion:
        for syllable in sentence:
            match syllable:
                case "¯":
                    newScansion.append("l")
                case "˘":
                    newScansion.append("u")
                case "|":
                    if newScansion[len(newScansion) - 1] != "x":
                        newScansion.append("d")
                case _:
                    newScansion.append("x")
    return newScansion

def checkLineRight(line, patterns):
    # Checks an individual line for any of the pattern provided
    # Returns true or false, whether it contains the line or not, and the pattern matched
    for i in range(len(patterns)):
        patternLength = len(line) - len(patterns[i])
        if(line[patternLength:] == patterns[i]):
            return True, patterns[i]
        
    return False, 0

def checkLineWrong(line, patterns):
    # Checks an individual line for any of the pattern provided
    # Returns true or false, whether it contains the line or not, and the pattern matched
    for i in range(len(patterns)):
        patternLength = len(patterns[i])
        if(line[0:patternLength] == patterns[i]):
            return True, patterns[i]

    return False, 0

def checkScansion(scansion, prolog=False):
    # This checks the scansion for any of the patterns we're looking for
    # Will return a 2 lists of sentence indexes with the patterns found within, one for right way patterns and one for wrong way patterns
    # [[SentenceIndex, PatternIndex], ...] is the format of the returned list
    returnListRight = []
    returnListWrong = []

    if(prolog):
        import janus_swi as janus
        janus.consult("prolog/scansion.pl")

        for i in range(len(scansion)):
            tempSentence = makePrologPresentable(scansion[i])

            # Check for patterns found while reading the right way
            tempObjRight = janus.query_once("rightWay({}, X)".format(tempSentence))
            if(tempObjRight["truth"]):
                returnListRight.append([i, tempObjRight["X"]])

            # Check for patterns found while reading the wrong way
            tempObjWrong = janus.query_once("wrongWay({}, X)".format(tempSentence))
            if(tempObjWrong["truth"]):
                returnListWrong.append([i, tempObjWrong["X"]])
    else:
        for i in range(len(scansion)):
            tempSentence = scansion[i]

            # Check for patterns found while reading the right way
            rightPatterns = [['¯','˘','˘','¯','¯','¯','X'], ['¯','¯','¯','¯','¯','X']]
            tempObjRight = checkLineRight(tempSentence, rightPatterns)
            if(tempObjRight[0]):
                returnListRight.append([i, tempObjRight[1]])

            # Check for patterns found while reading the wrong way
            wrongPatterns = [['¯','¯','¯','¯','¯','¯'], ['¯','˘','˘','¯','¯','¯','¯'], ['¯','˘','˘','¯','¯','¯','˘','˘'], ['¯','¯','¯','¯','¯','˘','˘']]
            tempObjWrong = checkLineWrong(tempSentence, wrongPatterns)
            if(tempObjWrong[0]):
                returnListWrong.append([i, tempObjWrong[1]])
    
    return returnListRight, returnListWrong
    
def displayMatches(scansion, matchesRight, matchesWrong, sentences, fileNameMod = ""):
    # This function displayes matches found in the scansion in a file
    file = open("researchProject/outputs/scansion/output" + fileNameMod + ".txt", "w")
    if matchesRight == [] and matchesWrong == []:
        file.write(":(")
    else:
        file.write("Matches found reading the right way:\n\n")
        for match in matchesRight:
            file.write("Match found in sentence {}:\n".format(match[0]))
            file.write("Pattern found: {}\n".format(match[1]))
            file.write("Sentence: {}\n".format(makeSyllablesPresentable(sentences[match[0]]).replace("\n", "")))
            file.write("Scansion: {}\n\n".format(makePresentable(scansion[match[0]])))

        file.write("\nMatches found reading the wrong way:\n\n")
        for match in matchesWrong:
            file.write("Match found in sentence {}:\n".format(match[0]))
            file.write("Pattern found: {}\n".format(match[1]))
            file.write("Sentence: {}\n".format(makeSyllablesPresentable(sentences[match[0]]).replace("\n", "")))
            file.write("Scansion: {}\n\n".format(makePresentable(scansion[match[0]])))
    
    file.close()

def evaluateScansionRuntime():
    # This function is used to evaluate the runtime of the scansion function
    import timeit
    setup="from __main__ import greekToScansion"
    wasteRun = timeit.timeit(lambda: greekToScansion('researchProject/texts/shortTheogeny.txt'), setup=setup, number=1)

    time10 = timeit.timeit(lambda: greekToScansion('researchProject/texts/shortTheogeny.txt'), setup=setup, number=100)
    time100 = timeit.timeit(lambda: greekToScansion('researchProject/texts/100Theogeny.txt'), setup=setup, number=100)
    timeWhole = timeit.timeit(lambda: greekToScansion('researchProject/texts/theogeny.txt'), setup=setup, number=100)

    print("10 Line Runtime: ", time10)
    print("100 Line Runtime: ", time100)
    print("Theogeny Runtime: ", timeWhole)

def scansionForWebsite(file_content):
    # This function is used to run the scansion function for the website
    # Makes file to hold the contents, then passes the file to the scansion function
    file = open("researchProject/texts/websiteTemp.txt", "w")
    file.write(file_content)
    scans = greekToScansion("researchProject/texts/websiteTemp.txt")
    matchesRight, matchesWrong = checkScansion(scans[0])
    return scans[0], matchesRight, matchesWrong, scans[1]


# ------------------------- UI Part -------------------------------------------------------------------------
def open_file():
    filename = filedialog.askopenfilename(initialdir = "C:/Downloads",title = "Select a File", filetypes = (("Text files", "*.txt*"),("all files","*.*")))
    label_file_explorer.configure(text="Preview of Scansion for File: "+filename)
    file_path = filename
    if file_path:
        global scans, abs_path
        abs_path = os.path.abspath(file_path)
        output.configure(text="Scanning file, please wait...")
        output.update()
        scans = greekToScansion(abs_path)
        output.configure(text=makeMorePresentable(scans[0], scans[3], True))

def downloadScansion():
    # This function is used to download the scansion output
    if(output.cget("text") == "" or output.cget("text") == "Please provide a file to scan first."):
        output.configure(text="Please provide a file to scan first.")
    else:
        filename = filedialog.asksaveasfilename(initialdir = "C:/Downloads",title = "Save File", filetypes = (("Text files", "*.txt*"),("all files","*.*")))
        pathToSave = os.path.abspath(filename)
        file = open(pathToSave, "w")
        file.write("Ariadne Scansion of {}\n".format(abs_path))
        file.write("Any scansions that inclue a ? could not be confidently determined by the algorithm.\n")
        file.write("This is either due to an incomplete line or a notable irregularity in the text.\n\n")
        file.write(makeMorePresentable(scans[0], scans[3], False, True))
        file.close()

# Window Declaration
window = tk.Tk()
window.title("Ariadne")
window.geometry("1200x900")
abs_path = ""

# Title Label
label = tk.Label(text="Ariadne Scansion Tool", font=("Courier", 16))
label.pack()

# File Input
# Create a File Explorer label
label_file_explorer = tk.Label(window, text = "Provide a file to scan", width = 100)        
frame_buttons = tk.Frame(window)
button_explore = tk.Button(frame_buttons, text = "Browse Files", command = open_file) 
button_download = tk.Button(frame_buttons, text = "Download Scansion", command = downloadScansion)
button_explore.pack(side=tk.LEFT, padx=5)
button_download.pack(side=tk.LEFT, padx=5)
frame_buttons.pack()
label_file_explorer.pack()

#File Output
output = tk.Label(text="", font=("Courier", 14), justify="left")
output.pack()

window.mainloop()