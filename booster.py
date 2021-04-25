import json
import time

from image_manip import grid
from scryfall import get_card, Card, get_set_list, get_card_image, api_get
import random


class BoosterPack:
    def __init__(self, contents: list):
        self.contents = contents

    def get_cards(self):
        return self.contents

    def add_card(self, card: Card):
        self.contents.append(card)

    def remove_card(self, index: int):
        del self.contents[int(index)]

    def gen_image(self, cols: int = 6):
        card_images = []
        for card in self.contents:
            img = get_card_image(card)
            card_images.append(img)
            time.sleep(0.03) #avoid sending API calls too quickly
        return grid(imgs=card_images, cols=cols)


def get_random_card(set_list: list, rarity: str = "any", cards_already_chosen: list = []):
    rarity = rarity.lower()
    valid_rarities = ["common", "uncommon", "rare", "special", "mythic", "bonus", "any"]
    if rarity not in valid_rarities:
        raise ValueError("api_get: rarity must be one of %r." % valid_rarities)
    else:
        while True:
            random_card = random.choice(set_list)
            if random_card.get_param("rarity") == rarity or rarity == "any":
                if random_card not in cards_already_chosen:
                    return random_card


def get_random_basic(set_id: str):
    return Card(json.loads(api_get("https://api.scryfall.com/cards/random?q=is%3Abooster+t%3Abasic+unique%3Aart+e%3A" + set_id.lower(), response_type="text")))


def generate_booster(set_id: str):
    set_id = set_id.lower()
    cards = []
    if set_id == "test":
        cards.append(get_card("Inspiring Commander", exact_name=True))
    else:
        commons = 10
        uncommons = 3
        basics = 1
        if random.randint(1, 8) == 1:
            mythics = 1
            rares = 0
        else:
            mythics = 0
            rares = 1
        if set_id == "stx":
            stx_cards = get_set_list("stx")
            sta_cards = get_set_list("sta", is_booster=False)
            for i in range(commons):
                cards.append(get_random_card(set_list=stx_cards, rarity="common", cards_already_chosen=cards))
            for i in range(uncommons):
                cards.append(get_random_card(set_list=stx_cards, rarity="uncommon", cards_already_chosen=cards))
            for i in range(rares):
                cards.append(get_random_card(set_list=stx_cards, rarity="rare", cards_already_chosen=cards))
            for i in range(mythics):
                cards.append(get_random_card(set_list=stx_cards, rarity="mythic", cards_already_chosen=cards))
            cards.append(get_random_card(set_list=sta_cards, cards_already_chosen=cards))
            return BoosterPack(contents=cards)
        card_list = get_set_list(set_id=set_id)
        for i in range(commons):
            cards.append(get_random_card(set_list=card_list, rarity="common", cards_already_chosen=cards))
        for i in range(uncommons):
            cards.append(get_random_card(set_list=card_list, rarity="uncommon", cards_already_chosen=cards))
        for i in range(rares):
            cards.append(get_random_card(set_list=card_list, rarity="rare", cards_already_chosen=cards))
        for i in range(mythics):
            cards.append(get_random_card(set_list=card_list, rarity="mythic", cards_already_chosen=cards))
        for i in range(basics):
            cards.append(get_random_basic(set_id=set_id))
    return BoosterPack(contents=cards)

test_booster = generate_booster("m21")
test_booster.gen_image().save("booster.png")
