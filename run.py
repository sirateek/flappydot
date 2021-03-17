import os
import tkinter as tk
import sys

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600


def announce(icon, messages, prefix=""):
    print(f"{prefix}[{icon}]: {messages}")


def start_game():
    from flappydot import FlappyGame
    root = tk.Tk()
    root.title("Flappydot Game")

    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT)
    app.start()
    root.mainloop()


welcome_message = """\
                Welcome to flappydot game
                        Ver. 1.0.0
"""
print("-" * 60)
print(welcome_message, end="")
print("-" * 60)
announce("*", "Running game prerequested check-list")

PREREQUEST_CHECK_PASS = False
# Check if the PIL helper is compiled
try:
    from PIL import Image, ImageTk
    announce("P", "PIL is installed", prefix=" |-")
    PREREQUEST_CHECK_PASS = True
except ImportError as e:
    if e.args[0][0:37] == "cannot import name 'Image' from 'PIL'" or e.args[0] == "No module named 'PIL'":
        announce("X", "PIL is not installed", prefix=" |-")
        while True:
            ask_install = input(
                "PIL is an imaging lib required in this game. Do you want to install it now (`y` or `n`)? ")
            if ask_install == "y":
                os.system(
                    f"python3 -m pip install --upgrade Pillow")
                announce("P", "Complete to install Pillow", prefix="   |-")
                announce("i", "Please restart the game", prefix="   |-")
                sys.exit(0)
            elif ask_install == "n":
                announce("X", "Skiped installing Pillow", prefix="   |-")
                break
            else:
                announce("?", "Please insert only `y` or `n`", prefix="   |-")
    else:
        announce(
            "X", "Unknown error occurrend while importing required library and can't be fixed automatically")
        announce("*", e.args[0], prefix=" |-")

if not PREREQUEST_CHECK_PASS:
    announce(
        "X", "Prerequesed check-list not pass. Game can not be launched")
    sys.exit(1)

announce("P", "Prerequested check-list passed. Launching the game. Enjoy!")
start_game()
