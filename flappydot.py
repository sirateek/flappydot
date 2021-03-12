import tkinter as tk
import random
from gamelib import Sprite, GameApp, Text

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
JUMP_VELOCITY = -20
STARTING_VELOCITY = -30


class PillarPair(Sprite):
    def init_element(self):
        self.is_started = True

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    def update(self):
        if self.is_started:
            self.x -= 2
        else:
            pass

    def is_out_of_screen(self):
        return self.x < -30

    def reset_position(self):
        self.x = CANVAS_WIDTH + 30

    def random_height(self):
        self.y = random.randint(0.25*CANVAS_HEIGHT,
                                CANVAS_HEIGHT-0.25*CANVAS_HEIGHT)


class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False

    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    def jump(self):
        self.vy = JUMP_VELOCITY

    def is_out_of_screen(self):
        return self.y > CANVAS_HEIGHT or self.y < 0


class FlappyGame(GameApp):
    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png',
                       CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)

    def create_pillar(self):
        self.pillar_pair = PillarPair(
            self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.pillar_pair.random_height()
        self.elements.append(self.pillar_pair)

    def check_pillar_onscreen(self):
        if len(self.elements[1:]) != 4 and self.elements[-1].x == CANVAS_WIDTH-0.275*CANVAS_WIDTH:
            self.create_pillar()

    def init_game(self):
        self.create_sprites()
        for element in self.elements[1:]:
            element.random_height()
        self.is_started = False
        self.is_gameover = False

    def pre_update(self):
        pass

    def post_update(self):
        # Check if the dot is falling out from the screen
        if self.dot.is_out_of_screen():
            # Change game state to gameover
            self.is_started = False
            self.is_gameover = True
            # Stop every eliments
            for element in self.elements:
                element.stop()
        self.check_pillar_onscreen()
        for element in self.elements[1:]:
            if element.is_out_of_screen():
                element.reset_position()
                element.random_height()

    def on_key_pressed(self, event):
        if event.keysym == "space":
            if not self.is_started and not self.is_gameover:
                self.create_pillar()
                self.is_started = True
                self.dot.start()
                return
            if self.is_gameover:
                # TODO: Implement the restart game function
                for _ in range(len(self.elements)):
                    self.canvas.delete(self.elements[0].canvas_object_id)
                    self.elements.pop(0)
                self.init_game()
                self.is_gameover = False
                return
            self.dot.jump()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")

    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
