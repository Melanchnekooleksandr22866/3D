import pickle

class Mapmanager():
    def __init__(self):
        self.model = 'block'
        self.texture = 'block.png'  # Це не використовуватиметься для текстури за замовчуванням
        self.textures = [
            'bedrock.png',  # Текстура для бедроку
            'stoyn.png',    # Текстура для каменю
            'dirt.png',     # Текстура для землі
            'grass.png'    # Текстура для трави
        ]
        self.startNew()

    def startNew(self):
        self.land = render.attachNewNode("Land")

    def getTexture(self, z):
        if z == 0:
            return self.textures[0]  # Бедрок
        elif 1 <= z <= 7:
            return self.textures[1]  # Стоун
        elif z == 8:
            return self.textures[2]  # Дірт
        elif z == 9:
            return self.textures[3]  # Грасс
        else:
            return None  # Якщо блок поза межами визначених рівнів

    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        z = int(position[2])
        self.texture = self.getTexture(z)

        if self.texture:  # Якщо текстура визначена
            self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)

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
        return not blocks

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
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)
