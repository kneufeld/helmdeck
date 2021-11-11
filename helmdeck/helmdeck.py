import asyncio

from streamdeckui import Deck, Page
from streamdeckui import Key, KeyState

async def main(loop, deck):

    deck.background('greatwave.jpg')
    for key in deck:
        key.set_image(KeyState.DOWN, 'examples/Assets/Pressed.png')

    deck.turn_on()

    await deck.wait()
