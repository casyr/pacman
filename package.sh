#!/bin/bash

RELEASE_DIR="pacman_release"
mkdir -p $RELEASE_DIR

cp -r src sprites 42_modules $RELEASE_DIR/
cp pyproject.toml uv.lock pac-man.py config.json $RELEASE_DIR/

cat << 'EOF' > $RELEASE_DIR/start.sh
#!/bin/bash
echo "Installation dependencies..."
uv sync
echo "Lunch Game..."
uv run python3 pac-man.py config.json
EOF

chmod +x $RELEASE_DIR/start.sh

cat << 'EOF' > $RELEASE_DIR/INSTRUCTIONS.txt
To play, open a terminal in this folder and run: ./start.sh

The game is configured via a JSON file that supports inline comments (starting with #). A config.json is furnished. If invalid or missing values are encountered, the game clamps to safe defaults.
Key configuration parameters include:  

highscore_filename: Path to the highscore save file (Default: "highscore.json").
lives: Initial number of player lives (Default: 3, Minimum: 1, Maximum: 10).
pacgum: Number of pacgums required. If the value is too high compared to the maze size, it clamps to a safe value (Default: 42, Minimum: 1).
super_pacgum: Number of super pacgums (Default: 4, Minimum: 1, Maximum: 4).
points_per_pacgum: Points awarded for eating a regular pacgum (Default: 10, Minimum: 1, Maximum: 10).
points_per_super_pacgum: Points awarded for eating a super pacgum (Default: 50, Minimum: 1, Maximum: 50).
points_per_ghost: Points awarded for eating a vulnerable ghost (Default: 200, Minimum: 1, Maximum: 200).
level_max_time: Maximum time allowed per level in seconds (Default: 90, Minimum: 40, Maximum: 3600).
seed: Seed controlling the maze generation (Default: 42).
levels: Array defining multiple levels (Default: 10 levels, Maximum: 20).
width, height: Dimensions for each level configuration (Default: 10, Minimum: 10, Maximum: 20).

To know how to play when the game is lunched go on instruction menu.
EOF

zip -r pacman_release.zip $RELEASE_DIR
rm -rf $RELEASE_DIR