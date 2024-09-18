# Parker Holland
# Hangman Function
# Design Doc - https://docs.google.com/document/d/1RYhjB8fTZh8LteizXC3_8jNXELYuW8u3lTbO_olbo0w/edit
# Format of substitutionList: [ [[patternToSub], lettersSubbedIn], [[patternToSub], lettersSubbedIn], ... ]
def hangman(substitutionList, diskOption = "default", symbolSet = "Greek1"):
    import random
    singleSubs, multiSubs, diskSymbols, possibleSymbols, symbolsToReplace, replacedSymbols = [], [], [], [], [], []
    
    # Setting the values of the disk, default factors in the damage but nothing else
    if(diskOption == "default"):
        diskSymbols = [[38, 3, 10, '|', 1, 13, '|', 21, 37, 35, 27, 27, 12, 2, '|', 38, 3, 10, '|', 35, 19, 23, '|', 1, 13, 12, 2, '|', 12, 26, 31],
                       [19, 17, 18, 6, '|', 27, 18, 32, 14, 27, 12, 2, '|', 26, 31, 12, 2, '|', 1, 28, '|', 18, 22, 10, 25, 27, 2, '|', 26, 31, 12, 2],
                       [23, 33, '|', 21, 37, 35, 27, 27, 12, 2, '|', 26, 31, 12, 2, '|', 1, 28, '|', 18, 23, 10, 25, 27, 2, '|', 11, 39],
                       [38, 23, 32, 12, 2, '|', 7, 40, 41, 1, '|', 35, 19, 41, 12, 2, '|', 35, 26, 31, '|', 46, 18, 6, 12, 2, '|', 2, 44, 27],
                       [12, 7, 45, 27, '|', 33, 40, 4, 12, 2, '|', 34, 29, 29, '|', 7, 45, 29, '|', 12, 40, 24, '|', 18, 1, 13, 12, 2],
                       [7, 45, '|', 25, 23, 34, 29, '|', 7, 23, 35, 6, 2, '|', 7, 18, 39, 30, 9, '|', 8, 7, 36, 29, 22, '|', 24, 18, 23, 7],
                       [7, 45, 7, '|', 35, 18, 7, '|', 25, 23, 34, 27, '|', 8, 7, 36, 29, 22, '|', 7, 25, 29, '|', 13, 8, 29],
                       [8, 7, 36, 29, '|', 1, 27, 9, 2, '|', 33, 39, 32, 35, 6, '|', 1, 33, 29, '|', 18, 14, 16, '|', 35, 20, 24, 24, 29],
                       [1, 38, 25, 27, '|', 40, 36, 26, 2, '|', 35, 40, 24, 7, '|', 25, 42, 37, 22, '|', 18, 1, 13, 7, 15, '|', 33, 39, 1],
                       [43, 18, 23, 16, '|', 12, 20, 24, 33, '|', 27, 25, 22, '|', 5, 23, 37, 2, '|', 35, 7, 45, 27, '|', 7, 40, 22, 12, 2]]
        symbolsToReplace = list(range(1, 47))
        singleSubs = list(range(0, 47))

    # Setting the possible symbols to replace the disk symbols with
    if(symbolSet == "IPA"):
        possibleSymbols = ['k', "kʰ", 'j', 'g', 'p', "pʰ", 'b', 'w', 't', "tʰ", 'd', 'h', 'l', 'm', 'n', 'ŋ', 'r', 'r̥', 's', 'z', "ks", "ps", "d͡z", 'a', "aː", "ɛː", 'e', "eː", 'i', "iː", "ɔː", 'o', "uː", 'y', "yː", "ai", "au", "ei", "eu̯", "oi̯", "yi̯", "aːi̯", "ɛːi̯", "ɔːi̯"]
    elif(symbolSet == "Greek1"):
        possibleSymbols = ['κ', 'χ', 'ι', 'γ', 'π', 'φ', 'β', 'υ', 'τ', 'θ', 'δ', '῾', 'λ', 'μ', 'ν', 'γ', 'ρ', 'ῤ', 'σ', 'ζ', 'ξ', 'ψ', 'ζ', 'ᾰ', 'ᾱ', 'η', 'ε', "ει", 'ῐ', 'ῑ', 'ω', 'ο', "ου", 'ῠ', 'ῡ', "αι", "αυ", "ει", "ευ", "οι", "υι", 'ᾳ', 'ῃ', 'ῳ']
        
    # Divides the substitutions between single and multi symbol substitutions
    for pair in substitutionList:
        if(len(pair[0]) == 1):
            del symbolsToReplace[pair[0][0] - 1]
            singleSubs[pair[0][0]] = pair[1]
        else:
            multiSubs.append(pair)

    # Randomly replaced all symbols without a single substitution
    for symbol in symbolsToReplace:
        singleSubs[symbol] = possibleSymbols[random.randint(0, len(possibleSymbols) - 1)]

    #Creates a list of strings with the substitions, each element is a individual row
    for row in diskSymbols:
        tempString = ""
        i = 0

        while(i < len(row)):
            if(row[i] != '|'):
                replaced = False
                for pattern in multiSubs:
                    if(row[i:i + len(pattern[0])] == pattern[0]):
                        tempString += pattern[1] + ' '
                        i += len(pattern[0]) - 1
                        replaced = True
                        break
                
                if(not(replaced)):
                    tempString += str(singleSubs[row[i]]) + ' '
            else:
                tempString += " | "
            
            i += 1
        
        replacedSymbols.append(tempString)

    hangmanVisualizer(diskSymbols, replacedSymbols)

def hangmanVisualizer(diskSymbols, replacedSymbols):
    # Put symbols in here once you have them
    # https://ctan.org/pkg/phaistos?lang=en
    phaistosSymbols = []

    from datetime import date

    date = str(date.today())
    print(date)
    file = open("researchProject/hangman" + date + ".txt", "w")
    
    for i in range(len(diskSymbols)):
        # Go through disk symbols and replace them with the symbols in phaistosSymbols
        file.write(str(diskSymbols[i]) + "\n")
        file.write(str(replacedSymbols[i]) + "\n\n")

    file.close()

hangman([[[12, 2], "ην"], [[27], 'τ']])