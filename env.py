from tkinter import *
from time import *
import random

class Renderer:
    global playerHP
    
    def __init__(self, state):
        self.main = Tk()
        self.canvas = Canvas(self.main, width=500, height=400)
        self.canvas.pack()
        self.main.bind('<Left>', keyLDown)
        self.main.bind('<KeyRelease-Left>', keyLUp)
        self.main.bind('<Right>', keyRDown)
        self.main.bind('<KeyRelease-Right>', keyRUp)
        self.main.bind('<Up>', keyUDown)
        self.main.bind('<KeyRelease-Up>', keyUUp)
        self.main.bind('<Down>', keyDDown)
        self.main.bind('<KeyRelease-Down>', keyDUp)
        self.main.bind('z', keyZDown)
        self.main.bind('x', keyXDown)
        self.main.bind('q', summon1)
        self.main.bind('w', summon2)
        self.main.bind('e', summon3)
        self.main.bind('r', summon4)
        self.main.bind('t', summon5)
        self.main.bind('y', summon6)
        
        self.spritesheet = PhotoImage(file="spritesheet.gif")

        self.img = [] # 스프라이트에서 이미지 뽑아서 저장
        self.imgXY = []
        tmp = []
        tmp.append([112, 4, 136, 48]) # left, up, right, down
        tmp.append([137, 4, 161, 48]) # left, up, right, down
        tmp.append([164, 4, 182, 48]) # left, up, right, down
        tmp.append([184, 4, 207, 51]) # left, up, right, down
        tmp.append([212, 4, 233, 51]) # left, up, right, down
        tmp.append([234, 4, 251, 48]) # left, up, right, down
        tmp.append([255, 4, 279, 48]) # left, up, right, down
        tmp.append([281, 4, 304, 48]) # left, up, right, down

        tmp.append([172, 50, 214, 92]) # left, up, right, down
        tmp.append([214, 50, 252, 92]) # left, up, right, down
        self.imgXY.append(tmp)

        tmp = []
        tmp.append([211, 345, 229, 387]) # left, up, right, down
        tmp.append([230, 345, 250, 387]) # left, up, right, down
        tmp.append([252, 345, 272, 387]) # left, up, right, down
        tmp.append([272, 345, 287, 387]) # left, up, right, down
        tmp.append([287, 345, 307, 387]) # left, up, right, down
        tmp.append([307, 345, 338, 387]) # left, up, right, down
        self.imgXY.append(tmp)
        
        tmp = []
        tmp.append([188, 345, 207, 387]) # left, up, right, down
        tmp.append([168, 345, 188, 387]) # left, up, right, down
        tmp.append([148, 345, 168, 387]) # left, up, right, down
        tmp.append([130, 345, 148, 387]) # left, up, right, down
        tmp.append([110, 345, 130, 387]) # left, up, right, down
        tmp.append([80, 345, 110, 387]) # left, up, right, down
        self.imgXY.append(tmp)
        
        for a in self.imgXY:

            newList = []
            for b in a:
                dst = PhotoImage()
                dst.tk.call(dst, 'copy', self.spritesheet, '-from', b[0], b[1], b[2], b[3], '-to', 0, 0)
                newList.append(dst)
            self.img.append(newList)

        self.update(state)
        
    def update(self, state):
        self.main.update()
        self.canvas.delete("all")
        for a in state: # 표시
            self.canvas.create_image(a.x, a.y - (self.imgXY[a.code][a.img][3] - self.imgXY[a.code][a.img][1]) / 2, anchor=NW, image=self.img[a.code][a.img])
        self.canvas.create_text(50, 50, text="HP: " + str(playerHP))

entitySize = 7
summon = [0, 1, 0, 0, 0, 0, 0]
death = [0, 0, 0, 0, 0, 0, 0]
def summon1(e):
    summon[1] += 1
def summon2(e):
    summon[2] += 1
def summon3(e):
    summon[3] += 1
def summon4(e):
    summon[4] += 1
def summon5(e):
    summon[5] += 1
def summon6(e):
    summon[6] += 1

