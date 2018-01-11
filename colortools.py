#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 11/28/2016
Revision : 01/10/2018
"""

import re

class color:
   def __init__(self, color):
      self._raw = color
      self.isFullHex = bool(re.match('#?[0-9A-f]{6}', self._raw))
      self.isShortHex = bool(re.match('^#?[0-9A-f]{3}$', self._raw))
      self.isRGB = bool(re.match('(rgb)?\(?(\d+, ?){2}\d+\)?', self._raw))
      self.isRGBA = bool(re.match('(rgba)?\(?(\d+, ?){3}\d+\)?', self._raw))
      self.hex = self.getHex()
      self.rgb = self.getRGB()
      self.hsl = self.getHSL()
      self.hsv = self.getHSV()
   def getHex(self):
      if (self.isFullHex):
         return self._raw.lstrip('#')
      elif (self.isShortHex):
         return ''.join([c * 2 for c in self._raw.lstrip('#')])
      elif (self.isRGB):
         prgb = re.split('(?:rgb)?(?:\()?(\d+), ?(\d+), ?(\d+)(?:\))?', self._raw)[1:4]
         return ''.join([f'{int(d):02X}' for d in prgb])
   def getRGB(self):
      li = [int(self.hex[i:i+2], 16) for i in [0, 2, 4]]
      return li
   def getHSL(self):
      tmp = [p / 255 for p in self.rgb]
      mn = min(tmp)
      mx = max(tmp)

      l = (mx + mn) / 2
      if (mx == mn):
         h, s = [0] * 2
      else:
         d = mx - mn
         s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)

         if (mx == tmp[0]): h = (tmp[1] - tmp[2]) / d + (6 if tmp[1] < tmp[2] else 0)
         elif (mx == tmp[1]): h = (tmp[2] - tmp[0]) / d + 2
         elif (mx == tmp[2]): h = (tmp[0] - tmp[1]) / d + 4

         h /= 6

      return [h, s, l]
   def getHSV(self):
      tmp = [p / 255 for p in self.rgb]
      mn = min(tmp)
      mx = max(tmp)

      v = mx
      d = mx - mn
      s = 0 if mx == 0 else d / mx
      if (mx == mn):
         h = 0
      else:
         if (mx == tmp[0]): h = (tmp[1] - tmp[2]) / d + (6 if tmp[1] < tmp[2] else 0)
         elif (mx == tmp[1]): h = (tmp[2] - tmp[0]) / d + 2
         elif (mx == tmp[2]): h = (tmp[0] - tmp[1]) / d + 4
      h /= 6
      return [h, s, v]



if __name__ == '__main__':
   print('Hello Console!')
   fav = color('#003366')
   ks = [
      'hex',
      'rgb',
      'hsl',
      'hsv'
   ]
   ml = max([len(k) for k in ks])
   for k in ks:
      print(f'{k:<{ml}} : {fav.__getattribute__(k)}')
