# TODO turn this into a function

import json
from constants import *

scryfallDataPath = 'scryfall.json'

cardOracle = {}
rarityOfCards = {}
cardPNGs = {}


def processScryfallData():
    with open(scryfallDataPath, 'r', encoding="utf-8") as scryfall:
        scryfallData = json.load(scryfall)

    # print all the names of each card within the collector ID cap for the set.
    # the collector ID cap is when the cards begin to move out of the boosters and
    # become cards in special Magic card boxes. We're not concerned about these
    # cards.
    for card in scryfallData:
        # we need to make sure that the collector number is actually an integer.
        # an example where this is not the case is in The List cards.
        isListCard = False

        try:
            int(card["collector_number"])
        except ValueError:
            isListCard = True

        if isListCard or (card["set"] != setCode) or (int(card["collector_number"]) <= collectorIDCap):
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

            try:
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

                cardOracle[card["name"]] = (
                    f'{card["name"]}   {card["mana_cost"]}\n'
                    f'{card["oracle_text"]}\n'
                    f'{stats}\n'
                    f'{flavor_text}\n'
                    )

                rarityOfCards[card["name"]] = card["rarity"]
                cardPNGs[card["name"]] = card["image_uris"]["png"]

            except KeyError:  # this means there are multiple card faces
                cardOracle[card["card_faces"][0]["name"]] = ""
                for face in card["card_faces"]:
                    try:
                        flavor_text = card["flavor_text"]
                    except KeyError:
                        flavor_text = ""

                    # handles absence of power/toughness
                    try:
                        stats = f'{face["power"]}/{face["toughness"]}'
                    except KeyError:
                        stats = ""

                    # this is a hack I came up with to address the fact that
                    # Scryfall names their cards based on both faces rather
                    # than just the front face
                    cardOracle[card["card_faces"][0]["name"]] += (
                        f'{face["name"]}   {face["mana_cost"]}\n'
                        f'{face["oracle_text"]}\n'
                        f'{stats}\n'
                        f'{flavor_text}\n'
                        )

                rarityOfCards[card["card_faces"][0]["name"]] = card["rarity"]

                if "image_uris" in card:
                    cardPNGs[card["card_faces"][0]["name"]] = card["image_uris"]["png"]
                else:
                    cardPNGs[card["card_faces"][0]["name"]] = (card["card_faces"][0]
                                                               ["image_uris"]["png"])

            else:
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

                rarityOfCards[card["name"]] = card["rarity"]

