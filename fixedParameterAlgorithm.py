import random
import pickle
import sys
import timeit

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
        # print()
        # print("current undecided position:", len(undecidedPositions), undecidedPositions)

        scoreboard = calculateScoreboard(letterFreqTable, undecidedPositions)
        # print("current scoreboard:", scoreboard)

        # sort and find string with maximum distance to current answer
        inputStringDistances = calculateDistancesWithInputStrings(answer, inputStrings)

        # first string is the one with maximum distance to the answer
        maxDistanceInputStringIndex, maxDistance = inputStringDistances[0]
        maxDistanceInputString = inputStrings[maxDistanceInputStringIndex]
        # print("current string with maximum Distance: ", maxDistanceInputStringIndex, maxDistanceInputString, maxDistance)

        # find the 1st (position, letter) in scoreboard  that matches
        # maxDistanceInputString
        for position, letter, score in scoreboard:
            if maxDistanceInputString[position] == letter:
                # found, update the answer
                # print("found position %d, letter '%s'" % (position, letter))
                answer[position] = letter
                # print("answer = ", answer)

                # remove position from undecided positions
                undecidedPositions.remove(position)
                break

    return answer


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


def main():
    alphabet = ["a", "c", "g", "t"]
    numStrings = 100
    stringLength = 20
    k = 4   # maximum Hamming distance

    testcases = []
    # create test case object
    testcase1 = ClosestStringTestCase(alphabet, numStrings, stringLength, k)
    testcase1.print()
    testcases.append(testcase1)

    testcase2 = ClosestStringTestCase(alphabet, numStrings, stringLength, k)
    testcase2.print()
    testcases.append(testcase2)

    filename = "testcases.pickle"
    pickle.dump(testcases, open(filename, "wb"))
    testcases2 = pickle.load(open(filename, "rb"))
    testcase3, testcase4 = testcases2

    testcase3.print()
    testcase4.print()

    testcase = testcase4

    for inputStringIndex in range(numStrings):
        print("input_strings %2d: %s, distance to expected answer: %d" % (
            inputStringIndex, testcase.inputStrings[inputStringIndex],
            calculateDistance(testcase.answer, testcase.inputStrings[inputStringIndex])))

    letterFreqTable = calculateLetterFreq(testcase.inputStrings, alphabet)
    print("letter frequency table:")
    printLetterFreqTable(letterFreqTable)

    s = testcase.inputStrings[0]    # start with the first s in S
    fixedParameterAlgoResult = CSd(testcase.inputStrings, k, s, k)
    print("expected answer      : ", testcase.answer)
    if fixedParameterAlgoResult == "not found":
        print("CSd failed find a closed string: ")
    else:
        print("CSd Found closest strings: ", fixedParameterAlgoResult)
        print("Distance between expected answer and result: ", calculateDistance(testcase.answer, fixedParameterAlgoResult))
    return 0

    result = findClosestString(alphabet, testcase.inputStrings, k)
    print("expected answer      : ", testcase.answer)
    print("Found closest strings: ", result)
    print("Distance between expected answer and result: ", calculateDistance(testcase.answer, result))

    for inputStringIndex in range(numStrings):
        print("input_strings %2d: %s, distance to result: %d" % (
            inputStringIndex, testcase.inputStrings[inputStringIndex],
            calculateDistance(result, testcase.inputStrings[inputStringIndex])))

    inputStringDistances = calculateDistancesWithInputStrings(result, testcase.inputStrings)
    print("maxDistance to result, stringIndex %d, distance: %d" % inputStringDistances[0])

    if inputStringDistances[0][1] > k:
        print("Algorithm Failed! Result has larger Hamming distance %d > %d", inputStringDistances[0][1], k)


def create_working_testcases(alphabet, numStrings, stringLength, k, count):
    testcases = []
    while len(testcases) < count:
        print("create_working_testcases: ", len(testcases))
        testcase = ClosestStringTestCase(alphabet, numStrings, stringLength, k)

        result = findClosestString(alphabet, testcase.inputStrings, k)
        inputStringDistances = calculateDistancesWithInputStrings(result, testcase.inputStrings)
        # print("maxDistance to result, stringIndex %d, distance: %d" % inputStringDistances[0])
        if inputStringDistances[0][1] > k:
            print(
                "Algorithm Failed! Result has larger Hamming distance %d > %d",
                inputStringDistances[0][1], k)
        else:
            # found a good test case
            testcases.append(testcase)

    return testcases


def save_testcases_to_file(testcases, filename):
    pickle.dump(testcases, open(filename, "wb"))


def load_testcases_from_file(filename):
    return pickle.load(open(filename, "rb"))


