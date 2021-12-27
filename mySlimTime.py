import random
import pickle
import sys
import timeit
import matplotlib.pyplot as plt
import pandas as pd

NOT_FOUND = "not found"


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
            prevPos = inputString[position]
            inputString[position] = random.choice(alphabet)
            while prevPos == inputString[position]:
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
            prevPos = inputString[position]
            inputString[position] = random.choice(alphabet)
            while prevPos == inputString[position]:
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
        prevPos = inputString[position]
        inputString[position] = random.choice(alphabet)
        while prevPos == inputString[position]:
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
        distances.append([inputStringIndex, distance])

    distances.sort(key=lambda entry: entry[1], reverse=True)
    return distances

def updateInputStringsDistances(inputStringDistances, answer, inputStrings, updatedPosition):
    for index in range(len(inputStringDistances)):
        inputStringIndex = inputStringDistances[index][0]
        if inputStrings[inputStringIndex][updatedPosition] == answer[updatedPosition]:
            # the updated position at answer has the same letter as the input string,
            # reduce Hamming distance of the input string by 1
            inputStringDistances[index][1] -= 1

    inputStringDistances.sort(key=lambda entry: entry[1], reverse=True)


def updateInputStringsDistances2(inputStringDistances, answer, inputStrings, updatedPosition):
    firstInputStringIndexDistanceUnchanged = None
    for index in range(len(inputStringDistances)):
        inputStringIndex = inputStringDistances[index][0]
        if inputStrings[inputStringIndex][updatedPosition] == answer[updatedPosition]:
            # the updated position at answer has the same letter as the input string,
            # reduce Hamming distance of the input string by 1
            inputStringDistances[index][1] -= 1
        else:
            if firstInputStringIndexDistanceUnchanged is None:
                # this is the first string for which the distance is changed:
                firstInputStringIndexDistanceUnchanged = index

    # check if we need to swap the every first entry with the first string updated
    if firstInputStringIndexDistanceUnchanged is not None and \
            inputStringDistances[0][1] < inputStringDistances[firstInputStringIndexDistanceUnchanged][1]:
        # swap this two entry
        temp = inputStringDistances[0]
        inputStringDistances[0] = inputStringDistances[firstInputStringIndexDistanceUnchanged]
        inputStringDistances[firstInputStringIndexDistanceUnchanged] = temp

def getMaxDistStr(strDistArray):
    maxDist=strDistArray[0][1]
    count = 0
    #print("strDistArray", strDistArray)
    for string, distance in strDistArray:
        if distance == maxDist:
            count += 1
    pick = random.randrange(count)
    return strDistArray[pick]

def findMaxLetters(maxDistanceInputString, scoreboard):
    maxLetters = []
    for position, letter, score in scoreboard:
        if maxDistanceInputString[position] == letter:
            maxLetters.append([position, letter, score])
    #print(maxLetters)
    try:
        maxDist = maxLetters[0][2]
    except IndexError as e:
        print(scoreboard)
        print(maxLetters)
    maxDistLetters = []
    for letter in maxLetters:
        if letter[2] == maxDist:
            maxDistLetters.append(letter)
    return random.choice(maxDistLetters)

def findClosestString(alphabet, inputStrings, maximumDistance):
    # all string are of same length
    stringLength = len(inputStrings[0])

    letterFreqTable = calculateLetterFreq(inputStrings, alphabet)

    # create initial answer with all SPACE
    answer = [" "] * stringLength
    undecidedPositions = set(range(stringLength))

    while len(undecidedPositions) > 0:
        # there is at least 1 undecided positions
        #print()
        #print("current undecided position:", len(undecidedPositions), undecidedPositions)

        scoreboard = calculateScoreboard(letterFreqTable, undecidedPositions)
        #print("current scoreboard:", scoreboard)

        # sort and find string with maximum distance to current answer
        inputStringDistances = calculateDistancesWithInputStrings(answer, inputStrings)

        # first string is the one with maximum distance to the answer
        maxDistanceInputStringIndex, maxDistance = getMaxDistStr(inputStringDistances)
        if maxDistance - len(undecidedPositions) > maximumDistance:
            answer = NOT_FOUND
            break
        maxDistanceInputString = inputStrings[maxDistanceInputStringIndex]
        #print("current string with maximum Distance: ", maxDistanceInputString, maxDistance)

        # find the 1st (position, letter) in scoreboard  that matches
        # maxDistanceInputString

        maxLetter = findMaxLetters(maxDistanceInputString, scoreboard)
        #print("maxLetter", maxLetter)# found, update the answer
        #print("found position %d, letter '%s'" % (position, letter))
        #maxLetter has [position, letter, score]
        answer[maxLetter[0]] = maxLetter[1]
        #print("answer = ", answer)

        # remove position from undecided positions
        undecidedPositions.remove(maxLetter[0])

    return answer


