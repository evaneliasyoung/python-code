#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2020-03-09
Revision : 2020-03-11
"""

from __future__ import annotations
import sys
import os
import json
from datetime import datetime as dt
from typing import Tuple, List, Dict, Union, Optional, Any
import requests

# The max length for the id printer.
MAX_ID_LEN: int = 11
# The max length for the album printer.
MAX_NAME_LEN: int = 32
# The max length for the artist printer.
MAX_ARTIST_LEN: int = 17
# The number of spaces inbetween standard fields.
SPACES_NUM: int = 3
# The spaces inbetween standard fields.
SPACES: str = ' ' * SPACES_NUM
# The dots sand spaces between cut fields.
DOTS: str = f'{"." * SPACES_NUM}{SPACES}'
# The number of characters in each line.
LINE_LENGTH: int = 4 + MAX_ID_LEN + MAX_NAME_LEN + MAX_ARTIST_LEN + SPACES_NUM * 5
assert LINE_LENGTH <= 79, f'line length too large, {LINE_LENGTH}'
# The default for the country option.
SEARCH_COUNTRY: str = 'US'
# The default for the media option.
SEARCH_MEDIA: str = 'music'
# The default for the entity option.
SEARCH_LIMIT: int = 10
# The default for the lang option.
SEARCH_LANG: str = 'en_us'
# The iTules version
VERSION: str = '0.2.0'


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
    def lookup(uid: int) -> Optional[Dict[Any, Any]]:
        """Sends a lookup request with a given id.

        Arguments:
            uid {int} -- The entity id.

        Returns:
            Dict[Any, Any] -- The raw data returned by iTunes.
        """
        data: Optional[Dict[Any, Any]] = None
        try:
            response: requests.Response = requests.get(
                'https://itunes.apple.com/lookup', params={'id': uid})
            data = json.loads(response.content.decode('utf-8'))['results'][0]
        except:
            data = None
        return data

    @staticmethod
    def lookup_entity(uid: int) -> Optional[Union[Artist, Album, Track]]:
        # Get the raw data.
        data: Optional[Dict[Any, Any]] = Wrapper.lookup(uid)
        entity: Optional[Union[Artist, Album, Track]] = None
        if data:
            entity = Wrapper.derive_entity(data).from_response(data)
        return entity

    @staticmethod
    def search(term: str, entity: str) -> Dict[Any, Any]:
        """Sends a search request with a given term and entity type.

        Arguments:
            term {str} -- The search term.
            entity {str} -- The entity type(s).

        Returns:
            Dict[Any, Any] -- The raw data returned by iTunes.
        """
        # The starting index of the actual data.
        start: int = 13
        # The ending index of the actual data.
        stop: int = -5
        # The search parameters.
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
        # The response for the request.
        response: requests.Response = requests.get(
            'https://itunes.apple.com/search', params=params)
        # The json data.
        data: Dict[Any, Any] = json.loads(
            response.content.decode('utf-8')[start:stop])
        return data

    @staticmethod
    def search_entities(term: str,
                        entity: str) -> List[Union[Artist, Album, Track]]:
        # Get the raw data.
        data: Dict[Any, Any] = Wrapper.search(term, entity)
        # Create the list of results.
        results: List[Union[Artist, Album, Track]] = []
        # The current entity when iterating.
        cur_ent: Union[Artist, Album, Track]

        for raw_ent in data['results']:
            cur_ent = Wrapper.derive_entity(raw_ent).from_response(raw_ent)
            results.append(cur_ent)
        return results

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
        track.album = Album.from_response(data)
        track.time = int(data['trackTimeMillis'])
        track.name = data['trackName']
        return track

    def print_details(self) -> None:
        """Prints more details about a track.
        """
        to_print: Dict[str, str] = {
            'ID': self.uid,
            'Name': self.name,
            'Artist': self.artist,
            'Album': self.album,
            'Genre': self.genre,
            'Release Date': self.release_date
        }
        print('\n'.join(align_dict(to_print)))

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


def send_search(term: str, entity: str) -> List[Union[Artist, Album, Track]]:
    """Sends a search request with a given term and entity type.

    Arguments:
        term {str} -- The search term.
        entity {str} -- The entity type(s).

    Returns:
        List[Union[Artist, Album, Track]] -- A list of all the search results.
    """
    # Get the raw data.
    data: Dict[Any, Any] = Wrapper.search(term, entity)
    # Create the list of results.
    results: List[Union[Artist, Album, Track]] = []
    # The current entity when iterating.
    cur_entity: Union[Artist, Album, Track]

    for raw_ent in data['results']:
        cur_entity = Wrapper.derive_entity(raw_ent).from_response(raw_ent)
        results.append(cur_entity)
    return results


def align_dict(collection: Dict[Any, Any]) -> List[str]:
    # The max length of all the keys.
    max_key_len: int = max([len(k) for k in collection])
    # The keys and descriptions.
    lines: List[str] = [
        f'{key:{max_key_len}} -- {collection[key]}'
        for _, key in enumerate(collection)
    ]
    return lines


def print_result(coll: Union[Artist, Album, Track]) -> None:
    """Prints the search results.

    Arguments:
        coll {Union[Artist, Album, Track]} -- The entity.
    """
    print(f'{coll.uid:<{MAX_ID_LEN}}', end=SPACES)
    if len(coll.name) > MAX_NAME_LEN:
        # entity name too big, trim it.
        print(f'{coll.name[:MAX_NAME_LEN]:{MAX_NAME_LEN}}', end='...   ')
    else:
        print(f'{coll.name:{MAX_NAME_LEN}}', end=SPACES * 2)
    if not isinstance(coll, Artist):
        # not an artist, so it has an artist field.
        if len(coll.artist.name) > MAX_ARTIST_LEN:
            # artist name too big, trim it.
            print(f'{coll.artist.name[:MAX_ARTIST_LEN]:{MAX_ARTIST_LEN}}',
                  end='...')
        else:
            print(f'{coll.artist.name:{MAX_ARTIST_LEN}}', end=SPACES * 2)
    print()


def print_centered(text: str, width: int = LINE_LENGTH) -> None:
    """Prints text centered in the menus.

    Arguments:
        text {str} -- The text to print.

    Keyword Arguments:
        width {int} -- The width of the container (default: {LINE_LENGTH})
    """
    print(f'{text:^{width}}')


def get_menu_opt(menu_name: str,
                 options: Dict[str, str],
                 strict: bool = True) -> Tuple[str, List[str]]:
    """Displays a menu and returns a valid option.

    Arguments:
        menu_name {str} -- The menu's name.
        options {Dict[str, str]} -- The valid options and descriptions.

    Keyword Arguments:
        strict {bool} -- Whether or not to disallow options not in the dictionary. (default: {True})

    Returns:
        Tuple[str, List[str]] -- The chosen option, and any extra pieces.
    """
    # The user's selected option.
    opt: str = ''
    # The options and decsriptions.
    lines: List[str] = align_dict(options)
    # The max length of all the lines.
    max_line_len: int = max([len(k) for k in lines])
    # The number of spaces to put before the options.
    left_pad: int = round((LINE_LENGTH - max_line_len) / 2)

    while True:
        print_header()
        print_centered(f'{menu_name} MENU')
        for line in lines:
            print(f'{" ":{left_pad}}{line}')
        opt = input()
        if not (strict) or opt.split(' ')[0] in options:
            break
    return (opt.split(' ')[0], opt.split(' ')[1:])


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
    print_centered('  _ _______    _           ')
    print_centered(' (_)__   __|  | |          ')
    print_centered('  _   | |_   _| | ___  ___ ')
    print_centered(' | |  | | | | | |/ _ \\/ __|')
    print_centered(' | |  | | |_| | |  __/\\__ \\')
    print_centered(' |_|  |_|\\__,_|_|\\___||___/')
    print_centered('                           ')
    print_centered(f'Version {VERSION}')
    print_centered(f'Copyright Evan Elias Young')
    print()


def search_menu() -> None:
    """The search menu for iTules.
    """
    # Whether or not to keep the menu alive.
    keep_alive: bool = True

    while keep_alive:
        # The valid options the user can pick.
        choices: Dict[str, str] = {
            'song': 'search for a song',
            'album': 'search for a album',
            'artist': 'search for a artist',
            'all': 'search for any of the above',
            'back': 'go back',
            'exit': 'exit the program'
        }
        # The option the user has chosen.
        choice: str
        # Any extra input the user has entered.
        args: List[str]
        # Actually retrieve the data.
        choice, args = get_menu_opt('SEARCH', choices)

        if choice == 'exit':
            sys.exit(0)
        elif choice == 'back':
            keep_alive = False
        else:
            search_term: str = ' '.join(args)
            if len(args) == 0:
                print_header()
                print_centered(f'{choice.upper()} SEARCH MENU')
                search_term = input('enter your search term:\n')
            entity_name: str = 'song,album,musicArtist' if choice == 'all' else \
                'musicArtist' if choice == 'artist' else choice
            search_results: List[Union[Artist, Album, Track]] = send_search(
                search_term, entity_name)
            clear()
            print_centered(f'{choice.upper()} SEARCH RESULTS')
            if len(search_results) > 0:
                for i, result in enumerate(search_results):
                    print(f'[{i}]', end=' ')
                    print_result(result)
                sel: str = input(
                    'Enter the index if you would like more details, otherwise I\'ll continue. . .\n'
                )
                if sel.isdigit() and int(sel) >= 0 and int(sel) < SEARCH_LIMIT:
                    clear()
                    print_centered('DETAILED SEARCH RESULTS')
                    search_results[int(sel)].print_details()
            else:
                print_centered('NO RESULTS')
            pause()


def lookup_menu(uid: Optional[int]) -> None:
    """The lookup menu for iTules.
    """
    # Whether or not to keep the menu alive.
    keep_alive: bool = True

    while keep_alive:
        choice: str
        if not isinstance(uid, int):
            # The valid options the user can pick.
            choices: Dict[str, str] = {
                'numeric': 'the ID to search for',
                'back': 'go back',
                'exit': 'exit the program'
            }
            # The option the user has chosen.
            choice: str
            # Actually retrieve the data.
            choice = get_menu_opt('LOOKUP', choices, False)[0]
        else:
            choice = str(uid)

        if choice == 'exit':
            sys.exit(0)
        elif choice == 'back':
            keep_alive = False
        elif choice.isdigit():
            keep_alive = False
            entity: Optional[Union[Artist, Album,
                                   Track]] = Wrapper.lookup_entity(str(choice))
            clear()
            print_centered('LOOKUP RESULTS')
            if entity:
                print_result(entity)
            else:
                print_centered('NO RESULTS')
            pause()


def main_menu() -> None:
    """The main menu for iTules.
    """
    # Whether or not to keep the menu alive.
    keep_alive: bool = True

    while keep_alive:
        # The valid options the user can pick.
        choices: Dict[str, str] = {
            'search': 'search the iTunes store by a term',
            'lookup': 'search the iTunes store by an entity ID',
            'exit': 'exit the program'
        }
        # The option the user has chosen.
        choice: str
        # Any extra input the user has entered.
        args: List[str]
        # Actually retrieve the data.
        choice, args = get_menu_opt('MAIN', choices)

        if choice == 'exit':
            sys.exit(0)
        elif choice == 'search':
            search_menu()
        elif choice == 'lookup':
            lookup_menu(int(args[0]) if len(args) > 0 else None)


if __name__ == '__main__':
    main_menu()
