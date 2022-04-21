import os
import platform
import random
import subprocess

from dcss.websockgame import WebSockGame
from dcss.connection.config import WebserverConfig

from dcss.agent.base import BaseAgent
from dcss.actions.command import Command
from dcss.state.game import GameState

import logging

logging.basicConfig(level=logging.WARNING)


class FastDownwardPlanningBaseAgent(BaseAgent) :
    """
    Agent that uses fast downward to solve planning problems to explore a floor.
    """

    pddl_domain_file = ""

    def __init__(self) :
        super().__init__()
        self.current_game_state = None
        self.next_command_id = 1
        self.plan_domain_filename = "../models/fastdownward_simple.pddl"
        self.plan_current_pddl_state_filename = "../models/fdtempfiles/state.pddl"
        self.plan_result_filename = "../models/fdtempfiles/dcss_plan.sas"
        self.plan = []
        self.actions_taken_so_far = 0
        self.current_goal = None
        self.previous_goal = None
        self.previous_goal_type = None
        self.new_goal = None
        self.new_goal_type = None
        self.current_goal_type = None
        self.num_cells_visited = 0
        self.player_has_seen_stairs_down = {x : False for x in range(0, 50)}
        self.level_up = False
        self.cells_not_visited = []
        self.cells_visited = []
        self.closed_door_cells = []
        self.need_to_heal = None

        self.found_item = None  # if not None, this will be a cell
        self.inventory_full = False

    def process_gamestate_via_cells(self) :
        # REMOVE CLOSED DOORS BY WIPING ARRAY
        # If I don't initialize the array again at the beginning of this, the player just dances between
        # all of the formerly closed doors, because they never get cleared out.  There is probably
        # A better way to do this, but that is for tinkering later.
        self.closed_door_cells = []

        for cell in self.current_game_state.get_cell_map().get_xy_to_cells_dict().values() :
            if cell.has_player_visited :
                self.cells_visited.append(cell)
            elif not cell.has_wall and not cell.has_player and not cell.has_statue and not cell.has_lava and not \
                    cell.has_plant and not cell.has_tree and not cell.teleport_trap and cell.g :
                # Looking for places we can walk. Teleport traps ARE technically walkable, however,
                # there is a dialogue that wants you to press yes to step onto them.  For the sake of
                # "Go down", We're just going to count them as walls.  Plants and trees also count.
                # I think the long delays in the processing are happening either here, or a bit lower down.
                # but given how fast the player can move when it has a goal that isn't exploration, this is rife for
                # cleanup
                self.cells_not_visited.append(cell)
            else :
                pass

            if cell.has_closed_door :
                self.closed_door_cells.append(cell)

            # Checking for either stairs down, which is preferable, or a shaft downwards, which can let you
            # skip several levels and probably die!  but I am trying to find more reliable set points to go to
            if cell.has_stairs_down :
                self.player_has_seen_stairs_down[self.current_game_state.player_depth] = True
                print("Setting stairs down to be True for depth {}".format(self.current_game_state.player_depth))

            if cell.has_shaft :
                self.player_has_seen_stairs_down[self.current_game_state.player_depth] = True
                print("Setting stairs down to be True for depth {}".format(self.current_game_state.player_depth))

        self.num_cells_visited = len(self.cells_visited)

    def get_full_health_goal(self) :
        self.need_to_heal = True
        return

    def get_random_nonvisited_nonwall_playerat_goal(self) :
        #this feels like the other place that could be causing the massive slowdown.
        #I ran a profiler.  Slowdown is here.

        i = 1
        farthest_away_cells = []
        target_cells = self.cells_not_visited
        while len(target_cells) > 1 :
            farthest_away_cells = target_cells
            # remove all cells that are i distance away from other visited cells
            new_target_cells = []
            for potential_cell in target_cells :
                found_close_visited_cell = False
                for visited_cell in self.cells_visited :
                    if visited_cell.straight_line_distance(potential_cell) <= i :
                        found_close_visited_cell = True

                if not found_close_visited_cell :
                    new_target_cells.append(potential_cell)


            target_cells = new_target_cells
            i += 1

        print("Found {} non visited cells {} distance away from player".format(len(farthest_away_cells), i - 1))

        if len(self.closed_door_cells) > 1 :
            # print("Attempting to choose a closed door as a goal if possible")
            goal_cell = random.choice(self.closed_door_cells)
        elif len(farthest_away_cells) > 0 :
            goal_cell = random.choice(farthest_away_cells)
            print("Visited {} cells - Goal is now {}".format(len(self.cells_visited), goal_cell.get_pddl_name()))
        else :
            # can't find any cells
            return None

        goal_str = "(playerat {})".format(goal_cell.get_pddl_name())
        # print("Returning goal str of {}".format(goal_str))
        return goal_str

    def get_first_monster_goal(self) :

        cells_with_monsters = []
        for cell in self.current_game_state.get_cell_map().get_xy_to_cells_dict().values() :
            if cell.monster and not cell.has_plant and not cell.has_tree :
                cells_with_monsters.append(cell)

        if len(cells_with_monsters) == 0 :
            return None

        monster_cell_goal = random.choice(cells_with_monsters)
        monster_goal_str = "(not (hasmonster {}))".format(monster_cell_goal.get_pddl_name())
        # print("about to return monster goal: {}".format(monster_goal_str))
        # time.sleep(1)
        return monster_goal_str

    def get_plan_from_fast_downward(self, goals) :
        # step 1: write state output so fastdownward can read it in
        if self.current_game_state :
            print("About to write out game state with filename {}".format(self.plan_current_pddl_state_filename))
            self.current_game_state.write_pddl_current_state_to_file(filename=self.plan_current_pddl_state_filename,
                                                                     goals=goals)
        else :
            print("WARNING current game state is null when trying to call fast downward planner")
            return []

        # run fastdownward
        # I do not have this compiled for running on linux.  Also tryingto run it via windows command line seems to be
        # un-working
        fast_downward_system_call = "python ../FastDownward/fast-downward.py --plan-file {} {} {} --search " \
                                    "\"astar(lmcut())\" {}".format(
            self.plan_result_filename,
            self.plan_domain_filename,
            self.plan_current_pddl_state_filename,
            "> NUL")

        os.system(fast_downward_system_call)

        # step 3: read in the resulting plan
        plan = []
        try :
            with open(self.plan_result_filename, 'r') as f :
                for line in f.readlines() :
                    line = line.strip()
                    if ';' not in line :
                        if line[0] == '(' :
                            pddl_action_name = line.split()[0][1 :]
                            command_name = pddl_action_name.upper()
                            plan.append(Command[command_name])
                    else :
                        pass
        except FileNotFoundError :
            print("Plan could not be generated...")
            return []
        except :
            print("Unknown error preventing plan from being generated")
            return

        return plan

    def can_create_plan_to_reach_next_floor(self) :
        """
        Returns a plan to go to the next floor
        """

        player_goal_str = None

        # first find a stair down
        cells_with_stairs_down = []
        for cell in self.current_game_state.get_cell_map().get_xy_to_cells_dict().values() :
            if cell.has_stairs_down :
                cells_with_stairs_down.append(cell)

        # set the goal to be player at cell with stairs down
        if len(cells_with_stairs_down) > 0 :
            player_goal_str = "(playerat {})".format(random.choice(cells_with_stairs_down).get_pddl_name())
        else :
            return False

        # create a plan to reach the stairs
        plan = self.get_plan_from_fast_downward(goals=[player_goal_str])

        # add an action to take the stairs down
        if plan and len(plan) > 0 :
            plan.append(Command.TRAVEL_STAIRCASE_DOWN)

        return plan

    def goal_selection(self) :

        # attack monsters first
        monster_goal = self.get_first_monster_goal()
        if monster_goal :
            return monster_goal, "monster"
        # Check your health.  If below 80%, send signal for healing.  Trying to keep out of bad situations
        elif self.current_game_state.player_current_hp < self.current_game_state.player_hp_max * .8 :
            return self.get_full_health_goal(), "heal"
        else :
            self.need_to_heal = False
        if self.player_has_seen_stairs_down[self.current_game_state.player_depth] :
            lower_place_str = "{}_{}".format(self.current_game_state.player_place.lower().strip(),
                                             self.current_game_state.player_depth + 1)
            lower_place_goal = "(playerplace {})".format(lower_place_str)
            print("Goal selection choosing next goal: {}".format(lower_place_goal))
            return lower_place_goal, "descend"
        else :
            goal = self.get_random_nonvisited_nonwall_playerat_goal()
            selected_goal = goal
            return selected_goal, "explore"

    def get_random_simple_action(self) :
        simple_commands = [Command.MOVE_OR_ATTACK_N,
                           Command.MOVE_OR_ATTACK_S,
                           Command.MOVE_OR_ATTACK_E,
                           Command.MOVE_OR_ATTACK_W,
                           Command.MOVE_OR_ATTACK_NE,
                           Command.MOVE_OR_ATTACK_NW,
                           Command.MOVE_OR_ATTACK_SW,
                           Command.MOVE_OR_ATTACK_SE]
        return random.choice(simple_commands)

    def get_action(self, gamestate: GameState) :
        self.current_game_state = gamestate
        self.process_gamestate_via_cells()
        self.level_up = self.current_game_state.leveling_up()

        print("Next Turn Debug Variables:")
        print("Are we leveling up?")
        print(self.current_game_state.leveling_up())
        print("Just the level up variable")
        print(self.level_up)
        print("Do we need to heal?")
        print(self.need_to_heal)

        self.new_goal, self.new_goal_type = self.goal_selection()
        print("Player at: {},{}".format(self.current_game_state.agent_x, self.current_game_state.agent_y))
        print("New goal: {} with type: {}".format(self.new_goal, self.new_goal_type))
        for a in self.plan :
            print("  plan action is {}".format(a))

        if self.new_goal and self.new_goal_type and (
                len(self.plan) < 1 or self.new_goal_type != self.previous_goal_type) :
            self.current_goal = self.new_goal
            self.current_goal_type = self.new_goal_type
            # plan
            print("Planning with goal {}".format(self.new_goal))
            self.plan = self.get_plan_from_fast_downward(goals=[self.new_goal])
            self.previous_goal = self.new_goal
            self.previous_goal_type = self.new_goal_type

        next_action = None
        if self.level_up == True :
            # I want to default to leveling strength, if I get far enough to level.  Therefore, I use the Save Game
            # and Exit command, as that is a capital S, the input required for Strength.
            next_action = Command.SAVE_GAME_AND_EXIT
            return next_action
        elif self.need_to_heal == True and self.current_goal_type != 'monster' and self.new_goal_type != 'monster' :
            # If low health, wait to regen - But only if t here are no monsters nearby (hopefully) or this ends in an
            # endless loop.
            next_action = Command.WAIT_1_TURN
            return next_action
        elif self.plan and len(self.plan) > 0 :
            # If we have a plan, get our next action from our plan
            next_action = self.plan.pop(0)
            #Wiping out the saved state file, to hopefully solve the confusion issues on new floor
            if next_action == Command.TRAVEL_STAIRCASE_DOWN:
                os.remove(self.plan_current_pddl_state_filename)
                os.remove(self.plan_result_filename)

            self.actions_taken_so_far += 1
            return next_action

        # We don't have a plan
        print("warning - no plan, taking random action!")
        next_action = self.get_random_simple_action()
        return next_action


if __name__ == "__main__" :
    my_config = WebserverConfig
    # Toggle what is commented in the game_id section to choose between a seeded and unseeded game
    my_config.game_id = 'dcss-web-trunk'
    # my_config.game_id = 'seeded-web-trunk'
    my_config.delay = 0.4
    my_config.species = 'Troll'
    my_config.background = 'Fighter'
    my_config.starting_weapon = 'war axe'

    # Set second value to true to make it s tart a new game every time you start this script.
    my_config.auto_start_new_game = True
    my_config.always_start_new_game = False

    # create game
    game = WebSockGame(config=my_config, agent_class=FastDownwardPlanningBaseAgent)
    game.run()