def findClosestStringOptimized(alphabet, inputStrings, maximumDistance):
    # all string are of same length
    stringLength = len(inputStrings[0])

    letterFreqTable = calculateLetterFreq(inputStrings, alphabet)

    # create initial answer with all SPACE
    answer = [" "] * stringLength
    undecidedPositions = set(range(stringLength))

    # sort and find string with maximum distance to current answer
    inputStringDistances = calculateDistancesWithInputStrings(answer,
                                                              inputStrings)

    while True:
        # there is at least 1 undecided positions
        #print()
        #print("current undecided position:", len(undecidedPositions), undecidedPositions)

        scoreboard = calculateScoreboard(letterFreqTable, undecidedPositions)
        #print("current scoreboard:", scoreboard)

        # first string is the one with maximum distance to the answer
        maxDistanceInputStringIndex, maxDistance = getMaxDistStr(inputStringDistances)
        maxDistanceInputString = inputStrings[maxDistanceInputStringIndex]
        #print("current string with maximum Distance: ", maxDistanceInputString, maxDistance)

        # find the 1st (position, letter) in scoreboard  that matches
        # maxDistanceInputString

        maxLetter = findMaxLetters(maxDistanceInputString, scoreboard)
        #print("maxLetter", maxLetter)# found, update the answer
        #print("found position %d, letter '%s'" % (position, letter))
        #maxLetter has [position, letter, score]
        answer[maxLetter[0]] = maxLetter[1]
        #print("answer = ", answer)

        # remove position from undecided positions
        undecidedPositions.remove(maxLetter[0])

        # update
        if len(undecidedPositions) > 0:
            updateInputStringsDistances(inputStringDistances, answer, inputStrings, maxLetter[0])
        else:
            # all position decided
            break

    return answer


def checkTestCase(numStrings, inputStrings, answer, alphabet, k):
    #for inputStringIndex in range(numStrings):
    #print("input_strings %2d: %s, distance to expected answer: %d" % (
    #inputStringIndex, inputStrings[inputStringIndex],
    #calculateDistance(answer, inputStrings[inputStringIndex])))

    letterFreqTable = calculateLetterFreq(inputStrings, alphabet)
    #print("letter frequency table:")
    #printLetterFreqTable(letterFreqTable)

    result = findClosestString(alphabet, inputStrings, k)
    #print("expected answer      : ", answer)
    #print("Found closest strings: ", result)
    #print("Distance between expected answer and result: ", calculateDistance(answer, result))

    #for inputStringIndex in range(numStrings):
    #print("input_strings %2d: %s, distance to result: %d" % (
    #inputStringIndex, inputStrings[inputStringIndex],
    #calculateDistance(result, inputStrings[inputStringIndex])))

    inputStringDistances = calculateDistancesWithInputStrings(result, inputStrings)
    #print("maxDistance to result, stringIndex %d, distance: %d" % inputStringDistances[0])

    if inputStringDistances[0][1] > k:
        #print("Algorithm Failed! Result has larger Hamming distance %d > %d" % (inputStringDistances[0][1], k))
        return False, result
    return True, result

