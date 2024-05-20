from itertools import cycle
from tkinter import Tk, Canvas, messagebox
from random import randrange


class EggCatcherGame:
    def __init__(self):
        self.canvas_width = 800
        self.canvas_height = 400
        self.win = Tk()
        self.c = Canvas(
            self.win,
            width=self.canvas_width,
            height=self.canvas_height,
            background="deep sky blue",
        )
        self.c.pack()

        self.create_game_elements()

    def create_game_elements(self):
        # Create ground
        self.c.create_rectangle(
            -5,
            self.canvas_height - 100,
            self.canvas_width + 5,
            self.canvas_height + 5,
            fill="sea green",
            width=0,
        )

        # Create sun
        self.c.create_oval(-80, -80, 120, 120, fill="orange", width=0)

        # Initialize eggs
        self.color_cycle = cycle(
            [
                "light blue",
                "light pink",
                "light yellow",
                "light green",
                "red",
                "blue",
                "green",
                "black",
            ]
        )
        self.egg_width = 45
        self.egg_height = 55
        self.egg_score = 10
        self.egg_speed = 500
        self.egg_interval = 2000  # Adjust this value to increase the speed of the eggs
        self.difficulty_factor = 0.95
        self.eggs = []

        # Create catcher
        self.catcher_color = "blue"
        self.catcher_width = 100
        self.catcher_height = 100
        self.catcher_start_x = self.canvas_width / 2 - self.catcher_width / 2
        self.catcher_start_y = self.canvas_height - self.catcher_height - 20
        self.catcher_start_x2 = self.catcher_start_x + self.catcher_width
        self.catcher_start_y2 = self.catcher_start_y + self.catcher_height
        self.catcher = self.c.create_arc(
            self.catcher_start_x,
            self.catcher_start_y,
            self.catcher_start_x2,
            self.catcher_start_y2,
            start=200,
            extent=140,
            style="arc",
            outline=self.catcher_color,
            width=3,
        )

        # Initialize score and lives
        self.score = 0
        self.score_text = self.c.create_text(
            10,
            10,
            anchor="nw",
            font=("Arial", 18, "bold"),
            fill="darkblue",
            text="Score : " + str(self.score),
        )
        self.live_remaining = 3
        self.live_text = self.c.create_text(
            self.canvas_width - 10,
            10,
            anchor="ne",
            font=("Arial", 18, "bold"),
            fill="darkblue",
            text="Lives : " + str(self.live_remaining),
        )

    def create_eggs(self):
        x = randrange(10, 740)
        y = 40
        new_egg = self.c.create_oval(
            x,
            y,
            x + self.egg_width,
            y + self.egg_height,
            fill=next(self.color_cycle),
            width=0,
        )
        self.eggs.append(new_egg)
        self.win.after(self.egg_interval, self.create_eggs)

    def move_eggs(self):
        for egg in self.eggs:
            self.c.move(egg, 0, 10)  # Move each egg downwards by 10 pixels
        self.win.after(
            100, self.move_eggs
        )  # Call this function again after 100 milliseconds

    def egg_dropped(self, egg):
        self.eggs.remove(egg)
        self.c.delete(egg)
        self.lose_a_life()
        if self.live_remaining == 0:
            messagebox.showinfo("GAME OVER!", "Final Score: " + str(self.score))
            self.win.destroy()

    def lose_a_life(self):
        self.live_remaining -= 1
        self.c.itemconfigure(self.live_text, text="Lives: " + str(self.live_remaining))

    def catch_check(self):
        (catcher_x, catcher_y, catcher_x2, catcher_y2) = self.c.coords(self.catcher)
        for egg in self.eggs:
            (egg_x, egg_y, egg_x2, egg_y2) = self.c.coords(egg)
            if (
                catcher_x < egg_x
                and egg_x2 < self.catcher_start_x2
                and catcher_x2 - egg_y2 < 40
            ):
                if (
                    catcher_x < egg_x
                    and egg_x2 < self.catcher_start_x2
                    and catcher_y2 - egg_y2 < 40
                ):
                    self.eggs.remove(egg)
                    self.c.delete(egg)
                    self.increase_score(self.egg_score)
        self.win.after(100, self.catch_check)

    def increase_score(self, points):
        self.score += points
        self.egg_speed = int(self.egg_speed * self.difficulty_factor)
        self.egg_interval = int(self.egg_interval * self.difficulty_factor)
        self.c.itemconfigure(self.score_text, text="Score : " + str(self.score))

    def move_left(self, event):
        (x1, y1, x2, y2) = self.c.coords(self.catcher)
        if x1 > 0:
            self.c.move(self.catcher, -20, 0)

    def move_right(self, event):
        (x1, y1, x2, y2) = self.c.coords(self.catcher)
        if x2 < self.canvas_width:
            self.c.move(self.catcher, 20, 0)

    def run(self):
        self.c.bind("<Left>", self.move_left)
        self.c.bind("<Right>", self.move_right)
        self.c.focus_set()
        self.win.after(1000, self.create_eggs)
        self.win.after(100, self.catch_check)
        self.win.after(100, self.move_eggs)  # Start moving the eggs downwards
        self.win.mainloop()


if __name__ == "__main__":
    game = EggCatcherGame()
    game.run()
