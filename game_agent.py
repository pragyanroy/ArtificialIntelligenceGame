"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def heuristic_1(game, player):

    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")

    currPlayer = len(game.get_legal_moves(player))
    oppPlayer = len(game.get_legal_moves(game.get_opponent(player)))


    heuristic_value = float(currPlayer - 2 * oppPlayer)

    return heuristic_value
def heuristic_2(game, player):

    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")

    currPlayer = len(game.get_legal_moves(player))
    oppPlayer = len(game.get_legal_moves(game.get_opponent(player)))


    heuristic_value = float(currPlayer - 4 * oppPlayer)

    return heuristic_value

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    #raise NotImplementedError


    return heuristic_1(game, player)


    #return (float (len(game.get_legal_moves(player))-2*len(game.get_legal_moves(game.get_opponent(player)))))

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
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """


        self.time_left = time_left

        if self.time_left() < self.TIMER_THRESHOLD :
            raise Timeout()

        legal_moves = game.get_legal_moves(game.active_player)

        if len(legal_moves)<=0:
            return(-1,-1) #outside board
        else:
            curr_move = legal_moves[0]



            return curr_move if self.time_left()<self.TIMER_THRESHOLD else self.move_get(game)

    def move_get(self,game):
        depth = 1
        if self.iterative:

            try:

                while True:
                    _, move = self.minimax(game, depth) if self.method == 'minimax' else self.alphabeta(game, depth)

                    if move != (-1, -1):
                        curr_move = move
                    else:
                        break
                    depth += 1

            except:
                return curr_move
        else:
            _, curr_move = self.minimax(game, depth) if self.method == 'minimax' else self.alphabeta(game, depth)
        return curr_move

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
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """


        return self.MAX(game,depth)

    def MAX(self,game,depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        valid_moves = game.get_legal_moves()


        if depth == 0 or not valid_moves:

            return (self.score(game, self), (-1,-1))




        best_max_post = (float('-inf'), (-1, -1))
        depth -= 1
        for mov in valid_moves:

            forecast_mov = game.forecast_move(mov)
            # print(forecast_mov.print_board())


            move = self.MIN(forecast_mov, depth)
            if move[0] > best_max_post[0]:
                best_max_post = (move[0], mov)
                best = best_max_post

        return best

    def MIN(self,game,depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        valid_moves = game.get_legal_moves()

        if depth == 0 or not valid_moves:

            return (self.score(game, self), (-1,-1))




        best_min_post = (float('inf'), (-1, -1))
        depth -= 1
        for mov in valid_moves:

            forecast_mov = game.forecast_move(mov)



            move = self.MAX(forecast_mov, depth)
            if move[0] < best_min_post[0]:
                best_min_post = (move[0], mov)
                best = best_min_post
        return best

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
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        valid_moves = game.get_legal_moves()



        if maximizing_player:
            bestscore = float('-inf')
            bestmove = (-1, -1)
            if not valid_moves:
                return bestscore,bestmove
            if depth == 0:
                return (self.score(game, game.active_player), (-1,-1))
            depth -= 1
            for mov in valid_moves:
                child = game.forecast_move(mov)
                mov_value = self.alphabeta(child, depth, alpha, beta, False)
                if float(mov_value[0]) > bestscore:
                    bestscore =float(mov_value[0])
                    bestmove = mov
                if bestscore > alpha:
                    alpha = bestscore
                if beta <= alpha:
                    break
            return bestscore,bestmove
        else:
            bestscore = float('inf')
            bestmove = (-1, -1)
            if not valid_moves:
                return bestscore,bestmove
            if depth == 0:
                return (self.score(game, game.inactive_player), (-1,-1))
            depth -= 1
            for mov in valid_moves:
                child = game.forecast_move(mov)
                mov_value= self.alphabeta(child, depth, alpha, beta, True)
                if float(mov_value[0]) < bestscore:
                    bestscore=mov_value[0]
                    bestmove = mov

                if bestscore < beta:
                    beta = bestscore
                if beta <= alpha:
                    break
            return bestscore,bestmove
