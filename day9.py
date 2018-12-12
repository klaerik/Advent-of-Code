
class Game():
    def __init__(self, player_count, final_marble):
        self.final_marble = final_marble
        self.current_marble = 0
        self.last_marble = self.current_marble
        self.circle = [self.current_marble,]
        self.players = [0 for x in range(player_count)]
        self.game_over = False

    def get_index(self, marble=None):
        if marble is None:
            marble = self.current_marble
        return self.circle.index(marble)
    
    def get_marble(self, index):
        return self.circle[index]
    
    def direction_to_index(self, direction):
        '''Clockwise is positive, counterclockwise negative'''
        circle_size = len(self.circle)
        current_index = self.get_index()
        target_index = current_index + direction
        while target_index > circle_size:
            target_index -= circle_size
        return target_index
    
    def play(self):
        score = 0
        play_marble = self.last_marble + 1
        self.last_marble = play_marble
        if play_marble % 23 == 0:
            score += play_marble
            remove_idx = self.direction_to_index(-7)
            self.current_marble = self.get_marble(self.direction_to_index(-6))
            score += self.circle.pop(remove_idx)
            #print(f"Score! - {score}")
        else:
            play_idx = self.direction_to_index(2)
            self.circle.insert(play_idx, play_marble)
            self.current_marble = play_marble
        return score
    
    def turn(self):
        for player_idx in range(len(self.players)):
            if self.last_marble == self.final_marble:
                max_score = max(self.players)
                print(f"Game over! Max score was {max_score}")
                self.game_over = True
                break
            else:
                self.players[player_idx] += self.play()
        



def play_game(players, final_marble):
    game = Game(players, final_marble)
    while game.game_over is False:
        game.turn()
    return max(game.players)


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
