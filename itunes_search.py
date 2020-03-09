#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2020-03-08
Revision : 2020-03-08
"""


import requests
import json
import argparse
from datetime import datetime as dt
from typing import List, Dict, Union, Any


# The max length for the type printer.
MAX_TYPE_LEN: int = 6
# The max length for the id printer.
MAX_ID_LEN: int = 11
# The max length for the album printer.
MAX_NAME_LEN: int = 27
# The max length for the artist printer.
MAX_ARTIST_LEN: int = 15
# The number of spaces inbetween standard fields.
SPACES_NUM: int = 3
# The spaces inbetween standard fields.
SPACES: str = ' ' * SPACES_NUM
# The dots sand spaces between cut fields.
DOTS: str = f'{"." * SPACES_NUM}{SPACES}'
# The number of characters in each line.
LINE_LENGTH: int = MAX_TYPE_LEN + MAX_ID_LEN + \
    MAX_NAME_LEN + MAX_ARTIST_LEN + SPACES_NUM * 5
# The default for the country option.
DEFAULT_COUNTRY: str = 'US'
# The default for the media option.
DEFAULT_MEDIA: List[str] = ['music']
# The default for the entity option.
DEFAULT_ENTITY: List[str] = ['song', 'album', 'musicArtist']
# The default for the limit option.
DEFAULT_LIMIT: int = 15
# The default for the lang option.
DEFAULT_LANG: str = 'en_us'

assert LINE_LENGTH <= 79, f'the sum of the field sizes is too big: {LINE_LENGTH}'


class WrapperNotDefined(Exception):
    pass


class iTunesArtist:
    type: str
    id: int
    name: str

    def __init__(self, r):
        self.type = 'Artist'
        self.id = int(r['artistId'])
        self.name = r['artistName']

    def __str__(self) -> str:
        return self.name


class iTunesWrapper:
    type: str
    genre: str
    artist: iTunesArtist
    name: str
    releaseDate: dt

    def __init__(self, r):
        self.type = r['wrapperType']
        self.genre = r['primaryGenreName']
        self.artist = iTunesArtist(r)
        self.releaseDate = dt.strptime(r['releaseDate'], '%Y-%m-%dT%H:%M:%SZ')


class iTunesTrack(iTunesWrapper):
    id: int
    collectionId: int
    time: int
    releaseDate: dt

    def __init__(self, r):
        iTunesWrapper.__init__(self, r)
        self.type = 'Track'
        self.id = int(r['trackId'])
        self.collectionId = int(r['collectionId'])
        self.time = int(r['trackTimeMillis'])
        self.name = r['trackName']

    def __str__(self) -> str:
        return self.name


class iTunesCollection(iTunesWrapper):
    id: int
    trackCount: int
    releaseDate: dt

    def __init__(self, r):
        iTunesWrapper.__init__(self, r)
        self.type = r['collectionType']
        self.id = int(r['collectionId'])
        self.name = r['collectionName']
        self.trackCount = int(r['trackCount'])

    def __str__(self) -> str:
        return self.name


parser = argparse.ArgumentParser(description='Search the iTunes store.')
parser.add_argument('term', type=str, nargs='+',
                    help='The URL-encoded text string you want to search for.')
parser.add_argument('--country', type=str, nargs='?',
                    help='The two-letter country code for the store you want to search. The search uses the default store front for the specified country.',
                    default=DEFAULT_COUNTRY)
parser.add_argument('--media', type=str, nargs='+',
                    help='The media type you want to search for.',
                    choices=['movie', 'podcast', 'music', 'musicVideo', 'audiobook',
                             'shortFilm', 'tvShow', 'software', 'ebook', 'all'],
                    default=DEFAULT_MEDIA)
parser.add_argument('--entity', type=str, nargs='+',
                    help='The type of results you want returned, relative to the specified media type.',
                    default=DEFAULT_ENTITY)
parser.add_argument('--limit', type=int, nargs='?',
                    help='The number of search results you want the iTunes Store to return.',
                    choices=(range(1, 201)), default=DEFAULT_LIMIT)
parser.add_argument('--lang', type=str, nargs='?',
                    help='The language, English or Japanese, you want to use when returning search results. Specify the language using the five-letter codename.',
                    choices=['en_us', 'ja_jp'], default=DEFAULT_LANG)
parser.add_argument('--clean', action='store_true',
                    help='A flag indicating whether or not you want to exclude explicit content in your search results.')


def build_request(args) -> requests.Request:
    """Builds the iTunes search request.
    Conforming to https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

    Arguments:
        args {[type]} -- The arguments from argparse.

    Returns:
        requests.Request -- The request to send.
    """
    params: Dict[str, str] = {
        'output': 'json',
        'callback': 'JSONP.run',
        'term': str(' '.join(args.term)),
        'country': str(args.country),
        'media': str(','.join(args.media)),
        'entity': str(','.join(args.entity)),
        'limit': str(args.limit),
        'lang': str(args.lang),
        'explicit': '0' if args.clean else '1'
    }
    req: requests.Request = requests.Request(
        'GET', 'https://itunes.apple.com/search', params=params)
    return req


def send_request(req: requests.Request) -> requests.Response:
    """Sends the search request.

    Arguments:
        req {requests.Request} -- The request object to search.

    Returns:
        requests.Response -- The response from iTunes.
    """
    with requests.Session() as s:
        prep: requests.PreparedRequest = s.prepare_request(req)
        res: requests.Response = s.send(prep)
    return res


def cut_content(cont: str) -> str:
    """Cuts the JSONP.run function from the result.

    Arguments:
        cont {str} -- The raw content of the response.

    Returns:
        str -- The cut contents of the response.
    """
    STT: int = 13  # The starting index of the actual data.
    END: int = -5  # The ending index of the actual data.
    return cont[STT:END]


def print_result(w: Union[iTunesArtist, iTunesCollection, iTunesTrack]) -> None:
    """Prints the search results.

    Arguments:
        r {Dict[Any, Any]} -- The collection.
    """
    print(f'{w.type:{MAX_TYPE_LEN}}', end=SPACES)
    print(f'{w.id:<{MAX_ID_LEN}}', end=SPACES)
    if len(w.name) > MAX_NAME_LEN:
        print(f'{w.name[:MAX_NAME_LEN]:{MAX_NAME_LEN}}', end='...   ')
    else:
        print(f'{w.name:{MAX_NAME_LEN}}', end=SPACES * 2)
    if w.type != 'Artist':
        if len(w.artist.name) > MAX_ARTIST_LEN:
            print(
                f'{w.artist.name[:MAX_ARTIST_LEN]:{MAX_ARTIST_LEN}}', end='...')
        else:
            print(f'{w.artist.name:{MAX_ARTIST_LEN}}', end=SPACES * 2)
    print()


if __name__ == '__main__':
    args: argparse.Namespace = parser.parse_args()
    req: requests.Request = build_request(args)
    res: requests.Response = send_request(req)
    data: Dict[Any, Any] = json.loads(cut_content(res.content.decode('utf-8')))

    print(f'{"Type":{MAX_TYPE_LEN}}', end=SPACES)
    print(f'{"ID":{MAX_ID_LEN}}', end=SPACES)
    print(f'{"Name":{MAX_NAME_LEN}}', end=SPACES*2)
    print(f'{"Artist":{MAX_ARTIST_LEN}}')
    print('-' * 79)
    for r in data['results']:
        if r['wrapperType'] == 'collection':
            w = iTunesCollection(r)
        elif r['wrapperType'] == 'track':
            w = iTunesTrack(r)
        elif r['wrapperType'] == 'artist':
            w = iTunesArtist(r)
        else:
            raise WrapperNotDefined(
                f'"{r["wrapperType"]}" not a known wrapper type')
        print_result(w)
