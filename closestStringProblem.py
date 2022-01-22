import os
import random
import pickle
import sys
import timeit
import matplotlib.pyplot as plt
import pandas as pd

NOT_FOUND = "not found"
ALPHABET_4 = ["a", "b", "c", "d"]
ALPHABET_20 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
TEST_CONFIGURATION = {
    # alphabet
    #'alphabet': ALPHABET_20,
    'alphabet': ALPHABET_4,

    # number of strings
    'K': [10, 20, 40],

    # hamming distance
    'd': [5, 10, 20, 40, 60, 80],

    # string length
    'L': [10, 15, 20, 30, 40, 60, 80, 120, 160, 180, 240, 320],

    # number of test cases in each configuration
    'totalCases': 1000,

    # maxTries
    'maxTries': 1000
}


def skipTest(alphabet, K, d, L):
    if len(alphabet) == 20 and K > 20:
        return True

    if d/L > 1/2:
        return True

    if d == 5 and L > 120:
        return True

    if d == 10 and L > 120:
        return True

    if d == 20 and L > 180:
        return True

    return False


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



def calculateLetterFreq(inputStrings, alphabet):
    """
    :param inputStrings:  list of input strings, all strings ar of  the same length
    :param alphabet: alphabet used to create the input strings
    """

    # find string length from the first string
    stringLength = len(inputStrings[0])

    # letter frequency table is a 2-D array implemented as list of list
    letterFreqTable = {}
    letterPositionTable = {}
    for position in range(stringLength):
        # create frequency for all alphabet letter at this position
        alphabetFreqTable = {}
        alphabetIndexTable = {}
        for alphabetLetter in alphabet:
            alphabetFreqTable[alphabetLetter] = 0
            alphabetIndexTable[alphabetLetter] = []
            for index in range(len(inputStrings)):
                if inputStrings[index][position] == alphabetLetter:
                    alphabetFreqTable[alphabetLetter] += 1
                    alphabetIndexTable[alphabetLetter].append(index)
        letterFreqTable[position] = alphabetFreqTable
        letterPositionTable[position] = alphabetIndexTable
    return letterFreqTable, letterPositionTable


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


def getMaxDistStr(strDistArray):
    maxDist = strDistArray[0][1]
    count = 0
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

    letterFreqTable, letterPositionTable = calculateLetterFreq(inputStrings, alphabet)

    # create initial answer with all SPACE
    answer = [" "] * stringLength
    undecidedPositions = set(range(stringLength))

    # sort and find string with maximum distance to current answer
    inputStringDistances = calculateDistancesWithInputStrings(answer,
                                                              inputStrings)

    while True:
        # there is at least 1 undecided positions
        scoreboard = calculateScoreboard(letterFreqTable, undecidedPositions)

        # first string is the one with maximum distance to the answer
        maxDistanceInputStringIndex, maxDistance = getMaxDistStr(inputStringDistances)
        maxDistanceInputString = inputStrings[maxDistanceInputStringIndex]
        #print("current string with maximum Distance: ", maxDistanceInputString, maxDistance)

        # find the 1st (position, letter) in scoreboard  that matches
        # maxDistanceInputString

        maxLetter = findMaxLetters(maxDistanceInputString, scoreboard)
        answer[maxLetter[0]] = maxLetter[1]

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

    letterFreqTable, letterPositionTable = calculateLetterFreq(inputStrings, alphabet)

    result = findClosestString(alphabet, inputStrings, k)

    inputStringDistances = calculateDistancesWithInputStrings(result, inputStrings)

    if inputStringDistances[0][1] > k:
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

    def save_to_ant_instance_file(self, filename):
        f = open(filename, "w")

        # Alphabet size
        print(len(self.alphabet), file=f)

        # number of strings
        print(self.numStrings, file=f)

        # string length
        print(self.stringLength, file=f)

        # alphabet
        print(" ".join(self.alphabet), file=f)

        for s in self.inputStrings:
            print("".join(s), file=f)

        f.close()


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
        testcase = ClosestStringTestCase(alphabet, numStrings, stringLength, k)
        testcases.append(testcase)

    return testcases