def compare_algorithms(testcases):

    closestStringAlgoStartTime = timeit.default_timer()
    closestStringAlgoSuccessCount = 0
    for testcase in testcases:
        result = findClosestString(testcase.alphabet,
                                   testcase.inputStrings,
                                   testcase.maxDistance)
        if result != NOT_FOUND: # just for comparison
            closestStringAlgoSuccessCount += 1
        print(closestStringAlgoSuccessCount)
    closestStringAlgoEndTime = timeit.default_timer()
    print("Closest String Algorithm Execute Time (%d tests)" % len(testcases),
          closestStringAlgoEndTime - closestStringAlgoStartTime)
    print("Success count-", closestStringAlgoSuccessCount)

    fixedParameterAlgoStartTime = timeit.default_timer()
    fixedParameterAlgoSuccessCount = 0
    for testcase in testcases:
        fixedParameterAlgoResult = CSd(testcase.inputStrings,
                                       testcase.maxDistance,
                                       testcase.inputStrings[0],
                                       testcase.maxDistance)
        if fixedParameterAlgoResult != NOT_FOUND:
            fixedParameterAlgoSuccessCount += 1
        print(fixedParameterAlgoSuccessCount)
    fixedParameterAlgoEndTime = timeit.default_timer()
    print("Fixed Parameter Algorithm Execute Time (%d tests)" % len(testcases),
          fixedParameterAlgoEndTime - fixedParameterAlgoStartTime)
    print("Success count-", fixedParameterAlgoSuccessCount)

def main_default():
    alphabet = ["a", "c", "g", "t"]
    numStrings = 100
    stringLength = 20
    k = 4   # maximum Hamming distance

    testcases = []
    # create test case object
    testcase1 = ClosestStringTestCase(alphabet, numStrings, stringLength, k)
    testcase1.print()
    testcases.append(testcase1)

    testcase2 = ClosestStringTestCase(alphabet, numStrings, stringLength, k)
    testcase2.print()
    testcases.append(testcase2)

    filename = "testcases.pickle"
    pickle.dump(testcases, open(filename, "wb"))
    testcases2 = pickle.load(open(filename, "rb"))
    testcase3, testcase4 = testcases2

    testcase3.print()
    testcase4.print()

    testcase = testcase4

    for inputStringIndex in range(numStrings):
        print("input_strings %2d: %s, distance to expected answer: %d" % (
            inputStringIndex, testcase.inputStrings[inputStringIndex],
            calculateDistance(testcase.answer, testcase.inputStrings[inputStringIndex])))

    letterFreqTable = calculateLetterFreq(testcase.inputStrings, alphabet)
    print("letter frequency table:")
    printLetterFreqTable(letterFreqTable)

    s = testcase.inputStrings[0]    # start with the first s in S
    fixedParameterAlgoResult = CSd(testcase.inputStrings, k, s, k)
    print("expected answer      : ", testcase.answer)
    if fixedParameterAlgoResult == "not found":
        print("CSd failed find a closed string: ")
    else:
        print("CSd Found closest strings: ", fixedParameterAlgoResult)
        print("Distance between expected answer and result: ", calculateDistance(testcase.answer, fixedParameterAlgoResult))
    return 0

    result = findClosestString(alphabet, testcase.inputStrings, k)
    print("expected answer      : ", testcase.answer)
    print("Found closest strings: ", result)
    print("Distance between expected answer and result: ", calculateDistance(testcase.answer, result))

    for inputStringIndex in range(numStrings):
        print("input_strings %2d: %s, distance to result: %d" % (
            inputStringIndex, testcase.inputStrings[inputStringIndex],
            calculateDistance(result, testcase.inputStrings[inputStringIndex])))

    inputStringDistances = calculateDistancesWithInputStrings(result, testcase.inputStrings)
    print("maxDistance to result, stringIndex %d, distance: %d" % inputStringDistances[0])

    if inputStringDistances[0][1] > k:
        print("Algorithm Failed! Result has larger Hamming distance %d > %d", inputStringDistances[0][1], k)


def main():
    alphabet = ["a", "c", "g", "t"]
    numStrings = 10
    stringLength = 100
    k = 16   # maximum Hamming distance

    testcaseCount = 1000

    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate":
            assert len(sys.argv) == 3, "Need filename to save generated testcases"
            filename = sys.argv[2]
            testcases = create_working_testcases(alphabet, numStrings, stringLength, k, testcaseCount)
            for testcase in testcases:
                testcase.print()

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
            compare_algorithms(testcases[0:1000])
    else:
        main_default()


if __name__ == "__main__":
    main()