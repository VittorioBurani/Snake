from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint, random
from kivy.uix.label import Label


class Points(Label):
    def __init__(self, **kwargs):
        super(Points,self).__init__(**kwargs)
        self.color = (random(), random(), random(), 1)
        self.markup = True
        self.x = (Window.width - self.width)//2
        self.y = (Window.height - self.height)//2


class SnakePart(Widget):
    pass


class GameScreen(Widget):
    step_size = 40
    movement_x = 0
    movement_y = 0
    snake_parts = []
    snakes = 0

    def new_game(self):
        #Cleaner:
        to_be_removed = []
        for child in self.children:
            if isinstance(child, SnakePart):
                to_be_removed.append(child)
        for child in to_be_removed:
            self.remove_widget(child)
        #Initializer:
        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart()
        head.pos = (0, 0)
        self.snake_parts.append(head)
        self.add_widget(head)
        

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            #Moving left or right:
            self.movement_y = 0
            if dx > 0:
                self.movement_x = self.step_size
            else:
                self.movement_x = - self.step_size
        else:
            #Moving up or down:
            self.movement_x = 0
            if dy > 0:
                self.movement_y = self.step_size
            else:
                self.movement_y = - self.step_size
        #Removing the points-label!!
        for child in self.children:
            if isinstance(child, Points):
                self.remove_widget(child)

    def collides_widget(self, wid1, wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True

    def next_frame(self, *args):
        #Move the snake:
        head = self.snake_parts[0]
        food = self.ids.food
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y

        #Move the body:
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            part.new_y = self.snake_parts[i-1].y
            part.new_x = self.snake_parts[i-1].x
        for part in self.snake_parts[1:]:
            part.y = part.new_y
            part.x = part.new_x

        #Move the head:
        head.x += self.movement_x
        head.y += self.movement_y

        #Check for the snake colliding with food:
        if self.collides_widget(head, food):
            food.x = randint(0, Window.width - food.width)
            food.y = randint(0, Window.height - food.height)
            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)

        #Check for the snake colliding with snake:
        for part in self.snake_parts[1:]:
            if self.collides_widget(part, head):
                GameScreen.snakes = len(self.snake_parts)
                self.add_widget(Points(
                    text=f'[b][size=50][font=fonts/Azonix]You Lost!\nNumber of Blocks: {GameScreen.snakes}[/font][/size][/b]'))
                self.new_game()

        #Check for the snake colliding with wall:
        if not self.collides_widget(self, head):
            GameScreen.snakes = len(self.snake_parts)
            self.add_widget(Points(
                text=f'[b][size=50][font=fonts/Azonix]You Lost!\nNumber of Blocks: {GameScreen.snakes}[/font][/size][/b]'))
            self.new_game()



class PySnakeApp(App):
    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame, .2)


if __name__ == '__main__':
    PySnakeApp().run()
