# Parker Holland
# Hangman Function

# Class for each symbol on the Phaistos Disk
class PhaistosSymbol:
    index = 0
    vegas = False
    capital = False
    vowel = False

    def __init__(self, index, vegas = False, capital = False, vowel = False):
        self.index = index
        self.vegas = vegas
        self.capital = capital
        self.vowel = vowel

# Function used to get the pattern of symbol indexes in a row
def getPattern(row, start, length):
    returnList = []
    for i in range(length):
        try:
            returnList.append(row[start + i].index)
        except:
            break
    return returnList

# Function used to convert a list of PhaistosSymbols to a list of integers
def listIntegerify(list):
    returnList = []
    for row in list:
        tempRow = []
        for i in row:
            if(i == '|'):
                tempRow.append(i)
            else:
                tempRow.append(i.index)
        
        returnList.append(tempRow)
    return returnList

# Design Doc - https://docs.google.com/document/d/166eCGtQkY7p9fehHq0iQ09CN0OKHsNsVhem0qRNi9nE/edit?usp=sharing
# Format of substitutionList: [ [[patternToSub], lettersSubbedIn, sectionForSub], [[patternToSub], lettersSubbedIn, sectionForSub], ... ]
def hangman(substitutionList, diskOption = "default", symbolSet = "Greek1", fileNameMod = ""):
    import random
    singleSubs, vegasSubs, capSubs, vowelSubs, multiSubs, diskSymbols, possibleSymbols, possibleVegasSymbols, possibleVowelSymbols, replacedSymbols = [], [], [], [], [], [], [], [], [], []
    
    # Setting the values of the disk, default factors in the damage but nothing else
    if(diskOption == "default"):
        diskSymbols = [[PhaistosSymbol(38), PhaistosSymbol(3), PhaistosSymbol(10), '|', PhaistosSymbol(1), PhaistosSymbol(13), '|', PhaistosSymbol(21), PhaistosSymbol(37), PhaistosSymbol(35), PhaistosSymbol(27), PhaistosSymbol(27), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(38), PhaistosSymbol(3), PhaistosSymbol(10), '|', PhaistosSymbol(35), PhaistosSymbol(19), PhaistosSymbol(23), '|', PhaistosSymbol(1), PhaistosSymbol(13), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(12), PhaistosSymbol(26), PhaistosSymbol(31)],
                   [PhaistosSymbol(19), PhaistosSymbol(17), PhaistosSymbol(18), PhaistosSymbol(6), '|', PhaistosSymbol(27), PhaistosSymbol(18), PhaistosSymbol(32), PhaistosSymbol(14), PhaistosSymbol(27), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(26), PhaistosSymbol(31), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(1), PhaistosSymbol(28), '|', PhaistosSymbol(18), PhaistosSymbol(22), PhaistosSymbol(10), PhaistosSymbol(25), PhaistosSymbol(27), PhaistosSymbol(2), '|', PhaistosSymbol(26), PhaistosSymbol(31), PhaistosSymbol(12), PhaistosSymbol(2)],
                   [PhaistosSymbol(23), PhaistosSymbol(33), '|', PhaistosSymbol(21), PhaistosSymbol(37), PhaistosSymbol(35), PhaistosSymbol(27), PhaistosSymbol(27), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(26), PhaistosSymbol(31), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(1), PhaistosSymbol(28), '|', PhaistosSymbol(18), PhaistosSymbol(23), PhaistosSymbol(10), PhaistosSymbol(25), PhaistosSymbol(27), PhaistosSymbol(2), '|', PhaistosSymbol(11), PhaistosSymbol(39)],
                   [PhaistosSymbol(38), PhaistosSymbol(23), PhaistosSymbol(32), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(7), PhaistosSymbol(40), PhaistosSymbol(41), PhaistosSymbol(1), '|', PhaistosSymbol(35), PhaistosSymbol(19), PhaistosSymbol(41), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(35), PhaistosSymbol(26), PhaistosSymbol(31), '|', PhaistosSymbol(46), PhaistosSymbol(18), PhaistosSymbol(6), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(2), PhaistosSymbol(44), PhaistosSymbol(27)],
                   [PhaistosSymbol(12), PhaistosSymbol(7), PhaistosSymbol(45), PhaistosSymbol(27), '|', PhaistosSymbol(33), PhaistosSymbol(40), PhaistosSymbol(4), PhaistosSymbol(12), PhaistosSymbol(2), '|', PhaistosSymbol(34), PhaistosSymbol(29), PhaistosSymbol(29), '|', PhaistosSymbol(7), PhaistosSymbol(45), PhaistosSymbol(29), '|', PhaistosSymbol(12), PhaistosSymbol(40), PhaistosSymbol(24), '|', PhaistosSymbol(18), PhaistosSymbol(1), PhaistosSymbol(13), PhaistosSymbol(12), PhaistosSymbol(2)],
                   [PhaistosSymbol(7), PhaistosSymbol(45), '|', PhaistosSymbol(25), PhaistosSymbol(23), PhaistosSymbol(34), PhaistosSymbol(29), '|', PhaistosSymbol(7), PhaistosSymbol(23), PhaistosSymbol(35), PhaistosSymbol(6), PhaistosSymbol(2), '|', PhaistosSymbol(7), PhaistosSymbol(18), PhaistosSymbol(39), PhaistosSymbol(30), PhaistosSymbol(9), '|', PhaistosSymbol(8), PhaistosSymbol(7), PhaistosSymbol(36), PhaistosSymbol(29), PhaistosSymbol(22), '|', PhaistosSymbol(24), PhaistosSymbol(18), PhaistosSymbol(23), PhaistosSymbol(7)],
                   [PhaistosSymbol(7), PhaistosSymbol(45), PhaistosSymbol(7), '|', PhaistosSymbol(35), PhaistosSymbol(18), PhaistosSymbol(7), '|', PhaistosSymbol(25), PhaistosSymbol(23), PhaistosSymbol(34), PhaistosSymbol(27), '|', PhaistosSymbol(8), PhaistosSymbol(7), PhaistosSymbol(36), PhaistosSymbol(29), PhaistosSymbol(22), '|', PhaistosSymbol(7), PhaistosSymbol(25), PhaistosSymbol(29), '|', PhaistosSymbol(13), PhaistosSymbol(8), PhaistosSymbol(29)],
                   [PhaistosSymbol(8), PhaistosSymbol(7), PhaistosSymbol(36), PhaistosSymbol(29), '|', PhaistosSymbol(1), PhaistosSymbol(27), PhaistosSymbol(9), PhaistosSymbol(2), '|', PhaistosSymbol(33), PhaistosSymbol(39), PhaistosSymbol(32), PhaistosSymbol(35), PhaistosSymbol(6), '|', PhaistosSymbol(1), PhaistosSymbol(33), PhaistosSymbol(29), '|', PhaistosSymbol(18), PhaistosSymbol(14), PhaistosSymbol(16), '|', PhaistosSymbol(35), PhaistosSymbol(20), PhaistosSymbol(24), PhaistosSymbol(24), PhaistosSymbol(29)],
                   [PhaistosSymbol(1), PhaistosSymbol(38), PhaistosSymbol(25), PhaistosSymbol(27), '|', PhaistosSymbol(40), PhaistosSymbol(36), PhaistosSymbol(26), PhaistosSymbol(2), '|', PhaistosSymbol(35), PhaistosSymbol(40), PhaistosSymbol(24), PhaistosSymbol(7), '|', PhaistosSymbol(25), PhaistosSymbol(42), PhaistosSymbol(37), PhaistosSymbol(22), '|', PhaistosSymbol(18), PhaistosSymbol(1), PhaistosSymbol(13), PhaistosSymbol(7), PhaistosSymbol(15), '|', PhaistosSymbol(33), PhaistosSymbol(39), PhaistosSymbol(1)],
                   [PhaistosSymbol(43), PhaistosSymbol(18), PhaistosSymbol(23), PhaistosSymbol(16), '|', PhaistosSymbol(12), PhaistosSymbol(20), PhaistosSymbol(24), PhaistosSymbol(33), '|', PhaistosSymbol(27), PhaistosSymbol(25), PhaistosSymbol(22), '|', PhaistosSymbol(5), PhaistosSymbol(23), PhaistosSymbol(37), PhaistosSymbol(2), '|', PhaistosSymbol(35), PhaistosSymbol(7), PhaistosSymbol(45), PhaistosSymbol(27), '|', PhaistosSymbol(7), PhaistosSymbol(40), PhaistosSymbol(22), PhaistosSymbol(12), PhaistosSymbol(2)]]
        singleSubs = list(range(0, 47))
    elif(diskOption == "vegas"):
        diskSymbols = [[PhaistosSymbol(38), PhaistosSymbol(3), PhaistosSymbol(10), '|', PhaistosSymbol(1, vowel=True), PhaistosSymbol(13), '|', PhaistosSymbol(21), PhaistosSymbol(37), PhaistosSymbol(35, vowel=True), PhaistosSymbol(27, vegas=True), PhaistosSymbol(27, vegas=True), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(38), PhaistosSymbol(3), PhaistosSymbol(10), '|', PhaistosSymbol(35, vowel=True), PhaistosSymbol(19), PhaistosSymbol(23, vowel=True), '|', PhaistosSymbol(1, vowel=True), PhaistosSymbol(13), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(12), PhaistosSymbol(26, vowel=True), PhaistosSymbol(31, vegas=True)],
               [PhaistosSymbol(19), PhaistosSymbol(17), PhaistosSymbol(18), PhaistosSymbol(6), '|', PhaistosSymbol(27, vegas=True), PhaistosSymbol(18), PhaistosSymbol(32), PhaistosSymbol(14), PhaistosSymbol(27, vegas=True), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(26, vowel=True), PhaistosSymbol(31, vegas=True), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(1, vowel=True), PhaistosSymbol(28, vowel=True), '|', PhaistosSymbol(18), PhaistosSymbol(22), PhaistosSymbol(10), PhaistosSymbol(25), PhaistosSymbol(27, vegas=True), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(26, vowel=True), PhaistosSymbol(31, vegas=True), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True)],
               [PhaistosSymbol(23, vowel=True), PhaistosSymbol(33, vowel=True), '|', PhaistosSymbol(21), PhaistosSymbol(37), PhaistosSymbol(35, vowel=True), PhaistosSymbol(27, vegas=True), PhaistosSymbol(27, vegas=True), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(26, vowel=True), PhaistosSymbol(31, vegas=True), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(1, vowel=True), PhaistosSymbol(28, vowel=True), '|', PhaistosSymbol(18), PhaistosSymbol(23, vowel=True), PhaistosSymbol(10), PhaistosSymbol(25), PhaistosSymbol(27, vegas=True), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(11, vowel=True), PhaistosSymbol(39, vowel=True)],
               [PhaistosSymbol(38), PhaistosSymbol(23, vowel=True), PhaistosSymbol(32), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(7, vowel=True), PhaistosSymbol(40), PhaistosSymbol(41), PhaistosSymbol(1, vowel=True), '|', PhaistosSymbol(35, vowel=True), PhaistosSymbol(19), PhaistosSymbol(41), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(35, vowel=True), PhaistosSymbol(26, vowel=True), PhaistosSymbol(31, vegas=True), '|', PhaistosSymbol(46), PhaistosSymbol(18), PhaistosSymbol(6), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(2, vegas=True), PhaistosSymbol(44), PhaistosSymbol(27, vegas=True)],
               [PhaistosSymbol(12), PhaistosSymbol(7, vowel=True), PhaistosSymbol(45, vowel=True), PhaistosSymbol(27, vegas=True), '|', PhaistosSymbol(33, vowel=True), PhaistosSymbol(40), PhaistosSymbol(4), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(34), PhaistosSymbol(29, vegas=True), PhaistosSymbol(29, vegas=True), '|', PhaistosSymbol(7, vowel=True), PhaistosSymbol(45, vowel=True), PhaistosSymbol(29, vegas=True), '|', PhaistosSymbol(12), PhaistosSymbol(40), PhaistosSymbol(24), '|', PhaistosSymbol(18), PhaistosSymbol(1, vowel=True), PhaistosSymbol(13), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True)],
               [PhaistosSymbol(7, vowel=True), PhaistosSymbol(45, vowel=True), '|', PhaistosSymbol(25), PhaistosSymbol(23, vowel=True), PhaistosSymbol(34), PhaistosSymbol(29, vegas=True), '|', PhaistosSymbol(7, vowel=True), PhaistosSymbol(23, vowel=True), PhaistosSymbol(35, vowel=True), PhaistosSymbol(6), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(7, vowel=True), PhaistosSymbol(18), PhaistosSymbol(39, vowel=True), PhaistosSymbol(30), PhaistosSymbol(9), '|', PhaistosSymbol(8, vowel=True), PhaistosSymbol(7, vowel=True), PhaistosSymbol(36), PhaistosSymbol(29, vegas=True), PhaistosSymbol(22), '|', PhaistosSymbol(24), PhaistosSymbol(18), PhaistosSymbol(23, vowel=True), PhaistosSymbol(7, vowel=True)],
               [PhaistosSymbol(7, vowel=True), PhaistosSymbol(45, vowel=True), PhaistosSymbol(7, vowel=True), '|', PhaistosSymbol(35, vowel=True), PhaistosSymbol(18), PhaistosSymbol(7, vowel=True), '|', PhaistosSymbol(25), PhaistosSymbol(23, vowel=True), PhaistosSymbol(34), PhaistosSymbol(27, vegas=True), '|', PhaistosSymbol(8, vowel=True), PhaistosSymbol(7, vowel=True), PhaistosSymbol(36), PhaistosSymbol(29, vegas=True), PhaistosSymbol(22), '|', PhaistosSymbol(7, vowel=True), PhaistosSymbol(25), PhaistosSymbol(29, vegas=True), '|', PhaistosSymbol(13), PhaistosSymbol(8, vowel=True), PhaistosSymbol(29, vegas=True)],
               [PhaistosSymbol(8, vowel=True), PhaistosSymbol(7, vowel=True), PhaistosSymbol(36), PhaistosSymbol(29, vegas=True), '|', PhaistosSymbol(1, vowel=True), PhaistosSymbol(27, vegas=True), PhaistosSymbol(9), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(33, vowel=True), PhaistosSymbol(39, vowel=True), PhaistosSymbol(32), PhaistosSymbol(35, vowel=True), PhaistosSymbol(6), '|', PhaistosSymbol(1, vowel=True), PhaistosSymbol(33, vowel=True), PhaistosSymbol(29, vegas=True), '|', PhaistosSymbol(18), PhaistosSymbol(14), PhaistosSymbol(16), '|', PhaistosSymbol(35, vowel=True), PhaistosSymbol(20), PhaistosSymbol(24), PhaistosSymbol(24), PhaistosSymbol(29, vegas=True)],
               [PhaistosSymbol(1, vowel=True), PhaistosSymbol(38), PhaistosSymbol(25), PhaistosSymbol(27, vegas=True), '|', PhaistosSymbol(40), PhaistosSymbol(36), PhaistosSymbol(26, vowel=True), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(35, vowel=True), PhaistosSymbol(40), PhaistosSymbol(24), PhaistosSymbol(7, vowel=True), '|', PhaistosSymbol(25), PhaistosSymbol(42), PhaistosSymbol(37), PhaistosSymbol(22), '|', PhaistosSymbol(18), PhaistosSymbol(1, vowel=True), PhaistosSymbol(13), PhaistosSymbol(7, vowel=True), PhaistosSymbol(15), '|', PhaistosSymbol(33, vowel=True), PhaistosSymbol(39, vowel=True), PhaistosSymbol(1, vowel=True)],
               [PhaistosSymbol(43, vowel=True), PhaistosSymbol(18), PhaistosSymbol(23, vowel=True), PhaistosSymbol(16), '|', PhaistosSymbol(12), PhaistosSymbol(20), PhaistosSymbol(24), PhaistosSymbol(33, vowel=True), '|', PhaistosSymbol(27, vegas=True), PhaistosSymbol(25), PhaistosSymbol(22), '|', PhaistosSymbol(5), PhaistosSymbol(23, vowel=True), PhaistosSymbol(37), PhaistosSymbol(2, vegas=True), '|', PhaistosSymbol(35, vowel=True), PhaistosSymbol(7, vowel=True), PhaistosSymbol(45, vowel=True), PhaistosSymbol(27, vegas=True), '|', PhaistosSymbol(7, vowel=True), PhaistosSymbol(40), PhaistosSymbol(22), PhaistosSymbol(12), PhaistosSymbol(2, vegas=True)]]
        singleSubs = list(range(0, 47))
        vegasSubs = list(range(0, 47))
        vowelSubs = list(range(0, 47))

    # Setting the possible symbols to replace the disk symbols with
    if(symbolSet == "IPA"):
        possibleSymbols = ['k', "kʰ", 'j', 'g', 'p', "pʰ", 'b', 'w', 't', "tʰ", 'd', 'h', 'l', 'm', 'n', 'ŋ', 'r', 'r̥', 's', 'z', "ks", "ps", "d͡z", 'a', "aː", "ɛː", 'e', "eː", 'i', "iː", "ɔː", 'o', "uː", 'y', "yː", "ai", "au", "ei", "eu̯", "oi̯", "yi̯", "aːi̯", "ɛːi̯", "ɔːi̯"]
        possibleVegasSymbols = []
        possibleVowelSymbols = []
    elif(symbolSet == "Greek1"):
        possibleSymbols = ['κ', 'χ', 'ι', 'γ', 'π', 'φ', 'β', 'υ', 'τ', 'θ', 'δ', '῾', 'λ', 'μ', 'ν', 'γ', 'ρ', 'ῤ', 'σ', 'ζ', 'ξ', 'ψ', 'ζ', 'ᾰ', 'ᾱ', 'η', 'ε', "ει", 'ῐ', 'ῑ', 'ω', 'ο', "ου", 'ῠ', 'ῡ', "αι", "αυ", "ει", "ευ", "οι", "υι", 'ᾳ', 'ῃ', 'ῳ']
        possibleVegasSymbols = ['α', 'ε', 'η', 'ι', 'o', 'υ', 'ω', 'σ', 'ρ', 'ν']
        possibleVowelSymbols = ['α', 'ε', 'η', 'ι', 'o', 'υ', 'ω']

    # Divides the substitutions between single and multi symbol substitutions
    for pair in substitutionList:
        if(len(pair[0]) == 1):
            try:
                if(pair[2] == "v"):
                    vegasSubs[pair[0][0]] = pair[1]
                elif(pair[2] == "c"):
                    capSubs[pair[0][0]] = pair[1]
                elif(pair[2] == "vo"):
                    vowelSubs[pair[0][0]] = pair[1]
                else:
                    singleSubs[pair[0][0]] = pair[1]
            except:
                singleSubs[pair[0][0]] = pair[1]
        else:
            multiSubs.append(pair)

    # Randomly replaced all symbols without a single substitution
    for i in range(len(singleSubs)):
        if(isinstance(singleSubs[i], int)):
            singleSubs[i] = possibleSymbols[random.randint(0, len(possibleSymbols) - 1)]
    for i in range(len(vegasSubs)):
        if(isinstance(vegasSubs[i], int)):
            vegasSubs[i] = possibleVegasSymbols[random.randint(0, len(possibleVegasSymbols) - 1)]
    for i in range(len(capSubs)):
        if(isinstance(capSubs[i], int)):
            capSubs[i] = possibleSymbols[random.randint(0, len(possibleSymbols) - 1)]
    for i in range(len(vowelSubs)):
        if(isinstance(vowelSubs[i], int)):
            vowelSubs[i] = possibleVowelSymbols[random.randint(0, len(possibleVowelSymbols) - 1)]

    #Creates a list of strings with the substitions, each element is a individual row
    for row in diskSymbols:
        tempScan = []
        tempFoot = []
        i = 0

        while(i < len(row)):
            if(row[i] != '|'):
                replaced = False
                for pattern in multiSubs:
                    tempList = getPattern(row, i, len(pattern[0]))
                    if(tempList == pattern[0]):
                        for j in pattern[1]:
                            tempFoot.append(j)
                        i += len(pattern[0]) - 1
                        replaced = True
                        break
                
                if(not(replaced)):
                    if(row[i].vegas):
                        tempFoot.append(str(vegasSubs[row[i].index]))
                    elif(row[i].capital):
                        tempFoot.append(str(capSubs[row[i].index]))
                    elif(row[i].vowel):
                        tempFoot.append(str(vowelSubs[row[i].index]))
                    else:
                        tempFoot.append(str(singleSubs[row[i].index]))
            else:
                tempScan.append(tempFoot)
                tempFoot = []
            
            i += 1

        tempScan.append(tempFoot)
        replacedSymbols.append(tempScan)

    diskSymbols = listIntegerify(diskSymbols)
    hangmanVisualizer(diskSymbols, replacedSymbols, fileNameMod)

