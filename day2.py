import asyncio
import random
from pathlib import Path

from rich.style import Style
from textual.app import App
from textual.containers import Container
from textual.widgets import Digits, Label, Sparkline
from textual_snowfall.widgets import Snowfall

TIMEOUT = 0.5


class Day2(App):
    CSS_PATH = "day2.tcss"

    def on_load(self):
        self.input = Path("day2.input").read_text().splitlines()

    def on_mount(self):
        # self.set_interval(0.1, self.add_sparks)
        self.set_timer(2, self.process)

    async def process(self):
        valid_total = 0
        for game in self.input:
            game_no, _, counts = game.partition(":")
            *_, game_no = game_no.partition(" ")
            self.game_number.update(game_no)

            valid = True
            for showing in counts.split(";"):
                self.red_count.update("0")
                self.green_count.update("0")
                self.blue_count.update("0")
                for cubes in showing.split(","):
                    count, _, color = cubes.strip().partition(" ")
                    if color == "red":
                        self.red_count.update(count)
                        count = int(count)
                        self.red_sparks.data = self.red_sparks.data + [count]
                        if count > 12:
                            self.notify(
                                "Impossible game: Too many [b][i]Reds!",
                                severity="error",
                                timeout=TIMEOUT,
                            )
                            valid = False
                    elif color == "green":
                        self.green_count.update(count)
                        count = int(count)
                        self.green_sparks.data = self.green_sparks.data + [count]
                        if count > 13:
                            self.notify(
                                "Impossible game: Too many [b i]Greens!",
                                timeout=TIMEOUT,
                            )
                            valid = False
                    elif color == "blue":
                        self.blue_count.update(count)
                        count = int(count)
                        self.blue_sparks.data = self.blue_sparks.data + [count]
                        if count > 14:
                            self.notify(
                                "Impossible game: Too many [b i]Blues!",
                                severity="warning",
                                timeout=TIMEOUT,
                            )
                            valid = False

                await asyncio.sleep(0.1)
            if valid:
                valid_total += int(game_no)
                self.id_total.update(str(valid_total))

    def add_sparks(self):
        self.red_sparks.data = self.red_sparks.data[-self.size.width :] + [
            random.random() * 10
        ]
        self.blue_sparks.data = self.blue_sparks.data[-self.size.width :] + [
            random.random() * 10
        ]
        self.green_sparks.data = self.green_sparks.data[-self.size.width :] + [
            random.random() * 10
        ]

    def compose(self):
        self.game_number = Digits()
        self.id_total = Digits("0")

        self.red_count = Digits(id="red_count")
        self.blue_count = Digits(id="blue_count")
        self.green_count = Digits(id="green_count")

        self.red_sparks = Sparkline(id="red-spark", data=[0])
        self.green_sparks = Sparkline(id="green-spark", data=[0])
        self.blue_sparks = Sparkline(id="blue-spark", data=[0])

        with Snowfall():
            with Container(id="content"):
                with Container(classes="game_count") as c:
                    c.border_title = "Analysing Game Number:"
                    yield self.game_number
                with Container(id="show_counts") as c:
                    c.border_title = "Shown cubes:"
                    yield self.red_count
                    yield self.blue_count
                    yield self.green_count
                with Container(classes="game_count") as c:
                    c.border_title = "Game ID Total"
                    yield self.id_total
                with Container(id="sparks"):
                    yield self.red_sparks
                    yield self.blue_sparks
                    yield self.green_sparks


if __name__ == "__main__":
    Day2().run()
