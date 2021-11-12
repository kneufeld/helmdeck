import aiohttp

from streamdeckui import Key

import logging
logger = logging.getLogger(__name__)

class NumberKey(Key):
    """
    dev page, show key index as text
    any key exits
    """

    def __init__(self, page, **kw):
        super().__init__(page, **kw)

        # can't call self.index until after it's been added to page
        self.deck._loop.call_soon(self._add_label)

    def _add_label(self):
        index = self.index

        if index < 0:
            return

        self.add_label(Key.UP, str(index), False)


class QuitKey(Key):
    def __init__(self, page, **kw):
        super().__init__(page, **kw)
        self.set_image(Key.UP, 'assets/exit.png')

    async def key_up(self, *args, **kw):
        logger.info("you pushed the exit key")
        self.deck._quit_future.set_result(None)


class UrlKey(Key):

    def __init__(self, page, url, **kw):
        super().__init__(page, **kw)
        self._url = url
        self.set_image('fetch', 'assets/safari-icon.png')
        self.set_image('error', 'assets/error.png')

    async def key_up(self, *args, **kw):
        resp = await self.fetch(self._url)
        logger.info(f"GET: {self._url}: {resp.status}")

        if 200 >= resp.status <= 299:
            self.state = Key.UP
        else:
            self.state = 'error'

    async def fetch(self, url):
        logger.debug("GETing: %s", self._url)
        self.state = 'fetch'

        # https://docs.aiohttp.org/en/stable/client_reference.html
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as client:
            try:
                return await client.get(url)
            except Exception as e:
                logger.error(e)
                return aiohttp.web.Response(status=499)


class BackKey(Key):

    def __init__(self, page, **kw):
        super().__init__(page, **kw)
        self.set_image(Key.UP, 'assets/back.png')

    async def key_up(self, *args, **kw):
        self.state = Key.UP
        self.deck.prev_page()


class SwitchKey(Key):

    def __init__(self, page, to_page, **kw):
        super().__init__(page, **kw)
        self._to_page = to_page

    async def key_up(self, *args, **kw):
        self.state = Key.UP
        self.deck.change_page(self._to_page)
