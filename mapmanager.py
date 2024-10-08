import pickle
class Mapmanager():
    def __init__(self):
        self.model = 'block'
        self.texture = 'block.png'          
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ]
        self.startNew() 

    def startNew(self):
        self.land = render.attachNewNode("Land")

    def getColor(self, z):
        doubled_limit = len(self.colors) * 2  
        if z < doubled_limit:
            index = min(z // 2, len(self.colors) - 1)  
            return self.colors[index]
        else:
            return self.colors[len(self.colors) - 1]

    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture)) 
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)

        self.block.setTag("at", str(position))

        self.block.reparentTo(self.land)

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.strip().split(' ') 
                for z in line:
                    if z.isdigit():  
                        for z0 in range(int(z) + 1):
                            self.addBlock((x, y, z0))
                        x += 1
                y += 1
        return x, y
    
    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z - 1
        for block in self.findBlocks(pos):
                block.removeNode()

    def saveMap(self):

        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:

            pickle.dump(len(blocks), fout)

            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        self.clear()

        with open('my_map.dat', 'rb') as fin:
            
            length = pickle.load(fin)

            for i in range(lenght):
                pos = pickle.load(fin)

                self.addBlock(pos)