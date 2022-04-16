from dcss.agent.base import BaseAgent
from dcss.state.game import GameState
from dcss.actions.action import Action

from dcss.websockgame import WebSockGame
from dcss.connection.config import WebserverConfig

import random


class MyAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self.gamestate = None

    def get_action(self, gamestate: GameState):
        self.gamestate = gamestate

        cellmap = self.gamestate.get_cell_map()



        print(cellmap)
        cellmap.draw_cell_map()
        cellmap.get_radius_around_agent_cells()
        currenthp = self.gamestate.player_current_hp
        maxhp = self.gamestate.player_hp_max
        not_autoexplore = self.gamestate.is_exploration_done()
        not_autofight = self.gamestate.is_enemy_around()
        on_stairs = self.gamestate.can_go_down()
        print(currenthp)
        print(maxhp)
        print(maxhp * .3)
        print(not_autofight)
        print(not_autoexplore)
        print(on_stairs)

        # get all possible actions
        if currenthp < (.3 * maxhp) :
            actions = Action.get_all_move_commands()
            return random.choice(actions)
        elif on_stairs:
            actions = Action.get_stairs_down()
            return random.choice(actions)
        elif not not_autofight:
            actions = Action.get_auto_fight()
            return random.choice(actions)
        elif not not_autoexplore :
            actions = Action.get_auto_explore()
            return random.choice(actions)
        else:
            actions = Action.get_all_move_commands()
        # pick an action at random
            return random.choice(actions)


if __name__ == "__main__":
    my_config = WebserverConfig

    # set game mode to Tutorial #1
    my_config.game_id = 'dcss-web-trunk'

    # create game
    game = WebSockGame(config=my_config, agent_class=MyAgent)
    game.run()
