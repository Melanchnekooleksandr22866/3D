from panda3d.core import Vec3, TransparencyAttrib 
from direct.gui.OnscreenImage import OnscreenImage  
from direct.gui.DirectGui import DirectFrame  

key_switch_camera = 'c'
key_switch_mode = 'z'

key_forward = 's'
key_back = 'w'
key_left = 'd'
key_right = 'a'
key_jump = 'space'
key_down = 'shift'

key_savemap = 'k'
key_loadmap = 'l'

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True  
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setH(180)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.create_crosshair()  # Добавляем прицел
        self.cameraBind()
        self.accept_events()
        self.max_vert_angle = 60

    def create_crosshair(self):
        """Создаём прицел в виде крестика в центре экрана."""
        # Создаем GUI элемент - простой крестик
        self.crosshair = DirectFrame(frameColor=(1, 1, 1, 0),  # Прозрачный фон
                                     frameSize=(-0.01, 0.01, -0.01, 0.01),  # Размеры прицела
                                     pos=(0, 0, 0))  # Позиция по центру экрана
        # Загружаем текстуру для крестика
        self.crosshair_image = OnscreenImage(image='crosshair.png', pos=(0, 0, 0), scale=0.03)
        self.crosshair_image.setTransparency(TransparencyAttrib.MAlpha)  # Устанавливаем прозрачность

    def cameraBind(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        base.camera.lookAt(self.hero)
        self.cameraOn = True

        taskMgr.add(self.mouse_task, "mouse_task")

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def changeMode(self):
        self.mode = not self.mode

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def look_at_block(self):
        """Метод для нахождения блока перед героем в пределах 5 блоков."""
        direction = base.camera.getQuat().getForward()  
        start_pos = self.hero.getPos() + Vec3(0, 0, 1.5)  
        max_distance = 5 

        for i in range(1, max_distance + 1):  
            check_pos = start_pos + direction * i  
            block_pos = (round(check_pos.getX()), round(check_pos.getY()), round(check_pos.getZ())) 
            if not self.land.isEmpty(block_pos):  
                return block_pos

        return None

    def destroy_or_build(self, action):
        """Метод для разрушения или установки блоков в зависимости от действия."""
        block_pos = self.look_at_block()
        if block_pos:
            if action == 'destroy':  
                self.land.delBlock(block_pos)
        else:
            if action == 'build':  
                direction = base.camera.getQuat().getForward()
                build_pos = self.hero.getPos() + direction
                build_pos = (round(build_pos.getX()), round(build_pos.getY()), round(build_pos.getZ()))
                self.land.addBlock(build_pos)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at_block(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at_block(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    def accept_events(self):
        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)

        base.accept(key_jump, self.up)
        base.accept(key_jump + '-repeat', self.up)

        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)

        base.accept('mouse1', lambda: self.destroy_or_build('destroy'))  # Ломать блоки на левую кнопку
        base.accept('mouse3', lambda: self.destroy_or_build('build'))    # Ставить блоки на правую кнопку

        base.accept(key_savemap, self.land.saveMap)
        base.accept(key_loadmap, self.land.loadMap)

    def mouse_task(self, task):
        if base.mouseWatcherNode.hasMouse():

            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()

            hero_heading = self.hero.getH() - (x * 50)
            self.hero.setH(hero_heading)

            cam_pitch = base.camera.getP() - (y * 30)
            cam_pitch = max(-self.max_vert_angle, min(self.max_vert_angle, cam_pitch))
            base.camera.setP(cam_pitch)

            base.win.movePointer(0, int(base.win.getProperties().getXSize() / 2),
                                    int(base.win.getProperties().getYSize() / 2))

        return task.cont
