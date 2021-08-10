import random

def setup(alphabet, numStrings, stringLength, k):
    answer = []
    S = []

    for position in range(stringLength):
        randomIndex = random.randint(0, len(alphabet) - 1)
        answer.append(alphabet[randomIndex])

    for i in range(numStrings):
        S.append(answer.copy())

    for i in range(numStrings):
        positionsChecked = 0
        while positionsChecked <= k:
            index = random.randint(0, len(answer) - 1)
            randomIndex = random.randint(0, len(alphabet) - 1)
            temp = alphabet[randomIndex]
            S[i][index] = temp
            positionsChecked += 1

    return answer, S

def findMaxLetter(S):
    maxLetters = []
    maxFreq = []

    for string in S:
        maxFreq = 0
        firstLetter = True
        for letter in string:
            if firstLetter == True:
                maxLetter = letter

def findLetterFreq(S, alphabet):
    allLetterFreq = []

    for alphabetLetterIndex in range(len(alphabet)):
        init = []
        for columnIndex in range(len(S[alphabetLetterIndex])):
            init.append(0)
        allLetterFreq.append(init)

    for letterIndex in range(len(S)):
        for columnIndex in range(len(S[letterIndex])):
            for alphabetLetterIndex in range(len(alphabet)):
                if S[letterIndex][columnIndex] == alphabet[alphabetLetterIndex]:
                    allLetterFreq[alphabetLetterIndex][columnIndex] += 1
    return allLetterFreq

def findMaxLetter(arr):
    firstTime = True
    for letter1 in arr:
        for letter2 in arr:
            if firstTime:
                maxLetter = letter1
                maxFreq = 1
                firstTime = False
            if letter1 == letter2:
                maxLetter = letter1
                maxFreq += 1

    return maxLetter, maxFreq

def main():
    alphabet = ["a", "c", "g", "t"]
    numStrings = 10
    stringLength = 8
    k = 4
    answer, S = setup(alphabet, numStrings, stringLength, k)
    print("Answer: ", answer)
    print("S: ", S)

    allLetterFreq = findLetterFreq(S, alphabet)
    print("allLetterFreq: ", allLetterFreq)
main()