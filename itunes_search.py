#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2020-03-08
Revision : 2020-03-08
"""

import json
from datetime import datetime as dt
import argparse
from typing import List, Dict, Union, Any
import requests

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
    """Represents the exception for when an iTunes wrapper in undefined.
    """


class Artist:
    """Represents an iTunes Artist.

    Returns:
        Artist -- An iTunes Artist object.
    """
    type: str
    uid: int
    name: str

    def __init__(self, r):
        self.type = 'Artist'
        self.uid = int(r['artistId'])
        self.name = r['artistName']

    def __str__(self) -> str:
        return self.name


class Wrapper:
    """Represents an iTunes Wrapper.

    Returns:
        Wrapper -- An iTunes Wrapper object.
    """
    type: str
    uid: int
    genre: str
    artist: Artist
    name: str
    release_date: dt

    def __init__(self, r):
        self.type = r['wrapperType']
        self.genre = r['primaryGenreName']
        self.artist = Artist(r)
        self.release_date = dt.strptime(r['releaseDate'], '%Y-%m-%dT%H:%M:%SZ')

    def __str__(self):
        return self.name


class Track(Wrapper):
    """Represents an iTunes Track.

    Returns:
        Track -- An iTunes Track object.
    """
    collection_id: int
    time: int

    def __init__(self, r):
        Wrapper.__init__(self, r)
        self.type = 'Track'
        self.uid = int(r['trackId'])
        self.collection_id = int(r['collectionId'])
        self.time = int(r['trackTimeMillis'])
        self.name = r['trackName']

    def __str__(self) -> str:
        return self.name


class Collection(Wrapper):
    """Represents an iTunes Collection.

    Returns:
        Collection -- An iTunes Collection object.
    """
    track_count: int

    def __init__(self, r):
        Wrapper.__init__(self, r)
        self.type = r['collectionType']
        self.uid = int(r['collectionId'])
        self.name = r['collectionName']
        self.track_count = int(r['trackCount'])

    def __str__(self) -> str:
        return self.name


PARSER = argparse.ArgumentParser(description='Search the iTunes store.')
PARSER.add_argument('term',
                    type=str,
                    nargs='+',
                    help='The URL-encoded text string you want to search for.')
PARSER.add_argument(
    '--country',
    type=str,
    nargs='?',
    help=
    'The two-letter country code for the store you want to search.',
    default=DEFAULT_COUNTRY)
PARSER.add_argument('--media',
                    type=str,
                    nargs='+',
                    help='The media type you want to search for.',
                    choices=[
                        'movie', 'podcast', 'music', 'musicVideo', 'audiobook',
                        'shortFilm', 'tvShow', 'software', 'ebook', 'all'
                    ],
                    default=DEFAULT_MEDIA)
PARSER.add_argument(
    '--entity',
    type=str,
    nargs='+',
    help=
    'The type of results you want returned, relative to the specified media type.',
    default=DEFAULT_ENTITY)
PARSER.add_argument(
    '--limit',
    type=int,
    nargs='?',
    help='The number of search results you want the iTunes Store to return.',
    choices=(range(1, 201)),
    default=DEFAULT_LIMIT)
PARSER.add_argument(
    '--lang',
    type=str,
    nargs='?',
    help=
    'The language, English or Japanese, you want to use when returning search results.',
    choices=['en_us', 'ja_jp'],
    default=DEFAULT_LANG)
PARSER.add_argument(
    '--clean',
    action='store_true',
    help=
    'A flag indicating whether or not you want to exclude explicit content in your search results.'
)


def build_request(args: argparse.Namespace) -> requests.Request:
    """Builds the iTunes search request.
    https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

    Arguments:
        args {argparse.Namespace} -- The arguments from argparse.

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
    req: requests.Request = requests.Request('GET',
                                             'https://itunes.apple.com/search',
                                             params=params)
    return req


def send_request(req: requests.Request) -> requests.Response:
    """Sends the search request.

    Arguments:
        req {requests.Request} -- The request object to search.

    Returns:
        requests.Response -- The response from iTunes.
    """
    with requests.Session() as session:
        prep: requests.PreparedRequest = session.prepare_request(req)
        resp: requests.Response = session.send(prep)
    return resp


def cut_content(cont: str) -> str:
    """Cuts the JSONP.run function from the result.

    Arguments:
        cont {str} -- The raw content of the response.

    Returns:
        str -- The cut contents of the response.
    """
    start: int = 13  # The starting index of the actual data.
    stop: int = -5  # The ending index of the actual data.
    return cont[start:stop]


def print_result(coll: Union[Artist, Collection, Track]) -> None:
    """Prints the search results.

    Arguments:
        coll {Union[Artist, Collection, Track]} -- The collection.
    """
    print(f'{coll.type:{MAX_TYPE_LEN}}', end=SPACES)
    print(f'{coll.id:<{MAX_ID_LEN}}', end=SPACES)
    if len(coll.name) > MAX_NAME_LEN:
        print(f'{coll.name[:MAX_NAME_LEN]:{MAX_NAME_LEN}}', end='...   ')
    else:
        print(f'{coll.name:{MAX_NAME_LEN}}', end=SPACES * 2)
    if coll.type != 'Artist':
        if len(coll.artist.name) > MAX_ARTIST_LEN:
            print(f'{coll.artist.name[:MAX_ARTIST_LEN]:{MAX_ARTIST_LEN}}',
                  end='...')
        else:
            print(f'{coll.artist.name:{MAX_ARTIST_LEN}}', end=SPACES * 2)
    print()


if __name__ == '__main__':
    ARGS: argparse.Namespace = PARSER.parse_args()
    request: requests.Request = build_request(ARGS)
    res: requests.Response = send_request(request)
    data: Dict[Any, Any] = json.loads(cut_content(res.content.decode('utf-8')))

    print(f'{"Type":{MAX_TYPE_LEN}}', end=SPACES)
    print(f'{"ID":{MAX_ID_LEN}}', end=SPACES)
    print(f'{"Name":{MAX_NAME_LEN}}', end=SPACES * 2)
    print(f'{"Artist":{MAX_ARTIST_LEN}}')
    print('-' * 79)
    for raw_ent in data['results']:
        if raw_ent['wrapperType'] == 'collection':
            entity = Collection(raw_ent)
        elif raw_ent['wrapperType'] == 'track':
            entity = Track(raw_ent)
        elif raw_ent['wrapperType'] == 'artist':
            entity = Artist(raw_ent)
        else:
            raise WrapperNotDefined(
                f'"{raw_ent["wrapperType"]}" not a known wrapper type')
        print_result(entity)
