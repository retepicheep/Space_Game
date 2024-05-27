# game_launcher.py

import os

# import sys
import subprocess


def main():
    # Change directory to where your game script is located
    os.chdir("/Users/peterdillow/git_repos/Space_Game/game.py")

    # Run your game script using Python
    subprocess.run(["python", "game.py"])


if __name__ == "__main__":
    main()
