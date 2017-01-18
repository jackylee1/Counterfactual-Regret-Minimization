"""
Created on Wed Jan 18 11:14:26 2017

@author: 4bet20x

"""
import random


actions = ["Rock","Paper","Scissors"]

class RPS_Player:
    def __init__(self,base=[0,0,0]):
        self.strategy = base
        self.regretSum = [0,0,0]
        self.strategySum = [0,0,0]
        self.avgStrategy = [0,0,0]

# Regret Matching for Rock-Paper-Scissors
class RegretMatching_RPC:
    def __init__(self, iterations):
        self.iterations = iterations
    
    def getStrategy(self, player):
        for a in range(3):
            if player.regretSum[a] > 0:
                player.strategy[a] = player.regretSum[a]
            else:
                player.strategy[a] = 0
        normalizingSum = sum(player.strategy)
        for a in range(3):
            if normalizingSum > 0:
                player.strategy[a] /= float(normalizingSum)
            else:
                player.strategy[a] = 1.0 / 3
            player.strategySum[a] += player.strategy[a]
            
    def getAction(self,strategy):
        r = random.random()
        a = 0
        cumulativeProbability = 0.0
        while a < (3):
            cumulativeProbability += strategy[a]
            if r < cumulativeProbability:
                return a
            a+=1
        
    def train(self, p1, p2):
        actionUtility = [0]*3
        for i in xrange(self.iterations):
            # Get regret-matched mixed strategy actions
            self.getStrategy(p1)
            myAction = self.getAction(p1.strategy)
            otherAction = self.getAction(p2.strategy)
            
            # Compute Action Utilities
            actionUtility[otherAction] = 0
            if otherAction == 3 - 1:
                actionUtility[0] = 1
            else:
                actionUtility[otherAction+1] = 1
            if otherAction == 0:
                actionUtility[3-1] = -1
            else:
                actionUtility[otherAction-1] = -1
            
            # Accumulate Action Regrets
            for a in range(3):
                p1.regretSum[a] += (actionUtility[a] - actionUtility[myAction])
            ###################################################################
            # Player 2
            ###################################################################
            self.getStrategy(p2)
            myAction = self.getAction(p2.strategy)
            otherAction = self.getAction(p1.strategy)
            
            # Compute Action Utilities
            actionUtility[otherAction] = 0
            if otherAction == 3 - 1:
                actionUtility[0] = 1
            else:
                actionUtility[otherAction+1] = 1
            if otherAction == 0:
                actionUtility[3-1] = -1
            else:
                actionUtility[otherAction-1] = -1
            
            # Accumulate Action Regrets
            for a in range(3):
                p2.regretSum[a] += (actionUtility[a] - actionUtility[myAction])
    
    def getAverageStrategy(self,player):
        normalizingSum = sum(player.strategy)
        for a in range(3):
            if normalizingSum > 0:
                player.avgStrategy[a] = player.strategySum[a] / float(normalizingSum)
            else:
                player.avgStrategy[a] = 1.0 / 3
        for a in range(3):
            player.avgStrategy[a] /= self.iterations
            print actions[a], ":", player.avgStrategy[a]
            
    def Expected_Utility(self,p1,p2):
        utilities = [[0,-1,1],[1,0,-1],[-1,1,0]]
        total = 0
        for i in range(len(p1)):
            for j in range(len(p2)):
                total += p1[i]*p2[j]*utilities[i][j]
        print "Expected Utility for Player: ", total
        
            
            
p1 = RPS_Player()
p2 = RPS_Player([.4,.3,.3])
x = RegretMatching_RPC(1000000)
x.train(p1,p2)
x.getAverageStrategy(p1)
x.getAverageStrategy(p2)
x.Expected_Utility(p1.avgStrategy,p2.avgStrategy)
