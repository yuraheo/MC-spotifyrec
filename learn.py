# command to get dict file, and inputfile
# python learn.py <dictionaryName> <matrixName> <inputName> # input file should be the json with the list of 
import os.path
import json
import sys
from pathlib import Path
import numpy as np

def main():
    dictionaryFile, matrixFile, inputFile = readArguments() 
    dictionary = loadDictionary(dictionaryFile)
    a_matrix = loadMatrix(matrixFile)

    if inputFile == "":
        # interactive mode (putting values into dict)
        while True:
            userInput = input(">> ")
            if userInput == "":
                break

            dictionary = learn(dictionary, userInput)
            updateDictFile(dictionaryFile, dictionary)
    else:
        # read from file
        # file_pattern = "mpd.slice.*.json"
        file_pattern = "mpd.slice.test.json"
        for file_path in Path("data").glob(file_pattern):
            with open(file_path, 'r', encoding='utf-8') as file:
                dictionary, a_matrix = learnify(dictionary, a_matrix, file)
                updateDictFile(dictionaryFile, dictionary)
                updateMatrixFile(matrixFile, a_matrix)
        

def readArguments():
    numArguments = len(sys.argv) - 1
    inputFile = ""

    if numArguments >= 1:
        dictionaryFile = sys.argv[1]
    if numArguments >= 2:
        matrixFile = sys.argv[2]
    if numArguments >= 3:
        inputFile = sys.argv[3]

    return dictionaryFile, matrixFile, inputFile

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

def loadMatrix(filename):
    if not os.path.exists(filename):
        # if the file doesn't exist, create that file
        file = open(filename, "w")
        empty_matrix = np.zeros((1, 1)).tolist() 
        json.dump( empty_matrix, file) # dump empty object into file and setup json file
        file.close()
    
    file = open(filename, "r")
    a_matrix = json.load(file)
    file.close()
    return a_matrix
    

# Find the next empty row without iteration
def find_next_empty_row(matrix):
    empty_row_index = None
    for i, row in enumerate(matrix):
        if all(val == 0 for val in row):
            empty_row_index = i
            break

    if empty_row_index:
        return empty_row_index
    else:
        old_size = len(matrix)

        # matrix.extend([[0] * len(matrix[0]) for _ in range(100)])
        # for row in matrix:
        #     row.extend([0] * 100)
        matrix.extend([[0] * len(matrix[0])])
        for row in matrix:
            row.append(0)

        
        return old_size  


def learnify(dict, a_matrix, file): # one json file
    # Parse the JSON
    data = json.load(file)
    for playlist in data["playlists"]:
        for track in playlist['tracks']:
            currentSong = track['track_name']
            for track2 in playlist['tracks']:
                if track2['track_name'] != currentSong:
                    nextSong = track2['track_name']
                    currentIdx = None
                    if currentSong not in dict:
                        currentIdx = find_next_empty_row(a_matrix)
                        dict[currentSong] = currentIdx
                    currentIdx = dict[currentSong]

    
                    if nextSong not in dict:
                        nextIdx = find_next_empty_row(a_matrix)
                        dict[nextSong] = nextIdx
                    nextIdx = dict[nextSong]

                        # currentSong and nextSong now all in dict
                    if a_matrix[currentIdx][dict[nextSong]] == 0:
                        a_matrix[currentIdx][dict[nextSong]] = 1 

                    else:
                        a_matrix[currentIdx][dict[nextSong]] = a_matrix[currentIdx][dict[nextSong]] + 1
    return (dict, a_matrix)

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

def updateDictFile(filename, dictionary):
    file = open(filename, "w")
    json.dump(dictionary, file)
    file.close


def updateMatrixFile(filename, a_matrix):
    print("matrix was updated") 
    file = open(filename, "w")
    json.dump(a_matrix, file)
    file.close

main()