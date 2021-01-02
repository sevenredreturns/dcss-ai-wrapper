from gamestate import GameState
from actions import Command, Action
import subprocess
import random
import platform
import os
import time

class Agent:
    def __init__(self):
        pass

    def get_game_mode_setup_actions(self):
        raise NotImplementedError()

    def get_action(self, gamestate: GameState):
        raise NotImplementedError()


class SimpleRandomAgent(Agent):
    """
    Agent that takes random cardinal actions to move/attack.
    """

    def do_sprint(self):
        # select sprint and character build
        return [{'msg': 'key', 'keycode': ord('a')},
                {'msg': 'key', 'keycode': ord('b')},
                {'msg': 'key', 'keycode': ord('h')},
                {'msg': 'key', 'keycode': ord('b')}
                ]

    def do_dungeon(self):
        # select dungeon and character build
        return [{'msg': 'key', 'keycode': ord('b')},
                {'msg': 'key', 'keycode': ord('i')},
                {'msg': 'key', 'keycode': ord('c')},
                ]

    def do_dungeon_webserver(self):
        # select dungeon and character build
        return [{'msg': 'input', 'text': 'b'},
                {'msg': 'input', 'text': 'i'},
                {'msg': 'input', 'text': 'c'},
                ]

    def get_game_mode_setup_actions(self):
        return self.do_dungeon()

    def get_game_mode_setup_actions_webserver(self):
        return self.do_dungeon_webserver()

    def get_action(self, gamestate):
        simple_commands = [Command.MOVE_OR_ATTACK_N,
                           Command.MOVE_OR_ATTACK_S,
                           Command.MOVE_OR_ATTACK_E,
                           Command.MOVE_OR_ATTACK_W,
                           Command.MOVE_OR_ATTACK_NE,
                           Command.MOVE_OR_ATTACK_NW,
                           Command.MOVE_OR_ATTACK_SW,
                           Command.MOVE_OR_ATTACK_SE]
        return random.choice(simple_commands)


class TestAllCommandsAgent(Agent):
    """
    Agent that serves to test all commands are working. Cycles through commands in actions.Command enum.
    """

    def __init__(self):
        super().__init__()
        self.next_command_id = 1

    def do_dungeon(self):
        # select dungeon and character build
        return [{'msg': 'key', 'keycode': ord('b')},
                {'msg': 'key', 'keycode': ord('h')},
                {'msg': 'key', 'keycode': ord('b')},
                ]

    def get_game_mode_setup_actions(self):
        return self.do_dungeon()

    def get_action(self, gamestate):

        problematic_actions = [Command.REST_AND_LONG_WAIT,  # some kind of message delay issue
                               Command.WAIT_1_TURN,  # some kind of message delay issue
                               Command.FIND_ITEMS,  # gets stuck on a prompt
                               ]

        try:
            next_command = Command(self.next_command_id)
        except IndexError:
            self.next_command_id = 1
            next_command = Command(self.next_command_id)

        self.next_command_id += 1

        #  skip any known problematic actions for now
        while next_command in problematic_actions:
            next_command = self.get_action(gamestate)

        return next_command


