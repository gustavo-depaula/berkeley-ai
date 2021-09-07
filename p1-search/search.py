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
    return [s, s, w, s, w, w, s, w]


def genericProblemSearch(problem, fringeDataStructure):
    startingNode = problem.getStartState()
    visitedNodes = set()
    visitNode = lambda node: visitedNodes.add(node)
    hasVisitedNode = lambda node: node in visitedNodes

    isTargetNode = lambda node: problem.isGoalState(node)
    getSuccessors = lambda node: problem.getSuccessors(node)
    getNext = lambda node: [s for s in getSuccessors(node) if not hasVisitedNode(s[0])]

    getNode = lambda t: t[0]
    getAction = lambda t: t[1]

    solution = None
    fringe = fringeDataStructure()
    fringe.push([(startingNode, "None", 1)])

    while not fringe.isEmpty():
        candidate = fringe.pop()
        node = getNode(candidate[-1])

        if isTargetNode(node):
            solution = candidate[1:]
            break

        if not hasVisitedNode(node):
            visitNode(node)

            ns = getNext(node)
            for n in ns:
                newCandidate = candidate[:]
                newCandidate.append(n)
                fringe.push(newCandidate)

    moves = [getAction(n) for n in solution]
    return moves


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return genericProblemSearch(problem, util.Stack)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return genericProblemSearch(problem, util.Queue)


def getBackwardsCosts(candidate):
    getCost = lambda t: t[2]
    allCosts = [getCost(t) for t in candidate]
    return sum(allCosts)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    def priorityFunction(candidate):
        return getBackwardsCosts(candidate)

    class PriorityQueue(util.PriorityQueueWithFunction):
        def __init__(self):
            util.PriorityQueueWithFunction.__init__(self, priorityFunction)

    return genericProblemSearch(problem, PriorityQueue)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    def priorityFunction(candidate):
        backwardCost = getBackwardsCosts(candidate)

        node = candidate[-1][0]
        forwardCost = heuristic(node, problem)
        return backwardCost + forwardCost

    class PriorityQueue(util.PriorityQueueWithFunction):
        def __init__(self):
            util.PriorityQueueWithFunction.__init__(self, priorityFunction)

    return genericProblemSearch(problem, PriorityQueue)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
