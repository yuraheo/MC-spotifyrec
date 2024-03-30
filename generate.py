import sys
import os.path
import json
import random
# command call: python generate.py <length> <dictionary>

def main():
    length, filename = readArguments()
    dictionary = loadDictionary(filename)

    lastSong = "~~~~~~~~~~~~~~~~" # sth we are unlikely to encounter at the begining
    result = ""

    for i in range(0, length):
        newSong = getNextSong(lastSong, dictionary)
        result = result + "->" + newSong
        lastSong = newSong

    print(result)



def readArguments():
    length = 50
    filename = "dictionary.json"

    numArguments = len(sys.argv) - 1
    if numArguments >= 1:
        length = int(sys.argv[1])
    if numArguments >= 2:
        filename = sys.argv[2]
    return length, filename

def loadDictionary(filename):
    if not os.path.exists(filename):
        sys.exit("Error: Dictionary not found")
        
    file = open(filename, "r")
    dictionary = json.load(file)
    file.close()
    return dictionary

def getNextSong(lastSong, dict):
    if lastSong not in dict:
        # pick new random state
        newSong = pickRandom(dict)
        return newSong

    else:
        # pick new word from list
        candidates = dict[lastSong]
        candidatesNormalized = []

        for song in candidates:
            freq = candidates[song]
            for i in range(0, freq):
                candidatesNormalized.append(song)

        rnd = random.randint(0, len(candidatesNormalized) - 1)
        return candidatesNormalized[rnd]

def pickRandom(dict):
    randNum = random.randint(0, len(dict) - 1)
    newSong = dict.keys()[randNum]
    return newSong

main()