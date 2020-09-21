import sys
import copy
import time
from queue import PriorityQueue

class State:
    def __init__(self, left, right, parent, depth):
        self.left = list(left)
        self.right = list(right)
        self.parent = parent
        self.depth = depth
    def __lt__(self,other):
        return self.depth < other.depth

def getCost(state):
    cost = 0
    ani = 0
    if(goal_state.left[2]==1):
        ani+= state.left[0]
        ani += state.left[1]
    else:
        ani+= state.right[0]
        ani+= state.right[1]
    if(ani <= 2):
        cost = 1
    else:
        cost+= (ani-2)*2 + 1
    return cost


def checkHash(state):
    temp = ""
    for x in range(3):
        temp += str(state.left[x])
        temp += str(state.right[x])
    if not temp in hashtable:
        return False
    else:
        return True
def addHash(state):
    temp = ""
    for x in range(3):
        temp += str(state.left[x])
        temp += str(state.right[x])
    hashtable[temp] = "1"
def printFrontier():
    for x in range(len(frontier)):
        print(x)
        print(frontier[x].left)
        print(frontier[x].right)
        print("\n")

def action(temp, left, nleft, right, nright, boat):
    # state = copy.deepcopy(temp)
    state = State(temp.left, temp.right, temp, temp.depth+1)
    # state.parent = temp
    state.left[left] += nleft
    state.right[right] += nright
    if(boat == 0):
        state.left[2]=0
        state.right[2]=1
    else:
        state.left[2]=1
        state.right[2]=0

    if(valid(state) == True):
            if(checkHash(state)==False):
                addHash(state)
                frontier.append(state)
def actionDFS(temp, left, nleft, right, nright, boat):
    # state = copy.deepcopy(temp)
    state = State(temp.left, temp.right, temp, temp.depth+1)
    # state = copy.copy(temp)
    state.parent = temp
    state.left[left] += nleft
    state.right[right] += nright
    if(boat == 0):
        state.left[2]=0
        state.right[2]=1
    else:
        state.left[2]=1
        state.right[2]=0

    if(valid(state) == True):
            if(checkHash(state)==False):
                addHash(state)
                frontier.insert(0+buffer,state)
def actionASTAR(temp, left, nleft, right, nright, boat):
    # state = copy.deepcopy(temp)
    state = State(temp.left, temp.right, temp, temp.depth+1)
    # state = copy.copy(temp)
    state.parent = temp
    state.left[left] += nleft
    state.right[right] += nright
    if(boat == 0):
        state.left[2]=0
        state.right[2]=1
    else:
        state.left[2]=1
        state.right[2]=0

    if(valid(state) == True):
            if(checkHash(state)==False):
                addHash(state)
                state.depth += getCost(state)
                q.put((state.depth, state))


def expandNode(state):
    special = State(state.left, state.right, state, state.depth+1)
    if(state.left[2]==1):
        action(state, 0, -1, 0, 1, 0)
        action(state, 0, -2, 0, 2, 0)
        action(state, 1, -1, 1, 1, 0)
        special.left[1] -= 1
        special.right[1] += 1
        special.left[0] -= 1
        special.right[0] += 1
        special.left[2] = 0
        special.right[2] = 1
        if(valid(special) == True):
            if(checkHash(special)==False):
                special.parent = state
                addHash(special)
                frontier.append(special)
        action(state, 1, -2, 1, 2, 0)
        
    else:
        action(state, 0, 1, 0, -1, 1)
        action(state, 0, 2, 0, -2, 1)
        action(state, 1, 1, 1, -1, 1)
        special.left[1] += 1
        special.right[1] -= 1
        special.left[0] += 1
        special.right[0] -= 1
        special.left[2] = 1
        special.right[2] = 0
        if(valid(special) == True):
            if(checkHash(special)==False):
                special.parent = state
                addHash(special)
                frontier.append(special)
                
        action(state, 1, 2, 1, -2, 1)

