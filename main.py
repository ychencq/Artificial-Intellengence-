
from __future__ import division
from expectationMaximizer import ExpectationMaximizer as EM
from math import sqrt

def getMeanAndSd(accu):
    mean = sum(accu)/len(accu)
    sd = sqrt((1/(len(accu)-1)) * reduce(lambda x,y: x + (y-mean)**2, accu, 0))

    return (mean,sd)


def getData(fn):
    Data = []
    with open(fn, 'r') as f:
        for line in f:
            Data.append([int(x) for x in line.strip().split()])

    return Data



def main():
    AccuracyOfMeanBefore = []
    AccuracyOfMeanAfter = []

    num = 20
    testData = getData('testdata.txt')
    trainData = getData('traindata.txt')
    em = EM(20, trainData)



    for i in xrange(0, num):
        #ued to record the AccuracyOfMeanBefore  &   AccuracyOfMeanAfter
        accuracyOfTwoTimes = [[],[]]
            # each time we will do 20 trials
        print(i)
        for j in xrange(0, 20):

            em.randomizeCPTs()
            beforeEM = em.predict(testData)

            em.run()
            afterEM = em.predict(testData)

            accuracyOfTwoTimes[0].append(beforeEM)
            accuracyOfTwoTimes[1].append(afterEM)

        AccuracyOfMeanBefore.append(getMeanAndSd(accuracyOfTwoTimes[0]))
        AccuracyOfMeanAfter.append(getMeanAndSd(accuracyOfTwoTimes[1]))

        em.updateDelta()

    for i in xrange(0, num):

        print ("delta Value: %f    Mean Before: %f    Mean After: %f " %(i * (4/num),AccuracyOfMeanBefore[i][0],AccuracyOfMeanAfter[i][0]))

    print '\r\n'



    for i in xrange(0, num):

        print ("delta Value: %f    sd Before: %f    sd After: %f " %(i * (4/num),AccuracyOfMeanBefore[i][1],AccuracyOfMeanAfter[i][1]))

    print '\r\n'

main()
