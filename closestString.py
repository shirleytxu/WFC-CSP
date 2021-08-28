import random
import math

def createRandomTestCase(alphabet, numStrings, stringLength, maxDistance):
    """
    :param alphabet:  list of letters that can be used in string
    :param numStrings:  the number of test case input strings to create
    :param stringLength: the length test case input string
    :param maxDistance: the maximum Hamming distance allowed between input
                        string and test case answer
    :return: (test case answer, list of test case input strings)
    """
    # create test case answer
    testCaseAnswer = random.choices(alphabet, k=stringLength)

    # create test case input strings
    testCaseInputStrings = []

    # create test case input strings
    for i in range(numStrings):
        # start with the answer
        inputString = testCaseAnswer.copy()

        # pick maxDistance position to changes
        positions_to_change = random.sample(range(stringLength), maxDistance)
        for position in positions_to_change:
            # replace the letter at position with a random letter
            inputString[position] = random.choice(alphabet)

        # add the changed inputString to results
        testCaseInputStrings.append(inputString)

    return testCaseAnswer, testCaseInputStrings


def createSpecialTestCase1(alphabet, numStrings, stringLength, maxDistance, count):
    """
    :param alphabet:  list of letters that can be used in string
    :param numStrings:  the number of test case input strings to create
    :param stringLength: the length test case input string
    :param maxDistance: the maximum Hamming distance allowed between input
                        string and test case answer
    :return: (test case answer, list of test case input strings)
    """

    assert numStrings > count, "Special test case requires numbStrings > count"

    # create test case answer
    testCaseAnswer = random.choices(alphabet, k=stringLength)

    # create test case input strings
    testCaseInputStrings = []

    # create test case input strings
    for i in range(count + 1):
        # start with the answer
        inputString = testCaseAnswer.copy()

        # pick maxDistance position to changes
        positions_to_change = random.sample(range(stringLength), maxDistance)
        for position in positions_to_change:
            # replace the letter at position with a random letter
            inputString[position] = random.choice(alphabet)

        # add the changed inputString to results
        if i == 0:
            # repeat the 1st string (numStrings - count) times
            testCaseInputStrings.extend([inputString] * (numStrings-count))
        else:
            testCaseInputStrings.append(inputString)

    return testCaseAnswer, testCaseInputStrings


