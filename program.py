from referee.game import PlayerColor, Action, PlaceAction, Coord
from .monte_carlo_tree_search import MonteCarloTreeSearch
from .board import BitBoard
import time

class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")
        self._board = BitBoard()
        self.max_turns = 150

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        # Below we have hardcoded two actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.
        if self._board.turn_count >= 7:
            tree = MonteCarloTreeSearch()
            remaining_time = referee["time_remaining"] / (((self.max_turns - self._board.turn_count) / 2))
            tree.estimated_max_turns = 0
            # Run MCTS algorithm with the calculated number of simulations
            start_time = time.time()
            simulation = 0
            while(True):
                simulation +=1 
                tree.do_rollout(self._board)
                end_time = time.time()
                elapsed_time = end_time - start_time
                if (elapsed_time > remaining_time): break
            print(simulation)
            self.max_turns = tree.estimated_max_turns
            selected_action = tree.choose(self._board)
            return selected_action.last_move_to_coordinates()
        elif self._board.turn_count > 2:
            new_board = self._board.find_random_child()
            return new_board.last_move_to_coordinates()
        else:
            match self._color:
                case PlayerColor.RED:
                    return PlaceAction(
                        Coord(3, 3), 
                        Coord(3, 4), 
                        Coord(4, 3), 
                        Coord(4, 4)
                    )
                case PlayerColor.BLUE:
                    if self._board.is_valid_move(503316480):
                        return PlaceAction(
                            Coord(2, 3), 
                            Coord(2, 4), 
                            Coord(2, 5), 
                            Coord(2, 6) 
                    )
                    else:
                        return PlaceAction(
                            Coord(6, 4), 
                            Coord(6, 5), 
                            Coord(7, 3), 
                            Coord(7, 4) 
                    )
        
    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.
        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")

        self._board.move_coordinates(place_action)