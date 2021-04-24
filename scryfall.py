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


def get_card(name: str, exact_name: bool = False, return_dict: bool = True):
    name = name.lower().replace(" ", "+")
    if exact_name:
        response = api_get(url=SCRYFALL_API + "/cards/named?fuzzy=" + name, response_type="text")
    else:
        response = api_get(url=SCRYFALL_API + "/cards/named?fuzzy=" + name, response_type="text")
        if json.loads(response)["object"] == "error":
            raise UnrefinedSearch
    if return_dict:
        return json.loads(response)
    else:
        return response


def get_card_image(name: str, exact_name: bool = False, return_url: bool = False, image_type: str = "png",
                   front_face: bool = True):
    """

    :param name: name of card
    :param exact_name: if True, requires the card name to be spelled correctly
    :param return_url: If True, returns the card art as an image url (string), else returns as Image
    :param image_type:
    :param front_face:
    :return: URL string if return_url is True, Image otherwise
    """
    image_type = image_type.replace(" ", "_")
    valid_image_types = ["png", "border_crop", "art_crop", "large", "normal", "small"]
    if image_type not in valid_image_types:
        raise ValueError("get_card_image: response_type must be one of %r." % valid_image_types)
    else:
        try:
            url = get_card(name=name, exact_name=exact_name, return_dict=True)["image_uris"][image_type]
            if return_url:
                return url
            else:
                return Image.open(
                    requests.get(get_card(name=name, exact_name=exact_name, return_dict=True)["image_uris"][image_type],
                                 stream=True).raw)
        except KeyError:
            url = get_card(name=name, exact_name=exact_name, return_dict=True)["card_faces"][int(not front_face)][
                "image_uris"][image_type]
            if return_url:
                return url
            else:
                return Image.open(
                    requests.get(
                        get_card(name=name, exact_name=exact_name, return_dict=True)["card_faces"][int(not front_face)][
                            "image_uris"][image_type],
                        stream=True).raw)
