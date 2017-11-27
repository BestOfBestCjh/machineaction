# -*- coding:utf-8 -*-

from numpy import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList, classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in  inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix, trainCategory):
    '''
    计算p(wi|c1),p(wi|c0) 二分类问题中，表示词在某类文档中出现的概率.计算的前提条件是trainMatrix是按词表统一排列的文档矩阵，每一列都是表示相同的词在文档中出现的次数
    :param trainMatrix:
    :param trainCategory:
    :return:
    '''
    numTrainDocs = len(trainMatrix) #训练文档数目
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs) # 侮辱性类别文档的概率
    p0Num = zeros(numWords); p1Num = zeros(numWords)
    p0Denom = 0.0; p1Denom = 0.0
    for i in range(numTrainDocs):
        print 'trainMatrix[ %s ]' % i
        print trainMatrix[i]
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            print 'p1Num:'
            print p1Num
            p1Denom += sum(trainMatrix[i])
            print 'p1Denom'
            print p1Denom
        else:
            p0Num += trainMatrix[i]
            print 'p0Num:'
            print p0Num
            p0Denom += sum(trainMatrix[i])
            print 'p0Denom'
            print p0Denom
    p1Vect = p1Num / p1Denom
    p0Vect = p0Num / p0Denom
    return p0Vect, p1Vect, pAbusive

if __name__ == '__main__':
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    print myVocabList
    print setOfWords2Vec(myVocabList, listOPosts[0])
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(trainMat, listClasses)
    print 'p0V:'
    print p0V
    print 'p1V:'
    print p1V
    print 'PAb:'
    print pAb