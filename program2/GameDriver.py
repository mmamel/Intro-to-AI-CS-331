'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
from Players import *
import sys
import OthelloBoard
import Globals 

def minimiax_decision(state):
    temp = 0
    for x in range(len(state.children)):
        if(temp<min_value(state)):
            temp = min_value(state)
    return col, row
def deleteme(state):
    state.v = 135135
    return
def max_value(state):
    if (state.terminal == True):
        return state.v
    v = -100
    for x in range(len(state.children)):
        if (state.children[x].symbol == 'O'):
            temp_v = min_value(state.children[x])
        else:
            temp_v = max_value(state.children[x])
        if(temp_v > v):
            v = temp_v
    state.v = v
    return v 

def min_value(state):
    if (state.terminal == True):
        return state.v 
    v = 100
    for x in range(len(state.children)):
        if (state.children[x].symbol == 'X'):
            temp_v = max_value(state.children[x])
        else:
            temp_v = min_value(state.children[x])
        if(temp_v < v):
            v = temp_v
    state.v = v 
    # print(state.v)       
    return v

class Node:
    def __init__(self, board, parent, symbol, terminal, v, row_move, col_move):
        self.board = board
        self.parent = parent
        self.children = []
        self.symbol = symbol
        self.v = v
        self.terminal = terminal
        self.row_move = row_move
        self.col_move = col_move
    def generate_successors(self):
        temp_board = self.board.cloneOBoard()
        v = 100
        if(self.symbol =='X'):
            new_symbol = 'O'
        else:
            new_symbol = 'X'
            v = -100
        terminal = False
        next_symbol = 'a'
        new_board = temp_board.cloneOBoard()
        if(new_board.has_legal_moves_remaining(self.symbol) == False):
            if(new_board.has_legal_moves_remaining(new_symbol)== False):
                terminal = True
                x_score = new_board.count_score('X')
                o_score = new_board.count_score('O')
                if(x_score > o_score):
                    v=1
                elif (x_score < o_score):
                    v = -1
                elif (x_score == o_score):
                    v = 0  
                self.children.append(Node(new_board, self, next_symbol, terminal, v, 0, 0))
 
   
        else:
            new_symbol = self.symbol
        if(new_symbol =='X'):
            next_symbol = 'O'
        else:
            next_symbol = 'X'        
        for x in range(4):
            for y in range(4):
                if(temp_board.is_cell_empty(x,y) == True):
                    if(temp_board.is_legal_move(x,y, new_symbol) ):
                        new_board = temp_board.cloneOBoard()
                        new_board.set_cell(x,y,new_symbol)
                        new_board.flip_pieces(x,y,new_symbol)

                        self.children.append(Node(new_board, self, next_symbol, terminal, v, x, y))
        for z in range(len(self.children)):
            if(self.children[z].terminal == False):
                Globals.frontier.append(self.children[z])

        del temp_board

class GameDriver:
    def __init__(self, p1type, p2type, num_rows, num_cols):
        if p1type.lower() in "human":
            self.p1 = HumanPlayer('X')

        elif p1type.lower() in "minimax" or p1type in "ai":
            self.p1 = MinimaxPlayer('X')

        else:
            print("Invalid player 1 type!")
            exit(-1)

        if p2type.lower() in "human":
            self.p2 = HumanPlayer('O')

        elif p2type.lower() in "minimax" or p1type in "ai":
            self.p2 = MinimaxPlayer('O')

        else:
            print("Invalid player 2 type!")
            exit(-1)

        self.board = OthelloBoard.OthelloBoard(num_rows, num_cols, self.p1.symbol, self.p2.symbol)
        self.board.initialize();

    def display(self):
        print("Player 1 (", self.p1.symbol, ") score: ", \
                self.board.count_score(self.p1.symbol))

    def process_move(self, curr_player, opponent):
        invalid_move = True
        while(invalid_move):
            (col, row) = curr_player.get_move(self.board)
            if(row == -1):
                return
            else:
                if( not self.board.is_legal_move(col, row, curr_player.symbol)):
                    print("Invalid move")
                else:
                    print("Move:", [col,row], "\n")
                    self.board.play_move(col,row,curr_player.symbol)
                    if(Globals.state != None):
                        for x in range(len(Globals.state.children)):
                            if (Globals.state.children[x].board.is_cell_empty(col, row) == False):
                                Globals.state = Globals.state.children[x]
                                return;
                    return
                


    def run(self):

        current = self.p1
        opponent = self.p2
        self.board.display();
        cant_move_counter, toggle = 0, 1
        
        #main execution of game
        print("Player 1(", self.p1.symbol, ") move:")
        self.process_move(current, opponent);
        self.board.display()
        current, opponent = self.p2, self.p1
        tree = Node(self.board.cloneOBoard(), None, 'O', False,100, 0,0)
        Globals.frontier.append(tree)
        while(len(Globals.frontier) != 0):
            curr = Globals.frontier.pop(0)
            curr.generate_successors()
        
        min_value(tree)
        print("Player 2(", self.p2.symbol, ") move:")
        Globals.state = tree
        while True:
            # print("current state -------------")
            # Globals.state.board.display()
            # print("----------------------")
            if self.board.has_legal_moves_remaining(current.symbol):
                cant_move_counter = 0
                self.process_move(current, opponent);
                self.board.display()
            else:
                print("Can't move")
                if(cant_move_counter == 1):
                    break
                else:
                    cant_move_counter +=1
            toggle = (toggle + 1) % 2
            if toggle == 0:
                current, opponent = self.p1, self.p2
                print("Player 1(", self.p1.symbol, ") move:")
            else:
                current, opponent = self.p2, self.p1
                print("Player 2(", self.p2.symbol, ") move:")

        #decide win/lose/tie state
        state = self.board.count_score(self.p1.symbol) - self.board.count_score(self.p2.symbol)
        if( state == 0):
            print("Tie game!!")
        elif state >0:
            print("Player 1 Wins!")
        else:
            print("Player 2 Wins!")
            


def main():
    if(len(sys.argv)) != 3:
        print("Usage: python3 GameDriver.py <player1 type> <player2 type>")
        exit(1)
    game = GameDriver(sys.argv[1], sys.argv[2], 4, 4)
    game.run();
    return 0


main()
