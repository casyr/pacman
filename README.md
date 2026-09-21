*This project has been created as part of the 42 curriculum by yriffard, advacher.*
## Description
This project is a playable recreation of the classic arcade game PacMan. Built in Python 3.10, a strict Model-View-Controller (MVC) architecture, and use MiniLibX functions equivalence as graphical library. The game features : graphical UI, persistent highscores, autonomous ghost AI, and dynamic level generation.
## Instructions
**Installation & Setup:**  
This project relies on `uv` for package management and uses Python >=3.10 features.  
Dependencies can be installed via the provided Makefile using `make install`.  
**Execution:**  
The game must be launched from the command line, taking exactly one argument (a JSON configuration file).  
`uv run python3 -m src src/config.json`  
Use `make run` to execute the main script

## Configuration
The game is configured via a JSON file that supports inline comments (starting with #). A config.json is furnished. If invalid or missing values are encountered, the game clamps to safe defaults and logs a clear message without crashing or displaying a Python traceback.
Key configuration parameters include:  

* **highscore_filename:** Path to the highscore save file (Default: "highscore.json").

* **lives:** Initial number of player lives (Default: 3, Minimum: 1, Maximum: 10).

* **pacgum:** Number of pacgums required. If the value is too high compared to the maze size, it clamps to a safe value (Default: 42, Minimum: 1).

* **super_pacgum:** Number of super pacgums (Default: 4, Minimum: 1, Maximum: 4).

* **points_per_pacgum:** Points awarded for eating a regular pacgum (Default: 10, Minimum: 1, Maximum: 10).

* **points_per_super_pacgum:** Points awarded for eating a super pacgum (Default: 50, Minimum: 1, Maximum: 50).

* **points_per_ghost:** Points awarded for eating a vulnerable ghost (Default: 200, Minimum: 1, Maximum: 200).

* **level_max_time:** Maximum time allowed per level in seconds (Default: 90, Minimum: 40, Maximum: 3600).

* **seed:** Seed controlling the maze generation (Default: 42).

* **levels:** Array defining multiple levels (Default: 10 levels).

* **width, height:** Dimensions for each level configuration. 


## Highscore

The game features highscore system managed by the HighScoreManager and JsonModelLoader classes.It retains the top 10 scores alongside player names (limited to a maximum of 10 alphanumeric characters and spaces).  
Scores are stored locally in a JSON format.  
The system loads at the game start to display scores in the Main Menu and ask the player to save their score at the end of a session (Win or Lose).

## Maze GenerationLevel
Maze are generated dynamically using an external assigned A-Maze-ing package.  
The package is used exactly as-is without internal modification.  
The generator's PERFECT parameter is set to False to ensure the creation of looped ,Pac-Man-compatible corridors.  
The first level is generated using a fixed seed (e.g., 42) to ensure first level is the same, while others levels are randomly generated. 

## Implementation
The codebase strictly adheres to the **flake8** coding standard and uses **mypy** for static type checking across all functions. **Exception handling** is implemented using try-except blocks and context managers to ensure graceful failure without application crashes or resource leaks. A **cheat mode** is also implemented to facilitate evaluation.


## General Software Architecture
**Model:** The logic resides in classes like GameSession, LevelBuilder, GameBoard and Entity. 
* The `GameSession` tracks value update during the party, including the current score, remaining lives, active power mode, and level timers.

* `LevelBuilder` acts as interprets configuration data to construct the maze, determine bounds, and instantiate the initial entities for the GameBoard.

* The `GameBoard` dataclass serves as centralizing to the active level :  
    * `MazeAdapter` (grid data),
    * `PacMan` player entity,
    * `Ghost` list of entities,
    * the coordinate for all `pacgums` and `super-pacgums`.

* `Entity` abstract base class defining base properties, spawn positions, movement vectors, and speed parameters. all entity will herit from this class


**Controller:** The GameController acts as the orchestrator.  

* Initialized from main() entry point, it loads the configuration, initializes the LevelBuilder and HighScoreManager, captures real-time, updates session timers, and triggers the update(elapsed_time) loop for all active entities.  

* Game loop governed by a state machine (MENU, PLAYING, PAUSED, VICTORY, DEFEAT, ENTER_HIGHSCORE).

* It independently resolves spatial collisions (detecting intersections between the player, collectibles, and ghosts), manages score accruals via the session manager, handles ghost vulnerability transitions, and coordinates entity respawns.

**View:**   
The graphical user interface manages the Main Menu, the in-game GUI (Graphical user interface) (displaying score, lives, level, and remaining time), the Pause Menu, and the Game Over / Victory screens.


## Resources