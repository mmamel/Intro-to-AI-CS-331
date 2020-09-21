'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
import Globals
class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
    
    def get_move(self, board):
        # global state
        index = -1
        temp_v = 100
        for x in range(len(Globals.state.children)):
            if (Globals.state.children[x].v <= temp_v):
                index = x 
                temp_v = Globals.state.children[x].v
        # Globals.state.children[index].board.display()
        # print(state.children[index].col_move)
        # print(state.children[index].row_move)
        # return (state.children[index].col_move, state.children[index].row_move)
        if(index == -1):
             return (-1,-1)
        else:
            return (Globals.state.children[index].row_move,Globals.state.children[index].col_move)

       
        





