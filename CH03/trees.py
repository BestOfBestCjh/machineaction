# -*- coding:utf-8 -*-

from math import log
import operator

def calcShannonEnt(dataSet):
    '''
    计算数据集的经验熵,计算公式参考"<统计学习方法>李航著"62页
    :param dataSet: 
    :return: 
    '''
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt


def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
    '''
    根据特征值划分子集
    :param dataSet: 数据集
    :param axis: 特征索引，也就是数据集中的第几列
    :param value: 特征值
    :return: 
    '''
    retDataSet = []
    for featVec in dataSet:
        # print featVec[axis]
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            # print reducedFeatVec
            reducedFeatVec.extend(featVec[axis + 1 :])
            # print reducedFeatVec
            retDataSet.append(reducedFeatVec)
    return  retDataSet


def chooseBestFeatureToSplit(dataSet):
    '''
    求出信息增益最高的特征，计算特征A对数据集D的经验条件熵H(D|A)。计算公式参考"<统计学习方法>李航著"62页
    H(D|A) = [(|Di|/|D|) * H(Di)]求和,i=1,..n 表示A的取值个数
    :param dataSet: 
    :return: 
    '''
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        # print featList
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    '''
    多数表决
    :param classList: 类的标签列表
    :return: 占多数的类
    '''
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key= operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

if __name__ == '__main__':
    dataSet, labels = createDataSet()
    print dataSet
    print labels
    #splitDataSet(dataSet,0,1)
    # num = len(dataSet[0]) - 1
    # for i in range(num):
    #     featList = [example[i] for example in dataSet]
    #     print featList
    #     uniqueVals = set(featList)
    #     newEntropy = 0.0
    #     for value in uniqueVals:
    #         subDataSet = splitDataSet(dataSet, i, value)
    #         prob = len(subDataSet) / float(len(dataSet))
    print chooseBestFeatureToSplit(dataSet)

