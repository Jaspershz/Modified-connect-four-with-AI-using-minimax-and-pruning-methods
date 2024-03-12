import random
import math


BOT_NAME =  "BIGFISH"


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
  
    rseed = None  # change this to a value if you want consistent random choices

    def __init__(self):
        if self.rseed is None:
            self.rstate = None
        else:
            random.seed(self.rseed)
            self.rstate = random.getstate()

    def get_move(self, state):
        if self.rstate is not None:
            random.setstate(self.rstate)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move.  Very slow and not always smart."""

    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None
        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Gets called by get_move() to determine the value of each successor state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        if state.is_full():
            return state.utility()
        else:
            util = []
            for i in state.successors():
                util.append(self.minimax(i[1]))
            max = -math.inf
            min = math.inf
            for i in util:
                if i > max:
                    max = i
                if i < min:
                    min = i
            if state.next_player() == 1:
                return max
            else:
                return min
                    
                



class MinimaxLookaheadAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move.
 
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        Gets called by get_move() to determine the value of successor states.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation(). 

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the (possibly estimated) minimax utility value of the state
        """
        
        if state.is_full() or self.depth_limit == 0:
            return self.evaluation(state)
        else:
            score = []
            for i in state.successors():
                self.depth_limit -= 1
                score.append(self.minimax(i[1]))
                self.depth_limit += 1
            max = -math.inf
            min = math.inf
            for i in score:
                if i > max:
                    max = i
                if i < min:
                    min = i
            if state.next_player() == 1:
                return max
            else:
                return min

    def minimax_depth(self, state, depth):
        """This is just a helper method for minimax(). Feel free to use it or not. """
        pass

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        Gets called by minimax() once the depth limit has been reached.  
        N.B.: This method must run in "constant" time for all states!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heuristic estimate of the utility value of the state
        """

        nextp = state.next_player()
        rows = state.get_rows()
        cols = state.get_cols()

        diags = state.get_diags()
        diags_left = diags[:len(diags)//2]
        diags_right = diags[len(diags)//2:]

        rev_diags_left = []
        i = len(diags_left)-1
        while i >= 0:
            rev_diags_left.append(diags_left[i])
            i -= 1
        row_score = self.get_line_score(rows)
        col_score = self.get_line_score(cols)
        diags_score = self.get_line_score(diags)
        if self.depth_limit == 0 and state.is_full() == False:
            diags_score_left = 0 
            diags_score_right = 0
            row_score += self.get_predict_score(rows, True, False)
            col_score += self.get_predict_score(cols, False, False)
            diags_score_left =self.get_predict_score(rev_diags_left, False, True)
            diags_score_right = self.get_predict_score(diags_right, False, True)
            diags_score += diags_score_left + diags_score_right
        total_score = row_score + col_score + diags_score  
        return total_score
    
    def get_line_score(self, lines):
        score = 0
        for i in lines:
            p1_count = i.count(1)
            p2_count = i.count(-1)
            if p1_count<2 and p2_count<2:
                continue
            else:
                combos = []
                combo = 0
                j = 1
                while j < len(i):
                    if i[j] == i[j-1] and j == len(i)-1:
                        combo += 2
                        combos.append([i[j], combo])
                        break
                    elif i[j] == i[j-1]:
                        combo += 1
                    else:
                        combo += 1
                        combos.append([i[j-1], combo])
                        combo = 0
                    j += 1
                
                for j in combos:
                    if j[1] >= 3:
                        score += j[0] * (j[1] ** 2)
        return score
                    


    def get_predict_score(self, lines, row, diag):
        line_score = 0
        for i in lines:                             #traverse through all the lines (either rows or columns)
            i = list(i)
            try: 
                i.index(0)                          #if index of 0 cannot be found, it means the line is full and the loop will skip the current line
            except:
                continue
            prev_full = False
            prev_empty = False
            try:
                lines[lines.index(i)-1]
            except:
                prev_empty = True
            if prev_empty == False:
                prev = lines[lines.index(i)-1]
            try:
                prev.index(0)
            except:
                prev_full = True
            skip = False
            if i.count(0) > 1:
                index = []
                j = 0
                while j < len(i):
                    if i[j] == 0:
                        index.append(j)
                    j += 1
            if prev_full == False:
                if row == True:
                    if i.count(0) == 1:
                        if prev[i.index(0)] == 0:
                            continue
                    else:
                        for j in index:
                            if prev[j] == 0:
                                skip = True
                elif diag == True:
                    if i.count(0) == 1:
                        if len(prev) > len(i):
                            if prev[i.index(0)] == 0:
                                continue
                        else:
                            if prev[i.index(0)-1] == 0:
                                continue
                    else:
                        if len(prev) > len(i):
                            for j in index:
                                if prev[j] == 0:
                                    skip = True
                        else:
                            for j in index:
                                if j != 0:
                                    if prev[j-1] == 0:
                                        skip = True
                if skip == True:
                    continue

            p1_count = i.count(1)
            p2_count = i.count(-1)
            if p1_count<2 and p2_count<2:           #if both 1 and -1 are less than 2, it means there are no combos and therefore the line is skipped
                continue
            else:
                combo = 0
                combos = []
                split_left = i[:i.index(0)]
                split_right = i[i.index(0)+1:]
                split_left.reverse()
                j = 0
                while j < len(split_left)-1:                   
                    if split_left[j] == -2 or split_left[j] == 0:
                        j += 1
                        continue
                    if split_left[j+1] == split_left[j] and j == len(split_left)-2:
                        combo += 1
                        combos.append([split_left[j], combo+1])
                    elif split_left[j-1] == split_left[j]:
                        combo += 1
                    else:
                        combos.append([split_left[j-1], combo+1])
                        break
                    j += 1
                j = 0
                while j < len(split_right)-1:                   
                    if split_right[j] == -2 or split_right[j] == 0:
                        j += 1
                        continue
                    if split_right[j+1] == split_right[j] and j == len(split_right)-2:
                        combo += 1
                        combos.append([split_right[j], combo+1])
                    elif split_right[j-1] == split_right[j]:
                        combo += 1
                    else:
                        combos.append([split_right[j-1], combo+1])
                        break
                    j += 1
                if len(combos) == 1 and combos[0][1] > 1:
                    line_score += combos[0][1] ** 2
                elif len(combos) == 2:
                    if(combos[0][0] == combos[1][0]):
                        line_score += combos[0][0] * (combos[0][1] + combos[1][1]) ** 2
                    else:
                        if(combos[0][1] > 1):
                            line_score += combos[0][0] * (combos[0][1] ** 2)
                        elif(combos[1][1] > 1):
                            line_score += combos[1][0] * (combos[1][1] ** 2)
            
        return line_score


class AltMinimaxLookaheadAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state."""
        #
        # Fill this in, if it pleases you.
        #
        return 19  # Change this line, unless you have something better to do.


