from collections import deque

def play_game(players, final_marble):
    circle = deque([0]) # Rotate: - clockwise, + counterclockwise
    scores = deque([0 for i in range(players)])
    current_marble = 0
    
    while current_marble < final_marble:
        score = 0
        current_marble += 1
        if current_marble % 23 == 0:
            circle.rotate(7)
            removed = circle.pop()
            score = removed + current_marble
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(current_marble)

        #print(current_marble, circle)            
        scores.rotate(-1)
        scores[-1] += score
    
    high_score = max(scores)
    print(f"Game finished! High score: {high_score}")
    return high_score

assert play_game(9, 25) == 32
assert play_game(10, 1618) == 8317
assert play_game(13, 7999) == 146373
assert play_game(17, 1104) == 2764
assert play_game(21, 6111) == 54718
assert play_game(30, 5807) == 37305

solution = play_game(403, 71920)
print(f"Solution 1: Max score was {solution} points")

solution2 = play_game(403, 71920 * 100)
print(f"Solution 2: Max score was {solution2} points")
