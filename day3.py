import asyncio
from pathlib import Path

from rich.style import Style
from rich.text import Text
from textual.app import App
from textual.containers import Container, ScrollableContainer
from textual.widgets import Digits, Label, Placeholder
from textual_snowfall.widgets import Snowfall

MAIN_LINE_STYLE = Style(color="#EEEEEE", bgcolor="default")
MAIN_LINE_HIGHLIGHT = Style(bgcolor="yellow", color="black")
MAIN_LINE_FOUND = Style(bgcolor="default", color="red")
OTHER_LINE_STYLE = Style(color="#444444", bgcolor="default")
OTHER_LINE_HIGHLIGHT = Style(color="green", bgcolor="default")


class Day3(App):
    CSS_PATH = "day3.tcss"

    def on_load(self):
        self.input = Path("day3.input").read_text().splitlines()

    def on_mount(self):
        # self.set_interval(0.1, self.add_sparks)
        self.set_timer(3, self.process)

    async def process(self):
        self.input = (
            [" " * len(self.input[0])] + self.input + [" " * len(self.input[0])] * 2
        )
        for line_no, line in enumerate(self.input[:-3]):
            top_line = Text(self.input[line_no] + "\n", OTHER_LINE_STYLE)
            bottom_line = Text(self.input[line_no + 2] + "\n", OTHER_LINE_STYLE)
            mid_line = Text(self.input[line_no + 1] + "\n", MAIN_LINE_STYLE)
            found_control_chars = []
            found_mid_digits = []
            for index, char in enumerate(mid_line):
                if index - 1 not in found_control_chars:
                    mid_line.stylize(MAIN_LINE_STYLE, index - 1, index)
                if index not in found_mid_digits:
                    mid_line.stylize(MAIN_LINE_HIGHLIGHT, index, index + 1)
                self.ticker.update(top_line + mid_line + bottom_line)
                await asyncio.sleep(0.01)
                if not str(char).isdigit() and str(char) not in (" ", ".", "\n"):
                    mid_line.stylize(MAIN_LINE_FOUND, index, index + 1)
                    found_control_chars.append(index)

                    ## Top line
                    found_digit = []
                    for col in (-1, 0, 1):
                        top_line.stylize(
                            MAIN_LINE_HIGHLIGHT, index + col, index + col + 1
                        )
                        self.ticker.update(top_line + mid_line + bottom_line)
                        self.total.update(str(top_line[index + col]))
                        await asyncio.sleep(0.1)
                        if str(top_line[index + col]).isdigit():
                            found_digit.append(index + col)
                            top_line.stylize(
                                OTHER_LINE_HIGHLIGHT, index + col, index + col + 1
                            )
                        if index + col - 1 not in found_digit:
                            top_line.stylize(
                                OTHER_LINE_STYLE, index + col - 1, index + col
                            )
                    if str(top_line[index + 1]).isdigit():
                        top_line.stylize(OTHER_LINE_HIGHLIGHT, index + 1, index + 2)
                    else:
                        top_line.stylize(OTHER_LINE_STYLE, index + 1, index + 2)

                    ## Mid line
                    mid_line.stylize(MAIN_LINE_HIGHLIGHT, index + 1, index + 2)
                    self.ticker.update(top_line + mid_line + bottom_line)
                    await asyncio.sleep(0.1)
                    if str(mid_line[index + 1]).isdigit():
                        mid_line.stylize(OTHER_LINE_HIGHLIGHT, index + 1, index + 2)
                        found_mid_digits.append(index + 1)
                    else:
                        mid_line.stylize(MAIN_LINE_STYLE, index + 1, index + 2)

                    ## Bottom line
                    for col in (1, 0, -1):
                        bottom_line.stylize(
                            MAIN_LINE_HIGHLIGHT, index + col, index + col + 1
                        )
                        self.ticker.update(top_line + mid_line + bottom_line)
                        await asyncio.sleep(0.1)
                        bottom_line.stylize(
                            OTHER_LINE_STYLE, index + col, index + col + 1
                        )
                    bottom_line.stylize(OTHER_LINE_STYLE, index - 1, index)
                    mid_line.stylize(MAIN_LINE_HIGHLIGHT, index - 1, index)
                    self.ticker.update(top_line + mid_line + bottom_line)
                    await asyncio.sleep(0.1)
                    if index - 1 not in found_control_chars:
                        mid_line.stylize(MAIN_LINE_STYLE, index - 1, index)
                    self.ticker.update(top_line + mid_line + bottom_line)
                    await asyncio.sleep(0.1)

    def compose(self):
        self.ticker = Label()
        self.total = Digits()
        with Snowfall():
            with Container(id="contents"):
                yield self.ticker
                with Container(classes="total"):
                    yield self.total
                    yield Placeholder()


if __name__ == "__main__":
    Day3().run()
