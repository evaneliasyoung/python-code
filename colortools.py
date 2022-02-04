#!/usr/bin/env python3
"""
@file      colortools.py
@brief     Tools for colors.

@author    Evan Elias Young
@date      2016-11-28
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import re


class Color:
    """Represents a color object which contains multiple conversions.

    Returns:
        Color -- A color object.
    """

    def __init__(self, color: str) -> None:
        self._raw: str = color
        self.hex_type = (
            "full"
            if re.match("#?[0-9A-f]{6}", self._raw)
            else "short"
            if re.match("^#?[0-9A-f]{3}$", self._raw)
            else "none"
        )
        self.is_rgb: bool = bool(re.match("(rgb)?\\(?(\\d+, ?){2}\\d+\\)?", self._raw))
        self.hex: str = self.get_hex()
        self.rgb: tuple[float, float, float] = self.get_rgb()
        self.hsl: tuple[float, float, float] = self.get_hsl()
        self.hsv: tuple[float, float, float] = self.get_hsv()

    def get_hex(self) -> str:
        """Will calculate the hex form.

        Returns:
            string: The long form hex color.

        """
        long_hex: str = ""
        if self.hex_type == "full":
            long_hex = self._raw.lstrip("#")
        elif self.hex_type == "short":
            long_hex = "".join([c * 2 for c in self._raw.lstrip("#")])
        else:
            prgb = re.split(
                "(?:rgb)?(?:\\()?(\\d+), ?(\\d+), ?(\\d+)(?:\\))?", self._raw
            )[1:4]
            long_hex = "".join([f"{int(d):02X}" for d in prgb])
        return long_hex

    def get_rgb(self) -> tuple[int, int, int]:
        """Will calculate the rgb form.

        Returns:
            list: The red, green, and blue values.

        """
        return (
            int(self.hex[0:2], 16),
            int(self.hex[2:4], 16),
            int(self.hex[4:6], 16),
        )

    def get_hsl(self) -> tuple[float, float, float]:
        """Will calculate the hsl form.

        Returns:
            list: The hue, saturation, and lightness values.

        """
        tmp: list[float] = [p / 255 for p in self.rgb]
        min_rgb: float = min(tmp)
        max_rgb: float = max(tmp)
        delta: float = max_rgb - min_rgb

        light: float = (max_rgb + min_rgb) / 2
        hue: float = 0
        sat: float = 0
        if max_rgb != min_rgb:
            sat = (
                delta / (2 - max_rgb - min_rgb)
                if light > 0.5
                else delta / (max_rgb + min_rgb)
            )

            if max_rgb == tmp[0]:
                hue = (tmp[1] - tmp[2]) / delta + (6 if tmp[1] < tmp[2] else 0)
            elif max_rgb == tmp[1]:
                hue = (tmp[2] - tmp[0]) / delta + 2
            elif max_rgb == tmp[2]:
                hue = (tmp[0] - tmp[1]) / delta + 4

            hue /= 6

        return (hue, sat, light)

    def get_hsv(self) -> tuple[float, float, float]:
        """Will calculate the hsv form.

        Returns:
            list: The hue, saturation, and value values.

        """
        tmp: list[float] = [p / 255 for p in self.rgb]
        min_rgb: float = min(tmp)
        max_rgb: float = max(tmp)
        delta: float = max_rgb - min_rgb

        val: float = max_rgb
        sat: float = 0 if max_rgb == 0 else delta // max_rgb
        hue: float = 0
        if max_rgb != min_rgb:
            if max_rgb == tmp[0]:
                hue = (tmp[1] - tmp[2]) / delta + (6 if tmp[1] < tmp[2] else 0)
            elif max_rgb == tmp[1]:
                hue = (tmp[2] - tmp[0]) / delta + 2
            elif max_rgb == tmp[2]:
                hue = (tmp[0] - tmp[1]) / delta + 4
        hue /= 6
        return (hue, sat, val)


if __name__ == "__main__":
    print("Hello Console!")

    fav: Color = Color("#003366")
    print(f"hex : {fav.hex}")
    print(f"rgb : {fav.rgb}")
    print(f"hsl : {fav.hsl}")
    print(f"hsv : {fav.hsv}")