def createSpecialTestCase2(alphabet, numStrings, stringLength, maxDistance, count):
    """
    :param alphabet:  list of letters that can be used in string
    :param numStrings:  the number of test case input strings to create
    :param stringLength: the length test case input string
    :param maxDistance: the maximum Hamming distance allowed between input
                        string and test case answer
    :return: (test case answer, list of test case input strings)
    """
    # create test case answer
    testCaseAnswer = random.choices(alphabet, k=stringLength)

    # create test case input strings
    testCaseInputStrings = []

    # create test case input strings
    inputString = testCaseAnswer.copy()

    # pick maxDistance position to changes from the 1st half of the string
    positions_to_change = random.sample(range(stringLength//2), maxDistance)
    for position in positions_to_change:
        # replace the letter at position with a random letter
        inputString[position] = random.choice(alphabet)

    # add the changed inputString to results
    testCaseInputStrings.extend([inputString] * (numStrings - count))

    for i in range(count):
        # start with the answer
        inputString = testCaseAnswer.copy()

        # pick maxDistance position to changes from the 1st half of the string
        positions_to_change = random.sample(range(stringLength//2, stringLength), maxDistance)
        for position in positions_to_change:
            # replace the letter at position with a random letter
            inputString[position] = random.choice(alphabet)

        # add the changed inputString to results
        testCaseInputStrings.append(inputString)

    return testCaseAnswer, testCaseInputStrings


def calculateLetterFreq(inputStrings, alphabet):
    """
    :param inputStrings:  list of input strings, all strings ar of  the same length
    :param alphabet: alphabet used to create the input strings
    """

    # find string length from the first string
    stringLength = len(inputStrings[0])

    # letter frequency table is a 2-D array implemented as list of list
    letterFreqTable = {}
    for position in range(stringLength):
        # create frequency for all alphabet letter at this position
        alphabetFreqTable = {}

        for alphabetLetter in alphabet:
            alphabetFreqTable[alphabetLetter] = 0
            for inputString in inputStrings:
                if inputString[position] == alphabetLetter:
                    alphabetFreqTable[alphabetLetter] += 1

        letterFreqTable[position] = alphabetFreqTable

    return letterFreqTable


def calculateScoreboard(letterFreqTable, positions):
    scoreboard = []
    for position in positions:
        alphabetFreqTable = letterFreqTable[position]
        for letter, freq in alphabetFreqTable.items():
            score = (position, letter, freq)
            scoreboard.append(score)

    scoreboard.sort(key=lambda entry: entry[2], reverse=True)
    return scoreboard


def printLetterFreqTable(letterFreqTable):
    for position in range(len(letterFreqTable)):
        print("pos: %2d, freq: %s" % (position, letterFreqTable[position]))


def calculateDistance(string1, string2):
    """
    find the Hamming distance between string1 and string 2
    :param string1: string 1
    :param string2: string 2
    :return:
    """

    distance = 0
    stringLength = len(string1)
    for index in range(stringLength):
        if string1[index] != string2[index]:
            distance += 1

    return distance


def calculateDistancesWithInputStrings(answer, inputStrings):
    distances = []
    for inputStringIndex in range(len(inputStrings)):
        distance = calculateDistance(answer, inputStrings[inputStringIndex])
        distances.append((inputStringIndex, distance))

    distances.sort(key=lambda entry: entry[1], reverse=True)
    return distances


def findClosestString(alphabet, inputStrings, maximumDistance):
    # all string are of same length
    stringLength = len(inputStrings[0])

    letterFreqTable = calculateLetterFreq(inputStrings, alphabet)

    # create initial answer with all SPACE
    answer = [" "] * stringLength
    undecidedPositions = set(range(stringLength))

    while len(undecidedPositions) > 0:
        # there is at least 1 undecided positions
        print()
        print("current undecided position:", len(undecidedPositions), undecidedPositions)

        scoreboard = calculateScoreboard(letterFreqTable, undecidedPositions)
        print("current scoreboard:", scoreboard)

        # sort and find string with maximum distance to current answer
        inputStringDistances = calculateDistancesWithInputStrings(answer, inputStrings)

        # first string is the one with maximum distance to the answer
        maxDistanceInputStringIndex, maxDistance = inputStringDistances[0]
        maxDistanceInputString = inputStrings[maxDistanceInputStringIndex]
        print("current string with maximum Distance: ",
              maxDistanceInputStringIndex, maxDistanceInputString, maxDistance)

        # find the 1st (position, letter) in scoreboard  that matches
        # maxDistanceInputString
        for position, letter, score in scoreboard:
            if maxDistanceInputString[position] == letter:
                # found, update the answer
                print("found position %d, letter '%s'" % (position, letter))
                answer[position] = letter
                print("answer = ", answer)

                # remove position from undecided positions
                undecidedPositions.remove(position)
                break

    return answer


def checkTestCase(numStrings, inputStrings, answer, alphabet, k):
    for inputStringIndex in range(numStrings):
        print("input_strings %2d: %s, distance to expected answer: %d" % (
            inputStringIndex, inputStrings[inputStringIndex],
            calculateDistance(answer, inputStrings[inputStringIndex])))

    letterFreqTable = calculateLetterFreq(inputStrings, alphabet)
    print("letter frequency table:")
    printLetterFreqTable(letterFreqTable)

    result = findClosestString(alphabet, inputStrings, k)
    print("expected answer      : ", answer)
    print("Found closest strings: ", result)
    print("Distance between expected answer and result: ", calculateDistance(answer, result))

    for inputStringIndex in range(numStrings):
        print("input_strings %2d: %s, distance to result: %d" % (
            inputStringIndex, inputStrings[inputStringIndex],
            calculateDistance(result, inputStrings[inputStringIndex])))

    inputStringDistances = calculateDistancesWithInputStrings(result, inputStrings)
    print("maxDistance to result, stringIndex %d, distance: %d" % inputStringDistances[0])

    if inputStringDistances[0][1] > k:
        print("Algorithm Failed! Result has larger Hamming distance %d > %d" % (inputStringDistances[0][1], k))
        return False
    return True


def main():
    alphabet = ["a", "c", "g", "t"]
    numStrings = 10
    stringLength = 10
    k = 4

    numCases = 0
    numCasesFailed = 0
    numCasesSaved = 0
    while numCases < 1000:
        failedCaseState = random.getstate()
        answer, inputStrings = createRandomTestCase(alphabet, numStrings, stringLength, k)
        #answer, inputStrings = createSpecialTestCase2(alphabet, numStrings,stringLength, k, 2)
        print("Answer: ", answer)
        caseResult = checkTestCase(numStrings, inputStrings, answer, alphabet, k)
        print("done")
        numCases += 1
        timesToTryAgain = 0
        #while caseResult == False and timesToTryAgain <= math.factorial(stringLength):
        while caseResult == False and timesToTryAgain <= 10:
            if timesToTryAgain == 0:
                numCasesFailed += 1
            random.shuffle(inputStrings)
            caseResult = checkTestCase(numStrings, inputStrings, answer,
                                       alphabet, k)
            if caseResult == True:
                print("Failed before, now works! Hurray! ")
                numCasesSaved += 1
                break
            timesToTryAgain += 1

    print("Out of", numCases, "test cases", numCasesFailed, "cases failed. State:", failedCaseState)
    print("Saved cases: ", numCasesSaved)

    random.setstate(failedCaseState)
    #answer, inputStrings = createRandomTestCase(alphabet, numStrings, stringLength,
                                               # k)
    #print("Answer: ", answer)
    #betterResult = checkTestCase(numStrings, inputStrings, answer, alphabet, k)

if __name__ == "__main__":
    main()