def checkTestCaseOptimized(numStrings, inputStrings, answer, alphabet, k):
    #for inputStringIndex in range(numStrings):
        #print("input_strings %2d: %s, distance to expected answer: %d" % (
            #inputStringIndex, inputStrings[inputStringIndex],
            #calculateDistance(answer, inputStrings[inputStringIndex])))

    letterFreqTable = calculateLetterFreq(inputStrings, alphabet)
    #print("letter frequency table:")
    #printLetterFreqTable(letterFreqTable)

    result = findClosestStringOptimized(alphabet, inputStrings, k)
    #print("expected answer      : ", answer)
    #print("Found closest strings: ", result)
    #print("Distance between expected answer and result: ", calculateDistance(answer, result))

    #for inputStringIndex in range(numStrings):
        #print("input_strings %2d: %s, distance to result: %d" % (
            #inputStringIndex, inputStrings[inputStringIndex],
            #calculateDistance(result, inputStrings[inputStringIndex])))

    inputStringDistances = calculateDistancesWithInputStrings(result, inputStrings)
    #print("maxDistance to result, stringIndex %d, distance: %d" % inputStringDistances[0])

    if inputStringDistances[0][1] > k:
        #print("Algorithm Failed! Result has larger Hamming distance %d > %d" % (inputStringDistances[0][1], k))
        return False, result
    return True, result


class ClosestStringTestCase(object):
    def __init__(self, alphabet, numStrings, stringLength, maxDistance):
        self.alphabet = alphabet
        self.numStrings = numStrings
        self.stringLength = stringLength
        self.maxDistance = maxDistance

        # generate test case answer
        self.answer, self.inputStrings = createRandomTestCase(alphabet, numStrings, stringLength, maxDistance)

    def save(self, filename):
        pickle.dump(self, open(filename, "wb"))

    @staticmethod
    def load(filename):
        return pickle.load(open(filename, "rb"))

    def print(self):
        print("CloseStringTestCase:")
        print("    alphabet", self.alphabet)
        print("    numStrings", self.numStrings)
        print("    stringLength", self.stringLength)
        print("    maxDistance", self.maxDistance)
        print("    answer: ", self.answer)
        print("    inputStrings: ", self.inputStrings)


def CSd(S, d, s, deltaD):
    """
    :param S:   global variable, set of input strings
    :param d:   global variable, integer d
    :param s:   candidate string s
    :param deltaD:  integer detalD
    :return:    result string or NOT_FOUND
    """

    # print("CSd s: ", s, "deltaD: ", deltaD)
    # D0
    if deltaD < 0:
        # print("     D0: ", NOT_FOUND)
        return NOT_FOUND

    # D1
    for i in range(len(S)):
        if calculateDistance(s, S[i]) > d + deltaD:
            # print("     D1: ", NOT_FOUND)
            return NOT_FOUND
    # D2
    sWorks = True
    for i in range(len(S)):
        if calculateDistance(s, S[i]) > d:
            sWorks = False
    if sWorks:
        # print("     D2 found: ", s)
        return s

    # D3
    inputStringDistances = calculateDistancesWithInputStrings(s, S)
    # find all stringIndex that Dh(s, si) > d:
    allSiIndex = []
    for stringIndex, distance in inputStringDistances:
        if distance > d:
            allSiIndex.append(stringIndex)

    # randomly pick some i from allSiIndex
    i = random.choice(allSiIndex)
    si = S[i]
    # print("     D3 si: ", si)

    # find P
    P = []
    for p in range(len(s)):
        if s[p] != si[p]:
            P.append(p)
    # print("     D3 P: ", P)

    # randomly choose d+1 from P
    PPrime = random.sample(P, d+1)
    # print("     D3 P': ", PPrime)

    for p in PPrime:
        sPrime = s.copy()
        sPrime[p] = si[p]
        sRet = CSd(S, d, sPrime, deltaD-1)
        if sRet != NOT_FOUND:
            # print("     D3 found: ", sRet)
            return sRet
    # print("      not found: ")
    return NOT_FOUND


def create_working_testcases(alphabet, numStrings, stringLength, k, count):
    testcases = []
    while len(testcases) < count:
        #print("create_working_testcases: ", len(testcases))
        testcase = ClosestStringTestCase(alphabet, numStrings, stringLength, k)
        testcases.append(testcase)

    return testcases


def save_testcases_to_file(testcases, filename):
    pickle.dump(testcases, open(filename, "wb"))


def load_testcases_from_file(filename):
    return pickle.load(open(filename, "rb"))

