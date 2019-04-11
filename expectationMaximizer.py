from __future__ import division
import random

class ExpectationMaximizer(object):
    # numDeltas indicate the # of deltas we will use
    # trainData is the trainData set from the txt file
    def __init__(self, num, trainData):
        # CPTs table is set to recored when var = True
        # WE combine the table here     classify the Dunetts with   0 1 2  which indicate the healthy  mild  serve
        # now we construct the table in the oreder :
        self.CPTs =[[[0.01, 0.3, 0.2],[0.01, 0.02, 0.02]],[0.02, 0.8, 0.2],[0.02, 0.2, 0.8],[0.1],[0.5, 0.25]]
        self.CPTsInRandom = [[[0, 0, 0],[0, 0, 0]],[0, 0, 0],[0, 0, 0],[0],[0,0]]

        self.numDeltas = num
        self.delta = 0

        self.jointTable = {}

        self.sumOfTotalLH = [[[0, 0, 0],[0, 0, 0]], [0, 0, 0],[0, 0, 0],[0],[0]]

        self.sumOfPresentLH = [[[0, 0, 0],[0, 0, 0]],[0, 0, 0],[0, 0, 0],[0], [0,0]]

        self.data = trainData

        # sum of weights
        # it is exactly jointProbability
        self.jointProb = 0

        random.seed(None)

    def calculatejointTable(self):
        for a in xrange(0,2):
            for b in xrange(0,2):
                for c in xrange(0,2):
                    for THTS in xrange(0,2):
                        jointProb = 0
                        strForms = [None] * 3
                        for DS in xrange(0,3):
                            point = [a,b,c,THTS,DS]
                            strForm = str(point)

                            jointProbability = 1
                            if a == 1:
                                jointProbability *= self.CPTsInRandom[0][THTS][DS]
                            else:
                                jointProbability *=(1-self.CPTsInRandom[0][THTS][DS])

                            if b == 1:
                                jointProbability *= self.CPTsInRandom[1][DS]
                            else:
                                jointProbability *= (1-self.CPTsInRandom[1][DS])

                            if c == 1:
                                jointProbability *= self.CPTsInRandom[2][DS]
                            else:
                                jointProbability *= (1-self.CPTsInRandom[2][DS])

                            if THTS == 1:
                                jointProbability *= self.CPTsInRandom[3][0]
                            else:
                                jointProbability *= (1-self.CPTsInRandom[3][0])

                            if (DS == 0 or DS == 1):
                                jointProbability *= self.CPTsInRandom[4][DS]
                            else:
                                jointProbability *= (1-self.CPTsInRandom[4][0]-self.CPTsInRandom[4][1])

                            strForms[DS] = strForm
                            self.jointTable[strForm] = [jointProbability, 0]

                            jointProb+= jointProbability
                    #likelihoods

                        for strForm in strForms:
                            self.jointTable[strForm][1] = self.jointTable[strForm][0]/jointProb

    def updateDelta(self):
        self.delta += 4/self.numDeltas




    def randomizeCPTs(self):
        for var in xrange(0, 5):
            if var == 1:
                for DS in xrange(0, 3):
                    x = random.uniform(0, self.delta)
                    y = random.uniform(0, self.delta)
                    self.CPTsInRandom[1][DS] = (self.CPTs[1][DS] + x)/(1 + x + y)

            elif var == 0:
                for THTS in xrange(0, 2):
                    for DS in xrange(0, 3):
                        x = random.uniform(0, self.delta)
                        y = random.uniform(0, self.delta)
                        self.CPTsInRandom[var][THTS][DS] = (self.CPTs[var][THTS][DS] + x)/(1 + x + y)
            elif var == 3:
                x = random.uniform(0, self.delta)
                y = random.uniform(0, self.delta)
                self.CPTsInRandom[var][0] = (self.CPTs[var][0] + x)/(1 + x + y)
            elif var == 2:
                for DS in xrange(0, 3):
                    x = random.uniform(0, self.delta)
                    y = random.uniform(0, self.delta)
                    self.CPTsInRandom[2][DS] = (self.CPTs[2][DS] + x)/(1 + x + y)
            else:
                for DS in xrange(0,2):
                    x = random.uniform(0, self.delta)
                    y = random.uniform(0, self.delta)
                    randNum3 = random.uniform(0, self.delta)
                    self.CPTsInRandom[var][DS] = (self.CPTs[var][DS] + x)/(1 + x + y + randNum3)



    def clearWeights(self):
        # reset to 0 directly
        self.jointProb = 0
        for var in xrange(0, 5):
            if var == 0:
                for gene in xrange(0, 2):
                    for DS in xrange(0, 3):
                        self.sumOfTotalLH[var][gene][DS] = 0
                        self.sumOfPresentLH[var][gene][DS] = 0
            else:
                for var2 in xrange(0, len(self.sumOfPresentLH[var])):
                    if var == 4:
                        if var2 == 0:
                            self.sumOfTotalLH[var][var2] = 0
                    else:
                        self.sumOfTotalLH[var][var2] = 0
                    self.sumOfPresentLH[var][var2] = 0



    def accuLH(self, point, value):
        # the same s f d thts DS indicate the their own array
        a = point[0]
        b = point[1]
        c = point[2]
        THTS = point[3]
        DS = point[4]

        # calculate the sum of likelihood values
        self.sumOfTotalLH[0][THTS][DS]+= value
        self.sumOfTotalLH[1][DS]+= value
        self.sumOfTotalLH[2][DS]+= value
        self.sumOfTotalLH[3][0]+= value
        self.sumOfTotalLH[4][0]+= value

        if a == 1:
            self.sumOfPresentLH[0][THTS][DS]+= value
        if b == 1:
            self.sumOfPresentLH[1][DS]+= value
        if c == 1:
            self.sumOfPresentLH[2][DS]+= value
        if THTS == 1:
            self.sumOfPresentLH[3][0]+= value
        if DS == 0 or DS == 1:
            self.sumOfPresentLH[4][DS]+= value

    def run(self):
        likelihood = None

        while True:
            # calculate JP and likelihood table
            self.calculatejointTable()
            for data in self.data:
                if data[-1] == -1:
                    # splitting the data
                    for DS in xrange(0,3):

                        data[-1] = DS
                        strForm = str(data)

                        self.jointProb+= self.jointTable[strForm][0]
                        self.accuLH(data, self.jointTable[strForm][1])

                    data[-1] = -1
                else:
                    # observe a DS
                    self.jointProb+= self.jointTable[str(data)][0]
                    self.accuLH(data, 1)

            #  for the  Foriennditis & Degar Spotes
            for DS in xrange(0,3):
                self.CPTsInRandom[1][DS] = self.sumOfPresentLH[1][DS] / self.sumOfTotalLH[1][DS]
                self.CPTsInRandom[2][DS] = self.sumOfPresentLH[2][DS] / self.sumOfTotalLH[2][DS]

            #  to update CPTs and update Sloepnea
            for THTS in xrange(0,2):
                for DS in xrange(0,3):
                    self.CPTsInRandom[0][THTS][DS] = self.sumOfPresentLH[0][THTS][DS] / self.sumOfTotalLH[0][THTS][DS]

            # DS
            self.CPTsInRandom[4][0] = self.sumOfPresentLH[4][0] / self.sumOfTotalLH[4][0]
            self.CPTsInRandom[4][1] = self.sumOfPresentLH[4][1] / self.sumOfTotalLH[4][0]


            # THTS
            self.CPTsInRandom[3][0] = self.sumOfPresentLH[3][0] / self.sumOfTotalLH[3][0]


            if likelihood != None and self.jointProb - likelihood <= 0.01:
                self.clearWeights()

                break

            likelihood = self.jointProb
            self.clearWeights()

    def predict(self, testData):
        correct = 0
        for data in testData:
            predi = None
            # no Dunetts Syndrome
            healthy = 1
            # Mild Dunetts Syndrome
            mild = 1
            # Severe Dunetts Syndrome
            severe = 1

            for var in xrange(0, len(self.CPTs)):
                if var == 0:
                    if data[var] == 1:
                        healthy*= self.CPTsInRandom[var][data[3]][0]
                        mild*= self.CPTsInRandom[var][data[3]][1]
                        severe*= self.CPTsInRandom[var][data[3]][2]
                    else:
                        healthy *= (1 - self.CPTsInRandom[var][data[3]][0])
                        mild*= (1 - self.CPTsInRandom[var][data[3]][1])
                        severe*= (1 - self.CPTsInRandom[var][data[3]][2])

                elif var == 3:
                    mulitply = (self.CPTsInRandom[var][0] if data[var] == 1 else (1 - self.CPTsInRandom[var][0]))
                    healthy*= mulitply
                    mild*= mulitply
                    severe*= mulitply

                elif var < 3:
                    if data[var] == 1:
                        healthy*= self.CPTsInRandom[var][0]
                        mild*= self.CPTsInRandom[var][1]
                        severe*= self.CPTsInRandom[var][2]
                    else:
                        healthy*= (1 - self.CPTsInRandom[var][0])
                        mild*= (1 - self.CPTsInRandom[var][1])
                        severe*= (1 - self.CPTsInRandom[var][2])

                else:
                    healthy*= (self.CPTsInRandom[var][0])
                    mild*= (self.CPTsInRandom[var][1])
                    severe*= (1- self.CPTsInRandom[var][0] - self.CPTsInRandom[var][1])

            if healthy >= mild and healthy >= severe:
                predi = 0
            else:
                if mild >= healthy and mild >= severe:
                    predi = 1
                else:
                    predi = 2

            if predi == data[-1]:
                correct += 1
            else:
                correct += 0

        return correct/len(testData)
