import numpy as np
import sys




# -----------------------------------
# USEFUL CONSTANTS


        # simple action: turn every 10 iterations
        #turn = 1 if self.times_moved % 10 == 0 and iter != 0 else 0
        #no more turning
        # 'player_[num]': {
        # 'player_num': int,
        #  'resetting': bool,
        #  'head': [x,y],
        #  'direction': [-1, 0] or [1, 0] or [0, 1] or [0, -1] (or [-1, -1] if resetting)
        #               left       right     down      up
        #  'energy': int,
        #  'speed': int, 

#if self.times_moved == 0:
#    haveturned = True
        
LEFT = [-1, 0]
RIGHT = [1, 0]
DOWN = [0, 1]
UP = [0, -1]
TEMP = -1
UNOCCUPIED = 0
TAIL = 1
TERRITORY = 2
BOMB = 3
BOOST = 4
# -----------------------------------

class Agent():
    
    def __init__(self, player: str) -> None:
        self.player = player
        self.times_moved = 0
        self.goAroundBomb = 0
        self.haveturned = True
        self.myTerritory = [-1, -1]
        self.itsTimeToGoBackHome = False
        self.activeTailTrace = 0

    def formatAction(self, turn: int):
        return { 'turn': turn }
    
    #def avoidDanger():
    #    return self.formatAction(turn)

    def findTheIdealDirection(self, x: int, y: int, max_x: int, max_y: int):
        #need to find the shortest distance to the wall, and then return the direction
        idealDirection = UP
        diff_x = max_x - x #results in a positive x diff, if its small we are close to max x
        diff_y = max_y - y #results in a positive y diff, if its small we are close to max y
        if(x < diff_x):
            smallest_x = x
            idealDirection = LEFT
        else:
            smallest_x = diff_x
            idealDirection = RIGHT

        if(y < diff_y):
            if(y < smallest_x):
                idealDirection = UP
        else:
            if(diff_y < smallest_x):
                idealDirection = DOWN
        #print(idealDirection)
        return idealDirection

    #def evaluate(self, ):

    #def minimax(self, depth, maximizingPlayer):
        


    def act(self, iter: int, curr_step: int, obs, remainingOverageTime: int = 60):
        # get all info; note: _dones and _infos are irrelevant here
        obs, rewards, _dones, _infos = obs

        # if not allowed to move, don't waste time computing
        if (obs[self.player]['resetting']):
            return self.formatAction(0)

        # if first iteration, save constant observations like player_num
        if (iter == 0 and curr_step == 0):
            self.num = obs[self.player]['player_num']

        # separate player observation from board observation
        me_obs = obs[self.player]
        board_obs = obs['board']

        # collection essential player info
        direction = me_obs['direction']
        head = me_obs['head']
        energy = me_obs['energy']
        speed = me_obs['speed']

        # save arrays which describe board state to numpy arrays for processing
        board = np.array(board_obs['board_state'])
        player_owned = np.array(board_obs['players_state'])

        pos_x, pos_y = head #current x and y positions
        front_x, front_y = direction #used for looking a block in front of ourselves (based on direction)
        max_x, max_y = board.shape  #the borders of our board

        x = pos_x + front_x #for looking one block in front of our head
        y = pos_y + front_y #for looking one block in front of our head

        if(self.myTerritory == [-1, -1]):
            #update spawn point right when we start
            self.myTerritory = head
        
        if(self.times_moved == 0):
            #at the start turn to face the nearest wall
            idealDirection = self.findTheIdealDirection(pos_x, pos_y, max_x, max_y)
            #figure this out
            #while(self.turnToIdealDirection(direction, idealDirection) != 0):
            #    return self.turnToIdealDirection(direction, idealDirection)

        #if we don't update turn it will be zero
        turn = 0
        #for some reason adding a print statement breaks it
        if(self.goAroundBomb > 0):
            self.goAroundBomb -= 1
            if self.goAroundBomb % 2 == 0:
                #return self.formatAction(-1)
                turn = -1
            else:
                return self.formatAction(0)
        

        #turn = turnRightWhenOnWall(direction, pos_x, pos_y)
        #this should be a function but for some reason breaks when I do that 
        if direction == LEFT:
            if pos_x == 0:
                turn = 1
        elif direction == RIGHT:
            if pos_x == max_x-1:
                turn = 1
        elif direction == DOWN:
            if pos_y == max_y-1:
                turn = 1
        else:
            if pos_y == 0:
                turn = 1
        
        #this should also be a function but also breaks when I do that lol
        if x < max_x and y < max_y:
            if (board[x][y] == TAIL):
                turn = 1
            elif (board[x][y] == BOMB):
                #avoids a bomb if bomb is in front of
                #goAroundBomb();
                self.goAroundBomb = 3
                turn = 1
            elif(board[x][y] == TEMP):
                turn = 1
        
        #idk why im keeping track of this but I thought it would be helpful for somereason
        self.times_moved += 1
        #LEFT = [-1, 0]
        #RIGHT = [1, 0]
        #DOWN = [0, 1]
        #UP = [0, -1]
        #front_x, front_y = direction #used for looking a block in front of ourselves (based on direction)
        #if there is a tail to the left of us for some time, we change modes
        lookLeftBlock_x = pos_x + front_y
        lookLeftBlock_y = pos_y + front_x
        if(lookLeftBlock_x > 0 and lookLeftBlock_x < max_x and lookLeftBlock_y > 0 and lookLeftBlock_y < max_y):
            if(board[lookLeftBlock_x][lookLeftBlock_y] == TAIL):
                #activeTailTrace will let us trace a tail once it reaches 5
                self.activeTailTrace += 1
        #once we are in this state we will always turn left to trace tails, then spin forever
        if(lookLeftBlock_x > 0 and lookLeftBlock_x < max_x and lookLeftBlock_y > 0 and lookLeftBlock_y < max_y):
            if(self.activeTailTrace >= 4):
                if(board[lookLeftBlock_x][lookLeftBlock_y] != TAIL and board[lookLeftBlock_x][lookLeftBlock_y] != BOMB):
                    if(board[lookLeftBlock_x][lookLeftBlock_y] == TERRITORY):
                        self.activeTailTrace = 0
                    turn = -1
        
        # note action should be a dict with action['turn'] = -1, 0, or 1
        #if( againstWall == True):
        #    if(board[x, y] == TAIL):
                #we can assume this is our own tail right?
        return self.formatAction(turn)