class MinimaxPruneAgent(MinimaxAgent):
    """Computer agent that uses minimax with alpha-beta pruning to select the best move.
    
    Hint: Consider what you did for MinimaxAgent.  What do you need to change to prune a
    branch of the state space? 
    """
    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent does not have a depth limit.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to column 1 (we're trading optimality for gradeability here).

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        if state.is_full():
            return state.utility()
        else:
            util = []
            for i in state.successors():
                util.append(self.minimax(i[1]))
            max = -math.inf
            min = math.inf
            for i in util:
                if i > max:
                    max = i
                if i < min:
                    min = i
            if state.next_player() == 1:
                return max
            else:
                return min

    def alphabeta(self, state,alpha, beta):
        """This is just a helper method for minimax(). Feel free to use it or not."""
        if state.is_full():
            return state.utility()
        else:
            util = []
            max = alpha
            min = beta
            for i in state.successors():
                val = self.minimax(i, alpha, beta)
                if state.next_player() == 1:
                    if val > max:
                        break
                else:
                    if val < min:
                        break
                
                util.append(val)
            for i in util:
                if i > max:
                    max = i
                if i < min:
                    min = i
            if state.next_player() == 1:
                return max
            else:
                return min


def get_agent(tag):
    if tag == 'random':
        return RandomAgent()
    elif tag == 'human':
        return HumanAgent()
    elif tag == 'mini':
        return MinimaxAgent()
    elif tag == 'prune':
        return MinimaxPruneAgent()
    elif tag.startswith('look'):
        depth = int(tag[4:])
        return MinimaxLookaheadAgent(depth)
    elif tag.startswith('alt'):
        depth = int(tag[3:])
        return AltMinimaxLookaheadAgent(depth)
    else:
        raise ValueError("bad agent tag: '{}'".format(tag))       