def expandNodeDFS(state):
    special = State(state.left, state.right, state, state.depth+1)
    if(state.left[2]==1):
        actionDFS(state, 0, -1, 0, 1, 0)
        actionDFS(state, 0, -2, 0, 2, 0)
        actionDFS(state, 1, -1, 1, 1, 0)
        special.left[1] -= 1
        special.right[1] += 1
        special.left[0] -= 1
        special.right[0] += 1
        special.left[2] = 0
        special.right[2] = 1
        if(valid(special) == True):
            if(checkHash(special)==False):
                special.parent = state
                addHash(special)
                frontier.insert(0, special)
        actionDFS(state, 1, -2, 1, 2, 0)
        
    else:
        actionDFS(state, 0, 1, 0, -1, 1)
        actionDFS(state, 0, 2, 0, -2, 1)
        actionDFS(state, 1, 1, 1, -1, 1)
        special.left[1] += 1
        special.right[1] -= 1
        special.left[0] += 1
        special.right[0] -= 1
        special.left[2] = 1
        special.right[2] = 0
        if(valid(special) == True):
            if(checkHash(special)==False):
                special.parent = state
                addHash(special)
                frontier.insert(0, special)
        actionDFS(state, 1, 2, 1, -2, 1)

def expandNodeIDDFS(state):
    special = State(state.left, state.right, state, state.depth+1)
    if(state.left[2]==1):
        actionDFS(state, 0, -1, 0, 1, 0)
        actionDFS(state, 0, -2, 0, 2, 0)
        actionDFS(state, 1, -1, 1, 1, 0)
        special.left[1] -= 1
        special.right[1] += 1
        special.left[0] -= 1
        special.right[0] += 1
        special.left[2] = 0
        special.right[2] = 1
        if(valid(special) == True):
            if(checkHash(special)==False):
                special.parent = state
                addHash(special)
                frontier.insert(0+buffer, special)
        actionDFS(state, 1, -2, 1, 2, 0)
        
    else:
        actionDFS(state, 0, 1, 0, -1, 1)
        actionDFS(state, 0, 2, 0, -2, 1)
        actionDFS(state, 1, 1, 1, -1, 1)
        special.left[1] += 1
        special.right[1] -= 1
        special.left[0] += 1
        special.right[0] -= 1
        special.left[2] = 1
        special.right[2] = 0
        if(valid(special) == True):
            if(checkHash(special)==False):
                special.parent = state
                addHash(special)
                frontier.insert(0+buffer, special)
        actionDFS(state, 1, 2, 1, -2, 1)

def expandASTAR(state):
    special = State(state.left, state.right, state, state.depth+1)
    if(state.left[2]==1):
        actionASTAR(state, 0, -1, 0, 1, 0)
        actionASTAR(state, 0, -2, 0, 2, 0)
        actionASTAR(state, 1, -1, 1, 1, 0)
        special.left[1] -= 1
        special.right[1] += 1
        special.left[0] -= 1
        special.right[0] += 1
        special.left[2] = 0
        special.right[2] = 1
        if(valid(special) == True):
            if(checkHash(special)==False):
                special.parent = state
                addHash(special)
                special.depth += getCost(special)
                q.put((special.depth, special))
        actionASTAR(state, 1, -2, 1, 2, 0)
        
    else:
        actionASTAR(state, 0, 1, 0, -1, 1)
        actionASTAR(state, 0, 2, 0, -2, 1)
        actionASTAR(state, 1, 1, 1, -1, 1)
        special.left[1] += 1
        special.right[1] -= 1
        special.left[0] += 1
        special.right[0] -= 1
        special.left[2] = 1
        special.right[2] = 0
        if(valid(special) == True):
            if(checkHash(special)==False):
                special.parent = state
                addHash(special)
                special.depth += getCost(special)
                q.put((special.depth, special))
        actionASTAR(state, 1, 2, 1, -2, 1)

def valid(state):
    if(state.left[0] != 0):
        if(state.left[0]<state.left[1]):
            return False
    if(state.right[0] != 0):
        if(state.right[0]<state.right[1]):
            return False
    for x in range(3):
        if(state.left[x] < 0 or state.right[x] < 0):
            return False
    return True



def isGoal(state):
    for x in range(3):
        if state.left[x] != goal_state.left[x] or state.right[x] != goal_state.right[x]:
            return False
    return True
        
#get data from command line
initial_file = sys.argv[1]
goal_file = sys.argv[2]
mode = sys.argv[3]
output_file = sys.argv[4]

#define depth limit for iddfs
DEPTH_LIMIT=50
buffer=0
q = PriorityQueue()

#load data
initial = open(initial_file, "r")
initial_state = State(list(map(int, initial.readline().replace("\n","").split(','))), list(map(int, initial.readline().replace("\n","").split(','))), None, 1)
goal = open(goal_file, "r")
goal_state = State(list(map(int, goal.readline().replace("\n","").split(','))), list(map(int, goal.readline().replace("\n","").split(','))), None,1)
initial.close()
goal.close()

