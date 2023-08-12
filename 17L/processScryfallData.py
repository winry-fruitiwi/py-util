import json

scryfallDataPath = 'scryfall.json'

# constant for when LTR jumpstart cards start
ltrCollectorIDCap = 281

cardOracle = {}

with open(scryfallDataPath, 'r', encoding="utf-8") as scryfall:
    scryfallData = json.load(scryfall)

# print all the names of each card within the collector ID cap for the set.
# The collector ID cap is when the cards begin to move out of the boosters and
# become cards in special Magic card boxes. We're not concerned about these
# cards.
for card in scryfallData:
    if int(card["collector_number"]) < ltrCollectorIDCap:
        # cardOracle format:
        # Name ManaCost
        # OracleText
        # Power / Toughness
        # FlavorText

        # however, sometimes the power or toughness does not exist, so
        # we need to account for this. (like in the case of instants and
        # sorceries, although some artifacts or vehicles do have power or
        # toughness)
        # the same goes for flavor text

        # handles absence of flavor text
        try:
            flavor_text = card["flavor_text"]
        except KeyError:
            flavor_text = ""

        # handles absence of power/toughness
        try:
            stats = f'{card["power"]}/{card["toughness"]}'
        except KeyError:
            stats = ""


        cardOracle[card["name"]] = (f'{card["name"]}   {card["mana_cost"]}\n'
                                    f'{card["oracle_text"]}\n'
                                    f'{stats}\n'
                                    f'{flavor_text}\n'
                                    )
