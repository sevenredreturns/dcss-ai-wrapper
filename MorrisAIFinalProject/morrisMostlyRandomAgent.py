from dcss.agent.base import BaseAgent
from dcss.state.game import GameState
from dcss.actions.action import Action
from dcss.actions.command import Command
from dcss.websockgame import WebSockGame
from dcss.connection.config import WebserverConfig

import random


class MyAgent(BaseAgent) :

    def __init__(self) :
        super().__init__()
        self.gamestate = None

    def get_action(self, gamestate: GameState) :
        self.gamestate = gamestate

        cellmap = self.gamestate.get_cell_map()
        cellmaprad = cellmap.get_radius_around_agent_cells()

        print(cellmaprad)

        currenthp = self.gamestate.player_current_hp
        maxhp = self.gamestate.player_hp_max
        autoexplore = self.gamestate.is_exploration_done()
        autofight = self.gamestate.is_enemy_around()
        on_stairs = self.gamestate.can_go_down()
        too_injured = self.gamestate.too_injured()
        levelup = self.gamestate.leveling_up()
        print(currenthp)
        print(maxhp)
        print(maxhp * .45)
        print(autofight)
        print(autoexplore)
        print(on_stairs)

        # need to move toward > symbol
        def what_is_around() :
            #What can we see?  Hoping for more intelligent pathing.
            cellitems = []
            for cell in cellmap.get_xy_to_cells_dict().values() :
                cellitems.append(cell)

            return cellitems



        def path_to_stairs() :
            cells_with_stairs = []
            for cell in cellmap.get_xy_to_cells_dict().values() :
                if cell.has_stairs_down :
                    cells_with_stairs.append(cell)

            if len(cells_with_stairs) > 0 :
                player_goal_str = "(playerat {})".format(random.choice(cells_with_stairs))
                print(player_goal_str)
                return player_goal_str
            else :
                return False

        def monster_exists() :
            cells_with_monsters = []
            for cell in cellmap.get_xy_to_cells_dict().values():
                if cell.monster:
                    cells_with_monsters.append(cell)

            if len(cells_with_monsters) > 0 :
                return False
            else:
                return True

        path_to_stairs()
        what_is_around()
        autofight = monster_exists()

        # get all possible actions
        if too_injured :
            return Command.REST_AND_LONG_WAIT
        elif levelup :
            # Funky, I know, but the save game command a capital S, which is required for the prompt to level strength.
            return Command.SAVE_GAME_AND_EXIT
        elif on_stairs :
            return Command.TRAVEL_STAIRCASE_DOWN
        # These commands lead to an infinte loop?
        elif not autofight :
           return Command.AUTO_FIGHT
        #elif not autoexplore :
        #    return Command.AUTO_EXPLORE
        else :
            actions = Action.get_all_move_commands()
            # currentaction = self.gamestate.get
            # # pick an action at random
            # chosen = random.choice(actions)
            # if chosen is
            return random.choice(actions)


if __name__ == "__main__" :
    my_config = WebserverConfig

    # Toggle what is commented in the game_id section to choose between a seeded and unseeded game
    my_config.game_id = 'dcss-web-trunk'
    # my_config.game_id = 'seeded-web-trunk'

    my_config.delay = 0.4
    my_config.species = 'Troll'
    my_config.background = 'Fighter'
    my_config.starting_weapon = 'war axe'

    my_config.auto_start_new_game = True
    my_config.always_start_new_game = False

    # create game
    game = WebSockGame(config=my_config, agent_class=MyAgent)
    game.run()
