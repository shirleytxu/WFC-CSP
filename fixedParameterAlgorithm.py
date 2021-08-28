import closestString
import random
S = []
d = 0

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

def CSd(s, delta):
    sWorks = True
    kValid = False
    if delta < 0:
        return "not found"

    for str in S:
        if calculateDistance(S, str) >  d + delta:
            return "not found"
        if calculateDistance(S, str) > d:
            sWorks = False
    if sWorks == True:
        return s

    while kValid == False:
        i = random.randint(0, S.len())
        if calculateDistance(S, S[i] > d):
            kValid = True
            
def main():


main()