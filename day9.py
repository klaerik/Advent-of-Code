
class Game():
    def __init__(self, last_marble):
        self.last_marble = last_marble
        self.current_marble = 0
        self.circle = [self.current_marble,]

    def get_index(self, marble=self.current_marble):
        return self.circle.index(marble)
    
    def get_marble(self, index):
        return self.circle[index]
    
    def direction_to_index(direction):
        '''Clockwise is positive, counterclockwise negative'''
        circle_size = len(self.circle)
        current_index = self.get_index()
        

game = Game(1618)
game.get_index()
