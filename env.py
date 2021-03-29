from tkinter import *
from time import *
import random

class Renderer:
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

summon = [0, 0, 0, 0, 0, 0, 0]
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
keyZ = False
keyX = False

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
    keyZ = True

def keyZUp(e):
    global keyZ
    keyZ = False

def keyXDown(e):
    global keyX
    keyX = True

def keyXUp(e):
    global keyX
    keyX = False

class Entity:
    def __init__(self, code, img, x, y, data1, data2):
        self.code = code
        self.img = img
        self.x = x
        self.y = y
        self.data1 = data1
        self.data2 = data2

playerHP = 300
        
class Env:
    def __init__(self, manual=False):

        self.coolDown = 30 # 엔터티 등장 쿨다운
        self.state = []
        self.clearState()
        self.render = Renderer(self.state)
        
        if manual:
            while True:
                self.update()
                sleep(0.03)

    # 1프레임 마다
    def update(self):
        global playerHP

        self.coolDown -= 1
        if random.random() < 0.02 and self.coolDown <= 0:
            summon[random.randrange(1, 3)] += 1
            self.coolDown = 30

        # 소환
        for i in range(1, 7):
            while summon[i] > 0:
                summon[i] -= 1
                if i % 2 == 0:
                    self.state.append(Entity(i, 0, 500, 350, 0, 0))
                else:
                    self.state.append(Entity(i, 0, 0, 350, 0, 0))
        
        for a in self.state:
            if a.code == 0: # 플레이어인 경우

                if keyR == True:
                    a.x += 4
                    a.data1 += 1
                    if a.data1 % 6 < 3:
                        a.img = 4
                    else:
                        a.img = 5
                elif keyL == True:
                    a.x -= 4
                    a.data1 += 1
                    if a.data1 % 6 < 3:
                        a.img = 2
                    else:
                        a.img = 3
                    
            if a.code == 1: # 오른쪽으로 이동하는 적

                # 플레이어와 닿음
                if abs(self.state[0].x - a.x) < 12:
                    playerHP -= 1 # 플레이어 HP 감소
                else:
                    a.x += 4 # x좌표 오른쪽으로
                    a.data1 += 1 # 프레임 +1
                
                # 플레이어와 x거리 150 미만
                if self.state[0].x - a.x < 150:
                    a.data2 = 1

                # 이미지 처리
                if a.data2 == 0:
                    if a.data1 % 6 < 3:
                        a.img = 0
                    else :
                        a.img = 1
                else:
                    if a.data1 % 6 < 3:
                        a.img = 2
                    else :
                        a.img = 3

            if a.code == 2: # 왼쪽으로 이동하는 적

                # 플레이어와 닿음
                if abs(self.state[0].x - a.x) < 12:
                    playerHP -= 1 # 플레이어 HP 감소
                else:
                    a.x -= 4 # x좌표 왼쪽으로
                    a.data1 += 1 # 프레임 +1
                
                # 플레이어와 x거리 150 미만
                if a.x - self.state[0].x < 150:
                    a.data2 = 1

                # 이미지 처리
                if a.data2 == 0:
                    if a.data1 % 6 < 3:
                        a.img = 0
                    else :
                        a.img = 1
                else:
                    if a.data1 % 6 < 3:
                        a.img = 2
                    else :
                        a.img = 3

                
        # 화면 표시
        self.render.update(self.state)

    # 게임 상태 처음으로 초기화
    def clearState(self):
        self.state = []
        self.state.append(Entity(0, 3, 250, 350, 0, 0)) # player의 경우 = [entity code, img code, x, y, data1, data2]

    # 한 단계 진행할 때
    def step(self, action):
        pass
    
if __name__ == '__main__':
    Env(True)
