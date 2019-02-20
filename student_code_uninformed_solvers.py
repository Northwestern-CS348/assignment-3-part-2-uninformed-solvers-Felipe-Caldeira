
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #breakpoint() 
        # If this GameState's state is the winning condition, return True
        if self.currentState.state == self.victoryCondition:
            return True
        
        # Mark the current state as visited so that we don't explore it again in the future!
        self.visited[self.currentState] = True

        # Get the list of potential moves
        moves_list = self.gm.getMovables() if self.gm.getMovables() else []
        
        # If there are more children to explore, let's explore the next one
        while (self.currentState.nextChildToVisit < len(moves_list)) :
            move_taken = moves_list[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1 # Next time we come back to this GS, let's explore the next potential move
            self.gm.makeMove(move_taken)
            new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move_taken)
            
            # Assert parent/child relationship
            self.currentState.children.append(new_state)
            new_state.parent = self.currentState

            # Let's move to this child officially! Return False because we're not done.
            # Let's only move to it if we haven't aleady visited it though.
            if new_state not in self.visited:
                self.currentState = new_state
                return False
            
            # If we HAVE visited it, then don't move to it. Instead, undo the move and continue to check the next child.
            else:
                self.gm.reverseMove(move_taken)
                continue
        
        # If there are no more children to explore, add current GS to 'visited', undo the required move, and go back to parent node!
        self.visited[self.currentState] = True
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState = self.currentState.parent
        return False



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #breakpoint() 
              

        def enqueue(GS):
            self.visited["queue"].append(GS)

        def dequeue():
            GS = self.visited["queue"].pop(0)
            self.visited["visited"].append(GS)
            return GS

        def visited(GS):
            return (GS in self.visited["visited"])
       
        def required_steps(GS):
            steps = []
            curr_GS = self.currentState
            while (curr_GS.parent):
                steps.append(curr_GS.requiredMovable)
                curr_GS = curr_GS.parent
            return steps
        
        def Main():
            self.currentState = dequeue()
            #print(self.currentState.state)
        
            req_steps = required_steps(self.currentState)
        
            for step in self.visited["currSteps"]:
                self.gm.reverseMove(step)

            for step in reversed(req_steps):
                self.gm.makeMove(step)

            # If this GameState's state is the winning condition, return True
            if self.currentState.state == self.victoryCondition:
                return True

            # Get the list of potential moves
            moves_list = self.gm.getMovables() if self.gm.getMovables() else []

            # Generate all children
            for move_taken in moves_list:
                self.gm.makeMove(move_taken)
                new_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move_taken)
            
                # Assert parent/child relationship
                self.currentState.children.append(new_state)
                new_state.parent = self.currentState

                # Add it to queue if not seen before and not in queue already
                if ((not visited(new_state)) and (not new_state in self.visited["queue"])): 
                    enqueue(new_state)

                # Undo the step to go back to currentState
                self.gm.reverseMove(move_taken)
        
            # Store the steps so we can undo them for the next GameState explored.
            self.visited["currSteps"] = req_steps
            return False
        
        
        # If this is the first step, initialize the queue
        if (not self.currentState.parent) and (not self.currentState.children):
            if self.currentState.state == self.victoryCondition: return True
            self.visited["queue"] = [self.currentState]
            self.visited["visited"] = [self.currentState]
            self.visited["currSteps"] = []
            Main()
        
        
        return Main()






















