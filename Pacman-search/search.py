# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

#Helper function to store the path traversed by the algorithm
def actions (goal, path):
    action = []
    node = goal
    while(node[1]):
        action.append(node[1])
        node = path[node]
    action.reverse()
    return action

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    front = util.Stack()
    front.push((problem.getStartState(), "", 0))
    explored = []
    path = {}
    while front:
        node = front.pop()
        explored.append(node[0])
        if problem.isGoalState(node[0]):
            return actions(node, path)
        successors = problem.getSuccessors(node[0])
        for successor in successors:
            if (successor[0] not in explored):
               path[successor] = node
               front.push(successor)
    return "no path found"
    #util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    front = util.Queue()
    front.push((problem.getStartState(), "", 0))
    explored = []
    path = {}
    while front:
        node = front.pop()
        explored.append(node[0])
        if problem.isGoalState(node[0]):
            return actions(node, path)
        successors = problem.getSuccessors(node[0])
        for successor in successors:
            if (successor[0] not in explored) and (successor[0] not in [x[0] for x in front.list]):
               path[successor] = node
               front.push(successor)
    return "no path found"
    #util.raiseNotDefined()


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    front = util.PriorityQueue()
    front.push((problem.getStartState(), []),0)
    statefront =[(problem.getStartState)]
    path = {}
    tCost = {}
    explored = []
    tCost[problem.getStartState()] = 0
    while front:
        node = front.pop()
        statefront.pop()
        explored.append(node[0])
        if problem.isGoalState(node[0]):
            return actions(node, path)
        successors = problem.getSuccessors(node[0])
        for successor in successors:
            if (successor[0] not in explored):
                newCost = node[2] + successor[2]
                tCost[successor[0]] = newCost
                front.push((successor[0], successor[1], newCost))
                statefront.append(successor[0])
                path[(successor[0], successor[1], newCost)] = node
    return "no path found"
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    front = util.PriorityQueue()
    front.push((problem.getStartState(), "", 0), 0)
    statefront = [problem.getStartState]
    path = {}
    explored =[]
    tCost = {}
    tCost[problem.getStartState()] = 0
    while front:
        node = front.pop()
        statefront.pop()
        explored.append(node[0])
        if problem.isGoalState(node[0]):
            return actions(node, path)
        successors = problem.getSuccessors(node[0])
        for successor in successors:
            if ((successor[0] not in explored) and (successor[0] not in statefront)):
                pCost = successor[2] + node[2]
                dCost = heuristic(successor[0],problem)
                front.push((successor[0],successor[1],pCost), pCost + dCost)
                tCost[successor[0]] = pCost
                statefront.append(successor[0])
                path[(successor[0], successor[1], pCost)] = node
            elif ((successor[0] in statefront) and (tCost[successor[0]] > successor[2] + node[2])):
                pCost = successor[2] + node[2]
                dCost = heuristic(successor[0],problem)
                front.push((successor[0],successor[1],pCost), pCost + dCost)
                tCost[successor[0]] = pCost
                statefront.append(successor[0])
                path[(successor[0], successor[1], pCost)] = node
    return "no solutions"
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
