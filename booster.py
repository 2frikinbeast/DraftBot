from scryfall import get_card


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
                booster_list.append(card[parameter])
            return booster_list

    def add_card(self, card: str or list):
        if type(card) == str:
            self.cards.append(get_card(name=card))
        elif type(card) == list:
            self.cards.append(card)

    def remove_card(self, card: str or list):
        i = 0
        while i < len(self.cards):
            if (type(card) == str and self.cards[i]["name"] == card) or (
                    type(card) == list and self.cards[i] == list):
                del self.cards[i]
                return True
            else:
                i = i + 1


def generate_booster(set_id: str):
    set_id = set_id.upper()
    if set_id == "TEST":
        cards = [get_card("Inspiring Commander", exact_name=True)]
    return BoosterPack(contents=cards)