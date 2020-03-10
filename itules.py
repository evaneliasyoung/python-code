#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2020-03-09
Revision : 2020-03-09
"""

from __future__ import annotations
import sys
import os
import json
from datetime import datetime as dt
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
# The max length for a menu.
MAX_MENU_LEN: int = 27
# The default for the country option.
SEARCH_COUNTRY: str = 'US'
# The default for the media option.
SEARCH_MEDIA: str = 'music'
# The default for the entity option.
SEARCH_LIMIT: int = 10
# The default for the lang option.
SEARCH_LANG: str = 'en_us'
# The iTules version
VERSION: str = '0.1.0'


class Artist:
    """Represents an iTunes Artist.

    Returns:
        Artist -- An iTunes Artist object.
    """
    type: str
    uid: int
    name: str

    def __init__(self) -> None:
        pass

    @staticmethod
    def from_response(data: Dict[Any, Any]) -> Artist:
        """Generates an Artist with a dataset from iTunes.

        Arguments:
            data {Any} -- The dataset from iTunes.

        Returns:
            Artist -- The Artist object.
        """
        artist: Artist = Artist()
        artist.type = 'Artist'
        artist.uid = int(data['artistId'])
        artist.name = data['artistName']
        return artist

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

    def __init__(self, data: Dict[Any, Any]) -> None:
        self.type = data['wrapperType']
        self.genre = data['primaryGenreName']
        self.artist = Artist.from_response(data)
        self.release_date = dt.strptime(data['releaseDate'],
                                        '%Y-%m-%dT%H:%M:%SZ')

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def lookup(uid: int) -> Dict[Any, Any]:
        """Sends a lookup request with a given id.

        Arguments:
            uid {int} -- The entity id.

        Returns:
            Dict[Any, Any] -- The raw data returned by iTunes.
        """
        request: requests.Request = requests.Request(
            'GET', 'https://itunes.apple.com/lookup', params={'id': uid})
        response: requests.Response = send_request(request)
        data: Dict[Any, Any] = json.loads(
            response.content.decode('utf-8'))['results'][0]
        return data

    @staticmethod
    def search(term: str, entity: str) -> Dict[Any, Any]:
        """Sends a search request with a given term and entity type.

        Arguments:
            term {str} -- The search term.
            entity {str} -- The entity type(s).

        Returns:
            Dict[Any, Any] -- The raw data returned by iTunes.
        """
        request: requests.Request = build_search_request(term, entity)
        response: requests.Response = send_request(request)
        data: Dict[Any, Any] = json.loads(
            cut_content(response.content.decode('utf-8')))
        return data

    @staticmethod
    def derive_entity(data: Dict[Any, Any]) -> Union[Artist, Album, Track]:
        """Derives the entity type given raw data from iTunes.

        Arguments:
            data {Dict[Any, Any]} -- The raw data returned by iTunes.

        Raises:
            NotImplementedError: An uncoded wrapper type was returned.

        Returns:
            Union[Artist, Album, Track] -- The entity
        """
        entity: Union[Artist, Album, Track]
        if data['wrapperType'] == 'collection':
            entity = Album()
        elif data['wrapperType'] == 'track':
            entity = Track()
        elif data['wrapperType'] == 'artist':
            entity = Artist()
        else:
            raise NotImplementedError(
                f'"{data["wrapperType"]}" not a known wrapper type')
        return entity


class Track(Wrapper):
    """Represents an iTunes Track.

    Returns:
        Track -- An iTunes Track object.
    """
    album: Album
    time: int

    def __init__(self) -> None:
        pass

    @staticmethod
    def from_response(data: Dict[Any, Any]) -> Track:
        """Generates a Track with a dataset from iTunes.

        Arguments:
            data {Any} -- The dataset from iTunes.

        Returns:
            Track -- The Track object.
        """
        track: Track = Track()
        Wrapper.__init__(track, data)
        track.type = 'Track'
        track.uid = int(data['trackId'])
        track.album = Artist.from_response(data)
        track.time = int(data['trackTimeMillis'])
        track.name = data['trackName']
        return track

    def __str__(self) -> str:
        return self.name


class Album(Wrapper):
    """Represents an iTunes Album.

    Returns:
        Album -- An iTunes Album object.
    """
    track_count: int

    def __init__(self) -> None:
        pass

    @staticmethod
    def from_response(data: Dict[Any, Any]) -> Album:
        """Generates a Album with a dataset from iTunes.

        Arguments:
            data {Any} -- The dataset from iTunes.

        Returns:
            Album -- The Album object.
        """
        album: Album = Album()
        Wrapper.__init__(album, data)
        album.type = 'Album'
        album.uid = int(data['collectionId'])
        album.name = data['collectionName']
        album.track_count = int(data['trackCount'])
        return album

    def __str__(self) -> str:
        return self.name


def build_search_request(term: str, entity: str) -> requests.Request:
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
        'term': term,
        'country': SEARCH_COUNTRY,
        'media': SEARCH_MEDIA,
        'entity': entity,
        'limit': SEARCH_LIMIT,
        'lang': SEARCH_LANG
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


def send_lookup(uid: int) -> Union[Artist, Album, Track]:
    """Sends a lookup request with a given id.

    Arguments:
        uid {int} -- The entity id.

    Returns:
        Union[Artist, Album, Track] -- The lookup result.
    """
    data: Dict[Any, Any] = Wrapper.lookup(uid)
    entity: Union[Artist, Album,
                  Track] = Wrapper.derive_entity(data).from_response(data)
    return entity


def send_search(term: str, entity: str) -> List[Union[Artist, Album, Track]]:
    """Sends a search request with a given term and entity type.

    Arguments:
        term {str} -- The search term.
        entity {str} -- The entity type(s).

    Returns:
        List[Union[Artist, Album, Track]] -- A list of all the search results.
    """
    data: Dict[Any, Any] = Wrapper.search(term, entity)  # Get the raw data.
    results: List[Union[Artist, Album,
                        Track]] = []  # Create the list of results.
    cur_entity: Union[Artist, Album,
                      Track]  # The current entity when iterating.
    for raw_ent in data['results']:
        cur_entity = Wrapper.derive_entity(raw_ent).from_response(raw_ent)
        results.append(cur_entity)
    return results


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


def print_result(coll: Union[Artist, Album, Track]) -> None:
    """Prints the search results.

    Arguments:
        coll {Union[Artist, Album, Track]} -- The entity.
    """
    print(f'{coll.type:{MAX_TYPE_LEN}}', end=SPACES)
    print(f'{coll.uid:<{MAX_ID_LEN}}', end=SPACES)
    if len(coll.name) > MAX_NAME_LEN:  # entity name too big, trim it.
        print(f'{coll.name[:MAX_NAME_LEN]:{MAX_NAME_LEN}}', end='...   ')
    else:
        print(f'{coll.name:{MAX_NAME_LEN}}', end=SPACES * 2)
    if not isinstance(coll,
                      Artist):  # not an artist, so it has an artist field/
        if len(coll.artist.name
               ) > MAX_ARTIST_LEN:  # artist name too big, trim it.
            print(f'{coll.artist.name[:MAX_ARTIST_LEN]:{MAX_ARTIST_LEN}}',
                  end='...')
        else:
            print(f'{coll.artist.name:{MAX_ARTIST_LEN}}', end=SPACES * 2)
    print()


def print_centered(text: str, width: int = MAX_MENU_LEN) -> None:
    """Prints text centered in the menus.

    Arguments:
        text {str} -- The text to print.

    eyword Arguments:
        width {int} -- The width of the container (default: {MAX_MENU_LEN})
    """
    print(f'{text:^{width}}')


def get_menu_opt(menu_name: str, options: Dict[str, str]) -> str:
    """Displays a menu and returns a valid option.

    Arguments:
        menu_name {str} -- The menu's name.
        options {Dict[str, str]} -- The valid options and descriptions.

    Returns:
        str -- The chosen option.
    """
    opt: str = ''  # The user's selected option.
    max_key_len: int = max([len(k) for k in options
                            ])  # The max length of all the keys.
    while opt not in options:
        print_header()
        print_centered(f'{menu_name} MENU')
        for _, key in enumerate(options):
            print(f'{key:{max_key_len}} -- {options[key]}')
        opt = input()
    return opt


def clear() -> None:
    """Clears the screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def pause() -> None:
    """Prompts the user to press any key to continue.
    """
    os.system('pause' if os.name == 'nt' else
              'read -n1 -r -p "Press any key to continue . . . " key')


