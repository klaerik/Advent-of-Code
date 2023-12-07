import y2023.shared as shared
from string import ascii_uppercase
from collections import Counter

## Data
raw = shared.read_file("day07.txt")
test = shared.read_file("day07-test.txt")

## Functions
cards = ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2")
card_sort = dict(zip(cards, ascii_uppercase))

joker_cards = ("A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J")
joker_sort = dict(zip(joker_cards, ascii_uppercase))


def parse_hands(raw: list[str]) -> list[tuple]:
    out = []
    for row in raw:
        hand, bid = row.split(" ")
        bid = int(bid)
        out.append((hand, bid))
    return out


def convert_jokers(hand: str) -> str:
    if "J" not in hand:
        return hand
    counts = Counter(hand).most_common()
    best_card = counts[0][0]
    if best_card == "J" and len(counts) > 1:
        best_card = counts[1][0]
    if len(counts) == 5:
        for card in joker_cards:
            if card in hand:
                best_card = card
                break
    return hand.replace("J", best_card)


def get_hand_type(hand: str, jokers_wild: bool = False) -> str:
    if jokers_wild:
        hand = convert_jokers(hand)
    counts = [v for _, v in Counter(hand).most_common()]
    # Five of a kind
    if len(counts) == 1:
        return "A"
    # Four of a kind
    elif len(counts) == 2 and counts == [4, 1]:
        return "B"
    # Full house
    elif len(counts) == 2 and counts == [3, 2]:
        return "C"
    # Three of a kind
    elif len(counts) == 3 and counts == [3, 1, 1]:
        return "D"
    # Two pair
    elif len(counts) == 3 and counts == [2, 2, 1]:
        return "E"
    # One pair
    elif len(counts) == 4:
        return "F"
    else:
        return "G"


def sort_hand(hand: str, jokers_wild=False) -> str:
    if jokers_wild:
        return "".join([joker_sort[x] for x in hand])
    else:
        return "".join([card_sort[x] for x in hand])


def convert_hand(hand: str, jokers_wild=False) -> str:
    hand_type = get_hand_type(hand, jokers_wild)
    hand_sort = sort_hand(hand, jokers_wild)
    return hand_type + hand_sort


def solve(test, jokers_wild=False):
    hands = parse_hands(test)
    for i in range(len(hands)):
        hand, bid = hands[i]
        hand = convert_hand(hand, jokers_wild)
        hands[i] = (hand, bid)
    hands.sort(reverse=True)
    score = 0
    for rank, hand_bid in enumerate(hands, start=1):
        _, bid = hand_bid
        score += bid * rank
    return score


## Testing
assert convert_jokers("T55J5") == "T5555"
assert convert_jokers("KTJJT") == "KTTTT"
assert convert_jokers("QQQJA") == "QQQQA"
assert convert_hand("QQQQ2", True) > convert_hand("JKKK2", True)


assert solve(test) == 6440
assert solve(test, jokers_wild=True) == 5905


## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve(raw, jokers_wild=True)}")
