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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        # Giving equal weightage to food and ghost - Assume 10.0
        foodWeightage = 10.0
        ghostWeightage = 10.0

        # Getting score for Successor game state
        value = successorGameState.getScore()

        # Getting distance to ghost from next position of Pacman and reducing the weightage/distance
        # from total score
        ghostDistance = manhattanDistance(newPos, newGhostStates[0].getPosition())
        if ghostDistance > 0:
            value = value - ghostWeightage / ghostDistance

        # Getting minimum distance to food from next position of Pacman and adding the weightage/minimum distance
        # to total score
        foodDistance = []
        for food in newFood.asList():
            dist = manhattanDistance(newPos, food)
            foodDistance.append(dist)

        # If food points are available, calculate weightage to nearest food point
        if len(foodDistance):
            value = value + foodWeightage / min(foodDistance)

        return value

def scoreEvaluationFunction(currentGameState):
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

numNodesMM = 0
class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        #Returns the minimax action from the current gameState using self.depth and self.evaluationFunction.
        #Returns the total number of agents in the game
        totalAgents = gameState.getNumAgents() - 1

        def minimax_MAX(gameState,curDepth):
            legalPacmanMoves = gameState.getLegalActions()

            #Termination condition for Recursion - When we reached the depth of the tree/won/lost/no valid moves
            if (curDepth == self.depth) or (gameState.isWin() == True) or (gameState.isLose() == True) or (len(legalPacmanMoves) == 0):
                return self.evaluationFunction(gameState), None

            #Successor List - contains successor cost and action
            succCost = []
            for action in legalPacmanMoves:
                #Calculate Succossor states
                successorState = gameState.generateSuccessor(0,action)
                global numNodesMM
                numNodesMM += 1
                #Call Min for Max's chosen move
                succCost.append((minimax_MIN(successorState,1,curDepth), action))
            return max(succCost)

        def minimax_MIN(gameState,agentIndex,curDepth):
            legalGhostMoves = gameState.getLegalActions(agentIndex)

            # Termination condition for Recursion - When no legal moves exist or if we have completely explored the depth of the tree
            if (curDepth == self.depth) or (len(legalGhostMoves) == 0):
                return self.evaluationFunction(gameState), None

            # Successor List
            succCost = [] 
            for action in legalGhostMoves:
                successorState = gameState.generateSuccessor(agentIndex, action)
                # To calculate number of nodes expanded
                global numNodesMM
                numNodesMM+=1
                # Exhausted all possibilities for Min - Max's turn
                if agentIndex == totalAgents:
                    succCost.append(minimax_MAX(successorState, curDepth + 1))
                else:
                    #Evaluating max's move
                    succCost.append(minimax_MIN(successorState, agentIndex + 1,curDepth))
            return min(succCost)
        
        #Assume Pacman moves first - MAX
        move = minimax_MAX(gameState, 0)
        #print "Number of nodes expanded: ", numNodesMM
        return move[1]

numNodesAB = 0
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        totalAgents = gameState.getNumAgents()
        def pacmanMove_MAX(state, curDepth, alpha, beta):
            legalPacmanMoves = state.getLegalActions(0)

            bestMove = None
            maxCost = -9999
            for move in legalPacmanMoves:
                # generate successor state
                succState = state.generateSuccessor(0, move)
                global numNodesAB
                numNodesAB += 1
                #If generated move leads to terminal state then return score
                if(succState.isLose() or succState.isWin()):
                    cost = self.evaluationFunction(succState)
                    if cost > maxCost:
                        maxCost = cost
                        bestMove = move
                    if maxCost > beta: #Return maxCost if less than beta
                        return maxCost
                    alpha = max(alpha, maxCost)
                    continue
                cost = ghostMove_MIN(succState, curDepth, alpha, beta, 1)
                #take the best action till now
                if cost > maxCost:
                    maxCost = cost
                    bestMove = move
                if maxCost > beta:
                    return maxCost
                alpha = max(alpha, maxCost)

            #If there are no valid moves, then return cost and action if depth is 1, else return cost
            if(curDepth == 1):
                return maxCost, bestMove
            else:
                return maxCost

        def ghostMove_MIN(state, curDepth, alpha, beta, agentIndex):
            minCost = 9999
            # If the last agent has made the move
            if(agentIndex == totalAgents):
                #If we have reached the complete depth then return cost of current state
                if(curDepth == self.depth):
                    return self.evaluationFunction(state)
                else:
                    return pacmanMove_MAX(state, curDepth+1, alpha, beta)
            else:
                legalGhostMoves = state.getLegalActions(agentIndex)

                for move in legalGhostMoves:
                    #Succossor state
                    succState = state.generateSuccessor(agentIndex, move)
                    global numNodesAB
                    numNodesAB += 1
                    #If generated move leads to terminal state then return score
                    if(succState.isLose() or succState.isWin()):
                        cost = self.evaluationFunction(succState)
                        if cost < minCost:
                            minCost = cost
                        if minCost < alpha: #Return minCost if less than alpha
                            return minCost
                        beta = min(beta, minCost)
                        continue
                    #If not terminal state, explore the next ghost move
                    cost = ghostMove_MIN(succState, curDepth, alpha, beta, agentIndex + 1)
                    if cost < minCost:
                        minCost = cost
                    if minCost < alpha:
                        return minCost
                    beta = min(beta, minCost)
            return minCost

        #Assume Pacman moves first - MAX
        move = pacmanMove_MAX(gameState, 1, -100000, 100000)
        #print "Number of nodes expanded: ", numNodesAB
        return move[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectiMax(state,curDepth,agentIndex):

            totalAgents = state.getNumAgents()
            if agentIndex == totalAgents and (curDepth == self.depth):
                return self.evaluationFunction(state)
            #Finding the cost always happens from the end so traversing till the end depth.
            elif agentIndex == totalAgents and (curDepth != self.depth):
                return expectiMax(state,curDepth+1,0)
            else:
                legalPacmanMoves = state.getLegalActions(agentIndex)
                #If no actions pending then return evaluation function
                if len(legalPacmanMoves) == 0:
                    return self.evaluationFunction(state)

                # Append successor states
                succState = []
                for move in legalPacmanMoves:
                    succstate = state.generateSuccessor(agentIndex,move)
                    succState.append((expectiMax(succstate,curDepth,agentIndex+1)))

                # If last agent, return result of successor states
                if agentIndex == 0:
                    return max(succState)
                else:
                    # Returning probability as per expectimax algorithm 
                    return float(sum(succState))/float(len(succState))

        #Calculating legal actions
        legalMoves = gameState.getLegalActions()
        maxVal = -100000
        for move in legalMoves:
            # Find the action  which returns maximum value
            val = expectiMax(gameState.generateSuccessor(0,move),1,1)
            if val > maxVal:
                maxVal = val
                bestMove = move
        return bestMove
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction