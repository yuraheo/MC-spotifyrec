# command to get dict file, and inputfile
# python learn.py <dictionaryName> <inputName>
import os.path
import json
import sys

def main():
    dictionaryFile, inputFile = readArguments() 
    dictionary = loadDictionary(dictionaryFile)

    if inputFile == "":
        # interactive mode (putting values into dict)
        while True:
            userInput = raw_input(">> ")
            if userInput == "":
                break

            dictionary = learn(dictionary, userInput)
            updateFile(dictionaryFile, dictionary)
    else:
        # read from file
        print("Not yet implemented")


def readArguments():
    numArguments = len(sys.argv) - 1
    inputFile = ""

    if numArguments >= 1:
        dictionaryFile = sys.argv[1]
    if numArguments >= 2:
        inputFile = sys.argv[2]

    return dictionaryFile, inputFile

def loadDictionary(filename):
    if not os.path.exists(filename):
        # if the file doesn't exist, create that file
        file = open(filename, "w")
        json.dump( {}, file) # dump empty object into file and setup json file
        file.close()
    
    file = open(filename, "r")
    dictionary = json.load(file)
    file.close()
    return dictionary

def learn(dict, input):
    tokens = input.split("//") # we want to make songs into a list of strings with // seperating them
    for i in range(0, len(tokens) - 1):
        currentSong = tokens[i]
        nextSong = tokens[i+ 1]
        
    if currentSong not in dict:
        # create new entry in dictionary
        dict[currentSong] = { nextSong: 1}
    else:
        # current song was alr in dict
        allNextSongs = dict[currentSong]

        if nextSong not in allNextSongs:
            # add new next state
            dict[currentSong][nextSong] = 1

        else:
            # alr exists, just increment
            dict[currentSong][nextSong] = dict[currentSong][nextSong] + 1
    return dict

def updateFile(filename, dictionary):
    file = open(filename, "w")
    json.dump(dictionary, file)
    file.close


main()