# In This Script all the classes that are needed in game will be created
import random


def list_permutations(list_1, list_2):
    """
    This function is used to generate all the ordered pairs we can generate using two lists which contain strings
    and join values in each ordered pairs
    :param list_1: first list
    :param list_2: second list
    :return: list which contain all the string permutations we can generate from list_1 and list_2 items
    """
    nest_list = []
    for item_1 in list_1:
        for item_2 in list_2:
            nest_list.append("".join(tuple((item_1, item_2))))

    return nest_list


class Player:
    """
    This is the class of a player which are playing the game
    """
    pack_suit = ["H", "C", "S", "D"]
    pack_value = {"A": 11, "K": 10, "Q": 10, "J": 10, "10": 10, "9": 9,
                  "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
    card_pack = list_permutations(pack_suit, list(pack_value.keys()))  # we can create the card pack using
    game_round = True

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.lives = 3

    def get_hand(self):
        """
        This method will chose the player a random 3 cards, THIS IS DONE AT THE BEGINNING OF THE GAME
        :return: players hand
        """
        self.hand = []

        while len(self.hand) != 3:
            rand_card = random.choice(self.card_pack)
            self.hand.append(rand_card)
            self.card_pack.remove(rand_card)

        return self.hand

    def remove_card(self, r_card):
        """
        This will remove a card from players hand if he has more than three cards, when aa card is removed the
        removed card will be placed on the top of the discard cards.
        :param r_card: Name of the card that is needed to be removed
        :return: None
        """
        try:
            if len(self.hand) > 3:
                self.hand.remove(r_card)
            else:
                raise ValueError
        except ValueError:
            print("You entered an Invalid card")
            return False

    def get_card(self, card, old_card):
        """
        This will get the card on the table and player get chance to remove a card from his hand
        :param card: name of the card on the table
        :param old_card: name of the old card that is need to discard
        :return: New hand
        """
        self.hand.append(card)
        self.remove_card(old_card)

    def see_deck_card(self):
        """
        This will see the top card on the deck
        :return: Top card
        """
        top_card = random.choice(self.card_pack)
        self.card_pack.remove(top_card)
        return top_card

    def knock(self):
        """
        after this knock there will be only one chance for other players means this will be the last round
        :return: False for game_round
        """
        self.game_round = False
        return self.game_round

    def lose(self):
        """
        This is a method to reduce a players life when they are lost
        :return: None
        """
        self.lives -= 1


class Dealer(Player):
    """
    This is a class for single AI player in the game
    """

    def __init__(self):
        Player.__init__(self, name="Alex")

    def check_value(self, card_hand):
        card_sum = {"S": 0, "C": 0, "H": 0, "D": 0}

        for card in card_hand:
            suit = card[0]
            if suit == "S":
                card_sum["S"] += self.pack_value[card[1:]]
            elif suit == "C":
                card_sum["C"] += self.pack_value[card[1:]]
            elif suit == "D":
                card_sum["D"] += self.pack_value[card[1:]]
            elif suit == "H":
                card_sum["H"] += self.pack_value[card[1:]]

        return card_sum

    def card_collection(self, card):
        """
        This is a method to find out which three cards are best to take from four cards
        :param card: New card
        :return: best card collection
        """
        hand_copy = self.hand[:]  # This is a copy of hand
        card_details = self.check_value(hand_copy)  # This is the code for checking the values of first collection

        max_value = max(list(card_details.values()))  # This is for maximum value we have from sits
        max_hand = hand_copy[:]  # This is the best hand we have till we replace cards

        # In this loop we are replacing the card with each card in hand and see what as the maximum value of single\
        # suit cards
        for i in range(3):
            hand_copy[i] = card
            card_details = self.check_value(hand_copy)

            # This is the code to reassign max_hand and max_value if we found a collection better than before
            if max_value < max(list(card_details.values())):
                max_hand = hand_copy[:]  # because later when we change hand_copy max_hand should not be changed
                max_value = max(list(card_details.values()))

            hand_copy = self.hand[:]

        return max_hand
