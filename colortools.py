#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2016-11-28
Revision : 2019-12-12
"""


import re
from typing import List, Tuple


class Color:
    def __init__(self, color: str) -> None:
        """Will create a color object which contains multiple conversions.

        Args:
            color (string): The color, available in many formats.

        Returns:
            color: A color object.

        """
        self._raw: str = color
        self.isFullHex: bool = bool(re.match('#?[0-9A-f]{6}', self._raw))
        self.isShortHex: bool = bool(re.match('^#?[0-9A-f]{3}$', self._raw))
        self.isRGB: bool = bool(
            re.match('(rgb)?\(?(\d+, ?){2}\d+\)?', self._raw))
        self.isRGBA: bool = bool(
            re.match('(rgba)?\(?(\d+, ?){3}\d+\)?', self._raw))
        self.hex: str = self.getHex()
        self.rgb: Tuple[float, float, float] = self.getRGB()
        self.hsl: Tuple[float, float, float] = self.getHSL()
        self.hsv: Tuple[float, float, float] = self.getHSV()

    def getHex(self) -> str:
        """Will calculate the hex form.

        Returns:
            string: The long form hex color.

        """
        if (self.isFullHex):
            return self._raw.lstrip('#')
        elif (self.isShortHex):
            return ''.join([c * 2 for c in self._raw.lstrip('#')])
        else:
            prgb = re.split(
                '(?:rgb)?(?:\()?(\d+), ?(\d+), ?(\d+)(?:\))?', self._raw)[1:4]
            return ''.join([f'{int(d):02X}' for d in prgb])

    def getRGB(self) -> Tuple[int, int, int]:
        """Will calculate the rgb form.

        Returns:
            list: The red, green, and blue values.

        """
        return (int(self.hex[0:2], 16), int(self.hex[2:4], 16), int(self.hex[4:6], 16), )

    def getHSL(self) -> Tuple[float, float, float]:
        """Will calculate the hsl form.

        Returns:
            list: The hue, saturation, and lightness values.

        """
        tmp: List[float] = [p / 255 for p in self.rgb]
        mn: float = min(tmp)
        mx: float = max(tmp)

        l: float = (mx + mn) / 2
        h: float = 0
        s: float = 0
        d: float = 0
        if (mx != mn):
            d = mx - mn
            s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)

            if (mx == tmp[0]):
                h = (tmp[1] - tmp[2]) / d + (6 if tmp[1] < tmp[2] else 0)
            elif (mx == tmp[1]):
                h = (tmp[2] - tmp[0]) / d + 2
            elif (mx == tmp[2]):
                h = (tmp[0] - tmp[1]) / d + 4

            h /= 6

        return (h, s, l)

    def getHSV(self) -> Tuple[float, float, float]:
        """Will calculate the hsv form.

        Returns:
            list: The hue, saturation, and value values.

        """
        tmp: List[float] = [p / 255 for p in self.rgb]
        mn: float = min(tmp)
        mx: float = max(tmp)

        v: float = mx
        d: float = mx - mn
        s: float = 0 if mx == 0 else d // mx
        h: float = 0
        if (mx != mn):
            if (mx == tmp[0]):
                h = (tmp[1] - tmp[2]) / d + (6 if tmp[1] < tmp[2] else 0)
            elif (mx == tmp[1]):
                h = (tmp[2] - tmp[0]) / d + 2
            elif (mx == tmp[2]):
                h = (tmp[0] - tmp[1]) / d + 4
        h /= 6
        return (h, s, v)


if __name__ == '__main__':
    print('Hello Console!')
    fav: Color = Color('#003366')
    print(f'hex : {fav.hex}')
    print(f'rgb : {fav.rgb}')
    print(f'hsl : {fav.hsl}')
    print(f'hsv : {fav.hsv}')