# 키보드 눌렸는지 여부
keyL = False
keyR = False
keyU = False
keyD = False
keyZ = 0
keyX = 0

def keyLDown(e):
    global keyL
    keyL = True

def keyLUp(e):
    global keyL
    keyL = False

def keyRDown(e):
    global keyR
    keyR = True

def keyRUp(e):
    global keyR
    keyR = False

def keyUDown(e):
    global keyU
    keyU = True

def keyUUp(e):
    global keyU
    keyU = False

def keyDDown(e):
    global keyD
    keyD = True

def keyDUp(e):
    global keyD
    keyD = False

def keyZDown(e):
    global keyZ
    keyZ = 3

def keyXDown(e):
    global keyX
    keyX = 3

playerHP = 100

class Entity:
    def __init__(self, code, img, x, y):
        self.code = code
        self.img = img
        self.x = x
        self.y = y

def createEntity(code, img, x, y):
    ret = Entity(code, img, x, y)
    if code == 0:
        ret.direction = 0
        ret.walkFrame = 0
        ret.stopFrame = 0
    if code == 1:
        ret.walkFrame = 0
        ret.handsup = 0
        ret.hp = 1
        ret.deadFrame = 0
    if code == 2:
        ret.walkFrame = 0
        ret.handsup = 0
        ret.hp = 1
        ret.deadFrame = 0
    return ret

