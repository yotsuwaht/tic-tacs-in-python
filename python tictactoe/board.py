from enum import Enum;

# game states

class GameState(Enum):
    WIN_O = 1;
    WIN_X = 2;
    TIE = 3;
    WE_GOIN = 4;
    INVALID = 5;

TURN_O = True;
TURN_X = False;
    

# all possible win conditions into a single tuple

WIN_CASES = (
            # horizontal cases
            0b111000000, 
            0b000111000, 
            0b000000111, 
            # vertical cases
            0b100100100, 
            0b010010010, 
            0b001001001, 
            # diagonal cases
            0b100010001, 
            0b001010100
            );

class Board:

    def __init__(self):
        self.x = 0b000000000;
        self.o = 0b000000000;
        self.turn = TURN_O; # starting player
        self.moveStack = [];
    
    def __str__(self):
        result = "";

        for i in range(9):
            mask = (1 << i);
            if self.o & mask:
                result += "O";
            elif self.x & mask:
                result += "X";
            else:
                result += "#";
            if (i + 1) % 3 == 0:
                result += "\n";
        
        return result;

    def checkWin(self):
        player = self.o if self.turn else self.x;

        for case in WIN_CASES: # checks all win cases
            if (player & case) == case:
                return GameState.WIN_O if self.turn else GameState.WIN_X;

        if self.o | self.x == 0b111111111:
            return GameState.TIE;

        return GameState.WE_GOIN;

    def place(self, coord : int):
        if coord < 1 or coord > 9:
            return GameState.INVALID;
        
        mask = (1 << (coord-1)); # the move

        if (((self.o | self.x) & mask) != 0):
            return GameState.INVALID;
        
        if self.turn:
            self.o |= mask;
        else:
            self.x |= mask;

        boardstate = self.checkWin();
        self.moveStack.append(coord); # saves to movestack in case it needs undoing
        self.turn = not self.turn;

        return boardstate;

    def undo(self):
        if len(self.moveStack) == 0:
            return "empty";
        
        lastMove = self.moveStack.pop(); # removes last coord
        mask = ~(1 << (lastMove-1)) & 0b111111111; # inverts move

        self.turn = not self.turn;
        if self.turn:
            self.x &= mask;
        else:
            self.o &= mask;

    def start(self):
        while True:
            print(self);
            print(f"{'O' if self.turn else 'X'}'s turn.");
            try:
                newInput = int(input("input 1-9: "));
            except ValueError:
                print("invalid input"); # dont input non integers or strings duh
                continue;

            result = self.place(newInput);

            match result:
                case GameState.INVALID:
                    print("invalid input");
                case GameState.WE_GOIN:
                    continue;
                case GameState.WIN_O | GameState.WIN_X | GameState.TIE:
                    print("\n")
                    print("Result:", result.name);
                    print(self);
                    break;


if __name__ == "__main__":
    newBoard = Board();
    newBoard.start();
