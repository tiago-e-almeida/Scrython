import aiohttp
import asyncio
import urllib.parse
from threading import Thread

class CardsObject(object):
    """
    Master class that all card objects inherit from.

    Args:
        format (string, optional):
            Defaults to 'json'.
            Returns data in the specified method.
        face (string, optional):
            Defaults to empty string.
            If you're using the `image` format, this will specify if you want the front or back face.
        version (string, optional):
            Defaults to empty string.
            If you're using the `image` format, this will specify if you want the small, normal,
            large, etc version of the image.
        pretty (string, optional):
            Defaults to empty string.
            Returns a prettier version of the json object.
            Note that this may break functionality with Scrython.

    Raises:
        Exception: If the object returned is an error.
    """
    def __init__(self, _url, **kwargs):

        self.params = {
            'format': kwargs.get('format', 'json'), 'face': kwargs.get('face', ''),
            'version': kwargs.get('version', ''), 'pretty': kwargs.get('pretty', '')
        }

        self.encodedParams = urllib.parse.urlencode(self.params)
        self._url = 'https://api.scryfall.com/{0}&{1}'.format(_url, self.encodedParams)

        async def getRequest(client, url, **kwargs):
            async with client.get(url, **kwargs) as response:
                return await response.json()

        async def main(loop):
            async with aiohttp.ClientSession(loop=loop) as client:
                self.scryfallJson = await getRequest(client, self._url)

        def do_everything():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main(loop))

        t = Thread(target=do_everything)
        t.run()

        if self.scryfallJson['object'] == 'error':
            raise Exception(self.scryfallJson['details'])

    def _checkForKey(self, key):
        """Checks for a key in the scryfallJson object.
        This function should be considered private, and
        should not be accessed in production.
        
        Args:
            key (string): The key to check
        
        Raises:
            KeyError: If key is not found.
        """
        if not key in self.scryfallJson:
            raise KeyError('This card has no key \'{}\''.format(key))

    def _checkForTupleKey(self, parent, num, key):
        """Checks for a key of an object in an list.
        This function should be considered private, and
        should not be accessed in production.
        
        Args:
            parent (string): The key for the list to be accessed
            num (int): The index of the list
            key (string): The key to check
        
        Raises:
            KeyError: If key is not found.
        """
        if not key in self.scryfallJson[parent][num]:
            raise KeyError('This tuple has no key \'{}\''.format(key))

    def object(self):
        """Returns the type of object it is
        (card, error, etc)
        
        Returns:
            string
        """
        self._checkForKey('object')

        return self.scryfallJson['object']

    def id(self):
        """A unique ID for the returned card object
        
        Returns:
            string
        """
        self._checkForKey('id')

        return self.scryfallJson['id']

    def multiverse_ids(self):
        """The official Gatherer multiverse ids of the card
        
        Returns:
            list
        """
        self._checkForKey('multiverse_ids')

        return self.scryfallJson['multiverse_ids']

    def mtgo_id(self):
        """The official MTGO id of the of the card
        
        Returns:
            integer: The Magic Online id of the card
        """
        self._checkForKey('mtgo_id')

        return self.scryfallJson['mtgo_id']

    def mtgo_foil_id(self):
        """The corresponding MTGO foil ID of the card
        
        Returns:
            integer: The Magic Online foil id of the card
        """
        self._checkForKey('mtgo_foil_id')

        return self.scryfallJson['mtgo_foil_id']

    def name(self):
        """The oracle name of the card
        
        Returns:
            string
        """
        self._checkForKey('name')

        return self.scryfallJson['name']

    def uri(self):
        """The Scryfall API uri for the card
        
        Returns:
            string
        """
        self._checkForKey('uri')

        return self.scryfallJson['uri']

    def scryfall_uri(self):
        """The full Scryfall page of the card
        As if it was a URL from the site.
        
        Returns:
            string
        """
        self._checkForKey('scryfall_uri')

        return self.scryfallJson['scryfall_uri']

    def layout(self):
        """The image layout of the card. (normal, transform, etc)
        
        Returns:
            string
        """
        self._checkForKey('layout')

        return self.scryfallJson['layout']

    def highres_image(self):
        """Determine if a card has a highres scan available
        
        Returns:
            boolean
        """
        self._checkForKey('highres_image')

        return self.scryfallJson['highres_image']

    def image_uris(self):
        """All image uris of the card in various qualities
        
        Returns:
            dict
        """
        self._checkForKey('image_uris')

        return self.scryfallJson['image_uris']

    def cmc(self):
        """A float of the converted mana cost of the card
        
        Returns:
            float: The cmc of the card
        """
        self._checkForKey('cmc')

        return self.scryfallJson['cmc']

    def type_line(self):
        """The full type line of the card
        
        Returns:
            string
        """
        self._checkForKey('type_line')

        return self.scryfallJson['type_line']

    def oracle_text(self):
        """The official oracle text of a card
        
        Returns:
            string
        """
        self._checkForKey('oracle_text')

        return self.scryfallJson['oracle_text']

    def mana_cost(self):
        """The full mana cost using shorthanded mana symbols
        
        Returns:
            string
        """
        self._checkForKey('mana_cost')

        return self.scryfallJson['mana_cost']

    def colors(self):
        """A list of strings with all colors found in the mana cost
        
        Returns:
            list
        """
        self._checkForKey('colors')

        return self.scryfallJson['colors']

    def color_identity(self):
        """A list of strings with all colors found on the card itself
        
        Returns:
            list
        """
        self._checkForKey('color_identity')

        return self.scryfallJson['color_identity']

    def legalities(self):
        """A dictionary of all formats and their legality
        
        Returns:
            dict
        """
        self._checkForKey('legalities')

        return self.scryfallJson['legalities']

    def reserved(self):
        """Returns True if the card is on the reserved list
        
        Returns:
            boolean
        """
        self._checkForKey('reserved')

        return self.scryfallJson['reserved']

    def reprint(self):
        """Returns True if the card has been reprinted before
        
        Returns:
            boolean
        """
        self._checkForKey('reprint')

        return self.scryfallJson['reprint']

    def set_code(self):
        """The 3 letter code for the set of the card
        
        Returns:
            string
        """
        self._checkForKey('set')

        return self.scryfallJson['set']

    def set_name(self):
        """The full name for the set of the card
        
        Returns:
            string
        """
        self._checkForKey('set_name')

        return self.scryfallJson['set_name']

    def set_uri(self):
        """The API uri for the full set list of the card
        
        Returns:
            string
        """
        self._checkForKey('set_uri')

        return self.scryfallJson['set_uri']

    def set_search_uri(self):
        """Same output as set_uri
        
        Returns:
            string
        """
        self._checkForKey('set_search_uri')

        return self.scryfallJson['set_search_uri']

    def scryfall_set_uri(self):
        """The full link to the set on Scryfall
        
        Returns:
            string
        """
        self._checkForKey('scryfall_set_uri')

        return self.scryfallJson['scryfall_set_uri']

    def rulings_uri(self):
        """The API uri for the rulings of the card
        
        Returns:
            string
        """
        self._checkForKey('rulings_uri')

        return self.scryfallJson['rulings_uri']

    def prints_search_uri(self):
        """A link to where you can begin paginating all re/prints for this card on Scryfall’s API
        
        Returns:
            string
        """
        self._checkForKey('prints_search_uri')

        return self.scryfallJson['prints_search_uri']

    def collector_number(self):
        """The collector number of the card
        
        Returns:
            string
        """
        self._checkForKey('collector_number')

        return self.scryfallJson['collector_number']

    def digital(self):
        """Returns True if the card is the digital version
        
        Returns:
            boolean
        """
        self._checkForKey('digital')

        return self.scryfallJson['digital']

    def rarity(self):
        """The rarity of the card
        
        Returns:
            string
        """
        self._checkForKey('rarity')

        return self.scryfallJson['rarity']

    def illustration_id(self):
        """The related id of the card art
        
        Returns:
            string
        """
        self._checkForKey('illustration_id')

        return self.scryfallJson['illustration_id']

    def artist(self):
        """The artist of the card
        
        Returns:
            string
        """
        self._checkForKey('artist')

        return self.scryfallJson['artist']

    def frame(self):
        """The year of the card frame
        
        Returns:
            string
        """
        self._checkForKey('frame')

        return self.scryfallJson['frame']

    def full_art(self):
        """Returns True if the card is considered full art
        
        Returns:
            boolean
        """
        self._checkForKey('full_art')

        return self.scryfallJson['full_art']

    def border_color(self):
        """The color of the card border
        
        Returns:
            string
        """
        self._checkForKey('border_color')

        return self.scryfallJson['border_color']

    def timeshifted(self):
        """Returns True if the card is timeshifted
        
        Returns:
            boolean
        """
        self._checkForKey('timeshifted')

        return self.scryfallJson['timeshifted']

    def colorshifted(self):
        """Returns True if the card is colorshifted
        
        Returns:
            boolean
        """
        self._checkForKey('colorshifted')

        return self.scryfallJson['colorshifted']

    def futureshifted(self):
        """Returns True if the card is futureshifted
        
        Returns:
            boolean
        """
        self._checkForKey('futureshifted')

        return self.scryfallJson['futureshifted']

    def edhrec_rank(self):
        """The rank of the card on edhrec.co
        
        Returns:
            int: The rank of the card on edhrec.co
        """
        self._checkForKey('edhrec_rank')

        return self.scryfallJson['edhrec_rank']

    def currency(self, mode):
        """Returns currency from modes `usd`, `eur`, and `tix`
        
        Args:
            mode (string): The currency to get
        
        Raises:
            KeyError: If the mode parameter does not match a known key
        
        Returns:
            float: The currency as a float
        """
        modes = ['usd', 'eur', 'tix']
        if mode not in modes:
            raise KeyError("{} is not a key.".format(mode))

        self._checkForKey(mode)

        return self.scryfallJson[mode]

    def related_uris(self):
        """A dictionary of related websites for this card
        
        Returns:
            dict
        """
        self._checkForKey('related_uris')

        return self.scryfallJson['related_uris']

    def purchase_uris(self):
        """A dictionary of links to purchase the card
        
        Returns:
            dict
        """
        self._checkForKey('purchase_uris')

        return self.scryfallJson['purchase_uris']

    def life_modifier(self):
        """This is the cards life modifier value, assuming it's a Vanguard card
        
        Returns:
            string
        """
        self._checkForKey('life_modifier')

        return self.scryfallJson['life_modifier']

    def hand_modifier(self):
        """This cards hand modifier value, assuming it's a Vanguard card
        
        Returns:
            string
        """
        self._checkForKey('hand_modifier')

        return self.scryfallJson['hand_modifier']

    def color_indicator(self, num):
        """An list of all colors found in this card's color indicator
        
        Returns:
            list
        """
        self._checkForTupleKey('card_faces', num, 'color_indicator')

        return self.scryfallJson['card_faces'][num]['color_indicator']

    def all_parts(self):
        """This this card is closely related to other cards, this property will be an list with it
        
        Returns:
            list
        """
        self._checkForKey('all_parts')

        return self.scryfallJson['all_parts']

    def card_faces(self):
        """If it exists, all parts found on a card's face will be found as an object from this list
        
        Returns:
            list
        """
        self._checkForKey('card_faces')

        return self.scryfallJson['card_faces']

    def watermark(self):
        """The associated watermark of the card, if any
        
        Returns:
            string
        """
        self._checkForKey('watermark')

        return self.scryfallJson['watermark']

    def story_spotlight(self):
        """True if this card is featured in the story
        
        Returns:
            boolean
        """
        self._checkForKey('story_spotlight')

        return self.scryfallJson['story_spotlight']

    def power(self):
        """The power of the creature, if applicable
        
        Returns:
            string
        """
        self._checkForKey('power')

        return self.scryfallJson['power']

    def toughness(self):
        """The toughness of the creature, if applicable
        
        Returns:
            string
        """
        self._checkForKey('toughness')

        return self.scryfallJson['toughness']

    def flavor_text(self):
        """The flavor text of the card, if any
        
        Returns:
            string
        """
        self._checkForKey('flavor_text')

        return self.scryfallJson['flavor_text']

    def arena_id(self):
        """The Arena ID of the card, if any
        
        Returns:
            int: The Arena ID of the card, if any
        """
        self._checkForKey('arena_id')

        return self.scryfallJson['arena_id']

    def lang(self):
        """The language of the card
        
        Returns:
            string
        """
        self._checkForKey('lang')

        return self.scryfallJson['lang']

    def printed_name(self):
        """If the card is in a non-English language, this will be the name as it appears on the card
        
        Returns:
            string
        """
        self._checkForKey('printed_name')

        return self.scryfallJson['printed_name']

    def printed_type_line(self):
        """If the card is in a non-English language, this will be the type line as it appears on the card
        
        Returns:
            string
        """
        self._checkForKey('printed_type_line')

        return self.scryfallJson['printed_type_line']

    def printed_text(self):
        """If the card is in a non-English language, this will be the rules text as it appears on the card
        
        Returns:
            string
        """
        self._checkForKey('printed_text')

        return self.scryfallJson['printed_text']

    def oracle_id(self):
        """A unique ID for this card's oracle text
        
        Returns:
            string
        """
        self._checkForKey('oracle_id')

        return self.scryfallJson['oracle_id']

    def foil(self):
        """True if this printing exists in a foil version
        
        Returns:
            boolean
        """
        self._checkForKey('foil')

        return self.scryfallJson['foil']

    def loyalty(self):
        """This card's loyalty. Some loyalties may be X rather than a number
        
        Returns:
            string
        """
        self._checkForKey('loyalty')

        return self.scryfallJson['loyalty']

    def nonfoil(self):
        """True if this printing does not exist in foil
        
        Returns:
            boolean
        """
        self._checkForKey('nonfoil')

        return self.scryfallJson['nonfoil']

    def oversized(self):
        """True if this printing is an oversized card
        
        Returns:
            boolean
        """
        self._checkForKey('oversized')

        return self.scryfallJson['oversized']