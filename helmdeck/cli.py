import os
import sys
import click

from StreamDeck.DeviceManager import DeviceManager

import logging
from .logger import create_logger
logger = create_logger('')


def rename_proc( name ):
    """
    rename executabe from 'python <name>' to just '<name>'
    you can't show arguments because then `pidof <name>` would fail
    """
    from setproctitle import setproctitle
    setproctitle( name )


def _change_loglevel(logger, level):
    def get_handler(name):
        handlers = [
            h for h in logger.handlers
            if h.get_name() == name
        ]
        if handlers:
            return handlers[0]

    logger.setLevel(level)
    handler = get_handler('stderr')
    if handler:
        handler.setLevel(level)

# this is a click related function, not logging per se, hence it lives here
def change_loglevel(ctx, param, value):
    # 'stdout' is the name of a handler defined in .logger

    if param.name == 'debug' and value:
        _change_loglevel(logger, logging.DEBUG)
        _change_loglevel(logging.getLogger('streamdeckui'), logging.DEBUG)
    elif param.name == 'quiet' and value:
        _change_loglevel(logger, logging.WARNING)


# this is a click related function, not logging per se, hence it lives here
def enable_color(ctx, param, value):
    if value is False:
        for h in logger.handlers:
            h._enabled = False


def show_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    from . import __version__
    click.echo(__version__)
    ctx.exit()

def show_deck_info(deck):
    deck_id = deck.id()
    if len(deck_id) > 60:
        deck_id = f"{deck_id[:30]}...{deck_id[-30:]}"

    logger.debug(f"Deck: {deck.index} - {deck.deck_type()}")
    logger.debug(f"    ID: {deck_id}")
    logger.debug(f"    Serial: {deck.get_serial_number()}")
    logger.debug(f"    Firmware: {deck.get_firmware_version()}")

    row, col = deck.key_layout()
    logger.debug(f"    Key Count: {deck.key_count()} (in a {row}x{col} grid)")

    format = deck.key_image_format()

    x, y = format['size']
    logger.debug(f"    Key Images: {x}x{y} pixels")
    logger.debug(f"    Rotation : {format['rotation']}")
    logger.debug(f"    Format   : {format['format']}")
    logger.debug(f"    Flip     : {format['flip']}")

def choose_deck(ctx, param, value):
    streamdecks = DeviceManager().enumerate()

    logger.debug(f"Found {len(streamdecks)} stream deck(s)")

    try:
        deck = streamdecks[value]
        deck.open()

        deck.index = value
        deck.info = lambda: show_deck_info(deck)
        return deck
    except IndexError:
        raise click.ClickException(f"deck {value} greater than number of decks found: {len(streamdecks)}")


CTX_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CTX_SETTINGS)
@click.option('--version',
        is_flag=True, callback=show_version, expose_value=False, is_eager=True,
        help="show version and exit")
@click.option('-d', '--debug',
        is_flag=True, callback=change_loglevel, expose_value=True, is_eager=True,
        help="show extra info")
@click.option('-q', '--quiet',
        is_flag=True, callback=change_loglevel, expose_value=True, is_eager=True,
        help="show less info")
@click.option('--info',
        is_flag=True, default=False,
        help="show deck info and quit")
@click.option('--clear/--no-clear',
        type=bool, default=True,
        help="turn off streamdeck on exit")
@click.argument('deck',
        type=int, callback=choose_deck, default=0, expose_value=True, is_eager=True, )
@click.pass_context
def cli(ctx, deck, **opts):
    """
    helmdeck controls a stream deck
    """

    rename_proc('helmdeck')

    if opts['info']:
        _change_loglevel(logger, logging.DEBUG)
        deck.info()
        ctx.exit()
    else:
        deck.info() # maybe debug is on

    _change_loglevel(logging.getLogger('PIL'), logging.WARNING)

    import asyncio
    from .helmdeck import main
    from streamdeckui import Deck

    # KN: I don't like creating the Deck object here as opposed to
    # in main() but on a ctrl-c the exception is here, not in main()
    # so there is no way to call deck.release()

    try:
        loop = asyncio.get_event_loop()
        deck = Deck(deck, clear=opts['clear'], loop=loop) # convert to deck ui
        loop.run_until_complete(main(deck, opts, loop))
    except KeyboardInterrupt:
        logger.warning("ctrl-c quitting")
    finally:
        deck.release()

if __name__ == "__main__":
    cli()
