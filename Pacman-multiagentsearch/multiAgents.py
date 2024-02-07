# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #Initialize
        score = 0.0

        #Extract current food positions
        currentFood = currentGameState.getFood().asList()
        p1, p2 = newPos
        
        for g1 in range(len(newGhostStates)):
            a, b = newGhostStates[g1].getPosition()
            movesAway = abs(p1-a) + abs(p2-b)
            
            #Food
            if newPos in currentFood:
                score += 1
                
            #Obstacle
            if currentGameState.hasWall(p1, p2):
                score -= 2
                
            #Ghost
            if movesAway <= newScaredTimes[g1]:
                score += movesAway
            
            #Move
            if movesAway < 2:
                score -= 2
            
            #Evaluate food distance
            distanceToFood = []
            for f1 in currentFood:
                howFar = abs(p1-f1)
                distanceToFood.append(howFar)
            score -= 0.1 * min(distanceToFood)

        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        allowed_Action = gameState.getLegalActions(0)
        next_step = [gameState.generateSuccessor(0, action) for action in allowed_Action]
        max_fun = -float('inf')
        goal_state = 0
        for i in range(len(next_step)):
            aval = self.value(next_step[i], 1, 0)
            if aval > max_fun:
                max_fun = aval
                goal_state = i
        
        return allowed_Action[goal_state]
        
    def MAXvalue(self, gameState, agentIndex, depthSoFar):
        allowed = gameState.getLegalActions(agentIndex)
        next = [gameState.generateSuccessor(agentIndex, action) for action in allowed]
        i = -float('inf')
        for n_step in next:
            i = max(i, self.value(n_step, 1, depthSoFar))
        return i
        
    def MINvalue(self, gameState, agentIndex, depthSoFar):
        allowed = gameState.getLegalActions(agentIndex)
        next = [gameState.generateSuccessor(agentIndex, action) for action in allowed]
        i = float('inf')
        for n_step in next:
            if agentIndex + 1 == gameState.getNumAgents():
                i = min(i, self.value(n_step, 0, depthSoFar + 1))
            else:
                i = min(i, self.value(n_step, agentIndex + 1, depthSoFar))
        return i
        
    def value(self, gameState, agentIndex, depthSoFar):
        
        "If requisite no. of searches complete, evaluation function"
        if depthSoFar == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        "If agentIndex is 0, perform MAX"
        if agentIndex == 0:
            return self.MAXvalue(gameState, agentIndex, depthSoFar)
        "Else (if agentindex > 0), perform MIN"
        if agentIndex > 0:
            return self.MINvalue(gameState, agentIndex, depthSoFar)
        
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float('inf')
        beta = float('inf')
        allowed_actions = gameState.getLegalActions(0)
        next = [gameState.generateSuccessor(0, action) for action in allowed_actions]
        maxValue = -float('inf')
        goal_state = 0
        for x in range(len(next)):
            actionValue = self.value(next[x], 1, 0, alpha, beta)
            if actionValue > maxValue:
                maxValue = actionValue
                goal_state = x
                alpha = actionValue
        
        return allowed_actions[goal_state]
    def MAXvalue(self, gameState, agentIndex, depthSoFar, alpha, beta):
        allowed = gameState.getLegalActions(agentIndex)
        i = -float('inf')
        for action in allowed:
            n_step = gameState.generateSuccessor(agentIndex, action)
            i = max(i, self.value(n_step, 1, depthSoFar, alpha, beta))
            if i > beta:
                return i
            alpha = max(alpha, i)
        return i
        
    def MINvalue(self, gameState, agentIndex, depthSoFar, alpha, beta):
        allowed = gameState.getLegalActions(agentIndex)
        i = float('inf')
        for action in allowed:
            n_step = gameState.generateSuccessor(agentIndex, action)
            if agentIndex + 1 == gameState.getNumAgents():
                i = min(i, self.value(n_step, 0, depthSoFar + 1, alpha, beta))
            else:
                i = min(i, self.value(n_step, agentIndex + 1, depthSoFar, alpha, beta))
            if i < alpha:
                return i
            beta = min(beta, i)
        return i
        
    def value(self, gameState, agentIndex, depthSoFar, alpha, beta):
        
        "If requisite no. of searches complete, evaluation function"
        if depthSoFar == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        "If agentIndex is 0, perform MAX"
        if agentIndex == 0:
            return self.MAXvalue(gameState, agentIndex, depthSoFar, alpha, beta)
        "Else (if agentindex > 0), perform MIN"
        if agentIndex > 0:
            return self.MINvalue(gameState, agentIndex, depthSoFar, alpha, beta)
    
        
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        allowed_actions = gameState.getLegalActions(0)
        next = [gameState.generateSuccessor(0, action) for action in allowed_actions]
        maxValue = -float('inf')
        goal_state = 0
        for i in range(len(next)):
            actionValue = self.value(next[i], 1, 0)
            if actionValue > maxValue:
                maxValue = actionValue
                goal_state = i
        
        return allowed_actions[goal_state]
        
    def MAXvalue(self, gameState, agentIndex, depthSoFar):
        allowed = gameState.getLegalActions(agentIndex)
        next = [gameState.generateSuccessor(agentIndex, action) for action in allowed]
        i = -float('inf')
        for n_step in next:
            i = max(i, self.value(n_step, 1, depthSoFar))
        return i
        
    def EXPvalue(self, gameState, agentIndex, depthSoFar):
        allowed = gameState.getLegalActions(agentIndex)
        next = [gameState.generateSuccessor(agentIndex, action) for action in allowed]
        i = 0.0
        for n_step in next:
            if agentIndex + 1 == gameState.getNumAgents():
                i += self.value(n_step, 0, depthSoFar + 1)
            else:
                i += self.value(n_step, agentIndex + 1, depthSoFar)
        return i/len(next)
        
    def value(self, gameState, agentIndex, depthSoFar):
        
        "If requisite no. of searches complete, evaluation function"
        if depthSoFar == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        "If agentIndex is 0, perform MAX"
        if agentIndex == 0:
            return self.MAXvalue(gameState, agentIndex, depthSoFar)
        "Else (if agentindex > 0), perform EXP"
        if agentIndex > 0:
            return self.EXPvalue(gameState, agentIndex, depthSoFar)

        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    next = currentGameState.getPacmanPosition()
    n_food = [food for food in currentGameState.getFood().asList() if food]
    ghost = currentGameState.getGhostStates()
    scared = [ghostState.scaredTimer for ghostState in ghost]
    
    ghost_distance = min(manhattanDistance(next, ghost.configuration.pos) for ghost in ghost)
    closest_food_distance = min(manhattanDistance(next, nextFood) for nextFood in n_food) if n_food else 0
    scared_time = min(scared)

    left_food = -len(n_food)
    
    ghost_dis = -2 / (ghost_distance + 1) if scared_time == 0 else 0.5 / (ghost_distance + 1)
    food_dis = 0.5 / (closest_food_distance + 1)
    
    p_food = scared_time * 0.5
    score = currentGameState.getScore() * 0.5

    return left_food + ghost_dis + food_dis + p_food + score    
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
