import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.metrics import f1_score
import numpy as np
import pickle as pk

################# training #################


VOWEL_LIST =[ "AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"]
VOWELstress_LIST =[ "AA1", "AE1", "AH1", "AO1", "AW1", "AY1", "EH1", "ER1", "EY1", "IH1", "IY1", "OW1", "OY1", "UH1", "UW1"]
voweldict={"AA":11, "AE":12, "AH":13, "AO":14, "AW":15, "AY":16, "EH":17, "ER":18, "EY":19, "IH":20, "IY":21, "OW":22, "OY":23, "UH":24, "UW":25}
consonantdict={"CH":31, "DH":32, "HH":33, "JH":34, "NG":35,  "SH":36,"TH":37, "ZH":38,"P":39, "B":40,"D":41, "F":42, "G":43,"K":44, "L":45, "M":46, "N":47,"R":48, "S":49, "T":50,"V":51,"W":52, "Y":53,"Z":54}

CONSONANT_LIST =[  "CH", "DH", "HH","JH", "NG","SH","TH", "ZH","P", "B","D", "F", "G","K", "L", "M", "N","R", "S", "T","V","W", "Y", "Z"]


def read_data(file_path):
	with open(file_path) as f:
		lines = f.read().splitlines()
	return lines

def findSyll(strings):
    i=strings.index(":")
    for word in VOWEL_LIST:
        vowelPosition = strings.find(word)
        if vowelPosition:
            break
    head=strings[i+2:vowelPosition+2]

def findWord(strings):
    i=strings.index(":")
    word=strings[0:i]
    return word


def findStressPosition(strings):
    position=1
    stress='1'
    word=strings.split(":")[-1]
    pureword = ''.join([i for i in word if not i.isdigit()])
    syll=word.split()
    for letter in syll:
        if not letter.isalpha():
            if stress in letter:
                return position
            else:
                position+=1

    return position




def findPrefix(strings):
    prefixlist = []
    word=strings.split(":")[-1]
    word = ''.join([i for i in word if not i.isdigit()])
    syll=word.split()

    for vowel in VOWEL_LIST:
        if vowel in syll:
            vowelposition=syll.index(vowel)
            prefixlist.append(vowelposition)

    prefixPositon=min(prefixlist)
    prefix=syll[0:(prefixPositon+1)]
    if prefix=='':
        prefix=syll[0]
    return prefix

transferlist=[]
def findSuffix(strings):
    suffixList = []

    word = strings.split(":")[-1]

    word = ''.join([i for i in word if not i.isdigit()])
    syll = word.split()
    for consonant in CONSONANT_LIST:
        if consonant in syll:
            syll.reverse()
            consonantPosition=syll.index(consonant)
            suffixList.append(consonantPosition)
            syll.reverse()
    if suffixList==[]:
        suffixList.append(len(syll))
    suffixPosition=min(suffixList)
    suffixPosition=len(syll)-suffixPosition-1
    suffix=syll[suffixPosition:len(syll)]
    return suffix

def transferIntoNum(strings):
    numberstring=[]
    if len(strings)==0:
        return 99
    if len(strings)==1:
        for word in strings:
            if word in CONSONANT_LIST:
                numberstring.append(str(consonantdict[word]))
            else:
                numberstring.append(voweldict[word])

    if len(strings)==2:

        for word in strings:
            if word in CONSONANT_LIST:
                numberstring.append(consonantdict[word])
            else:
                numberstring.append(voweldict[word])


    if len(strings)==3:
        for word in strings:
            if word in CONSONANT_LIST:
                numberstring.append(consonantdict[word])
            else:
                numberstring.append(voweldict[word])
    if len(strings)==4:
        for i in range(0,3):
            word=strings[i]
            if word in CONSONANT_LIST:
                numberstring.append(consonantdict[word])
            else:
                numberstring.append(voweldict[word])


    return numberstring


def findsyllNumber(strings):
    prefixlist = []
    word = strings.split(":")[-1]
    word = ''.join([i for i in word if not i.isdigit()])
    syll = word.split()

    for vowel in VOWEL_LIST:
        if vowel in syll:
            for i, v in enumerate(syll):
                if v == vowel:
                    vowelposition=syll.index(vowel)
                    prefixlist.append(vowelposition)
    lenth=len(prefixlist)


    return lenth




