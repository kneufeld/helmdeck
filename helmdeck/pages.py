from streamdeckui import Page, Key
from streamdeckui.utils import solid_image

from .keys import QuitKey, SwitchKey, BackKey, UrlKey

class GreatWavePage(Page):
    def __init__(self, deck, keys):
        super().__init__(deck, keys)

        self._keys[0] = SwitchKey(self, 'numbers')
        self._keys[10] = BackKey(self)
        self._keys[14] = QuitKey(self)

        self.background('assets/greatwave.jpg')


class NumberedPage(Page):
    """
    a dev page that shows the index number of each key
    """
    def __init__(self, deck, keys):
        super().__init__(deck, [])

        self._keys = [
            Key(self, label=str(i))
            for i in range(self.device.key_count())
        ]

        self._keys[0] = SwitchKey(
            self, 'greatwave',
            up_image='assets/greatwave.jpg', label='0'
        )
        self._keys[1] = SwitchKey(self, 'errorpage', label='error\npage')
        self._keys[10] = BackKey(self, label='10')

        # 'https://www2.burgundywall.com/beast/'
        self._keys[-2] = UrlKey(
            self, "http://localhost:8080/",
            label='REST',
        )
        self._keys[-1] = QuitKey(self, label='14')


class ErrorPage(Page):
    """
    assuming a 3x5 grid deck and we're passed all keys
    """

    def __init__(self, deck, keys):
        super().__init__(deck, keys)

        x = [1, 3, 7, 11, 13]
        red_image = solid_image(self.deck, 'red')

        for i in x:
            key = self._keys[i]
            key.set_image(Key.UP, red_image)

        self._keys[0] = SwitchKey(self, 'greatwave')
        self._keys[10] = BackKey(self)
        self._keys[14] = QuitKey(self)
