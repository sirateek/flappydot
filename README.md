# flappydot
Flappy dot. KU Computer Programming II Homework.

![TitleImage](https://github.com/sirateek/flappydot/raw/main/images/example/title.png)
![In-Game Image](https://github.com/sirateek/flappydot/raw/main/images/example/in-game.png)

# Test
| Test       | Status                                                                                                                                                               |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PEP8 Check | [![Python PEP8 Check](https://github.com/sirateek/flappydot/actions/workflows/pep8.yml/badge.svg)](https://github.com/sirateek/flappydot/actions/workflows/pep8.yml) |

# Version
v.1.0.0
# Installation
1. Clone this repository into your local computer
2. Start game by running `python3 run.py`

# Complatibility
### Tested on these OS and Python Version
| Operating System | Python Version | Complatibility |
|------------------|----------------|----------------|
| Mac OSX 11.2.3   | 3.9            | ✅              |
| Windows 10       | 3.9            | ✅              |

### This game is depended on this 3rd party library
- [Pillow](https://github.com/python-pillow/Pillow)

The game launcher (`run.py`) will automatically check if the Pillow is available to be imported. If not it will ask the user to install it.

> Note: **If no `Pillow`, The game can't be launched** since it is needed to implement bird physical movement.

To install it manually. Use
```bash
python3 -m pip install --upgrade Pillow
```
or
```bash
pip3 install --upgrade Pillow
```