def totalHammingDistance(stringParts, answerString):
    totalDist = 0
    #print("stringParts", stringParts)
    #print("answerString", answerString)
    for string in stringParts:
        print("string, answerString:", string, answerString)
        for i in range(len(string)):
            if string[i] != answerString[i]:
                print("i:", i)
                totalDist += 1
                print(string[i], answerString[i], totalDist)
    #print("totalDist", totalDist)
    return totalDist

def compare_algorithms(testcases):
    CSAnswerDists = []
    CSResultDists = []

    FPAnswerDists = []
    FPResultDists = []

    numCases = 0
    numCasesFailed = 0
    numCasesSaved = 0

    caseSolution = []

    closestStringAlgoStartTime = timeit.default_timer()
    closestStringAlgoSuccessCount = 0
    for testcase in testcases:
        caseResult, caseSolution = checkTestCaseOptimized(len(testcase.inputStrings),
                                            testcase.inputStrings,
                                            testcase.answer,
                                            testcase.alphabet,
                                            testcase.maxDistance)
        # print("done")
        numCases += 1
        if caseResult is False:
            numCasesFailed += 1

        timesToTryAgain = 0
        caseSaveTimeStart = timeit.default_timer()
        while caseResult is False:
            caseSaveTimeStop = timeit.default_timer()
            if (caseSaveTimeStop-caseSaveTimeStart) > 0.01:
                break
            random.shuffle(testcase.inputStrings)
            caseResult, caseSolution = checkTestCaseOptimized(len(testcase.inputStrings),
                                                testcase.inputStrings,
                                                testcase.answer,
                                                testcase.alphabet,
                                                testcase.maxDistance)
            if caseResult:
                # print("Failed before, now works! Hurray! ")
                numCasesSaved += 1
                break
            timesToTryAgain += 1
        answerDist = totalHammingDistance(testcase.inputStrings,
                                              testcase.answer)
        resultDist = totalHammingDistance(testcase.inputStrings, caseSolution)
        CSAnswerDists.append(answerDist)
        CSResultDists.append(resultDist)
    closestStringAlgoEndTime = timeit.default_timer()

    fixedParameterAlgoStartTime = timeit.default_timer()
    fixedParameterAlgoSuccessCount = 0
    numCases = 0
    for testcase in testcases:
        numCases += 1
        #print("Csd: ", numCases)
        fixedParameterAlgoResult = CSd(testcase.inputStrings,
                                       testcase.maxDistance,
                                       testcase.inputStrings[0],
                                       testcase.maxDistance)
        if fixedParameterAlgoResult != NOT_FOUND:
            fixedParameterAlgoSuccessCount += 1
        answerDist = totalHammingDistance(testcase.inputStrings,
                                          testcase.answer)
        resultDist = totalHammingDistance(testcase.inputStrings,
                                          fixedParameterAlgoResult)
        FPAnswerDists.append(answerDist)
        FPResultDists.append(resultDist)
        #print(fixedParameterAlgoSuccessCount)
    fixedParameterAlgoEndTime = timeit.default_timer()
    print("CSAnswerDists:", CSAnswerDists)
    print("CSResultDists:", CSResultDists)
    print("Closest String Algorithm Execute Time (%d tests)" % len(testcases),
          closestStringAlgoEndTime - closestStringAlgoStartTime)
    print("Out of", len(testcases), "test cases", numCasesFailed, "cases failed.")
    print("Saved cases: ", numCasesSaved)
    print("-----")
    print("FPAnswerDists:", FPAnswerDists)
    print("FPResultDists:", FPResultDists)
    print("Fixed Parameter Algorithm Execute Time (%d tests)" % len(testcases),
          fixedParameterAlgoEndTime - fixedParameterAlgoStartTime)

    return CSAnswerDists, CSResultDists, FPAnswerDists, FPResultDists

