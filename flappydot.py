from gamelib import Sprite, GameApp, Text
from PIL import Image, ImageTk
import tkinter as tk
import random


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
JUMP_VELOCITY = -20
STARTING_VELOCITY = -30

# > Development Feature <
DEV_ENV = False
DEATH_MECHANISM = True
SCORE_PER_PIPE = 1


class PillarPair(Sprite):
    def init_element(self):
        self.is_started = True

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    def update(self):
        if self.is_started:
            self.x -= 5

    def is_out_of_screen(self):
        return self.x < -(0.05*CANVAS_WIDTH)

    def reset_position(self):
        self.x = CANVAS_WIDTH + 0.05*(CANVAS_WIDTH)

    def random_height(self):
        self.y = random.randint(0.25*CANVAS_HEIGHT,
                                CANVAS_HEIGHT-0.25*CANVAS_HEIGHT)

    def dot_passed(self):
        return self.x == CANVAS_WIDTH//2

    def is_hit(self, dot):
        assert type(
            dot) == Dot, "The dot param must be the instance of Dot object"
        dot_x_front = dot.x + 20
        dot_y_top = dot.y + 20
        dot_y_bottom = dot.y - 20

        return (dot_x_front >= self.x - 40 and dot_x_front <= self.x + 40) and \
            (dot_y_top < self.y - 100 or dot_y_top > self.y +
             100 or dot_y_bottom < self.y - 100 or dot_y_bottom > self.y + 100)


class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False
        self.facing_angle = 0
        if DEV_ENV:
            self.hit_box = self.canvas.create_rectangle(
                self.x - 20, self.y - 20, self.x + 20, self.y+20,
                width=1, dash=(4, 2))

    def init_canvas_object(self):

        self.image = Image.open(self.image_filename)
        self.image = self.image.rotate(0)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas_object_id = self.canvas.create_image(
            self.x,
            self.y,
            image=self.tk_image)

    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY
            self.facing_angle -= 6
            self.canvas.delete(self.canvas_object_id)
            self.tk_image = ImageTk.PhotoImage(
                self.image.rotate(self.facing_angle))
            self.canvas_object_id = self.canvas.create_image(
                self.x,
                self.y,
                image=self.tk_image)
            if DEV_ENV:
                self.canvas.coords(self.hit_box, self.x - 20,
                                   self.y - 20, self.x + 20, self.y+20)

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    def jump(self):
        self.facing_angle = 40
        self.vy = JUMP_VELOCITY

    def is_out_of_screen(self):
        return self.y > CANVAS_HEIGHT or self.y < 0


class TextImage(Sprite):
    pass


class FlappyGame(GameApp):
    def add_score(self):
        self.score += SCORE_PER_PIPE

    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png',
                       CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)

    def create_pillar(self):
        self.pillar_pair = PillarPair(
            self, 'images/pillar-pair.png', CANVAS_WIDTH+0.05*CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.pillar_pair.random_height()
        self.elements.append(self.pillar_pair)

    def check_pillar_onscreen(self):
        if len(self.elements[1:]) != 4 and self.elements[-1].x == CANVAS_WIDTH-0.275*CANVAS_WIDTH+0.05*CANVAS_WIDTH:
            self.create_pillar()

    def displayed_score(self):
        self.score_image_list = []
        for i in range(len(str(self.score))):
            image_name = 'images/number/'+str(self.score)[i]+'.png'
            position = CANVAS_WIDTH/(3*(len(str(self.score)) + 1))
            self.score_image_list.append(
                TextImage(self, image_name, CANVAS_WIDTH/3 + position*(i+1), CANVAS_HEIGHT*0.1))

    def init_game(self):
        self.score = 0
        self.displayed_score()
        self.create_sprites()
        for element in self.elements[1:]:
            element.random_height()
        self.is_started = False
        self.is_gameover = False

    def pre_update(self):
        pass

    def post_update(self):
        # Check if the dot is falling out from the screen
        if self.dot.is_out_of_screen() and DEATH_MECHANISM:
            # Change game state to gameover
            self.is_started = False
            self.is_gameover = True
            # Stop every eliments
            for element in self.elements[1:]:
                element.stop()
        self.check_pillar_onscreen()
        for element in self.elements[1:]:
            if element.is_hit(self.dot) and DEATH_MECHANISM:
                self.is_gameover = True
                self.is_started = False
            if element.dot_passed():
                self.add_score()
                self.displayed_score()
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
                return
            self.dot.jump()

        if event.keysym == "r" and self.is_gameover:
            # R button press to reset game when gameover.
            for item in self.elements:
                self.canvas.delete(item.canvas_object_id)
            self.elements = []
            self.init_game()
            self.is_gameover = False
            return


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")

    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
