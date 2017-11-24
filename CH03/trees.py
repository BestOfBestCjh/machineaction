# -*- coding:utf-8 -*-

from math import log
import operator
import treePlotter

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
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    '''
    创建决策树
    :param dataSet:
    :param labels:
    :return:
    '''
    classList = [example[-1] for example in dataSet]
    print classList
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(
            dataSet, bestFeat, value), subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):
    '''
    用训练出来的决策树来进行测试集的预测
    :param inputTree: 训练出的决策树模型
    :param featLabels: 特征标签集
    :param testVec: 测试集
    :return: 所属类型(预测结果)
    '''
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    '''
    存储构建好的决策树
    :param inputTree:
    :param filename: 文件名
    :return:
    '''
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    '''
    读取已经构建好的决策树
    :param filename:
    :return:
    '''
    import pickle
    fr = open(filename)
    return pickle.load(fr)

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
    # print chooseBestFeatureToSplit(dataSet)
    # classList = [example[-1] for example in dataSet]
    # print classList
    # print len(dataSet[0])
    # bestFeat = chooseBestFeatureToSplit(dataSet)
    # print bestFeat
    # bestFeatLabel = labels[bestFeat]
    # print bestFeatLabel
    # myTree = treePlotter.retrieveTree(0)
    # print myTree
    # print classify(myTree, labels, [1, 0])
    # storeTree(myTree,'tree.txt')
    # print grabTree('tree.txt')
    # 测试隐形眼镜数据集
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    print lenses
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = createTree(lenses, lensesLabels)
    print lensesTree
    treePlotter.createPlot(lensesTree)