def compare_closest_algorithms(testcases):
    CSAnswerDists = []
    CSResultDists = []

    FPAnswerDists = []
    FPResultDists = []
    numCases = 0
    numCasesFailed = 0
    numCasesSaved = 0

    closestStringAlgoStartTime = timeit.default_timer()
    closestStringAlgoSuccessCount = 0
    for testcase in testcases:
        caseResult, caseString = checkTestCase(len(testcase.inputStrings),
                                   testcase.inputStrings,
                                   testcase.answer,
                                   testcase.alphabet,
                                   testcase.maxDistance)
        # print("done")
        numCases += 1
        #print("ClosestString: ", numCases)
        if caseResult is False:
            numCasesFailed += 1

        timesToTryAgain = 0
        while caseResult is False and timesToTryAgain <= 10:
            random.shuffle(testcase.inputStrings)
            caseResult, caseString = checkTestCase(len(testcase.inputStrings),
                                       testcase.inputStrings,
                                       testcase.answer,
                                       testcase.alphabet,
                                       testcase.maxDistance)
            if caseResult:
                # print("Failed before, now works! Hurray! ")
                numCasesSaved += 1
                break
            timesToTryAgain += 1
        answerDist = totalHammingDistance(testcase.inputStrings,
                                          testcase.answer)
        resultDist = totalHammingDistance(testcase.inputStrings, caseString)
        CSAnswerDists.append(answerDist)
        CSResultDists.append(resultDist)
    closestStringAlgoEndTime = timeit.default_timer()

    CSAnswerDists2 = []
    CSResultDists2 = []
    numCases2 = 0
    numCasesFailed2 = 0
    numCasesSaved2 = 0
    closestStringAlgoStartTime2 = timeit.default_timer()
    closestStringAlgoSuccessCount2 = 0
    for testcase in testcases:
        caseResult, caseString = checkTestCaseOptimized(len(testcase.inputStrings),
                                   testcase.inputStrings,
                                   testcase.answer,
                                   testcase.alphabet,
                                   testcase.maxDistance)
        # print("done")
        numCases2 += 1
        #print("ClosestStringOptimized: ", numCases2)
        if caseResult is False:
            numCasesFailed2 += 1

        timesToTryAgain = 0
        while caseResult is False and timesToTryAgain <= 10:
            random.shuffle(testcase.inputStrings)
            caseResult, caseString = checkTestCaseOptimized(len(testcase.inputStrings),
                                                testcase.inputStrings,
                                                testcase.answer,
                                                testcase.alphabet,
                                                testcase.maxDistance)
            if caseResult:
                # print("Failed before, now works! Hurray! ")
                numCasesSaved2 += 1
                break
            timesToTryAgain += 1
        answerDist2 = totalHammingDistance(testcase.inputStrings, testcase.answer)
        resultDist2 = totalHammingDistance(testcase.inputStrings, caseString)
        CSAnswerDists2.append(answerDist2)
        CSResultDists2.append(resultDist2)
    closestStringAlgoEndTime2 = timeit.default_timer()

    print("Closest String Algorithm Execute Time (%d tests)" % len(testcases),
          closestStringAlgoEndTime - closestStringAlgoStartTime)
    print("Out of", len(testcases), "test cases", numCasesFailed, "cases failed.")
    print("Saved cases: ", numCasesSaved)
    print("-----")

    print("Closest String Algorithm Optimized Execute Time (%d tests)" % len(testcases),
          closestStringAlgoEndTime2 - closestStringAlgoStartTime2)
    print("Out of", len(testcases), "test cases", numCasesFailed2, "cases failed.")
    print("Saved cases: ", numCasesSaved2)

    return CSAnswerDists, CSResultDists, CSAnswerDists2, CSResultDists2


