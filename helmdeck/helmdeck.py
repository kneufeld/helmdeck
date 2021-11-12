import asyncio

from streamdeckui import Deck, Page
from streamdeckui import Key
from streamdeckui.page import GreatWavePage, NumberedPage, ErrorPage

async def main(loop, deck, opts):

    deck = Deck(deck, clear=opts['clear'], loop=loop) # convert to deck ui
    deck.add_page('greatwave', GreatWavePage(deck, None))
    deck.add_page('numbers', NumberedPage(deck, None))
    deck.add_page('errorpage', ErrorPage(deck, None))
    # deck.change_page('greatwave')
    deck.change_page('numbers')

    deck.turn_on()

    await deck.wait()
