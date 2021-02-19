import random
import numpy as np

class QLearning:
    def __init__(self,nbAction:int,nbState:int,gamma:float=0.9,learningRate:float=0.1):
        """
        nbParam : Number of action in state
        gamma : Reward power [0;1] (0.1 long path priority, 0.9 short path priority)
        learningRate : Learning power [0;1]
        nbState : The number of states
        """
        #Number of action
        self.nbAction = nbAction
        #Qtable
        self.QTable = np.zeros((nbState,nbAction))
        #gamma
        self.gamma = gamma
        #Learning Rate
        self.learningRate = learningRate
        #Old action
        self.oldAction = -1
        #New action
        self.newAction = -1
    def takeAction(self,state:int,epsilon:int):
        """
        state : Current State
        epsilone : exploration value [0;1]
        Return action
        """
        #Epsilon greedy
        if random.uniform(0,1) < epsilon:   #Exploration
            #Get random action
            action = random.randint(0,self.nbAction-1)
        else:   #Greedy action
            #Get the action with the highest Value Function in our state
            action = np.argmax(self.QTable[state])
        #Change the actions order
        self.oldAction = self.newAction
        self.newAction = action
        return action
    def updateQFunction(self,currentState:str,oldState:str,reward:int):
        """
        """
        #On prend la meilleur option pour le prochain etat
        self.takeAction(currentState,0.0)
        #On prend la difference entre l'etat+1 et l'etat de base
        a = self.QTable[currentState][self.newAction] - self.QTable[oldState][self.oldAction]
        #on le multiplie au gamma
        a = self.gamma*a
        #on additionne le reward
        a = reward + a
        #on le multiplie au learning rate
        a = self.learningRate*a
        #on ajoute la difference
        self.QTable[oldState][self.oldAction] += a