class Env:
    def __init__(self, manual=False):

        self.coolDown = 10 # 엔터티 등장 쿨다운
        self.state = []
        self.clearState()
        self.renderer = False
        
        if manual:
            self.renderer = Renderer(self.state)
            while True:
                self.update()
                self.render()
                sleep(0.03)

    # 1프레임 마다
    def update(self):
        global playerHP
        global keyZ
        global keyX

        self.coolDown -= 1
        if random.random() < 0.02 and self.coolDown <= 0:
            summon[random.randrange(1, 3)] += 1
            self.coolDown = 20

        # 소환
        for i in range(1, 7):
            while summon[i] > 0:
                summon[i] -= 1
                if i % 2 == 0:
                    self.state.append(createEntity(i, 0, 500, 350))
                else:
                    self.state.append(createEntity(i, 0, 0, 350))
        
        for a in self.state:
            if a.code == 0: # 플레이어인 경우

                if a.stopFrame > 0:
                    if a.stopFrame == 1:
                        a.walkFrame = 0
                        if a.direction == 0:
                            a.img = 3
                        else:
                            a.img = 4
                    a.stopFrame -= 1
                    continue
                
                if keyZ > 0:
                    keyZ = 0
                    if keyR == True:
                        a.direction = 1
                    elif keyL == True:
                        a.direction = 0
                    if a.direction == 0:
                        a.img = 8
                        for b in self.state:
                            if b.code == 0:
                                continue
                            if self.state[0].x - 25 <= b.x and b.x <= self.state[0].x:
                                b.hp -= 1
                    else:
                        a.img = 9
                        for b in self.state:
                            if b.code == 0:
                                continue
                            if self.state[0].x <= b.x and b.x <= self.state[0].x + 25:
                                b.hp -= 1
                    a.stopFrame = 3
                    continue
                if keyR == True:
                    if a.direction == 0:
                        a.direction = 1
                        a.walkFrame = 0
                    a.x += 4
                    if a.x > 470:
                        a.x = 470
                    a.walkFrame += 1
                    if a.walkFrame % 6 < 3:
                        a.img = 4
                    else:
                        a.img = 5
                elif keyL == True:
                    if a.direction == 1:
                        a.direction = 0
                        a.walkFrame = 0
                    a.x -= 4
                    if a.x < 30:
                        a.x = 30
                    a.walkFrame += 1
                    if a.walkFrame % 6 < 3:
                        a.img = 3
                    else:
                        a.img = 2
                else:
                    a.walkFrame = 0
                    if a.direction == 0:
                        a.img = 3
                    else :
                        a.img = 4
                    
            if a.code == 1: # 오른쪽으로 이동하는 적

                # 죽음
                if a.hp <= 0:
                    a.img = 5
                    a.x -= 3
                    a.deadFrame += 1
                    if a.deadFrame > 10:
                        self.state.remove(a)
                        death[a.code] += 1
                    continue
                
                # 플레이어와 닿음
                if abs(self.state[0].x - a.x) < 8:
                    playerHP -= 1 # 플레이어 HP 감소
                    a.x = min(a.x, self.state[0].x - 4)
                else:
                    a.x += 4 # x좌표 오른쪽으로
                    a.walkFrame += 1 # 프레임 +1
                
                # 플레이어와 x거리 150 미만
                if self.state[0].x - a.x < 150:
                    a.handsup = 1

                # 이미지 처리
                if a.handsup == 0:
                    if a.walkFrame % 6 < 3:
                        a.img = 0
                    else :
                        a.img = 1
                else:
                    if a.walkFrame % 6 < 3:
                        a.img = 2
                    else :
                        a.img = 3

            if a.code == 2: # 왼쪽으로 이동하는 적

                # 죽음
                if a.hp <= 0:
                    a.img = 5
                    a.x += 3
                    a.deadFrame += 1
                    if a.deadFrame > 10:
                        self.state.remove(a)
                        death[a.code] += 1
                    continue
                
                # 플레이어와 닿음
                if abs(self.state[0].x - a.x) < 8:
                    playerHP -= 1 # 플레이어 HP 감소
                    a.x = max(a.x, self.state[0].x + 4)
                else:
                    a.x -= 4 # x좌표 왼쪽으로
                    a.walkFrame += 1 # 프레임 +1
                
                # 플레이어와 x거리 150 미만
                if a.x - self.state[0].x < 150:
                    a.handsup = 1

                # 이미지 처리
                if a.handsup == 0:
                    if a.walkFrame % 6 < 3:
                        a.img = 0
                    else :
                        a.img = 1
                else:
                    if a.walkFrame % 6 < 3:
                        a.img = 2
                    else :
                        a.img = 3

        keyZ -= 1
        keyX -= 1

    # 게임 상태 처음으로 초기화
    def clearState(self):
        global playerHP
        playerHP = 100
        self.state = []
        self.state.append(createEntity(0, 3, 250, 350)) # player의 경우 = [entity code, img code, x, y]

        for i in range(entitySize):
            summon[i] = 0
            death[0] = 0
        summon[1] = 1
        
    # state 반환
    def getState(self):
        ret = []

        ret.append(self.state[0].x / 600.0)
        
        val = -100
        for a in self.state:
            if a.code == 1 and a.hp > 0:
                val = max(val, a.x)
                
        ret.append((val + 100) / 600.0)
            
        val = 600
        for a in self.state:
            if a.code == 2 and a.hp > 0:
                val = min(val, a.x)
        ret.append(val / 600.0)

        return ret

    # 게임 초기화 후 state 반환
    def reset(self):
        self.clearState()
        return self.getState()

    # 화면 표시
    def render(self):
        if self.renderer == False:
            self.renderer = Renderer(self.state)
        self.renderer.update(self.state)

    # 한 단계 진행할 때
    def step(self, action):
        global keyL
        global keyR
        global keyZ
        global playerHP

        keyL = False
        keyR = False
        keyZ = 0
        if action == 0: # stop
            pass
        if action == 1: # left
            keyL = True
        if action == 2: # right
            keyR = True
        if action == 3: # left kick
            keyL = True
            keyZ = 1
        if action == 4: # right kick
            keyR = True
            keyZ = 1

        cHP = playerHP
        self.update()
        while self.state[0].stopFrame > 0:
            if self.renderer != False:
                sleep(0.03)
                self.render()
            self.update()

        reward = 1
        if playerHP < cHP:
            reward -= 1
        if action == 3:
            reward -= 1
        if action == 4:
            reward -= 1
        for i in range(entitySize):
            reward += death[i] * 3
            death[i] = 0

        if playerHP <= 0:
            return self.getState(), reward, True, []
        else :
            return self.getState(), reward, False, []    
    
if __name__ == '__main__':
    Env(True)