def print_header() -> None:
    """Prints the main header for iTules.
    """
    clear()
    print('  _ _______    _           ')
    print(' (_)__   __|  | |          ')
    print('  _   | |_   _| | ___  ___ ')
    print(' | |  | | | | | |/ _ \\/ __|')
    print(' | |  | | |_| | |  __/\\__ \\')
    print(' |_|  |_|\\__,_|_|\\___||___/')
    print('                           ')
    print(f'      Version {VERSION}')
    print(f'Copyright Evan Elias Young')
    print()


def search_menu() -> None:
    """The search menu for iTules.
    """
    keep_alive: bool = True
    while keep_alive:
        choices: Dict[str, str] = {
            'song': 'search for a song',
            'album': 'search for a album',
            'artist': 'search for a artist',
            'all': 'search for any of the above',
            'back': 'go back',
            'exit': 'exit the program'
        }
        choice: str = get_menu_opt('SEARCH', choices)

        if choice == 'exit':
            sys.exit(0)
        elif choice == 'back':
            keep_alive = False
        else:
            print_header()
            print_centered(f'{choice.upper()} SEARCH MENU')
            search_term: str = input('enter your search term:\n')
            entity_name: str = 'song,album,musicArtist' if choice == 'all' else 'musicArtist' if choice == 'artist' else choice
            search_results: List[Union[Artist, Album, Track]] = send_search(
                search_term, entity_name)
            clear()
            print_centered('SEARCH RESULTS', LINE_LENGTH)
            for _, result in enumerate(search_results):
                print_result(result)
            pause()


def main_menu() -> None:
    """The main menu for iTules.
    """
    keep_alive: bool = True
    while keep_alive:
        choices: Dict[str, str] = {
            'search': 'search the iTunes store',
            'exit': 'exit the program'
        }
        choice: str = get_menu_opt('MAIN', choices)

        if choice == 'exit':
            sys.exit(0)
        elif choice == 'search':
            search_menu()


if __name__ == '__main__':
    main_menu()
