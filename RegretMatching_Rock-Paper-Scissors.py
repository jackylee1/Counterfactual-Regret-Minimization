# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 08:28:40 2015

@author: russell
""" 
import random

actions = ["Rock","Paper","Scissors"]
NUMACTIONS = 3

# Regret Matching for Rock-Paper-Scissors
class RegretMatching_RPC:
    def __init__(self,iterations):
        self.iterations = iterations
        self.regretSum = [0]*NUMACTIONS
        self.strategy = [0]*NUMACTIONS
        self.strategySum = [0]*NUMACTIONS
        self.oppStrategy = [.4, .3, .3]
        self.avgStrategy = [0]*NUMACTIONS
    
    def getStrategy(self):
        for a in range(NUMACTIONS):
            if self.regretSum[a] > 0:
                self.strategy[a] = self.regretSum[a]
            else:
                self.strategy[a] = 0
        normalizingSum = sum(self.strategy)
        for a in range(NUMACTIONS):
            if normalizingSum > 0:
                self.strategy[a] /= float(normalizingSum)
            else:
                self.strategy[a] = 1.0 / NUMACTIONS
            self.strategySum[a] += self.strategy[a]
            
    def getAction(self,strategy):
        r = random.random()
        a = 0
        cumulativeProbability = 0.0
        while a < (NUMACTIONS):
            cumulativeProbability += strategy[a]
            if r < cumulativeProbability:
                return a
            a+=1
        
    def train(self):
        actionUtility = [0]*3
        for i in xrange(self.iterations):
            # Get regret-matched mixed strategy actions
            self.getStrategy()
            myAction = self.getAction(self.strategy)
            otherAction = self.getAction(self.oppStrategy)
            
            # Compute Action Utilities
            actionUtility[otherAction] = 0
            if otherAction == NUMACTIONS - 1:
                actionUtility[0] = 1
            else:
                actionUtility[otherAction+1] = 1
            if otherAction == 0:
                actionUtility[NUMACTIONS-1] = -1
            else:
                actionUtility[otherAction-1] = -1
            
            # Accumulate Action Regrets
            for a in range(NUMACTIONS):
                self.regretSum[a] += (actionUtility[a] - actionUtility[myAction])
    
    def getAverageStrategy(self):
        normalizingSum = sum(self.strategy)
        for a in range(NUMACTIONS):
            if normalizingSum > 0:
                self.avgStrategy[a] = self.strategySum[a] / float(normalizingSum)
            else:
                self.avgStrategy[a] = 1.0 / NUMACTIONS
        for a in range(NUMACTIONS):
            self.avgStrategy[a] /= self.iterations
            print actions[a], ":", self.avgStrategy[a]
            
    def Expected_Utility(self,p1,p2):
        utilities = [[0,-1,1],[1,0,-1],[-1,1,0]]
        total = 0
        for i in range(len(p1)):
            for j in range(len(p2)):
                total += p1[i]*p2[j]*utilities[i][j]
        print "Expected Utility for Player: ", total
        
            
            
    
x = RegretMatching_RPC(10000)
x.train()
x.getAverageStrategy()
x.Expected_Utility(x.avgStrategy,x.oppStrategy)
