
from collections import deque
import random
from math import sqrt
from itertools import permutations

def getInput():
    input_file = open('input.txt', 'r')
    input_string = input_file.read()
    input_array = input_string.split(',')
    input_file.close()
    
    return input_array

def inputAsInt(input_list):
    temp_array = []
    for element in input_list:
        element = element.strip()
        if element == '_':
            element_as_int = 0
        else:
            element_as_int = int(element)
        temp_array.append(element_as_int)
    return temp_array

def getHM(game_state_array, goal_state):
        #gets the Manhatten distance to the goal state from the given puzzle state
        goal_index = 0
        current_state_index = 0        
        

        total_h = 0
        for num in goal_state:
            current_state_index = game_state_array.index(num)
            total_h += ((abs((current_state_index%3)-(goal_index%3)))+(abs((current_state_index//3)-(goal_index//3))))
            
            goal_index += 1
            
        return total_h

def getHE(game_state_array, goal_state):
        #gets the euclidean distance to the goal state from the given puzzle state
        goal_index = 0
        current_state_index = 0        

        total_h = 0
        for num in goal_state:
            current_state_index = game_state_array.index(num)
            total_h += (sqrt(((abs((current_state_index%3)-(goal_index%3)))**2)+((abs((current_state_index//3)-(goal_index//3)))**2)))
            
            goal_index += 1
            
        return total_h

def isSolvable(game_state_list):
    #determines if a puzzle is solvable given the initial state
    total_inversions = 0
    
    for index in range(0,9):
        for sub_index in range(index+1,9):
            if (game_state_list[index] != 0 and game_state_list[sub_index] != 0):
                if game_state_list[index] > game_state_list[sub_index]:
                    total_inversions += 1
                
    if total_inversions%2 == 1:
        return False
    
    return True


class puzzleGraph:
    

    def __init__(self, shuffle = False, force_solvable = False):
        #initialize puzzle from given input file
        state_list = inputAsInt(getInput())
        if shuffle:
            random.shuffle(state_list)
            
        if force_solvable:
            while((isSolvable(state_list)) == False):
                  random.shuffle(state_list)

        self.game_state_start = tuple(state_list)
        self.game_state_current = self.game_state_start
        self.game_state_previous = self.game_state_current
        
        self.traceback_dict = {}
        self.visited = set()
        
        self.goal_states = [(0,1,2,3,4,5,6,7,8)]
           
      


    def goalTest(self):
       #determine if the puzzle is solved
        for i in range(0,9):
            if self.game_state_current[i] != i:
                return False
        return True

    def moveRight(self):
        #imitates moving the puzzle to the right, returns new state of puzzle
        blank_index = self.game_state_current.index(0)
        temp_array = list(self.game_state_current)
        if blank_index%3 == 0:
            return self.game_state_current
        temp_array[blank_index] = temp_array[blank_index-1]
        temp_array[blank_index-1] = 0
        return tuple(temp_array)

    def moveUp(self):
        #imitates moving the puzzle up, returns new state of puzzle
        blank_index = self.game_state_current.index(0)
        temp_array = list(self.game_state_current)
        if blank_index//3 == 2:
            return self.game_state_current
        temp_array[blank_index] = temp_array[blank_index+3]
        temp_array[blank_index+3] = 0
        return tuple(temp_array)

    def moveLeft(self):
        #imitates moving the puzzle to the left, returns new state of puzzle
        blank_index = self.game_state_current.index(0)
        temp_array = list(self.game_state_current)
        
        if blank_index%3 == 2:
            return self.game_state_current
        temp_array[blank_index] = temp_array[blank_index+1]
        temp_array[blank_index+1] = 0
        return tuple(temp_array)

    def moveDown(self):
        #imitates moving the puzzle down, returns new state of puzzle
        blank_index = self.game_state_current.index(0)
        temp_array = list(self.game_state_current)
        if blank_index//3 == 0:
            return self.game_state_current
        temp_array[blank_index] = temp_array[blank_index-3]
        temp_array[blank_index-3] = 0
        return tuple(temp_array)


    def expand(self):
        #expands the current node, adding the subsequent states and associated actions to the fringe
        temp_fringe = []
        
        
        if self.game_state_current != self.moveLeft():
            temp_fringe.append((self.moveLeft(), ' L'))
        
        if self.game_state_current != self.moveRight():    
            temp_fringe.append((self.moveRight(), ' R'))

        if self.game_state_current != self.moveUp():   
            temp_fringe.append((self.moveUp(), ' U'))
            
        if self.game_state_current != self.moveDown():
            temp_fringe.append((self.moveDown(), ' D'))
    
        return temp_fringe
    
    
   
    def solvePuzzleDFS(self):
        #solves the given puzzle with a Depth First Search policy
        visited = set()
        fringe = deque()    
        fringe.append((self.game_state_start, '')) 
        expansion = []
        state_path_tuple = ()
        num_expanded = 0

        while len(fringe) != 0:

            state_path_tuple = fringe.pop()
            self.game_state_current = state_path_tuple[0]
            if self.game_state_current not in visited:

                if self.goalTest():
                    
                    return state_path_tuple[1]
                
                expansion = self.expand()
                num_expanded += 1
                for state in expansion:
                    fringe.append((state[0], state_path_tuple[1] + state[1]))   
                visited.add(self.game_state_current)
                
        return 'Unsolvable Start State'



    def solvePuzzleBFS(self):
        #solves the given puzzle with a Breadth First Search policy
        visited = set()
        fringe = deque()    
        fringe.append((self.game_state_start, '')) 
        expansion = []
        state_path_tuple = ()
        num_expanded = 0

        while len(fringe) != 0:

            state_path_tuple = fringe.popleft()
            self.game_state_current = state_path_tuple[0]
            if self.game_state_current not in visited:

                if self.goalTest():
                    return state_path_tuple[1]
                
                expansion = self.expand()
                num_expanded += 1
                for state in expansion:
                   
                    fringe.append((state[0], state_path_tuple[1] + state[1]))   
                visited.add(self.game_state_current)
        return 'Unsolvable start state'



    def solvePuzzleUCS(self):
        #solves the given puzzle with a Uniform Cost Search policy
        visited = set()
        fringe = {}   
        fringe[0] = deque([(self.game_state_start, '')])
        expansion = []
        state_path_tuple = ()
        current_cost = 0
        min_cost = 0
        num_expanded = 0

        while len(fringe) != 0:

            min_cost = min(fringe)
            
            state_path_tuple = fringe[min_cost].pop()
            if len(fringe[min_cost]) == 0:
                del fringe[min_cost]
                
            self.game_state_current = state_path_tuple[0]
            current_cost = min_cost
            
            if self.game_state_current not in visited:

                if self.goalTest():
                    return state_path_tuple[1]
                
                expansion = self.expand()
                num_expanded += 1
                for state in expansion:
                   if (current_cost+1 in fringe):
                       fringe[current_cost+1].append((state[0], state_path_tuple[1] + state[1]))
                   else:
                        fringe[current_cost+1] = deque([(state[0], state_path_tuple[1] + state[1])])
                visited.add(self.game_state_current)
        
        return 'Unsolvable start state'


    def heuristicTest(self, game_state_array, heuristic_function):
        
        
        return heuristic_function(game_state_array, self.goal_states[0])


    
    
    def solvePuzzleA(self, hFunc = getHM):
        #solves the given puzzle with a A* Search policy with the given heuristic (in this case either manhattan distance (default), or Euclidean Distance))
        visited = set()
        fringe = {}  
        current_cost = 0
        current_h_value = self.heuristicTest(self.game_state_start, hFunc)
        
        current_estimated_cost = current_h_value + current_cost
        fringe[current_h_value] = deque([[(self.game_state_start, ''), current_cost]])
        expansion = []
        state_path_tuple = ()
        
        num_expanded =0
        min_cost = 0

        while len(fringe) != 0:

            min_cost = min(fringe)
            
            state_path_and_cost_list = fringe[min_cost].pop()
            state_path_tuple = state_path_and_cost_list[0]
            current_cost =  state_path_and_cost_list[1]           

            if len(fringe[min_cost]) == 0:
                del fringe[min_cost]
                
            self.game_state_current = state_path_tuple[0]
            
            
            if self.game_state_current not in visited:

                if self.goalTest():
                    return state_path_tuple[1]
                
                expansion = self.expand()
                num_expanded += 1
                for state in expansion:
                  
                   current_h_value = self.heuristicTest(state[0], hFunc)
                   current_estimated_cost = current_h_value + current_cost + 1
                   if (current_estimated_cost in fringe):
                       fringe[current_estimated_cost].append([(state[0], state_path_tuple[1] + state[1]), current_cost+1])
                   else:
                        fringe[current_estimated_cost] = deque([[(state[0], state_path_tuple[1] + state[1]), current_cost+1]])
                visited.add(self.game_state_current)
        
        return 'Unsolvable start state'
    

def main():
    
    input_loop = True
    user_finished = True
    user_input = ''
    scramble_input_state = True
    force_solvable_state = True
    
        
    gr = puzzleGraph()  
 
    print('\n')
    print('THE DFS SOLUTION IS: \n  {0}'.format(gr.solvePuzzleDFS()))
    print('THE BFS SOLUTION IS: \n  {0}'.format(gr.solvePuzzleBFS()))
    print('THE UCS SOLUTION IS: \n  {0}'.format(gr.solvePuzzleUCS()))
    print('THE A* SOLUTION (WITH MANHATTEN DISTANCE HEURISTIC) IS: \n  {0}'.format(gr.solvePuzzleA()))  
    print('THE A* SOLUTION (WITH EUCLIDEAN DISTANCE HEURISTIC IS: \n  {0}'.format(gr.solvePuzzleA(getHE)))
    print('')        

            
        

    
  

    return



if __name__ == "__main__":
    main()
