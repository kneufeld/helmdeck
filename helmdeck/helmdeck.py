import asyncio

from streamdeckui import Deck

from .pages import GreatWavePage, NumberedPage, ErrorPage

import logging
logger = logging.getLogger(__name__)

async def main(deck, opts, loop):

    deck.add_page('greatwave', GreatWavePage(deck, None))
    deck.add_page('numbers', NumberedPage(deck, None))
    deck.add_page('errorpage', ErrorPage(deck, None))
    deck.change_page('greatwave')
    # deck.change_page('numbers')

    deck.turn_on()

    await deck.block_until_quit()