def save_testcases_to_file(testcases, filename):
    pickle.dump(testcases, open(filename, "wb"))


def save_testcases_to_ant_instance_files(testcases, filename):
    for i in range(len(testcases)):
        testcases[i].save_to_ant_instance_file("%s_%d" % (filename, i))


def load_testcases_from_file(filename):
    return pickle.load(open(filename, "rb"))


def getHammingDistanceMaxAndAvg(stringParts, answerString):
    maxDist = 0
    totalDist = 0
    for string in stringParts:
        dist = calculateDistance(string, answerString)
        if dist > maxDist:
            maxDist = dist
        totalDist += dist
    averageDist = totalDist / len(stringParts)
    return maxDist, averageDist


def compare_algorithms(testcases):
    closestStringAnswerDists = []
    closestStringSolutionDists = []

    fixedParameterAnswerDists = []
    fixedParameterSolutionDists = []

    numCases = 0
    numCasesFailed = 0
    numCasesSaved = 0

    testCaseSolution = []

    closestStringAlgoStartTime = timeit.default_timer()
    closestStringAlgoSuccessCount = 0
    for testcase in testcases:
        testCaseResult, testCaseSolution = checkTestCase(len(testcase.inputStrings),
                                            testcase.inputStrings,
                                            testcase.answer,
                                            testcase.alphabet,
                                            testcase.maxDistance)
        numCases += 1
        if testCaseResult is False:
            numCasesFailed += 1

        timesToTryAgain = 0
        caseSaveTimeStart = timeit.default_timer()
        while testCaseResult is False:
            caseSaveTimeStop = timeit.default_timer()
            if (caseSaveTimeStop-caseSaveTimeStart) > 0.01:
                break
            random.shuffle(testcase.inputStrings)
            testCaseResult, testCaseSolution = checkTestCase(len(testcase.inputStrings),
                                                testcase.inputStrings,
                                                testcase.answer,
                                                testcase.alphabet,
                                                testcase.maxDistance)
            if testCaseResult:
                numCasesSaved += 1
                break
            timesToTryAgain += 1
    closestStringAlgoEndTime = timeit.default_timer()

    fixedParameterAlgoStartTime = timeit.default_timer()
    fixedParameterAlgoSuccessCount = 0
    numCases = 0
    for testcase in testcases:
        numCases += 1
        fixedParameterAlgoSolution = CSd(testcase.inputStrings,
                                       testcase.maxDistance,
                                       testcase.inputStrings[0],
                                       testcase.maxDistance)
        if fixedParameterAlgoSolution != NOT_FOUND:
            fixedParameterAlgoSuccessCount += 1
    fixedParameterAlgoEndTime = timeit.default_timer()
    print("closestStringAnswerDists:", closestStringAnswerDists)
    print("closestStringSolutionDists:", closestStringSolutionDists)
    print("Closest String Algorithm Execute Time (%d tests)" % len(testcases),
          closestStringAlgoEndTime - closestStringAlgoStartTime)
    print("Out of", len(testcases), "test cases", numCasesFailed, "cases failed.")
    print("Saved cases: ", numCasesSaved)
    print("-----")
    print("fixedParameterAnswerDists:", fixedParameterAnswerDists)
    print("fixedParameterSolutionDists:", fixedParameterSolutionDists)
    print("Fixed Parameter Algorithm Execute Time (%d tests)" % len(testcases),
          fixedParameterAlgoEndTime - fixedParameterAlgoStartTime)


def compare_closest_algorithm_with_ant(testcases):
    results = []
    totalHammingDistance = 0
    for i in range(len(testcases)):
        testcase = testcases[i]
        testCaseResult, testCaseSolution = checkTestCase(len(testcase.inputStrings),
                                                         testcase.inputStrings,
                                                         testcase.answer,
                                                         testcase.alphabet,
                                                         testcase.maxDistance)
        timesToTryAgain = 0
        while testCaseResult is False and timesToTryAgain < 199:
            random.shuffle(testcase.inputStrings)
            testCaseResult, testCaseSolution = checkTestCase(
                len(testcase.inputStrings),
                testcase.inputStrings,
                testcase.answer,
                testcase.alphabet,
                testcase.maxDistance)
            timesToTryAgain += 1

        solutionDist, avgDist = getHammingDistanceMaxAndAvg(testcase.inputStrings, testCaseSolution)
        totalHammingDistance += solutionDist
        result = dict()
        result["Testcase No."] = i
        result["Solution Hamming Distance"] = solutionDist
        print(result)
        results.append(result)
    print("Total Hamming Distance", totalHammingDistance)

    df = pd.DataFrame(results,
                      columns=["Testcase No.",
                               "Solution Hamming Distance"])
    df.to_excel("to_ant.xlsx", index=False)


