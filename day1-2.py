import asyncio
import re
from itertools import takewhile
from pathlib import Path

from rich.style import Style
from rich.text import Text
from textual.app import App
from textual.containers import Container
from textual.coordinate import Coordinate
from textual.reactive import var
from textual.widgets import DataTable, Digits, Label
from textual_snowfall.widgets import Snowfall

DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGITS_RE = re.compile("|".join(DIGITS + ["[0-9]"]))
REVERSED_DIGITS_RE = re.compile("|".join([digit[::-1] for digit in DIGITS] + ["[0-9]"]))


def hunt_text(text, index):
    start_index = DIGITS_RE.search(text).start()
    end_index = REVERSED_DIGITS_RE.search(text[::-1]).start()

    ret = [Text(char, Style(color="white")) for char in text]

    if start_index <= index:
        ret[start_index] = Text(text[start_index], Style(color="red", bold=True))
    if start_index > index:
        ret[index] = Text(text[index], Style(color="red"))

    if end_index >= -index - 1:
        ret[end_index] = Text(text[end_index], Style(color="red", bold=True))
    if -index - 1 > end_index:
        ret[-index] = Text(text[-index], Style(color="red"))

    if start_index <= index and end_index >= -index - 1:
        digits = Text(text[start_index], Style(color="red", bold=True)) + Text(
            text[end_index], Style(color="red", bold=True)
        )
    else:
        digits = ""
    return Text("").join(ret), digits


class Day1(App):
    CSS = """
    #content {
            margin: 4;
            margin-left: 10;
            layout: grid;
            grid-columns: 4fr 1fr;
            grid-size: 2 1;
            }

Digits {
        padding-top: 4;
        margin-left: 2;
        height: 8;
        }
    """

    cursor_position = var(0)

    def on_load(self, _):
        self.input = Path("day1_input.txt").read_text().splitlines()

    def on_mount(self, _):
        self.set_timer(1, self.start_hunt)

    def rows_with_speed(self):
        x = 1.0 / float(len(self.input))
        for row_index in range(len(self.input)):
            yield row_index, 8 * pow(x, 4) if x < 0.5 else 1 - pow(-2 * x + 2, 4) / 2

    async def start_hunt(self):
        total = 0
        for row_index in range(len(self.input)):
            if row_index < 10:
                duration = 1.2
            elif 10 <= row_index <= 20:
                duration = 0.6
            elif 20 <= row_index <= 30:
                duration = 0.3
            elif 30 <= row_index <= 40:
                duration = 0.1
            elif 40 <= row_index <= 50:
                duration = 0.05
            elif row_index < len(self.input) - 10:
                duration = 0.001
            else:
                duration = 0.7

            to_add = await self.hunt_in_row(row_index, duration)
            if to_add:
                total += int(str(to_add))
                self.digits.update(str(total))

    async def hunt_in_row(self, row, duration):
        text = self.data_table.get_cell_at(Coordinate(row, 0))

        for i in range(len(text)):
            search, digits = hunt_text(text, i)
            self.data_table.update_cell_at(Coordinate(row, 0), search)
            self.data_table.update_cell_at(Coordinate(row, 1), digits)
            self.data_table.cursor_coordinate = Coordinate(row, 0)
            await asyncio.sleep(duration / len(text))

        return digits

    def compose(self):
        self.data_table = dt = DataTable(show_cursor=False)
        self.digits = Digits("0", id="sum")
        dt.add_column("Input")
        dt.add_column("Digits")
        for line in self.input:
            dt.add_row(line)

        with Snowfall():
            with Container(id="content"):
                yield dt
                yield self.digits


if __name__ == "__main__":
    Day1().run()
