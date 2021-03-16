from gamelib import Sprite, GameApp, Text
import tkinter as tk
import random
if __name__ != "__main__":
    from helper_modules.PIL import Image, ImageTk

CANVAS_WIDTH = None
CANVAS_HEIGHT = None

GRAVITY = 0.7
JUMP_VELOCITY = -10
STARTING_VELOCITY = -10

# Game Speed
DO_INCREASE_SPEED_RELATED_TO_SCORE = True
INIT_PIPE_REFRESH_RATE = 20
INIT_PIPE_SPEED = 3
PIPE_SPEED_STEP = 1
MAX_PIPE_SPEED = 100
PIPE_REFRESH_RATE_STEP = 1
DIFICULTY_STEP = 5

# Deprecated
UPDATE_DELAY = 33

# > Development Feature <
DEV_ENV = False
DEATH_MECHANISM = True
SCORE_PER_PIPE = 1


class PillarPair(Sprite):
    def init_element(self):
        self.is_started = True
        self.scored = False

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    def update(self, pipe_speed):
        if self.is_started:
            self.x -= pipe_speed

    def state_scored(self):
        if self.x <= (CANVAS_WIDTH//2 - 80):
            self.scored = False

        elif self.dot_passed():
            self.scored = True

    def is_out_of_screen(self):
        return self.x < -(0.05*CANVAS_WIDTH)

    def reset_position(self):
        self.x = CANVAS_WIDTH + 0.05*(CANVAS_WIDTH)

    def random_height(self):
        self.y = random.randint(0.25*CANVAS_HEIGHT,
                                CANVAS_HEIGHT-0.25*CANVAS_HEIGHT)

    def dot_passed(self):
        return CANVAS_WIDTH//2-20 < self.x < CANVAS_WIDTH//2+20 and self.is_started and not self.scored

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
        return self.y > CANVAS_HEIGHT-10 or self.y < 0


class Background(Sprite):
    def init_canvas_object(self):
        self.x += CANVAS_WIDTH/2
        self.image = Image.open(self.image_filename)
        self.image = self.image.resize(
            (CANVAS_WIDTH*2, CANVAS_HEIGHT), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas_object_id = self.canvas.create_image(
            self.x,
            self.y,
            image=self.tk_image)

    def init_element(self):
        self.is_started = False

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    def reset_position(self):
        self.x = CANVAS_WIDTH

    def update(self):
        if self.is_started:
            self.x -= 3

    def is_out_of_screen(self):
        return self.x < 0


class TextImage(Sprite):
    pass


class FlappyGame(GameApp):
    def add_score(self):
        self.score += SCORE_PER_PIPE
        if DO_INCREASE_SPEED_RELATED_TO_SCORE:
            self.calculate_speed()

    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png',
                       CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)

    def create_pillar(self):
        self.pillar_pair = PillarPair(
            self, 'images/pillar-pair.png', CANVAS_WIDTH+0.05*CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.pillar_pair.random_height()
        self.elements.append(self.pillar_pair)

    def create_background(self):
        self.background = Background(
            self, 'images/background.png', CANVAS_WIDTH/2, CANVAS_HEIGHT / 2)

    def check_pillar_onscreen(self):
        if len(self.elements) > 1 and len(self.elements[1:]) != 4 and self.elements[-1].x <= CANVAS_WIDTH-0.275*CANVAS_WIDTH+0.05*CANVAS_WIDTH:
            self.create_pillar()

    def displayed_score(self):
        self.score_image_list = []
        for i in range(len(str(self.score))):
            image_name = 'images/number/'+str(self.score)[i]+'.png'
            position = CANVAS_WIDTH/(3*(len(str(self.score)) + 1))
            self.score_image_list.append(
                TextImage(self, image_name, CANVAS_WIDTH/3 + position*(i+1), CANVAS_HEIGHT*0.1))

    def calculate_speed(self):
        if self.score % DIFICULTY_STEP == 0 and self.score != 0:
            if self.pipe_speed < MAX_PIPE_SPEED:
                self.pipe_speed += PIPE_SPEED_STEP
            if self.pipe_refresh_rate > 1:
                self.pipe_refresh_rate -= PIPE_REFRESH_RATE_STEP

    def init_game(self):
        # For updating the CANVAS_HEIGHT and CANVAS_WIDTH in the global scope.
        global CANVAS_HEIGHT, CANVAS_WIDTH
        CANVAS_WIDTH = self.canvas_width
        CANVAS_HEIGHT = self.canvas_height

        self.create_background()
        self.score = 0
        self.displayed_score()
        self.create_sprites()
        for element in self.elements[1:]:
            element.random_height()
        self.is_started = False
        self.is_gameover = False
        self.pipe_refresh_rate = INIT_PIPE_REFRESH_RATE
        self.pipe_speed = INIT_PIPE_SPEED
        self.update_pipe()

    def update_pipe(self):
        if self.is_started:
            for element in self.elements[1:]:
                element.update(self.pipe_speed)
                element.render()
            self.background.update()
            self.background.render()
            self.post_update()
        if not self.is_gameover:
            self.after(self.pipe_refresh_rate, self.update_pipe)

    def update_bird(self):
        if self.is_started or self.is_gameover:
            self.dot.update()
            self.dot.render()
        self.after(10, self.update_bird)

    def start(self):
        """For something that need to always be updated
        """
        self.update_bird()

    def animate(self):
        # animate method has been deprecated. Due to the animation shaking issue
        # Using update_bird() and update_pipe to update element instead
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
            self.background.stop()
        self.check_pillar_onscreen()
        if self.background.is_out_of_screen():
            self.background.reset_position()
        for element in self.elements[1:]:
            if element.is_hit(self.dot) and DEATH_MECHANISM:
                self.is_gameover = True
                self.is_started = False
            if element.dot_passed() and self.is_started:
                self.add_score()
                self.displayed_score()
            element.state_scored()
            if element.is_out_of_screen():
                element.reset_position()
                element.random_height()

    def on_key_pressed(self, event):
        if event.keysym == "space":
            if not self.is_started and not self.is_gameover:
                self.create_pillar()
                self.is_started = True
                self.background.start()
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

            return


if __name__ == "__main__":
    print("Please run this game from the launcher `run.py`")
