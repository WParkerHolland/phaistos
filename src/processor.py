# Phaistos Disc Project
# Declaration of processor function and calling of it
# Uses cltk, Fran did most of this

def greekToScansion(file_path):
    from cltk.prosody.grc import Scansion
    from cltk import NLP
    import sys
    sys.path.append("cltk")

    scanner = Scansion()
    with open(file_path, 'r', encoding="utf8") as file:
        file_content = file.read()

    # https://github.com/cltk/cltk/issues/1247
    # Including this here just in case
    cltk_nlp = NLP(language="grc")
    cltk_doc = cltk_nlp.analyze(file_content)
    tokens = cltk_doc.tokens
    clean_accents = Scansion()._clean_accents(tokens)
    syllables = Scansion()._make_syllables(clean_accents)
    condensed = Scansion()._syllable_condenser(syllables)
    scanned = Scansion()._scansion(condensed)
    return scanned, condensed, clean_accents

def makePresentable(scansion):
    # This function is used to make the scansion output more presentable
    newScansion = ""
    for sentence in scansion:
        for syllable in sentence:
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

def makeMorePresentable(scansion, syllables):
    # This function will make the scansion output more presentable while also displaying how each syllable was classified
    syllOffset = 0
    finString = ""
    for sentence in scansion:
        syllI = 0
        scanSent = ""
        syllSent = ""

        for syllable in sentence:
            match syllable:
                case "¯":
                    scanSent += "- "
                    syllSent += str(syllables[syllOffset][syllI]) + " "
                    syllI += 1
                case "˘":
                    scanSent += "u "
                    syllSent += str(syllables[syllOffset][syllI]) + " "
                    syllI += 1
                case "|":
                    if scanSent != "":
                        scanSent += "| "
                        syllSent += "| "
                case _:
                    scanSent += "x"
                    syllSent += str(syllables[syllOffset][syllI]) + " "
                    syllI += 1
                    syllSent = syllSent.replace("\n", "\\n")
                    finString += scanSent + "\n"
                    finString += syllSent + "\n"
                    scanSent = ""
                    syllSent = ""
        
        syllOffset += 1
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

def checkScansion(scansion):
    # This checks the scansion for any of the patterns we're looking for
    # Will return a 2 lists of sentence indexes with the patterns found within, one for right way patterns and one for wrong way patterns
    # [[SentenceIndex, PatternIndex], ...] is the format of the returned list
    import janus_swi as janus
    janus.consult("prolog/scansion.pl")
    returnListRight = []
    returnListWrong = []

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
    
    return returnListRight, returnListWrong
    
def displayMatches(scansion, matchesRight, matchesWrong, sentences):
    # This function displayes matches found in the scansion in a file
    file = open("researchProject/output.txt", "w")
    if matchesRight == [] and matchesWrong == []:
        file.write(":(")
    else:
        rightWayPatterns = ["- u u | - - | - x",
                             "- - | - - | - x"]
        wrongWayPatterns = ["- - | - - | - - |",
                             "- u u | - - | - - |",
                             "- u u | - - | - u u |",
                             "- - | - - | - u u |"]
        
        file.write("Matches found reading the right way:\n\n")
        for match in matchesRight:
            file.write("Match found in sentence {}:\n".format(match[0]))
            file.write("Pattern found: {}\n".format(rightWayPatterns[match[1]]))
            file.write("Sentence: {}\n\n".format(makeSyllablesPresentable(sentences[match[0]])))
            file.write("Scansion: \n{}\n".format(makePresentable(scansion[match[0]])))

        file.write("\nMatches found reading the wrong way:\n\n")
        for match in matchesWrong:
            file.write("Match found in sentence {}:\n".format(match[0]))
            file.write("Pattern found: {}\n".format(wrongWayPatterns[match[1]]))
            file.write("Sentence: {}\n\n".format(makeSyllablesPresentable(sentences[match[0]])))
            file.write("Scansion: \n{}\n".format(makePresentable(scansion[match[0]])))
    
    file.close()


scans = greekToScansion("researchProject/texts/shortTheogeny.txt")
print(scans[2])
#matchesRight, matchesWrong = checkScansion(scans[0])
#displayMatches(scans[0], matchesRight, matchesWrong, scans[1])