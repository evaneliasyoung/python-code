#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2020-03-06
Revision : 2020-03-06
"""


import requests
from bs4 import BeautifulSoup as bs4


def requestAlbum(album: str):
    return requests.get(f'https://music.apple.com/us/album/{album}', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})


def getTitle(soup: bs4) -> str:
    return soup.select(f'table.table > tbody > tr:nth-child({song}) > td:nth-child(2)')[0].text.strip()


def getArtist(soup: bs4) -> str:
    return soup.select('.product-header__identity.album-header__identity > a')[0].text.strip()


def getAlbum(soup: bs4) -> str:
    return soup.select('.product-header__title')[0].text.strip()


def getGenre(soup: bs4) -> str:
    return soup.select('.product-header__list > li > ul > li > a')[0].text.strip()


def getDate(soup: bs4) -> str:
    return soup.select('time')[0].attrs['datetime'][:10]


def getTracks(soup: bs4) -> int:
    return len(soup.select('table.table > tbody > tr'))


if __name__ == "__main__":
    album: str = input('Album ID:\n')
    song: int = int(input('Song Number:\n'))

    res = requestAlbum(album)
    soup: bs4 = bs4(res.content, 'html.parser')
    print('\t'.join([getTitle(soup), getArtist(soup), getAlbum(
        soup), getDate(soup), f'{song}/{getTracks(soup)}', getGenre(soup)]))
