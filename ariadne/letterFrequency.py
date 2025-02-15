# Parker Holland
# letterFrequency Algorithm

# This function will remove all unneccesary patterns from the letter_frequency output file
def clean_text(fileName, patternLength):
    with open(fileName, 'r') as file:
        lines = file.readlines()

    cleanedLines = []
    charsToClean = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
                    '.', ',', '!', '?', ':', ';', '-', '_', '(', ')', 
                    '[', ']', '{', '}', '"', "'", '`', '~', '@', '#', 
                    '$', '%', '^', '&', '*', '+', '=', '<', '>', '/', 
                    '\\', '|', '\t', ' ', '\n']
    for line in lines:
        try:
            tempString = line[0:patternLength]
            clean = True
            for char in tempString:
                if(char in charsToClean):
                    clean = False
                    break
            
            if(clean):
                cleanedLines.append(line)
        except:
            continue

    with open(fileName, 'w') as file:
        for line in cleanedLines:
            file.write(line)

def letter_frequency(fileName, cleaned = False, patternLength = 1):
    if(not cleaned):
        fileRead = open(fileName, 'r')
        fileWrite = open("researchProject/outputs/frequency/test.txt", 'w')
        # Create a dictionary to store the frequency of each letter
        frequency = {}
        pattern = ""
        
        # Read the file and count the frequency of each letter
        for line in fileRead:
            for char in line:
                pattern += char
                if(len(pattern) == patternLength):
                    if pattern in frequency:
                        frequency[pattern] += 1  # Increment the count
                    else:
                        frequency[pattern] = 1  # Initialize the count
                    
                    if(patternLength > 1):
                        pattern = pattern[1:len(pattern)]
                    else:
                        pattern = ""


        # Write the frequency to the output file
        for char, count in frequency.items():
            fileWrite.write(f"{char}: {count}\n")

        # Close the files  
        fileRead.close()
        fileWrite.close()
        clean_text("researchProject/outputs/frequency/test.txt", patternLength)
    else:
        from cltk.prosody.grc import Scansion
        from cltk import NLP
        import sys
        sys.path.append("cltk")

        scanner = Scansion()
        with open(fileName, 'r', encoding="utf8") as file:
            file_content = file.read()

        # https://github.com/cltk/cltk/issues/1247
        # Including this here just in case
        cltk_nlp = NLP(language="grc")
        cltk_doc = cltk_nlp.analyze(file_content)
        tokens = cltk_doc.tokens
        clean_accents = Scansion()._clean_accents(tokens)

        fileWrite = open("researchProject/outputs/frequency/testCleaned.txt", 'w')
        # Create a dictionary to store the frequency of each letter
        frequency = {}
        pattern = ""
        
        # Read the clean_accents and count the frequency of each letter
        for char in clean_accents:
            pattern += char
            if(len(pattern) == patternLength):
                if pattern in frequency:
                    frequency[pattern] += 1  # Increment the count
                else:
                    frequency[pattern] = 1  # Initialize the count
                
                if(patternLength > 1):
                    pattern = pattern[1:len(pattern)]
                else:
                    pattern = ""

        # Write the frequency to the output file
        for char, count in frequency.items():
            fileWrite.write(f"{char}: {count}\n")

        # Close the files
        fileWrite.close()
        clean_text("researchProject/outputs/frequency/testCleaned.txt", patternLength)


letter_frequency("researchProject/texts/thetheogeny.txt", True, 2)