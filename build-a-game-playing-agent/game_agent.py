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

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            print("CustomPlayer: method = ", self.method)
            print("CustomPlayer: score = ", self.score)
            pass

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        print ("CustomPlayer:  legal_moves = ", legal_moves)
        return legal_moves[0]
#       raise NotImplementedError

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
        print()
        print("minimax: top")
        print("minimax: game = ", game)
        print("minimax: depth = ", depth)
        print("minimax: maximizing_player = ", maximizing_player)
        print("minimax: utility = ", game.utility(self))
        print("minimax: score = ", self.score)
        print("minimax: game.move_count = ", game.move_count)
        print()
        print(game.print_board())
        print()
        
        # Verify we are still within valid depth range.
        # A two player game will always be initialized with
        # two moves.  Subtract one to get to current depth.
        current_search_depth = game.move_count-1
        print("minimax: currently at depth = ", current_search_depth)
            
        if len(game.get_legal_moves()) == 0:
            print("minimax: no legal moves remain")
            return 0, (-1,-1)
        else:
            if maximizing_player:
                opt_score_result = float("-inf")
                opt_move = (-1,-1)
            else:
                opt_score_result = float("inf")
                opt_move = (-1,-1)  
                
            if current_search_depth == depth:       
                for iMove in game.get_legal_moves():
                    print("minimax: at target search depth.")
                    print("minimax: iMove = ", iMove)
                    gameTemp= game.forecast_move(iMove)
                    score_result = self.score(gameTemp, self)
                    print("minimax: score = ", score_result)
                    print()
                    print(gameTemp.print_board())
                    print()
                    if maximizing_player:
                        if score_result > opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
                    else:
                        if score_result < opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
            else:
                # recurse to the next level down
                print("minimax: not at target depth")
                for iMove in game.get_legal_moves():
                    print("minimax: game depth before forecast = ", game.move_count-1)
                    print("minimax: legal moves before forecast = ", game.get_legal_moves())
                    gameTemp = game.forecast_move(iMove)
                    print("minimax: iMove = ", iMove)
                    print("minimax: game depth after forecast = ", gameTemp.move_count-1)
                    print("minimax: legal moves after forecast = ", gameTemp.get_legal_moves())
                    score_result, test_move = self.minimax(gameTemp, depth, not maximizing_player)
                    print("minimax recurse return:")
                    print("minimax: parent iMove = ", iMove)
                    print("minimax: opt_move = ", opt_move)
                    print("minimax: score = ", score_result)
                    print()
                   
                    if maximizing_player:
                        print ("minimax: in recursion step - maximize player is True")
                        print ("minimax: in recursion step - score_result = ", score_result)
                        print ("minimax: in recursion step - opt_score_result = ", opt_score_result)
                        if score_result > opt_score_result:
                            print ("minimax: in recursion step - updating optimum")
                            opt_score_result = score_result
                            opt_move = iMove
                            print ("minimax: in recursion step - opt_move = ", opt_move)
                            print ("minimax: in recursion step - opt_score_result = ", opt_score_result)
                            print()
                        else:
                            continue
                    else:
                        print ("minimax: in recursion step - maximize player is False")
                        if score_result < opt_score_result:
                            opt_score_result = score_result
                            opt_move = iMove
                        else:
                            continue
                print ("minimax: after recurse- returning opt_score_result, opt_move: ", opt_score_result, opt_move)       
                return opt_score_result, opt_move        
                    
            print ("minimax: returning opt_score_result, opt_move: ", opt_score_result, opt_move)       
            return opt_score_result, opt_move
                
#        return 0.0, (-1, -1)  # test value in expected format
#        raise NotImplementedError

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
        raise NotImplementedError
