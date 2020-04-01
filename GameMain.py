# This is the main logic and outputs in the game
from GameClass import *

# Welcome introduction of the game
print("Welcome to 31-CARD GAME!!!")
if input("Do You Know The Basic Rules Of This Game(Y/ N):").upper() == "N":
    print("Rules And Objectives of 31 CARD GAME".center(100, "_") + "\n")
    print("""
    The Basic game is played by four players but in this game you can play this game with any number 
    of players How ever the recommended number is four
    You can even play this game with the computer but it will be too easy if you are a pro ; )
    
    This game is played with a single card deck and what our objective is to collect cards in a
    single suit(Clubs, Diamonds, Hearts, Spades) which give the total value of 31,
    
    And here are the values of the cards
    
    A : Ace - 11
    K : King - 10
    Q : Queen - 10
    J : Jack - 10
    Other : Value of the card
    
    In this game we represent,
    H : Heart
    S : Spade
    C : Club
    D : Diamond
    
    each player can keep 3 cards in there hands and they have three lives at the beginning all players
    them self three cards and the what left in the deck is kept on the table and the top card is shown
    When each player playing their hand they they can either take the card shown on the table or they
    can take the top card from the deck and replace a card with you,
    How ever you should keep only 3 cards.
    
    If a player is satisfied with the value of card they have they can 'Knock'
    when he does every other player get a chance to get a card in either way mention above after all
    other players got their chance,
        1. The person who has the lowest cards will lose a life
        2. If the person who had knock has the lowest value he will lose two lives
        3. If two people have same lowest value then both of them will lose a life 
           
    How ever if a player got 31 in his hand in same suit he will win instantly and it is called blitZ
    
    every player can pass their hand without taking the card on the table or looking at the top card on 
    the deck. But if a player see the top card on the deck  he has to replace it or place it on the top
    of the discard cards on the table.
    
    So This is hove The Game Goes The Program Will Lead You through out the game
    So Enjoy ;-)""")

else:
    print("_"*100)
    print("Lets get started then,")


print("\n"
      "There are few things you need to know\n"
      "You may use following method to enter the names of cards\n"
      " CA : clubs ace\n"
      " h10: heart 10\n"
      " s2: spades 2\n"
      "Case does not matter but please use the method.\n"
      "You should use the given number for the command you wish to take.")

print("_"*100)


# commonly used functions in this code
def common_cmd():
    """ We use this function to take input for following common commands
            1. Exchange the table card
            2. See the deck card
            3. Knock
            4. Pass"""
    while True:
        command = input("What do you want to do(Enter the number of the command): ")
        if command in ["1", "2", "3", "4"]:
            return command
        else:
            print("Invalid input please enter the number of the command")


