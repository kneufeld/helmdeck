import aiohttp

from streamdeckui import Key
from streamdeckui.mixins import QuitKeyMixin

import logging
logger = logging.getLogger(__name__)

class QuitKey(QuitKeyMixin, Key):
    def __init__(self, page, **kw):
        super().__init__(page, **kw)
        self.set_image(Key.UP, 'assets/exit.png')

class UrlKey(Key):

    def __init__(self, page, url, **kw):
        super().__init__(page, **kw)
        self._url = url
        self.set_image('fetch', 'assets/safari-icon.png')
        self.set_image('error', 'assets/error.png')

    async def cb_key_up(self, *args, **kw):
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

    async def cb_key_up(self, *args, **kw):
        self.state = Key.UP
        self.deck.prev_page()


class SwitchKey(Key):

    def __init__(self, page, to_page, **kw):
        super().__init__(page, **kw)
        self._to_page = to_page

    async def cb_key_up(self, *args, **kw):
        self.state = Key.UP
        self.deck.change_page(self._to_page)