def hangmanVisualizer(diskSymbols, replacedSymbols, fileNameMod):
    # Put symbols in here once you have them
    # https://www.fontspace.com/unicode/block/phaistos-disc
    import webbrowser, os
    phaistosSymbols = ["&#101D0", "&#101D1", "&#101D2", "&#101D3", "&#101D4", "&#101D5", "&#101D6", "&#101D7", "&#101D8", "&#101D9", "&#101DA", "&#101DB", "&#101DC", "&#101DD", "&#101DE", "&#101DF", "&#101E0", "&#101E1", "&#101E2", "&#101E3", "&#101E4", "&#101E5", "&#101E6", "&#101E7", "&#101E8", "&#101E9", "&#101EA", "&#101EB", "&#101EC", "&#101ED", "&#101EE", "&#101EF", "&#101F0", "&#101F1", "&#101F2", "&#101F3", "&#101F4", "&#101F5", "&#101F6", "&#101F7", "&#101F8", "&#101F9", "&#101FA", "&#101FB", "&#101FC", "#"]
    displaySymbols = []

    # Replacing the symbols in displaySymbols with phaistosSymbols
    for i in range(len(diskSymbols)):
        tempScan = []
        for j in range(len(diskSymbols[i])):
            if(diskSymbols[i][j] != '|'):
                tempScan.append(phaistosSymbols[diskSymbols[i][j]-1])
            else:
                tempScan.append('|')
        displaySymbols.append(tempScan)

    # Formatting replacedSymbols, diskSymbols, and displaySymbols for output
    for i in range(len(replacedSymbols)):
        for j in range(len(replacedSymbols[i])):
            replacedSymbols[i][j] = ' '.join(replacedSymbols[i][j])
        replacedSymbols[i] = " | ".join(replacedSymbols[i])
    for i in range(len(displaySymbols)):
        displaySymbols[i] = ' '.join(displaySymbols[i])
    for i in range(len(diskSymbols)):
        diskSymbols[i] = ' '.join(map(str, diskSymbols[i]))
    
    from datetime import date

    date = str(date.today())
    file_path = "researchproject/outputs/hangman/" + fileNameMod + date + ".html"
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("<head><meta charset=\"utf-8\"></head>\n")
        file.write("<html><body style=\"font-size:2em;\"><div>\n")
        
        for i in range(len(diskSymbols)):
            # Write lines in the specified format
            file.write(''.join(displaySymbols[i]).replace("&#", "&#x") + "<br/>\n")
            file.write(diskSymbols[i] + "<br/>\n")
            file.write(replacedSymbols[i] + "<br/>\n<br/>\n")

        file.write("</div></body></html>")

    webbrowser.open_new_tab(os.path.abspath(file_path))

# Function to read CSV formatted hangman data, then produce a number of possible combinations equal to iterations
def hangmanCSV(filename, iterations = 1):
    import pandas as pd
    import os
    import random

    # Read the CSV file, then print clean data
    data = pd.read_csv(filename)
    data = data.fillna('')
    columns = data.columns[1:]
    subList = []

    # Loop through each collumn, creating a list of possible substitutions
    for column in columns:
        tempList = []
        for sub in data[column]:
            if(sub != ''):
                tempList.append(sub)
        subList.append(tempList)

    # Make new directory for the created html files to go to
    dirName = filename.split("/")[2].split(".")[0]
    fileMod = "researchproject/outputs/hangman/" + dirName
    try:
        os.makedirs(fileMod)
    except FileExistsError:
        pass

    # For iterations number of times, select a random substitution from each list and run hangman
    for j in range(iterations):
        argList = []
        for i in range(len(subList)):
            tempChar = subList[i][random.randint(0, len(subList[i]) - 1)]
            tempList = [[i+1], tempChar]
            argList.append(tempList)

        hangman(argList, fileNameMod=dirName + '/' + str(j + 1) + '_')

    
hangman([])