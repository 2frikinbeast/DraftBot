import requests
import json
from PIL import Image

SCRYFALL_API = "https://api.scryfall.com"


def api_get(url: str, response_type: str = None, query: dict = None):
    valid_response_types = ["content", "text", "json"]
    if query is None:
        response = requests.get(url)
    else:
        response = requests.get(url, params=query)
    if response_type is None or response_type in valid_response_types:
        if response_type == "content":
            return response.content
        elif response_type == "text":
            return response.text
        elif response_type == "json":
            return response.json
        else:
            return response
    else:
        raise ValueError("api_get: response_type must be one of %r." % valid_response_types)


class UnrefinedSearch(Exception):
    """Multiple cards were returned from your search because your search was not specific enough."""
    pass


class Card:
    def __init__(self, info: dict):
        self.info = info

    def get_info(self):
        return self.info

    def get_param(self, param: str):
        return self.info[param]


def get_card(name: str, exact_name: bool = False):
    name = name.lower().replace(" ", "+")
    if exact_name:
        response = api_get(url=SCRYFALL_API + "/cards/named?exact=" + name, response_type="text")
    else:
        response = api_get(url=SCRYFALL_API + "/cards/named?fuzzy=" + name, response_type="text")
        if json.loads(response)["object"] == "error":
            raise UnrefinedSearch
    return Card(info=json.loads(response))


def get_card_image(card: Card, return_url: bool = False, image_type: str = "png",
                   front_face: bool = True):
    image_type = image_type.replace(" ", "_")
    valid_image_types = ["png", "border_crop", "art_crop", "large", "normal", "small"]
    if image_type not in valid_image_types:
        raise ValueError("get_card_image: response_type must be one of %r." % valid_image_types)
    else:
        try:
            url = card.get_info()["image_uris"][image_type]
            if return_url:
                return url
            else:
                return Image.open(
                    requests.get(card.get_info()["image_uris"][image_type],
                                 stream=True).raw)
        except KeyError:
            url = card.get_info()["card_faces"][int(not front_face)][
                "image_uris"][image_type]
            if return_url:
                return url
            else:
                return Image.open(
                    requests.get(card.get_info()["card_faces"][int(not front_face)]["image_uris"][image_type],
                                 stream=True).raw)


def get_set_list(set_id: str):
    url = SCRYFALL_API + "/cards/search?q=is%3Abooster+e%3A" + set_id
    card_list = []
    while True:
        raw_list = json.loads(api_get(url, response_type="text"))
        for card_object in raw_list["data"]:
            card = Card(card_object)
            card_list.append(card)
        if raw_list["has_more"]:
            url = raw_list["next_page"]
        else:
            return card_list
