import os
import tkinter as tk
import sys

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 500


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
                        Ver. 0.1.0
"""
print("-" * 60)
print(welcome_message, end="")
print("-" * 60)
announce("*", "Running game prerequested check-list")

PREREQUEST_CHECK_PASS = False
# Check if the PIL helper is compiled
try:
    from helper_modules.PIL import Image, ImageTk
    announce("P", "PIL Binary is already compiled", prefix=" |-")
    PREREQUEST_CHECK_PASS = True
except ImportError as e:
    if e.args[0][0:29] == "cannot import name '_imaging'":
        announce("X", "PIL Binary is not compiled", prefix=" |-")
        announce("*", "Compiling now. . .", prefix="   |-")
        current_working_dir = os.getcwd()
        os.chdir(f"{current_working_dir}/helper_modules/PIL_compiler/")
        os.system(
            f"python3 setup.py -q build_ext --build-lib=../")
        announce("P", "Complete the compilation of PIL Binary", prefix="   |-")
        os.chdir(current_working_dir)
        PREREQUEST_CHECK_PASS = True
    else:
        announce(
            "X", "Unknown error occurrend while importing required library and can't be fixed automatically")
        announce("*", e.args[0], prefix=" |-")

if not PREREQUEST_CHECK_PASS:
    announce(
        "X", "Prerequesed check-list not pass. Game can't be launched")
    sys.exit(1)

announce("P", "Prerequested check-list passed. Launching the game. Enjoy!")
start_game()
