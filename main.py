from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        x, y = self.land.loadLand("land.txt")
        self.hero = Hero((x // 2, y // 2, 2), self.land)
        base.camLens.setFov(90)

        self.accept('escape', self.exit_game)
         
        start_x, start_y = x // 2, y // 2
        start_z = self.land.findHighestEmpty((start_x, start_y, 0))[2]  

        self.hero = Hero((start_x, start_y, start_z + 1), self.land)  
        base.camLens.setFov(90)

    def exit_game(self):
        print("Вихід з ігри...")
        self.userExit()

game = Game()
game.run()