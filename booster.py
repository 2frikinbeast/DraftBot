from scryfall import get_card, Card


class BoosterPack:
    def __init__(self, contents: list):
        self.cards = contents

    def get_cards(self, parameter: str = None):
        if parameter is None:
            return self.cards
        else:
            parameter = parameter.lower()
            booster_list = []
            for card in self.cards:
                booster_list.append(card.get_info()[parameter])
            return booster_list

    def add_card(self, card: Card):
        self.cards.append(Card)

    def remove_card(self, index: int):
        del self.cards[index]


def generate_booster(set_id: str):
    set_id = set_id.upper()
    if set_id == "TEST":
        cards = [get_card("Inspiring Commander", exact_name=True)]
    return BoosterPack(contents=cards)