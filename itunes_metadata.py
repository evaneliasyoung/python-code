#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2020-03-06
Revision : 2020-03-08
"""

import requests
from bs4 import BeautifulSoup as bs4


def request_album(album_id: str) -> requests.Response:
    """Sends a request to read an album.

    Arguments:
        album_id {str} -- The album ID.

    Returns:
        requests.Response -- The response.
    """
    return requests.get(
        f'https://music.apple.com/us/album/{album_id}',
        headers={
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'
        })


def get_title(soup: bs4) -> str:
    """Gets a song's title.

    Arguments:
        soup {bs4} -- The BeautifulSoup4 soup.

    Returns:
        str -- The song title.
    """
    return soup.select(
        f'table.table > tbody > tr:nth-child({song}) > td:nth-child(2)'
    )[0].text.strip()


def get_artist(soup: bs4) -> str:
    """Gets a song's artist.

    Arguments:
        soup {bs4} -- The BeautifulSoup4 soup.

    Returns:
        str -- The song artist.
    """
    return soup.select('.product-header__identity.album-header__identity > a'
                       )[0].text.strip()


def get_album(soup: bs4) -> str:
    """Gets a song's album.

    Arguments:
        soup {bs4} -- The BeautifulSoup4 soup.

    Returns:
        str -- The song album.
    """
    return soup.select('.product-header__title')[0].text.strip()


def get_genre(soup: bs4) -> str:
    """Gets a song's genre.

    Arguments:
        soup {bs4} -- The BeautifulSoup4 soup.

    Returns:
        str -- The song genre.
    """
    return soup.select(
        '.product-header__list > li > ul > li > a')[0].text.strip()


def get_date(soup: bs4) -> str:
    """Gets a song's date.

    Arguments:
        soup {bs4} -- The BeautifulSoup4 soup.

    Returns:
        str -- The song date.
    """
    return soup.select('time')[0].attrs['datetime'][:10]


def get_tracks(soup: bs4) -> int:
    """Gets a song's tracks.

    Arguments:
        soup {bs4} -- The BeautifulSoup4 soup.

    Returns:
        str -- The song tracks.
    """
    return len(soup.select('table.table > tbody > tr'))


if __name__ == "__main__":
    album: str = input('Album ID:\n')
    song: int = int(input('Song Number:\n'))

    res: requests.Response = request_album(album)
    resp_soup: bs4 = bs4(res.content, 'html.parser')
    print('\t'.join([
        get_title(resp_soup),
        get_artist(resp_soup),
        get_album(resp_soup),
        get_date(resp_soup), f'{song}/{get_tracks(resp_soup)}',
        get_genre(resp_soup)
    ]))