def train(data, classifier_file):# do not change the heading of the function

    wordlist = data


    wholewordList = []



    biglist = []
    resultList = []

    for i in range(0, len(wordlist)):
        minlist = []
        num = ''
        suffixnum = ''
        preprocess = wordlist[i]
        prefix = findPrefix(preprocess)
        number = transferIntoNum(prefix)
        for numbersi in number:
            num = num + str(numbersi)

        minlist.append(int(num))

        suffix = findSuffix(preprocess)

        suffixnumber = transferIntoNum(suffix)
        for sunumberi in suffixnumber:
            suffixnum = suffixnum + str(sunumberi)
        if suffixnum == '':
            suffixnum = 99
        minlist.append(int(suffixnum))
        minlist.append(findsyllNumber(preprocess))
        biglist.append(minlist)
        stressposition = findStressPosition(preprocess)
        resultList.append(stressposition)
        wholewordList.append(findWord(wordlist[i]))

    train = biglist
    target = resultList
    numblist = []
    train_X, test_X, train_y, test_y = train_test_split(train,
                                                            target,
                                                            test_size=0.245,
                                                            random_state=4)

    clf = tree.DecisionTreeClassifier(max_depth=17)
    clf = clf.fit(train_X, train_y)

    with open(classifier_file, "wb") as f:
        pk.dump(clf, f)







################# testing #################
voweldict={"AA":11, "AE":12, "AH":13, "AO":14, "AW":15, "AY":16, "EH":17, "ER":18, "EY":19, "IH":20, "IY":21, "OW":22, "OY":23, "UH":24, "UW":25}
consonantdict={"CH":31, "DH":32, "HH":33, "JH":34, "NG":35,  "SH":36,"TH":37, "ZH":38,"P":39, "B":40,"D":41, "F":42, "G":43,"K":44, "L":45, "M":46, "N":47,"R":48, "S":49, "T":50,"V":51,"W":52, "Y":53,"Z":54}
VOWEL_LIST =[ "AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"]
CONSONANT_LIST =[  "CH", "DH", "HH","JH", "NG","SH","TH", "ZH","P", "B","D", "F", "G","K", "L", "M", "N","R", "S", "T","V","W", "Y", "Z"]




def findPrefix(strings):
    prefixlist = []
    word=strings.split(":")[-1]
    word = ''.join([i for i in word if not i.isdigit()])
    syll=word.split()

    for vowel in VOWEL_LIST:
        if vowel in syll:
            vowelposition=syll.index(vowel)
            prefixlist.append(vowelposition)

    prefixPositon=min(prefixlist)
    prefix=syll[0:(prefixPositon+1)]
    if prefix=='':
        prefix=syll[0]
    return prefix
def findSuffix(strings):
    suffixList = []

    word = strings.split(":")[-1]

    word = ''.join([i for i in word if not i.isdigit()])
    syll = word.split()
    for consonant in CONSONANT_LIST:
        if consonant in syll:
            syll.reverse()
            consonantPosition=syll.index(consonant)
            suffixList.append(consonantPosition)
            syll.reverse()
    if suffixList==[]:
        suffixList.append(len(syll))
    suffixPosition=min(suffixList)
    suffixPosition=len(syll)-suffixPosition-1
    suffix=syll[suffixPosition:len(syll)]
    return suffix
def findsyllNumber(strings):
    prefixlist = []
    word = strings.split(":")[-1]
    word = ''.join([i for i in word if not i.isdigit()])
    syll = word.split()

    for vowel in VOWEL_LIST:
        if vowel in syll:
            for i, v in enumerate(syll):
                if v == vowel:
                    vowelposition=syll.index(vowel)
                    prefixlist.append(vowelposition)
    lenth=len(prefixlist)


    return lenth

def transferIntoNum(strings):
    numberstring=[]
    if len(strings)==0:
        return 99
    if len(strings)==1:
        for word in strings:
            if word in CONSONANT_LIST:
                numberstring.append(str(consonantdict[word]))
            else:
                numberstring.append(voweldict[word])

    if len(strings)==2:

        for word in strings:
            if word in CONSONANT_LIST:
                numberstring.append(consonantdict[word])
            else:
                numberstring.append(voweldict[word])


    if len(strings)==3:
        for word in strings:
            if word in CONSONANT_LIST:
                numberstring.append(consonantdict[word])
            else:
                numberstring.append(voweldict[word])
    if len(strings)==4:
        for i in range(0,3):
            word=strings[i]
            if word in CONSONANT_LIST:
                numberstring.append(consonantdict[word])
            else:
                numberstring.append(voweldict[word])


    return numberstring

def test(data, classifier_file):# do not change the heading of the function
        with open(classifier_file, 'rb', True) as f:

            clf = pk.load(f)
            f.close()


        wordlist = data
        biglist = []
        resultList = []

        for i in range(0, len(wordlist)):
            minlist = []
            num = ''
            suffixnum = ''
            preprocess = wordlist[i]
            prefix = findPrefix(preprocess)
            number = transferIntoNum(prefix)
            for numbersi in number:
                num = num + str(numbersi)

            minlist.append(int(num))

            suffix = findSuffix(preprocess)

            suffixnumber = transferIntoNum(suffix)
            for sunumberi in suffixnumber:
                suffixnum = suffixnum + str(sunumberi)
            if suffixnum == '':
                suffixnum = 99
            minlist.append(int(suffixnum))
            minlist.append(findsyllNumber(preprocess))
            biglist.append(minlist)




        a =  clf.predict(biglist)

        return a




