# -*- coding:utf-8 -*-

from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    '''
    使用k-近邻算法将每组数据划分到某个类中
    (1)计算已知类别数据集中的点与当前点之间的距离；
    (2)按照距离递增次序排序
    (3)选取与当前点距离最小的k个点
    (4)确定前k个点所在类别的出现频率
    (5)返回前k个点出现频率最高的类别作为当前点的预测分类
    :param inX: 
    :param dataSet: 
    :param labels: 
    :param k: 
    :return: 
    '''

    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    print 'diffMat:'
    print diffMat
    sqDiffMat = diffMat ** 2
    print 'sqDiffMat:'
    print sqDiffMat
    sqDistances = sqlDiffMat.sum(axis=1)
    print 'sqDistances:'
    print sqDistances
    distances =sqDistances ** 0.5
    print 'distances:'
    print distances
    sortedDistIndicies = distances.argSort()
    print 'sortedDistIndicies:'
    print sortedDistIndicies
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3))
    print 'returnMat:'
    print returnMat
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        print 'line :' + line
        listFromLine = line.split('\t')
        print 'listFromLine:'
        print listFromLine
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape(0)
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet, ranges, minVals



if __name__=='__main__':
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    #print datingDataMat
    print datingLabels
    print array(datingLabels)
    #制作原始数据的散点图
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.scatter(datingDataMat[:,1], datingDataMat[:,2])
    ax.scatter(datingDataMat[:,1], datingDataMat[:,2], 15.0 * array(datingLabels))
    plt.show()