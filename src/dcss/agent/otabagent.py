import os
import platform
import random
import subprocess

from dcss.websockgame import WebSockGame
from dcss.connection.config import WebserverConfig

from dcss.agent.base import BaseAgent
from dcss.actions.command import Command
from dcss.state.game import GameState
from dcss.state.monster import Monster

import logging
logging.basicConfig(level=logging.WARNING)


class OTabAgent(BaseAgent):
    """
    Agent that uses 'o' macro to explore and then 'tab' to fight whenever there is a monster. If health is low, behavior
    is undefined.
    """

    def __init__(self):
        super().__init__()
        self.current_game_state = None
        self.nearby_monster = False

    def check_for_monsters(self):
        """
        Returns true if one or more nearby monsters
        """
        print("all monsters are: {}".format(Monster.ids_to_monsters))
        for monster_id in Monster.ids_to_monsters.keys():
            print("  monster {} has cell {}".format(monster_id, Monster.ids_to_monsters[monster_id].cell))
        self.nearby_monster = False
        for cell in self.current_game_state.get_cell_map().get_xy_to_cells_dict().values():
            if cell.monster:
                print("cell.monster = {}".format(cell.monster))
                self.nearby_monster = True

    def get_action(self, gamestate: GameState):
        self.current_game_state = gamestate

        self.check_for_monsters()

        if self.nearby_monster:
            return Command.AUTO_FIGHT
        else:
            return Command.AUTO_EXPLORE



if __name__ == "__main__":
    my_config = WebserverConfig

    # set game mode to Tutorial #1
    my_config.game_id = 'dcss-web-trunk'
    my_config.delay = 1.0
    my_config.species = 'Minotaur'
    my_config.background = 'Berserker'
    my_config.always_start_new_game = True
    my_config.auto_start_new_game = True

    # create game
    game = WebSockGame(config=my_config, agent_class=OTabAgent)
    game.run()