def generate_comparison_data(filename):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
    totalCases = 10000
    numStringsList = [10, 20, 40, 80]
    numStringsList = [10]
    hammingDistList = [5, 10, 20, 40, 80]
    hammingDistList = [10]
    stringLengthList = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
    stringLengthList = [20]

    allResults = []
    for numStrings in numStringsList:
        for ham in hammingDistList:
            for s in stringLengthList:
                if ham >= s:
                    continue

                testCases = create_working_testcases(alphabet, numStrings, s, ham, totalCases)
                numCases = 0
                numCasesFailed = 0
                numCasesSaved = 0

                CSAnswerDists = []
                CSResultDists = []
                closestStringAlgoStartTime = timeit.default_timer()
                while numCases < totalCases:
                    testCase = testCases[numCases]
                    caseResult, caseString = checkTestCaseOptimized(testCase.numStrings, testCase.inputStrings, testCase.answer, testCase.alphabet, testCase.maxDistance)
                    timesToTryAgain = 0
                    while caseResult is False and timesToTryAgain < 199:
                        if timesToTryAgain == 0:
                            numCasesFailed += 1
                        random.shuffle(testCase.inputStrings)
                        caseResult, caseString = checkTestCaseOptimized(testCase.numStrings, testCase.inputStrings, testCase.answer, testCase.alphabet, testCase.maxDistance)

                        if caseResult == True:
                            #print("Failed before, now works! Hurray! ")
                            numCasesSaved += 1
                            break
                        timesToTryAgain += 1
                    numCases += 1
                    answerDist = totalHammingDistance(testCase.inputStrings,
                                                      testCase.answer)
                    resultDist = totalHammingDistance(testCase.inputStrings,
                                                      caseString)
                    CSAnswerDists.append(answerDist)
                    CSResultDists.append(resultDist)
                closestStringAlgoEndTime = timeit.default_timer()

                CSAnswerDistSum = 0
                CSResultDistSum = 0
                for i in range (len(CSAnswerDists)):
                    CSAnswerDistSum += CSAnswerDists[i]
                    CSResultDistSum += CSResultDists[i]

                result = dict()
                result["Algorithm"] = "WFC-CSP"
                result["Alphabet Size"] = len(alphabet)
                result["k"] = numStrings
                result["d"] = ham
                result["L"] = s
                result["Time"] = (closestStringAlgoEndTime - closestStringAlgoStartTime) / totalCases
                result["Total"] = totalCases
                result["Failed"] = numCasesFailed
                result["Saved"] = numCasesSaved
                result["Average Answer Distance"] = CSAnswerDistSum / (totalCases * testCase.maxDistance * testCase.numStrings)
                result["Average Result Distance"] = CSResultDistSum / (totalCases * testCase.maxDistance * testCase.numStrings)
                print(result)
                allResults.append(result)
                print("Closest String Algorithm Execute Time (%d tests)" % totalCases, closestStringAlgoEndTime - closestStringAlgoStartTime)
                print("numStrings=%d Hamming Distance=%d StringLength=%d: failed %d, saved %d" % (numStrings, ham, s, numCasesFailed, numCasesSaved))
                """

                if ham > 10:
                    # skip CSD algorithm if hamming distance > 15
                    continue
                if ham == 10 and s > 80:
                    continue

                fixedParameterAlgoStartTime = timeit.default_timer()
                fixedParameterAlgoSuccessCount = 0
                numCases = 0
                for testcase in testCases:
                    numCases += 1
                    # print("Csd: ", numCases)
                    fixedParameterAlgoResult = CSd(testcase.inputStrings,
                                                   testcase.maxDistance,
                                                   testcase.inputStrings[0],
                                                   testcase.maxDistance)
                    if fixedParameterAlgoResult != NOT_FOUND:
                        fixedParameterAlgoSuccessCount += 1
                    # print(fixedParameterAlgoSuccessCount)
                fixedParameterAlgoEndTime = timeit.default_timer()
                result = dict()
                result["Algorithm"] = "FP"
                result["k"] = numStrings
                result["d"] = ham
                result["L"] = s
                result["Time"] = (fixedParameterAlgoEndTime - fixedParameterAlgoStartTime) / totalCases
                result["Total"] = totalCases
                result["Failed"] = totalCases - fixedParameterAlgoSuccessCount
                result["Saved"] = 0
                print(result)
                print()
                allResults.append(result)
                """

                df = pd.DataFrame(allResults, columns=["Algorithm", "Alphabet Size", "k", "d", "L", "Time", "Total", "Failed", "Saved"])
                df.to_excel(filename, index=False)


