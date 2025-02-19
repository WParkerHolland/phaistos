# Phaistos Disc Project
# Declaration of processor function and calling of it
# Uses cltk, Fran did most of this
import tkinter as tk
from tkinter import filedialog
import os
import sys
sys.path.append("./../../src/")
from cltk import NLP
from cltk.prosody.grc import Scansion

def greekToScansion(file_path):
    with open(file_path, 'r', encoding="utf8") as file:
        file_content = file.read()

    # https://github.com/cltk/cltk/issues/1247
    # Including this here just in case
    cltk_nlp = NLP(language="grc")
    cltk_doc = cltk_nlp.analyze(file_content)
    tokens = cltk_doc.tokens
    clean_accents = Scansion()._clean_accents(tokens)
    syllables = Scansion()._make_syllables(clean_accents)
    
    # Formatting Syllable Output
    forFormat = []
    for grouping in syllables:
        for i in range(len(grouping)):
            tempArray = []
            lastIndex = 0
            for j in range(len(grouping[i])):
                if '\n' in grouping[i][j] and j < len(grouping[i]) - 1:
                    tempSlice = grouping[i][lastIndex:j]
                    if tempSlice != []:
                        tempArray.append(tempSlice)
                    lastIndex = j
            tempArray.append(grouping[i][lastIndex:])
            forFormat.append(tempArray)
    syllables = forFormat
    # Condensing Syllable Output
    forFormat = []
    for grouping in syllables:
        for line in grouping:
            forFormat.append(line)

    condensed = forFormat
    scanned = scansion(Scansion(), condensed)
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
    skip = False
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
                if(skip):
                    skip = False
                    continue
                if(line[i:i+2] == ['¯', '¯']):
                    scanLine += centerText('¯', len(syllables[lineOffset][i])) + " " + centerText('¯', len(syllables[lineOffset][i+1])) + " | "
                    syllLine += syllables[lineOffset][i] + " " + syllables[lineOffset][i+1] + " | "
                    skip = True
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

def checkScansion(scansion):
    # This checks the scansion for any of the patterns we're looking for
    # Will return a 2 lists of sentence indexes with the patterns found within, one for right way patterns and one for wrong way patterns
    # [[SentenceIndex, PatternIndex], ...] is the format of the returned list
    returnListRight = []
    returnListWrong = []
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

def scansionHelper(line: list[str], position: int, currentFoot: int) -> list[str]:
    # Recursive Function to develop a scansion for a single line
    # Line is list of syllables, position is the current syllable index
    # currentFoot is the current foot index, scansion is the scansion being developed

    # Check if two many feet in line
    tempLine = line.copy()

    if(currentFoot == 6):
        if(len(line[position:]) == 2):
            tempLine[position] = '¯'
            tempLine[position + 1] = 'X'
            return tempLine
        # Check if less than or greater than 2 syllables left
        else:
            raise Exception("Too many feet in line")
                

    # If syllable unknown
    if line[position] == '?':
        # If next syllable long, its a spondee
        if line[position + 1] == '¯':
            try:
                tempLine[position] = '¯'
                return scansionHelper(tempLine, position + 2, currentFoot + 1)
            except Exception as e:
                if(str(e) == "Too many feet in line" and line[position + 2] == '?'):
                    line[position] = '¯'
                    line[position + 1] = '˘'
                    line[position + 2] = '˘'
                    return scansionHelper(line, position + 3, currentFoot + 1)
                else:
                    raise e
        # If next two syllable unknown, most likely a dactyl
        # Consider putting a try except statement in to try spondee if error, depends on accuracy of function
        elif line[position + 1] == '?' and line[position + 2] == '?':
            try:
                tempLine[position] = '¯'
                tempLine[position + 1] = '˘'
                tempLine[position + 2] = '˘'
                return scansionHelper(tempLine, position + 3, currentFoot + 1)
            except Exception as e:
                if(str(e) == "End of line reached too early"):
                    line[position] = '¯'
                    line[position + 1] = '¯'
                    return scansionHelper(line, position + 2, currentFoot + 1)
                else:
                    raise e
        # If next syllable unknown and following syllable long, its probably a spondee
        elif line[position + 1] == '?' and line[position + 2] == '¯':
            tempLine[position] = '¯'
            tempLine[position + 1] = '¯'
            return scansionHelper(tempLine, position + 2, currentFoot + 1)
    
    # If syllable is known long
    elif line[position] == '¯':
        # If next syllable long, its a spondee
        # If an error is encountered, it may be a dactyl because of epic correption
        if line[position + 1] == '¯':
            try:
                tempLine[position + 1] = '¯'
                return scansionHelper(tempLine, position + 2, currentFoot + 1)
            except Exception as e:
                if(str(e) == "Too many feet in line" and line[position + 2] == '?'):
                    line[position + 1] = '˘'
                    line[position + 2] = '˘'
                    return scansionHelper(line, position + 3, currentFoot + 1)
                else:
                    raise e
        # If next two syllable unknown, most likely a dactyl
        # Unless run out of syllables, then it's a spondee
        # Consider including way to notify user of this because it may be an outlier and interesting to the classicist
        elif line[position + 1] == '?' and line[position + 2] == '?':
            try:
                tempLine[position + 1] = '˘'
                tempLine[position + 2] = '˘'
                return scansionHelper(tempLine, position + 3, currentFoot + 1)
            except Exception as e:
                if(str(e) == "End of line reached too early"):
                    line[position + 1] = '¯'
                    return scansionHelper(line, position + 2, currentFoot + 1)
                else:
                    raise e
        # If next syllable unknown and following syllable long, its a spondee
        # Unless scansion runs out of lines, then it's a dactyl
        # Consider including way to notify user of this because it may be an outlier and interesting to the classicist
        elif line[position + 1] == '?' and line[position + 2] == '¯':
            try:
                tempLine[position + 1] = '¯'
                return scansionHelper(tempLine, position + 2, currentFoot + 1)
            except Exception as e:
                if(str(e) == "Too many feet in line"):
                    line[position + 1] = '˘'
                    line[position + 2] = '˘'
                    return scansionHelper(line, position + 3, currentFoot + 1)
                else:
                    raise e

    # If the end of the line is reached too early
    raise Exception("End of line reached too early")
    
