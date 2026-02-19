from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import random
import time

Window.clearcolor = (0, 0, 0, 1)

class Dot:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = random.choice([-5, 5])
        self.y_speed = random.choice([-5, 5])

    def move(self, width, height):
        self.x += self.x_speed
        self.y += self.y_speed
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.x_speed *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.y_speed *= -1

    def is_clicked(self, touch):
        return ((self.x - touch.x)**2 + (self.y - touch.y)**2) ** 0.5 <= self.radius + 10

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dots = []
        self.start_time = time.time()
        self.elapsed_time = 0
        self.click_count = 0
        self.finished = False
        self.square_pos = None
        self.square_draw_time = 0
        self.SQUARE_DISPLAY_DURATION = 0.5

        self.click_sound = SoundLoader.load("click.wav")
        self.split_sound = SoundLoader.load("split.wav")

        self.time_label = Label(text="", font_size=40, size_hint=(None, None),
                                pos=(Window.width - 220, Window.height - 80), color=(1,1,1,1))
        self.click_label = Label(text="", font_size=40, size_hint=(None, None),
                                 pos=(60, Window.height - 80), color=(1,1,1,1))
        self.result_label = Label(text="", font_size=80, size_hint=(None, None),
                                  pos=(0, 0), color=(1,0,0,1), halign="center")
        self.result_label.bind(size=self.result_label.setter('text_size'))

        self.add_widget(self.time_label)
        self.add_widget(self.click_label)
        self.add_widget(self.result_label)

        self.restart_btn = Button(text="Restart", size_hint=(None, None), size=(300, 100),
                                  font_size=30, opacity=0)
        self.restart_btn.bind(on_release=self.restart_game)
        self.add_widget(self.restart_btn)

        Window.bind(on_resize=self.on_window_resize)

        self.spawn_start_dots()
        Clock.schedule_interval(self.update, 1/60)

    def on_window_resize(self, *args):
        if self.finished:
            self.update_result_position()

        self.time_label.pos = (Window.width - 220, Window.height - 80)
        self.click_label.pos = (60, Window.height - 80)

    def spawn_start_dots(self):
        center_x = Window.width / 2
        center_y = Window.height / 2
        self.dots = [
            Dot(center_x - 30, center_y, 50),
            Dot(center_x + 30, center_y, 50)
        ]

    def update(self, dt):
        if not self.finished:
            self.elapsed_time = round(time.time() - self.start_time, 2)
            self.time_label.text = f"{self.elapsed_time:.2f}s"
            self.click_label.text = f"Kliknutí: {self.click_count}"

        self.canvas.before.clear()
        with self.canvas.before:
            for dot in self.dots:
                dot.move(Window.width, Window.height)
                Color(1, 0, 0)
                Ellipse(pos=(dot.x - dot.radius, dot.y - dot.radius),
                        size=(dot.radius * 2, dot.radius * 2))
            if self.square_pos and (time.time() - self.square_draw_time < self.SQUARE_DISPLAY_DURATION):
                Color(1, 1, 1)
                Line(rectangle=(self.square_pos[0] - 25, self.square_pos[1] - 25, 50, 50), width=2)

        if not self.dots and not self.finished:
            self.end_game()

    def on_touch_down(self, touch):
        if self.finished:
            if self.restart_btn.collide_point(*touch.pos):
                self.restart_game(None)
            return
        self.click_count += 1
        if self.click_sound:
            self.click_sound.play()
        self.square_pos = (touch.x, touch.y)
        self.square_draw_time = time.time()
        for dot in self.dots[:]:
            if dot.is_clicked(touch):
                if dot.radius > 30:
                    new_radius = dot.radius // 2
                    offset = 20
                    dx1, dy1 = random.randint(-offset, offset), random.randint(-offset, offset)
                    dx2, dy2 = random.randint(-offset, offset), random.randint(-offset, offset)
                    self.dots.append(Dot(dot.x + dx1, dot.y + dy1, new_radius))
                    self.dots.append(Dot(dot.x + dx2, dot.y + dy2, new_radius))
                    if self.split_sound:
                        self.split_sound.play()
                self.dots.remove(dot)
                break

    def end_game(self):
        self.finished = True
        self.result_label.text = f"{self.elapsed_time:.2f} s"
        self.result_label.texture_update()
        self.update_result_position()
        self.restart_btn.opacity = 1

    def update_result_position(self):
        self.result_label.pos = (Window.width / 2 - self.result_label.texture_size[0] / 2 + 100,
                                 Window.height / 2 + 80)
        self.restart_btn.pos = (Window.width / 2 - 120, Window.height / 2 - 50)

    def restart_game(self, instance):
        self.dots.clear()
        self.click_count = 0
        self.finished = False
        self.result_label.text = ""
        self.restart_btn.opacity = 0
        self.start_time = time.time()
        self.square_pos = None
        self.spawn_start_dots()

class RedDotsApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    RedDotsApp().run()