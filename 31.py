import random

def distribute():
    suite_choice = ['spade', 'club', 'heart', 'diamond']
    card_choice = ['ace','king', 'queen','jack','2','3','4','5','6','7','8','9','10']
    distribution = []
    distributed = []
    widow = []
    remaining = [f'{i}:{j}' for i in suite_choice for j in card_choice]
    for j in range(3):  # 3 is constant, number of cards in hand
        k=0
        while k<4:  # 4 is number of players
            suite = random.choice(suite_choice)
            card = random.choice(card_choice)

            if f"{suite}:{card}" not in distributed:
                try:
                    distribution[k].append(f'{suite}:{card}')
                    distributed.append(f'{suite}:{card}')
                except IndexError:
                    # print(j)
                    distribution.append([f'{suite}:{card}'])
                    distributed.append(f'{suite}:{card}')
                k += 1
        if j==2:
            widow = []
            i = 0
            while i < 3:
                card_w = f'{random.choice(suite_choice)}:{random.choice(card_choice)}'
                if card_w not in distributed:
                    widow.append(card_w)
                    i+=1

    now_remaining = [card for card in remaining if card not in distributed and card not in widow]

    return distribution, now_remaining, widow

if __name__ == '__main__':
    distribution, remaining, widow = distribute()
    print(distribution)
    names = []
    for player in range(4):
        print(f"Enter name of player {player+1}:",end="")
        names.append(input())
        print(f'{names[player]} gets these cards:\n{distribution[player]}')
    print(f"And the widow cards are :{widow}")