def scansion(obj, sentence_syllables: list[list[str]]) -> list[str]:
    """Replace long and short values for each input syllable.

    Args:
        sentence_syllables: List of word tokens

    Returns:
        ``"˘"`` and ``"¯"`` to represent short and long syllables, respectively

    >>> from cltk.prosody.grc import Scansion
    >>> syllables_sentence = [["νε", "ος", "μεν", "και", "α", "πει", "ρος", "δι", "κων", "ε", "γω", "γε", "ε", "τι"], ["μεν", "και", "α", "πει", "ρος"]]
    >>> Scansion()._scansion(syllables_sentence)
    ['˘¯¯¯˘¯¯˘¯˘¯˘˘x', '¯¯˘¯x']
    """
    scanned_text = list()
    errCounter = 0
    for sentence in sentence_syllables:
        line = ['?'] * len(sentence)
        line[0] = '¯'
        line[len(sentence) - 1] = 'X'
        for i in range(1, len(sentence) - 1):
            if obj._long_by_nature(sentence[i]) or obj._long_by_position(i, sentence[i], sentence):
                line[i] = '¯'

        try:
            tempLine = line.copy()
            scanned_text.append(scansionHelper(line, 0, 1))
        except:
            print(str(errCounter) + ' ' + str(tempLine))
            print(sentence)
            scanned_text.append(tempLine)

        errCounter += 1

    return scanned_text

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
        output.configure(text=makeMorePresentable(scans[0], scans[3], True, False))

def downloadScansion():
    # This function is used to download the scansion output
    if(output.cget("text") == "" or output.cget("text") == "Please provide a file to scan first."):
        output.configure(text="Please provide a file to scan first.")
    else:
        filename = filedialog.asksaveasfilename(initialdir = "C:/Downloads",title = "Save File", filetypes = (("Text files", "*.txt*"),("all files","*.*")))
        pathToSave = os.path.abspath(filename)
        file = open(pathToSave + ".txt", "w")
        file.write("Ariadne Scansion of {}\n".format(abs_path))
        file.write("Any scansions that inclue a ? could not be confidently determined by the algorithm.\n")
        file.write("This is either due to an incomplete line or a notable irregularity in the text.\n\n")
        file.write(makeMorePresentable(scans[0], scans[3], False, True))
        file.close()

# Window Declaration
window = tk.Tk()
window.title("Ariadne")
window.geometry("1200x900")

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