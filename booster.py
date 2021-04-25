from scryfall import get_card, Card


class BoosterPack:
    def __init__(self, contents: list):
        self.contents = contents

    def get_cards(self):
        return self.contents

    def add_card(self, card: Card):
        self.contents.append(card)

    def remove_card(self, index: int):
        del self.contents[int(index)]


def generate_booster(set_id: str):
    set_id = set_id.upper()
    if set_id == "TEST":
        cards = [get_card("Inspiring Commander", exact_name=True)]
    return BoosterPack(contents=cards)