#initialize hash table
hashtable = {}
frontier = [initial_state]
cont = 1
n = 0;
solution = []
rerun = 1

#bfs graph-serach
if (mode == "bfs"):
    while(cont == 1):
        if(len(frontier) == 0):
            cont = 0;
            print("Failure")
        else:
            # curr = copy.deepcopy(frontier[0])
            curr = frontier[0]
            if isGoal(curr):
                cont = 0
                while(curr.parent != None):
                    frag = "\n" + str(curr.left) + "\n" +str(curr.right)
                    solution.insert(0,frag)
                    curr = curr.parent
                frag = str(curr.left) + "\n" +str(curr.right)
                solution.insert(0, frag)
                sol = open(output_file, "w")
                for i in range(len(solution)):
                    sol.write(solution[i])
                    sol.write("\n")
                    print(solution[i])
                sol.write("number of expanded nodes = " + str(n))
                sol.write("solution length = " + str(len(solution)-1))
                print("number of expanded nodes = ", n)

            else:
                addHash(curr)
                frontier.pop(0)
                n+=1;
                expandNode(curr)

        
elif(mode == "dfs"):
    while(cont == 1):
        if(len(frontier) == 0):
            cont = 0;
            print("Failure")
        else:
            # curr = copy.deepcopy(frontier[0])
            curr = frontier[0]
            if isGoal(curr):
                cont = 0
                
                while(curr.parent != None):
                    frag = "\n" + str(curr.left) + "\n" +str(curr.right)
                    solution.insert(0,frag)
                    curr = curr.parent
                frag = str(curr.left) + "\n" +str(curr.right)
                solution.insert(0, frag)
                sol = open(output_file, "w")
                for i in range(len(solution)):
                    sol.write(solution[i])
                    sol.write("\n")
                    print(solution[i])
                sol.write("number of expanded nodes = " + str(n))
                sol.write("solution length = " + str(len(solution)-1))
                print("number of expanded nodes = ", n)

            else:
                addHash(curr)
                frontier.pop(0)
                n+=1;
                expandNodeDFS(curr)

elif(mode == "iddfs"):
    while(cont == 1):
        if(len(frontier) == 0):
            cont = 0;
            print("Failure")
        else:
            # curr = copy.deepcopy(frontier[0])
            if(buffer == len(frontier)):
                buffer = 0
                rerun *= -1
            else:
                curr = frontier[0+buffer]
                if (curr.depth % DEPTH_LIMIT == 0 and rerun > 0):
                    buffer+=1
                else:
                    if isGoal(curr):
                        cont = 0
                        
                        while(curr.parent != None):
                            frag = "\n" + str(curr.left) + "\n" +str(curr.right)
                            solution.insert(0,frag)
                            curr = curr.parent
                        frag = str(curr.left) + "\n" +str(curr.right)
                        solution.insert(0, frag)
                        sol = open(output_file, "w")
                        for i in range(len(solution)):
                            sol.write(solution[i])
                            sol.write("\n")
                            print(solution[i])
                        sol.write("number of expanded nodes = " + str(n))
                        sol.write("solution length = " + str(len(solution)-1))
                        print("number of expanded nodes = ", n)

                    else:
                        addHash(curr)
                        frontier.pop(0+buffer)
                        n+=1;
                        expandNodeDFS(curr)

elif (mode == "astar"):
    
    q.put((1, initial_state))
    while(cont == 1):
        print("-------")
        if(q.qsize() == 0):
            cont = 0;
            print("Failure")
        else:
            curr = q.get()
            print(curr[1].left)
            print(curr[1].right)
            print()
            if isGoal(curr[1]):
                cont = 0
                temp = State(curr[1].left, curr[1].right, curr[1].parent, curr[1].depth)

                while(temp.parent != None):
                    frag = "\n" + str(temp.left) + "\n" +str(temp.right)
                    solution.insert(0,frag)
                    temp = temp.parent
                frag = str(temp.left) + "\n" +str(temp.right)
                solution.insert(0, frag)
                sol = open(output_file, "w")
                for i in range(len(solution)):
                    sol.write(solution[i])
                    sol.write("\n")
                    print(solution[i])
                sol.write("number of expanded nodes = " + str(n))
                sol.write("solution length = " + str(len(solution)-1))
                print("number of expanded nodes = ", n)

            else:
                addHash(curr[1])
                n+=1;
                expandASTAR(curr[1])
                print("size = ", q.qsize())
    

    


