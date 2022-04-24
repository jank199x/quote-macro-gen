#! /usr/bin/env python3

import json
from PIL import Image, ImageDraw, ImageFont
import textwrap

import click
from pydantic import BaseModel


TEXT_SIZE = 300
BG_COLOR = "black"
TEXT_COLOR = "white"
LINE_LENGTH = 37
LINE_SPACING = 95
QUOTE_FONT = "IndieFlower.ttf"
SOURCE_FONT = "Oswald.ttf"


class Params(BaseModel):
    quote: str
    source: str


@click.command()
@click.argument("configfile", type=click.Path(exists=True, dir_okay=False))
@click.argument("output", type=click.Path(exists=False, dir_okay=False))
def launch(configfile, output):
    """
    \b
    Creates image with a quote
    """
    with open(configfile) as f:
        quote = f.readline().strip()
        source = f.readline().strip()

    params = Params(
        quote=quote,
        source=source,
    )

    quote_font = ImageFont.truetype(
        font=QUOTE_FONT,
        size=TEXT_SIZE,
    )

    text = textwrap.wrap(
        text=params.quote,
        width=LINE_LENGTH,
    )

    width = int(TEXT_SIZE * LINE_LENGTH / 2)
    height = int(TEXT_SIZE * len(text) * 1.5 * 1.1)

    image = Image.new(
        mode="RGB",
        size=(width, height),
        color=BG_COLOR,
    )
    draw = ImageDraw.Draw(image)
    text = "\n".join(text)
    draw.multiline_text(
        xy=(width / 2, height / 2 * 0.9),
        text=text,
        font=quote_font,
        fill=TEXT_COLOR,
        anchor="mm",
        align="left",
        spacing=LINE_SPACING,
    )

    author_font = ImageFont.truetype(
        font=SOURCE_FONT,
        size=int(TEXT_SIZE * 0.7),
    )

    draw.multiline_text(
        xy=(width * 0.95, height * 0.95),
        text=params.source,
        font=author_font,
        fill=TEXT_COLOR,
        anchor="rd",
        align="right",
        spacing=LINE_SPACING,
    )

    image.save(output)


if __name__ == "__main__":
    launch()
