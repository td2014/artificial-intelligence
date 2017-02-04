"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import sample_players as sp #for testing


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    #for testing
    print("In custom_score:")
    print("custom_score: heuristic = ", sp.open_move_score(game, player) )
    return sp.open_move_score(game, player)
    
    # TODO: finish this function!
    #    raise NotImplementedError


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if len(legal_moves)==0:
            return (-1,-1)
            
        # If board uninitialized, select center position as default.    
        if game.move_count==0:
            start_row = game.height // 2
            start_col = game.width // 2
            return (start_row, start_col)
        
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
 
            if self.method=="minimax":
 
                opt_score_result = float("-inf")
                opt_move = (-1,-1)
                
                if self.iterative:
                    depth=1
                else:
                    depth=self.search_depth
            
                while True:
                    score_result, test_move = self.minimax(game, depth)
                    if score_result > opt_score_result:
                        opt_score_result = score_result
                        opt_move = test_move
                        
                    if self.iterative:
                        depth=depth+1
                    else:
                        break  #done with minimax to fixed depth
                        
            elif self.method=="alphabeta":
                
                opt_score_result = float("-inf")
                opt_move = (-1,-1)
                
                if self.iterative:
                    depth=1
                else:
                    depth=self.search_depth
            
                while True:
                    score_result, test_move = self.alphabeta(game, depth)
                    if score_result > opt_score_result:
                        opt_score_result = score_result
                        opt_move = test_move
                        
                    if self.iterative:
                        depth=depth+1
                    else:
                        break  #done with alphabeta to fixed depth
            
        except Timeout:
            # Handle any actions required at timeout, if necessary
            return opt_move

        # Return the best move from the last completed search iteration
        return opt_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        
        print("-----")
        print("minimax: top")
        print("minimax: depth = ", depth)
        print("minimax: maximizing_player = ", maximizing_player)
        print("minimax: starting positions:")
        print(game.print_board())
        
        # using depth to determine level to evaluate
        # score.  When depth==1 then stop recursing.
            
        if len(game.get_legal_moves()) == 0:
            print("minimax: no legal moves remain")
            if maximizing_player:
                return float("-inf"), (-1,-1)
            else:
                return float("inf"), (-1,-1)
        else:
        # initialize return scores and moves
            if maximizing_player:
                print("minimax: initializing maximizing player")
                opt_score_result = float("-inf")
                opt_move = (-1,-1)
            else:
                print("minimax: initializing minimizing player")
                opt_score_result = float("inf")
                opt_move = (-1,-1)  
                
        # we are at target depth
        # now loop over legal moves and determine max or min scoring move
        # depending on layer type.        
            if depth == 1:
                print("minimax: at target depth")
                print("minimax: at target depth - maximizing_player = ", maximizing_player)
                print("minimax: at target depth - legal_moves = ", game.get_legal_moves())
                for iMove in game.get_legal_moves():
                    print("minimax: at target depth ---start of iMove---")
                    gameTemp= game.forecast_move(iMove)
                    print("minimax: at target depth, checking iMove = ", iMove)
                    print(gameTemp.print_board())
                    score_result = self.score(gameTemp, self)
                    print("minimax: at target depth - score_result = ", score_result)
                    if maximizing_player:
                        print("minimax: at target depth - maximizing player")
                        if score_result > opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
                    else:
                        print("minimax: at target depth - minimizing player")
                        if score_result < opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
                print("minimax: at target depth ---end of iMoves---")
                return opt_score_result, opt_move
            else:
                # recurse to the next level down
                # Loop over legal moves
                for iMove in game.get_legal_moves():
                    # update game board with parent move before recursing.
                    gameTemp = game.forecast_move(iMove)
                    # recursive call:  decrease depth and invert maximize to toggle between min/max layers
                    print("======")
                    print("minimax: calling recursion: maximizing_player, iMove = ", maximizing_player, iMove)
                    score_result, test_move = self.minimax(gameTemp, depth-1, not maximizing_player)
                    print("minimax: recursion return - depth, score_result, iMove, test_move", depth, score_result, iMove, test_move)
                    # want to update max or min depending if current layer is maximizing or minimizing
                    if maximizing_player:
                        print("minimax: recursion return - maximizing player")
                        if score_result > opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
                    else:
                        print("minimax: recursion return - minimizing player")
                        if score_result < opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue       
                return opt_score_result, opt_move
            

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        
#
# Algorithm to implement alpha beta pruning.
#
# Peform depth first search to 
# target depth
#
# If on a minimizing layer
#    Loop over legal nodes
#       if score < alpha exit
#       else:
#          alpha = score
#          best_move = current_move
#
# If on a maximizing layer
#    Loop over legal nodes
#       if score > beta exit
#       else:
#           beta = score
#           best_move = current_move
#
                
        print("-----")
        print("alphabeta: top")
        print("alphabeta: depth = ", depth)
        print("alphabeta: maximizing_player = ", maximizing_player)
        print("alphabeta: starting positions:")
  ###      print(game.print_board())
        
        # using depth to determine level to evaluate
        # score.  When depth==1 then stop recursing.
            
        if len(game.get_legal_moves()) == 0:
            print("alphabeta: no legal moves remain")
            if maximizing_player:
                return float("-inf"), (-1,-1)
            else:
                return float("inf"), (-1,-1)
        else:
        # initialize return scores and moves
            if maximizing_player:
                print("alphabeta: initializing maximizing player")
                opt_score_result = float("-inf")
                opt_move = (-1,-1)
            else:
                print("alphabeta: initializing minimizing player")
                opt_score_result = float("inf")
                opt_move = (-1,-1)  
                
        # we are at target depth
        # now loop over legal moves and determine max or min scoring move
        # depending on layer type.        
            if depth == 1:
                print("alphabeta: at target depth")
                print("alpha, beta = ", alpha, beta)
                print("alphabeta: at target depth - maximizing_player = ", maximizing_player)
                print("alphabeta: at target depth - legal_moves = ", game.get_legal_moves())
                for iMove in game.get_legal_moves():
                    print("alphabeta: at target depth ---start of iMove---")
                    gameTemp= game.forecast_move(iMove)
                    print("alphabeta: at target depth, checking iMove = ", iMove)
  ###                  print(gameTemp.print_board())
                    score_result = self.score(gameTemp, self)
                    print("alphabeta: at target depth - score_result = ", score_result)
                    if maximizing_player:
                        print("alphabeta: at target depth - maximizing player")
                        if score_result >= beta:
                                print("alphabeta: beta pruning triggered")
                                opt_score_result=score_result
                                opt_move=iMove
                                break
                        if score_result > opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
                    else:
                        print("alphabeta: at target depth - minimizing player")
                        if score_result <= alpha:
                                print("alphabeta: alpha pruning triggered")
                                opt_score_result=score_result
                                opt_move=iMove
                                break
                        if score_result < opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
                print("alphabeta: at target depth ---end of iMoves---")
                return opt_score_result, opt_move
            else:
                # recurse to the next level down
                # Loop over legal moves
                for iMove in game.get_legal_moves():
                    print("alphabeta: calling recursion, maximizing_player = ", maximizing_player)
                    print("alphabeta: calling recursion, legal_moves() = ", game.get_legal_moves())
                    # update game board with parent move before recursing.
                    gameTemp = game.forecast_move(iMove)
                    # recursive call:  decrease depth and invert maximize to toggle between min/max layers
                    print("======")
                    print("alphabeta: calling recursion: maximizing_player, iMove = ", maximizing_player, iMove)
                    print("alphabeta: calling recursion: alpha, beta = ", alpha, beta)
                    score_result, test_move = self.alphabeta(gameTemp, depth-1, alpha, beta, not maximizing_player)
                    print("alphabeta: recursion return - depth, score_result, iMove, test_move", depth, score_result, iMove, test_move)
                    print("alphabeta: recursion return - alpha, beta = ", alpha, beta)
                    # want to update max or min depending if current layer is maximizing or minimizing
                    if maximizing_player:
                        print("alphabeta: recursion return - maximizing player")
                        print("alphabeta: recursion return - maximizing player, score_result, alpha = ", score_result, alpha)
                        if score_result > alpha:
                            alpha=score_result
                            print("alphabeta: recursion return, setting alpha = ", alpha)
                            opt_score_result = score_result
                            opt_move = iMove
##                               break
                        elif score_result > opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
                    else:
                        print("alphabeta: recursion return - minimizing player")
                        print("alphabeta: recursion return - minimizing player, score_result, beta = ", score_result, beta)
                        if score_result < beta:
                            beta=score_result
                            print("alphabeta: recursion return, setting beta = ", beta)
                            opt_score_result = score_result
                            opt_move = iMove
##                            break
                        elif score_result < opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue   
                        
                return opt_score_result, opt_move