def plot_figures(filename):
    df = pd.read_excel(filename, index_col=None)
    # convert time from seconds to millisecons
    df["Time"] = df["Time"] * 1000.0

    totalCases = 1000
    numStringsList = [10, 20, 40, 80]
    hammingDistList = [5, 10, 20, 40, 80]
    stringLengthList = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]

    # different line style for different number of strings
    plot_line_style = {
        10: "-",
        20: "--",
        40: "-.",
        80: ":"
    }

    # different plot marker for different hamming distance
    plot_marker = {
        5: "*",
        10: "+",
        20: "x",
        40: "o",
        80: "s",
    }

    plt.figure(figsize=(11.0, 8.5))
    plt.xlabel("String Length")
    plt.xticks(stringLengthList)
    plt.ylabel("Processing Time (milliseconds)")
    title = "Processing Time vs String Length (Alphabet Size 8)"
    # plt.title(title)

    for numStrings in numStringsList:
        for ham in hammingDistList:
            data = df[((df["Algorithm"] == "WFC-CSP") & (df["k"] == numStrings) & (df["d"] == ham))]
            xAxis = data["L"].tolist()
            yAxis = data["Time"].tolist()
            label = "k=%d d=%d " % (numStrings, ham)
            plt.plot(xAxis, yAxis, label=label, linestyle=plot_line_style[numStrings], marker=plot_marker[ham])

    plt.grid(linestyle=":")
    plt.legend()
    plt.savefig("%s.png" % title, dpi=300)
    """
    plt.figure(figsize=(11.0, 8.5))
    plt.xlabel("Hamming Distance")
    plt.xticks(hammingDistList)
    plt.ylabel("Processing Time (milliseconds)")
    title = "Processing Time vs Hamming Distance"
    # plt.title(title)
    for numStrings in numStringsList:
        for stringLength in stringLengthList:
            data = df[((df["Algorithm"] == "WFC-CSP") & (df["k"] == numStrings) & (df["L"] == stringLength))]
            xAxis = data["d"].tolist()
            yAxis = data["Time"].tolist()
            label = "k=%d L=%d " % (numStrings, stringLength)
            plt.plot(xAxis, yAxis, label=label, linestyle=plot_line_style[numStrings], marker=plot_marker[ham])

    plt.grid(linestyle=":")
    plt.legend()
    plt.savefig("%s.png" % title, dpi=300)
    plt.show()

    # compare WFC-CSP vs CSD
    plt.figure(figsize=(11.0, 8.5))
    plt.xlabel("String Length")
    plt.xticks(stringLengthList)
    plt.ylabel("Processing Time (milliseconds)")
    title = "WFC-CSP vs CSD"
    # plt.title(title)

    for numStrings in numStringsList:
        for ham in [5, 10]:
            data = df[((df["Algorithm"] == "WFC-CSP") & (df["k"] == numStrings) & (df["d"] == ham) & (df["L"] < 100))]
            xAxis = data["L"].tolist()
            yAxis = data["Time"].tolist()
            label = "k=%d d=%d WFC-CSP" % (numStrings, ham)
            plt.plot(xAxis, yAxis, label=label, color="red", linestyle=plot_line_style[numStrings], marker=plot_marker[ham])

    for numStrings in numStringsList:
        for ham in [5, 10]:
            data = df[((df["Algorithm"] == "FP") & (df["k"] == numStrings) & (df["d"] == ham) & (df["L"] < 100))]
            xAxis = data["L"].tolist()
            yAxis = data["Time"].tolist()
            label = "k=%d d=%d FP" % (numStrings, ham)
            plt.plot(xAxis, yAxis, label=label, color="blue", linestyle=plot_line_style[numStrings], marker=plot_marker[ham])

    plt.grid(linestyle=":")
    plt.legend()
    plt.savefig("%s.png" % title, dpi=300)
    plt.show()
    """