class FastDownwardPlanningAgent(Agent):
    """
    Agent that uses fast downward to solve planning problems to explore a floor.
    """

    pddl_domain_file = ""

    def __init__(self):
        super().__init__()
        self.current_game_state = None
        self.next_command_id = 1
        self.plan_domain_filename = "models/fastdownwardplanningagent_domain.pddl"
        self.plan_current_pddl_state_filename = "models/fdtempfiles/gamestate.pddl"
        self.plan_result_filename = "models/fdtempfiles/dcss_plan.sas"
        self.plan = []
        self.actions_taken_so_far = 0

    def do_dungeon(self):
        # select dungeon and character build
        return [{'msg': 'key', 'keycode': ord('b')},
                {'msg': 'key', 'keycode': ord('h')},
                {'msg': 'key', 'keycode': ord('b')},
                ]

    def do_dungeon_webserver(self):
        # select dungeon and character build
        return [{'msg': 'input', 'text': 'b'},
                {'msg': 'input', 'text': 'i'},
                {'msg': 'input', 'text': 'c'},
                ]

    def get_game_mode_setup_actions(self):
        return self.do_dungeon()

    def get_game_mode_setup_actions_webserver(self):
        return self.do_dungeon_webserver()

    def get_random_nonvisited_nonwall_playerat_goal(self):
        cells_not_visited = []
        cells_visited = []
        closed_door_cells = []
        for cell in self.current_game_state.get_cell_map().get_xy_to_cells_dict().values():
            if cell.has_player_visited:
                cells_visited.append(cell)
            elif not cell.has_wall and not cell.has_player and not cell.has_statue and not cell.has_lava and not cell.has_plant and not cell.has_tree and cell.g:
                # print("added {} as an available cell, it's g val is {}".format(cell.get_pddl_name(), cell.g))
                cells_not_visited.append(cell)
            else:
                pass

            if cell.has_closed_door:
                closed_door_cells.append(cell)

        print("Found {} not visited cells".format(len(cells_not_visited)))
        i = 1
        farthest_away_cells = []
        target_cells = cells_not_visited
        while len(target_cells) > 1:
            farthest_away_cells = target_cells
            # remove all cells that are i distance away from other visited cells
            new_target_cells = []
            for potential_cell in target_cells:
                found_close_visited_cell = False
                for visited_cell in cells_visited:
                    if visited_cell.straight_line_distance(potential_cell) <= i:
                        found_close_visited_cell = True

                if not found_close_visited_cell:
                    new_target_cells.append(potential_cell)

            print("  i={} with {} target cells".format(i, len(new_target_cells)))
            target_cells = new_target_cells
            i+=1

        print("Found {} non visited cells {} distance away from player".format(len(farthest_away_cells), i-1))

        if i < 4 and len(closed_door_cells) > 1:
            print("Attempting to choose a closed door as a goal if possible")
            goal_cell = random.choice(closed_door_cells)
        else:
            goal_cell = random.choice(farthest_away_cells)
            print("Visited {} cells - Goal is now {}".format(len(cells_visited), goal_cell.get_pddl_name()))

        return "(playerat {})".format(goal_cell.get_pddl_name())

    def get_first_monster_goal(self):
        """
        This picks a the first available monster and chooses that monsters cell to be the goal. In the process of trying to move
        into the monsters cell, the agent should end up attacking the monster, because movement and attacking are the
        same thing (for melee).
        """
        cells_with_monsters = []
        for cell in self.current_game_state.get_cell_map().get_xy_to_cells_dict().values():
            if cell.monster and cell.monster.threat != 0:
                cells_with_monsters.append(cell)

        if len(cells_with_monsters) == 0:
            return None

        monster_cell_goal = random.choice(cells_with_monsters)
        monster_goal_str = "(playerat {})".format(monster_cell_goal.get_pddl_name())
        print("about to return monster goal: {}".format(monster_goal_str))
        #time.sleep(1)
        return monster_goal_str

    def get_plan_from_fast_downward(self, goals):
        # step 1: write state output so fastdownward can read it in
        if self.current_game_state:
            self.current_game_state.write_pddl_current_state_to_file(filename=self.plan_current_pddl_state_filename,
                                                                     goals=goals)
        else:
            print("WARNING current game state is null when trying to call fast downward planner")
            return []

        # step 2: run fastdownward
        # fast_downward_process_call = ["./FastDownward/fast-downward.py",
        #                               "--plan-file {}".format(self.plan_result_filename),
        #                               "{}".format(self.plan_domain_filename),
        #                               "{}".format(self.plan_current_pddl_state_filename),
        #                               "--search \"astar(lmcut())\""]
        # This is used for linux
        fast_downward_process_call = [
            "./FastDownward/fast-downward.py --plan-file {} {} {} --search \"astar(lmcut())\"".format(
                self.plan_result_filename,
                self.plan_domain_filename,
                self.plan_current_pddl_state_filename), ]
        # This is used for windows
        fast_downward_system_call = "python FastDownward/fast-downward.py --plan-file {} {} {} --search \"astar(lmcut())\" {}".format(
            self.plan_result_filename,
            self.plan_domain_filename,
            self.plan_current_pddl_state_filename,
            "> NUL") # this last line is to remove output from showing up in the terminal, feel free to remove this if debugging

        # print("About to call fastdownward like:")
        # print(str(fast_downward_process_call))
        print("platform is {}".format(platform.system()))
        if platform.system() == 'Windows':
            os.system(fast_downward_system_call)
        elif platform.system() == 'Linux':
            subprocess.run(fast_downward_process_call, shell=True, stdout=subprocess.DEVNULL)

        # step 3: read in the resulting plan
        plan = []
        try:
            with open(self.plan_result_filename, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if ';' not in line:
                        if line[0] == '(':
                            pddl_action_name = line.split()[0][1:]
                            command_name = pddl_action_name.upper()
                            plan.append(Command[command_name])
                    else:
                        # we have a comment, ignore
                        pass
        except FileNotFoundError:
            print("Plan could not be generated...")
            # Todo - change the goal here
            return

        # for ps in plan:
        #    print("Plan step: {}".format(ps))

        return plan

    def equip_best_items(self):
        """
        Calling this will have the agent evaluate the best items
        """


    def read_scrolls(self):
        """
        The agent will read all scrolls in its inventory
        """


    def can_create_plan_to_reach_next_floor(self):
        """
        Returns a plan to go to the next floor
        """

        player_goal_str = None

        # first find a stair down
        cells_with_stairs_down = []
        for cell in self.current_game_state.get_cell_map().get_xy_to_cells_dict().values():
            if cell.has_stairs_down:
                cells_with_stairs_down.append(cell)

        # set the goal to be player at cell with stairs down
        if len(cells_with_stairs_down) > 0:
            player_goal_str = "(playerat {})".format(random.choice(cells_with_stairs_down).get_pddl_name())
        else:
            return False

        # create a plan to reach the stairs
        plan = self.get_plan_from_fast_downward(goals=[player_goal_str])

        # add an action to take the stairs down
        if plan and len(plan) > 0:
            plan.append(Command.TRAVEL_STAIRCASE_DOWN)

        return plan

    def get_action(self, gamestate: GameState):
        self.current_game_state = gamestate

        if self.current_game_state.more_prompt:
            print("More prompt is true, making a plan of 1 action to send Enter Key")
            self.plan = [Command.ENTER_KEY]

        if self.plan is None or len(self.plan) == 0:
            if self.actions_taken_so_far % 10 == 0:
                if random.random() < 0.15:
                    stair_plan = self.can_create_plan_to_reach_next_floor()
                    if stair_plan:
                        self.plan = stair_plan
                        print("PLAN: Going to next level via stairs down")

        while_loop_iterations = 0
        while self.plan is None or len(self.plan) == 0:
            # select a new goal and plan until we find a plan that's non empty

            selected_goal = None

            # attack monsters first
            monster_goal = self.get_first_monster_goal()
            if monster_goal:
                self.plan = self.get_plan_from_fast_downward(goals=[monster_goal])
                selected_goal = monster_goal
            else:
                goal = self.get_random_nonvisited_nonwall_playerat_goal()
                self.plan = self.get_plan_from_fast_downward(goals=[goal])
                selected_goal = goal

            while_loop_iterations += 1
            if while_loop_iterations > 1:
                print("  in while loop, goal is {}, iterations is {}".format(selected_goal, while_loop_iterations))

        next_action = None
        if len(self.plan) > 0:
            next_action = self.plan.pop(0)
            self.actions_taken_so_far += 1
        else:
            print("warning - no plan!")

        return next_action
