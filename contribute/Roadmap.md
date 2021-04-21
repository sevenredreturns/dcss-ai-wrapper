# Roadmap to Version 1.0 

The following is a tentative roadmap for the project to reach version 1.0.

### v0.1
*  ~~Sprint game mode is supported~~
*  ~~Items in cells can be parsed by the game state~~
*  ~~Add pddl actions to pickup, equip, drop, take-off, and more for items to PDDL domain file~~
*  Add mapping from pddl item actions to Commands, thereby making every pddl action executable
*  ~~New agent class that acts as a passthrough for a human player to play the game~~ 
*  Implement and test complete vector-based state representations
*  Implement and test partial-view vector-based state representations
*  Implement and test complete pddl-based state representations
*  Implement and test partial pddl-based state representations
*  ~~Simple planning agent working on tutorials~~
*  Document simple planning agent on tutorial 1
*  ~~Simple reinforcement learning agent working on tutorials~~
*  Document simple RL agent on tutorial 1
*  Consider switching to library name daiw, crawlai, crawlwrap, or similar similar to leave 'dcss' open
*  (Last) push to PyPi
*  (Last) test external examples work without having to install 
*  (Last) Record tutorial videos for installing, running, and creating custom agents.

### v0.2
*  Extend all features from O.1 to the Linux terminal version of the game
*  Add support for autobahn for terminal version of the game
*  Refactor game connection code to be less redundant between browser and terminal versions of the game

### v0.3
*  Implement mapping for the harder PDDL actions for casting spells, throwing, and other targetable abilities
*  Add sensing actions to PDDL
*  Add mapping from PDDL sensing actions to Commands

### v0.4
*  Add metrics for measuring API performance (speed of actions being sent to game, etc.)
*  Add metrics for measuring agent performance (number of tiles visited, experience level, number of monsters killed, etc.)

### v0.5
*  Add player skills into the gamestate data
*  Add actions to change experience point allocation for skills 

### v0.6 
*  Enable agent to receive spectator commands through spectator chat, including 'pause' and 'resume'

### v0.7
*  ?

### v0.8
*  Code refactoring to adhere to better design principles

### v 0.9
*  Replace debugging print statements with logging statements
*  Log files separated into agent logs and network logs

### v 1.0
*  Documentation of all functions
*  Documentation hosted on pypi packages page
 