def main_comaprison_plot():
    alphabet = ["a", "c", "g", "t"]
    numStrings = 10
    totalCases = 1000

    numStringsList = [10, 20, 40, 80]

    answers = []
    inputStrings = []
    hammingDistList = [10, 20, 40, 80]
    stringLengthList = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]

    # different line style for different number of strings
    plot_line_style = {
        10: "-",
        20: "--",
        40: "-.",
        80: ":"
    }

    # different plot marker for different hamming distance
    plot_marker = {
        10: "+",
        20: "x",
        40: "o",
        80: "s",
    }

    plt.figure(figsize=(11.0, 8.5))
    plt.xlabel("String Length")
    plt.xticks(stringLengthList)
    plt.ylabel("Processing Time (seconds)")
    title="Processing Time vs String Length (K=%d, Alphabet Size=%d)" % (numStrings, len(alphabet))
    plt.title(title)

    for numStrings in numStringsList:
        for ham in hammingDistList:
            grandList = []
            for s in stringLengthList:
                if ham >= s:
                    continue

                testCases = create_working_testcases(alphabet, numStrings, s, ham, totalCases)
                #(alphabet, numStrings, stringLength, k, testcaseCount)
                numCases = 0
                numCasesFailed = 0
                numCasesSaved = 0
                closestStringAlgoStartTime = timeit.default_timer()
                while numCases < totalCases:
                    testCase = testCases[numCases]
                    #(numStrings, inputStrings[numCases], answers[numCases],
                                                   #alphabet, k)
                    caseResult = checkTestCaseOptimized(testCase.numStrings, testCase.inputStrings, testCase.answer, testCase.alphabet, testCase.maxDistance)
                    #print("done")
                    timesToTryAgain = 0
                    #while caseResult == False and timesToTryAgain <= math.factorial(stringLength):
                    while caseResult is False and timesToTryAgain <= 1:
                        if timesToTryAgain == 0:
                            numCasesFailed += 1
                        random.shuffle(inputStrings)
                        caseResult = checkTestCaseOptimized(testCase.numStrings, testCase.inputStrings, testCase.answer, testCase.alphabet, testCase.maxDistance)

                        if caseResult == True:
                            #print("Failed before, now works! Hurray! ")
                            numCasesSaved += 1
                            break
                        timesToTryAgain += 1
                    numCases += 1
                closestStringAlgoEndTime = timeit.default_timer()
                smallList = [ham, s, closestStringAlgoEndTime-closestStringAlgoStartTime]
                print(smallList)
                grandList.append(smallList)
                print("Closest String Algorithm Execute Time (%d tests)" % totalCases, closestStringAlgoEndTime - closestStringAlgoStartTime)
                print("numStrings=%d Hamming Distance=%d StringLength=%d: failed %d, saved %d" % ( numStrings, ham, s, numCasesFailed, numCasesSaved))
                print()
            print(grandList)
            xAxis = [row[1] for row in grandList]
            yAxis = [row[2]/totalCases for row in grandList]
            label = "%d strings, Hamming distance %d " % (numStrings, ham)
            plt.plot(xAxis, yAxis, label=label, linestyle=plot_line_style[numStrings], marker=plot_marker[ham])

    plt.legend()
    plt.savefig("%s.png" % title, dpi=300)
    plt.show()


def main():
    alphabet = ["a", "c", "g", "t"]
    numStrings = 10
    stringLength = 20
    k = 8   # maximum Hamming distance

    testcaseCount = 100
    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate":
            assert len(sys.argv) == 3, "Need filename to save generated testcases"
            filename = sys.argv[2]
            testcases = create_working_testcases(alphabet, numStrings, stringLength, k, testcaseCount)
            save_testcases_to_file(testcases, filename)

        elif sys.argv[1] == "--load":
            assert len(sys.argv) == 3, "Need filename to load generated testcases"
            filename = sys.argv[2]
            testcases = load_testcases_from_file(filename)
            for testcase in testcases:
                testcase.print()

        elif sys.argv[1] == "--compare":
            assert len(sys.argv) == 3, "Need filename to load generated testcases"
            filename = sys.argv[2]
            testcases = load_testcases_from_file(filename)
            CSAnswerDists, CSResultDists, FPAnswerDists, FPResultDists = compare_algorithms(testcases)
        elif sys.argv[1] == "--compare-closest-string":
            assert len(
                sys.argv) == 3, "Need filename to load generated testcases"
            filename = sys.argv[2]
            testcases = load_testcases_from_file(filename)
            compare_closest_algorithms(testcases)
        elif sys.argv[1] == "--generate-comparison-data":
            assert len(
                sys.argv) == 3, "Need filename (.xlsx) to load generated testcases"
            filename = sys.argv[2]
            generate_comparison_data(filename)
        elif sys.argv[1] == "--plot":
            assert len(
                sys.argv) == 3, "Need filename (.xlsx) to load generated testcases"
            filename = sys.argv[2]
            plot_figures(filename)
    else:
        main_comaprison_plot()


if __name__ == "__main__":
    main()