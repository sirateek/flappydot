from gamelib import Sprite, GameApp, Text
from PIL import Image, ImageTk
import tkinter as tk
import random


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 0.7
JUMP_VELOCITY = -10
STARTING_VELOCITY = -10
SPEED = 4

# > Development Feature <
DEV_ENV = False
DEATH_MECHANISM = True


class PillarPair(Sprite):
    def init_element(self):
        self.is_started = True
        self.speed = 1

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    def update(self):
        if self.is_started:
            self.x -= 1

    def is_out_of_screen(self):
        return self.x < -(0.05*CANVAS_WIDTH)

    def reset_position(self):
        self.x = CANVAS_WIDTH + 0.05*(CANVAS_WIDTH)

    def random_height(self):
        self.y = random.randint(0.25*CANVAS_HEIGHT,
                                CANVAS_HEIGHT-0.25*CANVAS_HEIGHT)

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
        if self.is_started and self.y <= CANVAS_HEIGHT - 20:
            self.y += self.vy
            self.vy += GRAVITY
            self.facing_angle -= 4
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
        return self.y > CANVAS_HEIGHT-20 or self.y < 0


class Intro(Sprite):
    pass


class FlappyGame(GameApp):
    def intro_image(self):
        self.intro_list = self.image_name = ["intro1", "intro2", "intro3", "intro4", "intro5", "intro6", "intro7", "intro8", "intro9", "intro10",
                                             "intro11", "intro12", "intro13", "intro14", "intro15", "intro16", "intro17",
                                             "intro18", "intro19", "intro20", "intro21", "intro22", "intro23", "intro24",
                                             "intro25", "intro26", "intro27", "intro28", "intro29", "intro30", "intro31"]

    def move_out(self):
        self.intro.y += 3
        self.intro.render()
        self.after(30, self.move_out)
        self.intro_Done = True

    def create_intro(self, item):
        if item > 30:
            return
        image_name = "images/"+self.intro_list[item]+".png"
        self.intro = Intro(self, image_name, CANVAS_WIDTH //
                           2, CANVAS_HEIGHT // 2)
        self.after(SPEED, lambda: self.create_intro(item+1))

    def running_intro(self):
        self.intro_image()
        self.create_intro(0)

    def create_you_lost(self):
        self.lose = Intro(self, 'images/you-lose.png', CANVAS_WIDTH //
                          2, CANVAS_HEIGHT // 2)

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
        if len(self.elements) > 1 and len(self.elements[1:]) != 4 and self.elements[-1].x <= CANVAS_WIDTH-0.275*CANVAS_WIDTH+0.05*CANVAS_WIDTH:
            self.create_pillar()

    def init_game(self):

        self.create_sprites()
        for element in self.elements[1:]:
            element.random_height()
        self.is_started = False
        self.is_gameover = False
        if not self.intro_Done:
            self.running_intro()
        self.update_pipe()

    def update_pipe(self):
        global SPEED
        if self.is_started:
            for element in self.elements[1:]:
                element.update()
                element.render()
            self.post_update()
        if not self.is_gameover:
            self.after(SPEED, self.update_pipe)

    def update_bird(self):
        if self.is_started or self.is_gameover:
            self.dot.update()
            self.dot.render()
        self.after(10, self.update_bird)

    def start(self):
        self.update_pipe()
        self.update_bird()

    def animate(self):
        # animate method has been deprecated. Dut to the animation shaking issue
        # Using update_bird() and update_pipe to update element instead
        pass

    def post_update(self):
        # Check if the dot is falling out from the screen
        if self.dot.is_out_of_screen() and DEATH_MECHANISM:
            # Change game state to gameover
            self.is_started = False
            self.is_gameover = True
            self.create_you_lost()
            # Stop every eliments
            for element in self.elements[1:]:
                element.stop()
        self.check_pillar_onscreen()
        for element in self.elements[1:]:
            if element.is_hit(self.dot) and DEATH_MECHANISM:
                self.is_gameover = True
                self.is_started = False
                self.create_you_lost()
            if element.is_out_of_screen():
                element.reset_position()
                element.random_height()

    def on_key_pressed(self, event):
        if event.keysym == "space":
            if not self.intro_Done:
                self.move_out()
            if not self.is_started and not self.is_gameover and self.intro_Done:
                self.is_started = True
                self.create_pillar()
                self.dot.start()
                return
            if self.is_gameover:
                return
            if self.intro_Done:
                self.dot.jump()

        if event.keysym == "r" and self.is_gameover:
            self.canvas.delete(self.lose.canvas_object_id)
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