def generate_comparison_data(filename, excel_filename):
    alphabet = TEST_CONFIGURATION['alphabet']
    totalCases = TEST_CONFIGURATION['totalCases']
    numStringsList = TEST_CONFIGURATION['K']
    hammingDistList = TEST_CONFIGURATION['d']
    stringLengthList = TEST_CONFIGURATION['L']
    maxTries = TEST_CONFIGURATION['maxTries']
    configuration_df = pd.DataFrame(TEST_CONFIGURATION.items())

    testcase_dir = filename
    os.chdir(testcase_dir)

    allResults = []
    for numStrings in numStringsList:
        for ham in hammingDistList:
            for s in stringLengthList:
                if skipTest(alphabet, numStrings, ham, s):
                    continue

                print("numStrings = %d, hamming distance=%d, string length=%d" % (numStrings, ham, s))
                testCase_filename = "%s_testcase_%d_%d_%d" % (filename, numStrings, ham, s)
                testCases = load_testcases_from_file(testCase_filename)

                testCaseExcel = testCase_filename + "_WFC_CSP_maxTries_%d.xlsx" % TEST_CONFIGURATION['maxTries']
                testCaseStats = []
                numCases = 0
                numCasesFailed = 0
                numCasesSaved = 0

                closestStringMaxSolutionDists = []
                closestStringAvgSolutionDists = []
                closestStringAlgoStartTime = timeit.default_timer()
                while numCases < totalCases:
                    testCase = testCases[numCases]
                    testCaseResult, testCaseSolution = checkTestCase(testCase.numStrings, testCase.inputStrings, testCase.answer, testCase.alphabet, testCase.maxDistance)
                    if testCaseResult is False:
                        numCasesFailed += 1

                    tries = 1
                    while testCaseResult is False and tries < maxTries:
                        tries += 1
                        random.shuffle(testCase.inputStrings)
                        testCaseResult, testCaseSolution = checkTestCase(testCase.numStrings, testCase.inputStrings, testCase.answer, testCase.alphabet, testCase.maxDistance)

                        if testCaseResult is True:
                            numCasesSaved += 1
                            break

                    testCaseStat = dict()
                    testCaseStat["Testcase No."] = numCases
                    testCaseStat["Tries"] = tries
                    testCaseStats.append(testCaseStat)

                    numCases += 1
                    maxSolutionDist, avgDist = getHammingDistanceMaxAndAvg(testCase.inputStrings,
                                                                  testCaseSolution)
                    closestStringMaxSolutionDists.append(maxSolutionDist)
                    closestStringAvgSolutionDists.append(avgDist)
                closestStringAlgoEndTime = timeit.default_timer()
                closestStringAverageMaxSolutionDistance = sum(closestStringMaxSolutionDists) / float(totalCases * ham)
                closestStringAverageAvgSolutionDistance = sum(closestStringAvgSolutionDists) / float(totalCases * ham)

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
                result["Average Max Solution Distance/d"] = closestStringAverageMaxSolutionDistance
                result["Average Max Solution Distance"] = closestStringAverageMaxSolutionDistance * ham
                result["Average Avg Solution Distance"] = closestStringAverageAvgSolutionDistance
                result["Success Rate"] = (totalCases - numCasesFailed + numCasesSaved) / totalCases
                print(result)
                allResults.append(result)
                print("Closest String Algorithm Execute Time (%d tests)" % totalCases, closestStringAlgoEndTime - closestStringAlgoStartTime)
                print("numStrings=%d Hamming Distance=%d StringLength=%d: failed %d, saved %d" % (numStrings, ham, s, numCasesFailed, numCasesSaved))
                print("Average Max Answer Distance=%f and Average Avg Solution Distance=%f" % (closestStringAverageMaxSolutionDistance, closestStringAverageAvgSolutionDistance))
                df = pd.DataFrame(allResults, columns=["Algorithm", "Alphabet Size", "k", "d", "L", "Time", "Total", "Failed", "Saved", "Average Max Solution Distance/d", "Average Max Solution Distance", "Average Avg Solution Distance", "Success Rate"])
                with pd.ExcelWriter(excel_filename) as excelWriter:
                    df.to_excel(excelWriter, index=False)
                    configuration_df.to_excel(excelWriter, sheet_name="README", index=False)

                testCaseStats_df = pd.DataFrame(testCaseStats, columns=["Testcase No.", "Tries"])
                testCaseStats_df.to_excel(testCaseExcel, index=False)

                """
                # Fixed Position (CSD) algorithm
                if ham > 10:
                    # skip CSD algorithm if hamming distance > 10
                    continue
                
                if ham == 10 and s > 80:
                    continue

                fixedParameterAlgoStartTime = timeit.default_timer()
                fixedParameterMaxSolutionDists = []
                fixedParameterAvgSolutionDists = []
                fixedParameterAlgoSuccessCount = 0
                numCases = 0
                for testcase in testCases:
                    numCases += 1
                    fixedParameterAlgoSolution = CSd(testcase.inputStrings,
                                                   testcase.maxDistance,
                                                   testcase.inputStrings[0],
                                                   testcase.maxDistance)
                    if fixedParameterAlgoSolution != NOT_FOUND:
                        fixedParameterAlgoSuccessCount += 1
                    maxSolutionDist, avgDist = getHammingDistanceMaxAndAvg(testcase.inputStrings,
                                                                  fixedParameterAlgoSolution)
                    fixedParameterMaxSolutionDists.append(maxSolutionDist)
                    fixedParameterAvgSolutionDists.append(avgDist)
                fixedParameterAlgoEndTime = timeit.default_timer()
                fixedParameterAverageMaxSolutionDistance = sum(fixedParameterMaxSolutionDists) / float(totalCases * ham)
                fixedParameterAverageAvgSolutionDistance = sum(fixedParameterAvgSolutionDists) / float(totalCases * ham)

                result = dict()
                result["Algorithm"] = "FP"
                result["Alphabet Size"] = len(alphabet)
                result["k"] = numStrings
                result["d"] = ham
                result["L"] = s
                result["Time"] = (fixedParameterAlgoEndTime - fixedParameterAlgoStartTime) / totalCases
                result["Total"] = totalCases
                result["Failed"] = totalCases - fixedParameterAlgoSuccessCount
                result["Saved"] = 0
                result["Average Max Solution Distance/d"] = fixedParameterAverageMaxSolutionDistance
                result["Average Max Solution Distance"] = fixedParameterAverageMaxSolutionDistance * ham
                result["Average Avg Solution Distance"] = fixedParameterAverageAvgSolutionDistance
                result["Success Rate"] = fixedParameterAlgoSuccessCount / totalCases

                print(result)
                print()
                allResults.append(result)

                df = pd.DataFrame(allResults, columns=["Algorithm", "Alphabet Size", "k", "d", "L", "Time", "Total", "Failed", "Saved", "Average Max Solution Distance/d", "Average Max Solution Distance", "Average Avg Solution Distance", "Success Rate"])
                with pd.ExcelWriter(excel_filename) as excelWriter:
                    df.to_excel(excelWriter, index=False)
                    configuration_df.to_excel(excelWriter, sheet_name="README", index=False)
                """


