def recipe_score(puzzle, improve_after=None, stop_pattern=None):
    scoreboard = [int(x) for x in str(puzzle)]
    solution_length = 10
    elves = [0, 1]
    solved = False
    while not solved:
        elf0, elf1 = scoreboard[elves[0]], scoreboard[elves[1]]
        scoreboard.extend([int(x) for x in str(elf0 + elf1)])
        elves = [(elves[0] + ((elf0 + 1) % len(scoreboard))) % len(scoreboard), (elves[1] + ((elf1 + 1) % len(scoreboard))) % len(scoreboard)]
        #print(elves, scoreboard)
        if improve_after is not None:
            target_length = improve_after + solution_length
            solved = len(scoreboard) >= target_length
            if solved:
                solution = ''.join(str(x) for x in scoreboard[improve_after: target_length])
        else:
            last = ''.join(str(x) for x in scoreboard[-solution_length:])
            solved = stop_pattern in last
            if solved:
                stop_idx = last.index(stop_pattern)
                solution = len(scoreboard) - len(last) + stop_idx
    print(f"Found: {solution}")
    return solution


assert recipe_score(37, 9) == '5158916779'
assert recipe_score(37, 5) == '0124515891'
assert recipe_score(37, 18) == '9251071085'
assert recipe_score(37, 2018) == '5941429882'

solution = recipe_score(37, 894501)
print(f"Solution 1: {solution}")


assert recipe_score(37, stop_pattern='51589') == 9
assert recipe_score(37, stop_pattern='01245') == 5
assert recipe_score(37, stop_pattern='92510') == 18
assert recipe_score(37, stop_pattern='59414') == 2018

solution2 = recipe_score(37, stop_pattern='894501')
print(f"Solution 2: {solution2}")