def max_total(cards_hand):
    """
    This will return the total value of a list of card list
    :param cards_hand: list of cards
    :return: max value of a single suit cards
    """
    card_sum = {"S": 0, "C": 0, "H": 0, "D": 0}
    pack_value = {"A": 11, "K": 10, "Q": 10, "J": 10, "10": 10, "9": 9,
                  "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}

    for card in cards_hand:
        suit = card[0]
        if suit == "S":
            card_sum["S"] += pack_value[card[1:]]
        elif suit == "C":
            card_sum["C"] += pack_value[card[1:]]
        elif suit == "D":
            card_sum["D"] += pack_value[card[1:]]
        elif suit == "H":
            card_sum["H"] += pack_value[card[1:]]

    return max(list(card_sum.values()))


def is_blitz(cards_hand):
    if max_total(cards_hand) == 31:
        return True
    else:
        return False


def rearrange(number_list, start):
    new_list = number_list[number_list.index(start):] + number_list[:number_list.index(start)]
    return new_list


# This is the main game function
def main():
    try:
        # These are some variables that we should assign at the beginning
        num_players = int(input("Enter the number of players you want to play this game: "))
    except ValueError:
        print("Invalid input please enter a valid number of players!!")
        main()
    else:

        if not num_players > 1:
            print("There should be more than 1 players to play this game")
            main()

        blitz = None

        # Player variables are player_n (n in number_players)
        # In this code we take the names from the users and welcome each of them to the game
        for i in range(1, num_players + 1):
            vars()[f"player_{i}"] = Player(input(f"Enter player_{i} name: "))
            print(f"Hello {eval(f'player_{i}').name} you have {eval(f'player_{i}').lives} lives")

            print("*"*50)

        # These are the variables that are needed through out the game
        knock = False
        last_player_knocked = None
        first_knock = False
        result_check = False
        not_in_game = []
        player_list = list(range(1, num_players + 1))
        new_round = True
        table_card = None

        # This is the main game loop
        while True:

            if new_round:
                # This is a object of class player we create in case we needed to manipulate the card deck on the table
                table_ = Player("table")
                # This will create a new card pack because card pack is a class attribute and\
                # it is not an instantaneous attribute
                table_.card_pack = list_permutations(table_.pack_suit, list(table_.pack_value.keys()))

                # This is the loop which distribute card hands to each player
                for i in player_list:
                    eval(f'player_{i}').get_hand()
                    blitz = is_blitz(eval(f'player_{i}').hand)

                table_card = table_.see_deck_card()

                new_round = False

            # This is the loop for each player which player has to take decisions
            for player in player_list:

                # This is the condition for having a blitz at the very beginning\
                # when there is a blitz no other players will
                # get chance to do anything so we passing this loop by this selection
                if blitz:
                    continue

                # This is the code to skip below steps if the player is no longer in the game
                if player in not_in_game:
                    continue

                current_player = eval(f"player_{player}")  # We created this variable because it is easy to use

                # This is the code where player get chance to see his hand and card on the table at the moment
                print(f"{current_player.name} is playing: \n")
                print(f"Your Hand: {' '.join(current_player.hand)}")
                print(f"Table Card: {table_card}")
                if knock:
                    print(f"{eval(f'player_{player_list[last_player_knocked]}').name} has knocked!!!")
                print("""
                    1. Exchange the table card
                    2. See the deck card
                    3. Knock
                    4. Pass""")

                user_command = common_cmd()  # we are taking the user command from a function
                next_player = False

                # This is a loop to make user input correct secondary command after above command
                # Because we have to keep the user asking for input until he insert the correct input
                while not next_player:

                    # This code will execute if the command is 1
                    # After taking this option taking an another option is acceptable
                    if user_command == "1":
                        # in case we decided to chose another option
                        print("Enter 'X' if you want to chose another option")
                        ex_card = input("Enter the card you want to exchange: ").upper()  # card we want to exchange

                        # This code will execute if the user need to take another option
                        if ex_card == "X":
                            print("*"*50)
                            user_command = common_cmd()

                        # This what we accept from the user
                        # In this code it will replace the card on the table with an user said card in his hand
                        elif ex_card in current_player.hand:
                            current_player.get_card(table_card, ex_card)
                            table_card = ex_card  # card we discarded goes to the table
                            print(f'Your hand is: {" ".join(current_player.hand)}')
                            print("_" * 100 + "\n")

                            # we hve rearrange our hand so we need to check for blitz
                            blitz = is_blitz(current_player.hand)

                            break

                        # If user enter anything that is not his hand card this will be executed
                        else:
                            print("Invalid Card in your hand")
                            print("*" * 50)

                    # This is the second option that user can take
                    # After taking this option user can't try other options like before
                    # This the command to take a card from the deck
                    elif user_command == "2":
                        deck_card = current_player.see_deck_card()  # this is the card we took from the deck
                        print("-"*50)
                        print("""
                    1. Exchange with card in hand
                    2. Pass""")

                        # This loop is created to get the correct inputs from user to above commands
                        while True:
                            print(f'Your hand is: {" ".join(current_player.hand)}')
                            print(f"The card is :{deck_card}")
                            user_command_2 = input("Enter the Command: ")

                            # This is what we accept from the user
                            if user_command_2 in ["1", "2"]:

                                # This loop come because after we take this decision we can change it later
                                # We use this loop to handle that kinds of situation
                                while True:

                                    # This code will execute if user chose to replace a card in his hand
                                    if user_command_2 == "1":
                                        print("Enter 'X' if you want to chose another option")
                                        # ex_card: card we are going to discard
                                        ex_card = input("Enter the card you want to exchange: ").upper()

                                        # This is the code to remove the card from the hand if it is available in hand
                                        # After this condition next player can play
                                        if ex_card in current_player.hand:
                                            current_player.get_card(deck_card, ex_card)
                                            table_card = ex_card
                                            print(f'Your hand is: {" ".join(current_player.hand)}')
                                            print("_" * 100 + "\n")

                                            blitz = is_blitz(current_player.hand)

                                            next_player = True
                                            break

                                        elif ex_card == "X":
                                            print("*"*50)
                                            break

                                        else:
                                            print("Please enter a valid card")
                                            print("*"*50)

                                    # This is the code if the player chose to pass the hand by \
                                    # placing the card on the table
                                    elif user_command_2 == "2":
                                        table_card = deck_card
                                        print("_" * 100 + "\n")
                                        ex_card = "Passed"  # we use this variable to get away from the loop
                                        next_player = True
                                        break

                            else:
                                print("invalid command, please enter a valid command number")
                                print("*"*50)
                                continue

                            # This is the condition we created to check whether this player no need to be in this loop
                            # And he had a taken an action correctly
                            if ex_card == table_card or ex_card == "Passed":
                                break

                    # This is the code to if the player decided to knock
                    elif user_command == "3" and not knock:
                        knock = True
                        next_player = True
                        print("_" * 100 + "\n")

                    # This is the code to pass if player decided to pass
                    elif user_command == "4":
                        print(f'Your hand is: {" ".join(current_player.hand)}')
                        next_player = True
                        print("_" * 100 + "\n")

                    # If this loop is going on a knocked situation
                    # This code is created to display other players that they can't knock again
                    elif knock:
                        print("A player has already knocked you can't knock now")
                        user_command = common_cmd()

                # This selection was created to find out that the knock loop have gone correctly
                if knock:
                    # At the beginning first_knock was false
                    # and it is being True once this selection get executed
                    # Once it has been executed and get True for first_knock this selection will be always be false
                    if not first_knock:
                        # Here we are storing the number of the player who knocked
                        last_player_knocked = player_list.index(player)
                        first_knock = True

                    # This selection get passed if after knock the exact player before the knocked player has
                    # got his chance and it will break from the loop for each player
                    # After this become true we can who looses
                    if player_list[player_list.index(player)] == player_list[last_player_knocked - 1]:
                        result_check = True  # this variables will be need to check the result
                        knock = False  # because after this knock should be changed
                        first_knock = False
                        break

            # This will pass if now it is time to check the results
            if result_check:
                # Because we don't need to check the results as soon as other members finish there rounds
                result_check = False
                new_round = True
                # First we have to inform whther players that there was a blitz
                if blitz:
                    print("One Player got a blitz")
                print("_" * 100 + "\n")

                # This is the lowest value can be get for each suit
                lowest_result = 31
                loosing_player_list = []

                # This is the loop for check who got the lowest max suit value from all the players
                for i in range(1, num_players + 1):
                    # This is the code to skip below steps if the player is no longer in the game
                    if i in not_in_game:
                        continue

                    # If the current i th player has the lower value this selection get passed
                    if lowest_result > max_total(eval(f"player_{i}").hand):
                        lowest_result = max_total(eval(f"player_{i}").hand)  # New lowest value
                        loosing_player_list = [i]

                    # If we have multiple players who have same lowest value we are storing all of them in a list
                    elif lowest_result == max_total(eval(f"player_{i}").hand):
                        loosing_player_list.append(i)

                # if the all player is a losing player then it is a draw
                if len(loosing_player_list) == len(player_list):
                    print("It is a Draw, Let's Go another round")
                    continue

                # This is the loop for reduce life of each of losers and let them know
                for loser in loosing_player_list:
                    # This is the condition for last two players get the same value of card hands
                    # Because it is a draw this round it is need to be play again

                    looser_index = player_list.index(loser)

                    print(f"{eval(f'player_{loser}').name} You lost this round")
                    eval(f'player_{loser}').lives -= 1

                    # This is the code to kick a player who lost all his lives from the game
                    if eval(f'player_{loser}').lives < 1:
                        print(f"{eval(f'player_{loser}').name} You have loosen the game")
                        not_in_game.append(loser)
                        player_list.remove(loser)
                        if looser_index == player_list.index(player_list[-1]):
                            player_list = rearrange(player_list, player_list[0])

                        else:
                            player_list = rearrange(player_list, player_list[looser_index])

                    else:
                        player_list = rearrange(player_list, loser)

                # This is the code to check if there is a winner in the game
                # This means there is only one player left to play
                if len(player_list) == 1:
                    winner = list(set(x for x in range(1, num_players + 1)) - set(not_in_game))[0]
                    print(f"Congratulations {eval(f'player_{winner}').name} You Won The Game!!!")
                    print("_" * 100 + "\n")

                    play_again = input("Do You Want To Play Again[Y/N]: ").upper()

                    if play_again == "Y":
                        main()
                    else:
                        break

                print("*"*50)
                for i in range(1, num_players + 1):
                    # This is the code to skip below steps if the player is no longer in the game
                    if i in not_in_game:
                        continue
                    print(f"{eval(f'player_{i}').name} you have {eval(f'player_{i}').lives} lives left")
                print("_" * 100 + "\n")
                print("_" * 100 + "\n")
                print("\n")


main()