def generate_comparison_testcases(filename):
    alphabet = TEST_CONFIGURATION['alphabet']
    totalCases = TEST_CONFIGURATION['totalCases']
    numStringsList = TEST_CONFIGURATION['K']
    hammingDistList = TEST_CONFIGURATION['d']
    stringLengthList = TEST_CONFIGURATION['L']

    testcase_dir = filename
    os.mkdir(testcase_dir)
    os.chdir(testcase_dir)

    for numStrings in numStringsList:
        for ham in hammingDistList:
            for s in stringLengthList:
                if skipTest(alphabet, numStrings, ham, s):
                    continue

                print("numStrings = %d, hamming distance=%d, string length=%d" % (numStrings, ham, s))
                testCases = create_working_testcases(alphabet, numStrings, s, ham, totalCases)
                testCase_filename = "%s_testcase_%d_%d_%d" % (filename, numStrings, ham, s)
                save_testcases_to_file(testCases, testCase_filename)
                testCase_ant_dir = testCase_filename+"_ant"
                try:
                    os.mkdir(testCase_ant_dir)
                except FileExistsError:
                    pass
                save_testcases_to_ant_instance_files(testCases, os.path.join(testCase_ant_dir, testCase_filename))


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
                    caseResult = checkTestCase(testCase.numStrings, testCase.inputStrings, testCase.answer, testCase.alphabet, testCase.maxDistance)
                    timesToTryAgain = 0
                    while caseResult is False and timesToTryAgain <= 1:
                        if timesToTryAgain == 0:
                            numCasesFailed += 1
                        random.shuffle(inputStrings)
                        caseResult = checkTestCase(testCase.numStrings, testCase.inputStrings, testCase.answer, testCase.alphabet, testCase.maxDistance)
                        if caseResult == True:
                            numCasesSaved += 1
                            break
                        timesToTryAgain += 1
                    numCases += 1
                closestStringAlgoEndTime = timeit.default_timer()
                smallList = [ham, s, closestStringAlgoEndTime-closestStringAlgoStartTime]
                grandList.append(smallList)
                print("Closest String Algorithm Execute Time (%d tests)" % totalCases, closestStringAlgoEndTime - closestStringAlgoStartTime)
                print("numStrings=%d Hamming Distance=%d StringLength=%d: failed %d, saved %d" % (numStrings, ham, s, numCasesFailed, numCasesSaved))
                print()
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
    stringLength = 180
    k = 60   # maximum Hamming distance

    testcaseCount = 1000
    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate":
            assert len(sys.argv) == 3, "Need filename to save generated testcases"
            filename = sys.argv[2]
            testcases = create_working_testcases(alphabet, numStrings, stringLength, k, testcaseCount)
            save_testcases_to_file(testcases, filename)

        elif sys.argv[1] == "--generate-ant-instances":
            assert len(sys.argv) == 3, "Need filename to save generated testcases"
            filename = sys.argv[2]
            testcases = create_working_testcases(alphabet, numStrings, stringLength, k, testcaseCount)
            save_testcases_to_ant_instance_files(testcases, filename)

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
            compare_algorithms(testcases)

        elif sys.argv[1] == "--compare-with-ant":
            assert len(
                sys.argv) == 3, "Need filename to load generated testcases"
            filename = sys.argv[2]
            testcases = load_testcases_from_file(filename)
            save_testcases_to_ant_instance_files(testcases, filename+"_ant")
            compare_closest_algorithm_with_ant(testcases)

        elif sys.argv[1] == "--generate-comparison-data":
            assert len(
                sys.argv) >= 3, "Need filename (.xlsx) to load generated testcases"
            filename = sys.argv[2]
            excel_filename = filename + ".xlsx"
            if len(sys.argv) == 4:
                excel_filename = sys.argv[3]
                if not excel_filename.endswith(".xlsx"):
                    excel_filename = excel_filename + ".xlsx"
            generate_comparison_data(filename, excel_filename)
        elif sys.argv[1] == "--generate-comparison-testcases":
            assert len(
                sys.argv) == 3, "Need filename prefix to save generated testcases"
            filename = sys.argv[2]
            generate_comparison_testcases(filename)
        elif sys.argv[1] == "--plot":
            assert len(
                sys.argv) == 3, "Need filename (.xlsx) to load generated testcases"
            filename = sys.argv[2]
            plot_figures(filename)
        else:
            print("unknown option/command %s" % sys.argv[1])
    else:
        main_comaprison_plot()

    return 0


if __name__ == "__main__":
    main()