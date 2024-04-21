import sys
import os.path
import json
import random
# command call: python generate.py <length> <dictionary> <a_matrix>

def main():
    length, dictfilename, matrixfilename = readArguments()
    dictionary = loadDictionary(dictfilename)
    a_matrix = loadMatrix(matrixfilename)

    lastSong = "First Song" # set the first song
    result = "Music Recommendation: "
    musicreclist = []

    for i in range(0, length):
        newSong = getNextSong(lastSong, dictionary, a_matrix)
        musicreclist.append(newSong)
        # result = result + "->" + newSong
        lastSong = newSong
    result += " -> ".join(musicreclist)

    print(result)



def readArguments():
    length = 50
    dfilename = "dictionary.json"
    mfilename = "adjacency.json"

    numArguments = len(sys.argv) - 1
    if numArguments >= 1:
        length = int(sys.argv[1])
    if numArguments >= 2:
        dfilename = sys.argv[2]
    if numArguments >= 3:
        mfilename = sys.argv[3]

    return length, dfilename, mfilename

def loadDictionary(filename):
    if not os.path.exists(filename):
        sys.exit("Error: Dictionary not found")
        
    file = open(filename, "r")
    dictionary = json.load(file)
    file.close()
    return dictionary

def loadMatrix(filename):
    if not os.path.exists(filename):
        sys.exit("Error: Adjacency Matrix not found")
        
    file = open(filename, "r")
    a_matrix = json.load(file)
    file.close()
    return a_matrix

def getNextSong(lastSong, dict, a_matrix):
    if lastSong not in dict:
        # pick new random state
        newSong = pickRandom(dict)
        return newSong

    else:
        # pick new word from list
        lastIdx = dict[lastSong]
        candidates = a_matrix[lastIdx] # list of frequencies
        candidatesNormalized = []

        for idx in range(1, len(candidates)):
            freq = candidates[idx]
            song = [k for k,v in dict.items() if v == idx][0]
            
            for _ in range(0, freq):
                candidatesNormalized.append(song)

        rnd = random.randint(0, len(candidatesNormalized) - 1)
        return candidatesNormalized[rnd]

def pickRandom(dict):
    randNum = random.randint(0, len(dict) - 1)
    newSong = list(dict.keys())[randNum]
    return newSong

main()