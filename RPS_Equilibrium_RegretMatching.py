# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 09:16:09 2015

@author: russelljadams

Rock-Paper-Scissors Regret Matching for Two players. Solves the Mixed Strategy Nash Equilibrium of the game. Updating each players
strategy with each iteration.
"""


import random

actions = ["Rock","Paper","Scissors"]
NUMACTIONS = 3

class RPC_Player:
    def __init__(self,serial,strategy):
        self.serial = serial
        
        self.strategy = strategy
        self.strategySum = [0]*NUMACTIONS
        self.regretSum = [0]*NUMACTIONS
        self.avgStrategy = [0]*NUMACTIONS


# Regret Matching for Rock-Paper-Scissors
class RegretMatching_RPC:
    def __init__(self,iterations,p1,p2):
        self.iterations = iterations
        self.p1 = p1
        self.p2 = p2
    
    def getStrategy(self, player):
        for a in range(NUMACTIONS):
            if player.regretSum[a] > 0:
                player.strategy[a] = player.regretSum[a]
            else:
                player.strategy[a] = 0
        normalizingSum = sum(player.strategy)
        for a in range(NUMACTIONS):
            if normalizingSum > 0:
                player.strategy[a] /= float(normalizingSum)
            else:
                player.strategy[a] = 1.0 / NUMACTIONS
            player.strategySum[a] += player.strategy[a]
            
    def getAction(self,player):
        r = random.random()
        a = 0
        cumulativeProbability = 0.0
        while a < (NUMACTIONS):
            cumulativeProbability += player.strategy[a]
            if r < cumulativeProbability:
                return a
            a+=1
        
    def train(self):
        utilities = [[0,-1,1],[1,0,-1],[-1,1,0]]
        for i in xrange(self.iterations):
            # Get regret-matched mixed strategy actions
            self.getStrategy(self.p1)
            self.getStrategy(self.p2)
            myAction = self.getAction(self.p1)
            otherAction = self.getAction(self.p2)
            
            # Accumulate Action Regrets
            for a in range(NUMACTIONS):
                self.p1.regretSum[a] += (utilities[a][otherAction] - utilities[myAction][otherAction])
                self.p2.regretSum[a] += (utilities[a][myAction] - utilities[otherAction][myAction])
    
    def getAverageStrategy(self, player):
        normalizingSum = sum(player.strategy)
        for a in range(NUMACTIONS):
            if normalizingSum > 0:
                player.avgStrategy[a] = player.strategySum[a] / float(normalizingSum) / self.iterations
            else:
                player.avgStrategy[a] = 1.0 / NUMACTIONS
        for a in range(NUMACTIONS):
            print actions[a], ":", player.avgStrategy[a]
            
    def Expected_Utility(self,p1,p2):
        utilities = [[0,-1,1],[1,0,-1],[-1,1,0]]
        total = 0
        for i in range(len(p1)):
            for j in range(len(p2)):
                total += p1[i]*p2[j]*utilities[i][j]
        print "Expected Utility for Player: ", total
        
            
p1 = RPC_Player(1,[.4,.3,.3])
p2 = RPC_Player(2,[.1,.8,.1])
    
x = RegretMatching_RPC(10000,p1,p2)
x.train()
x.getAverageStrategy(x.p1)
x.getAverageStrategy(x.p2)
x.Expected_Utility(x.p1.avgStrategy,x.p2.avgStrategy)
