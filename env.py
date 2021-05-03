from tkinter import *
from time import *
import math
import random
import pygame # sound

#사운드 추가 정의
pygame.init()

mySound=pygame.mixer.Sound("Eye of the Storm.mp3")
mySound.set_volume(0.7)
#  mySound.play(-1) # 추가 효과음

clock = pygame.time.Clock()
sound_punch = pygame.mixer.Sound('punch.mp3')
sound_punch.set_volume(0.5)

sound_monster1 = pygame.mixer.Sound('monster.mp3')
sound_monster1.set_volume(0.1)
#추가

class Renderer:
    global playerHP
    
    def __init__(self, state):
        self.main = Tk()
        self.canvas = Canvas(self.main, width=640, height=640)
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
        self.main.bind('q', summon1) #적 1 소환
        self.main.bind('w', summon2)
        self.main.bind('e', summon3)
        self.main.bind('r', summon4)
        self.main.bind('t', summon5)
        self.main.bind('y', summon6)

        self.bg = PhotoImage(file="bg.png")
        self.spritesheet = PhotoImage(file="sprite.png")

        self.img = [] # 스프라이트에서 이미지 뽑아서 저장
        self.imgXY = []
        tmp = []
        tmp.append([35, 50, 140, 100]) # 왼쪽 이동 1
        tmp.append([185, 50, 290, 100]) # 왼쪽 이동 2
        tmp.append([160, 200, 265, 250]) # 오른쪽 이동 1
        tmp.append([310, 200, 415, 250]) # 오른쪽 이동 2
        tmp.append([35, 200, 140, 250]) # 왼쪽 공격1
        tmp.append([10, 350, 115, 400]) # 오른쪽 공격1
        self.imgXY.append(tmp)

        tmp = []
        tmp.append([210, 330, 280, 400]) # 보라적 이동 1 (왼쪽)
        tmp.append([360, 330, 430, 400]) # 보라적 이동 2 (왼쪽)
        tmp.append([620, 330, 690, 400]) # 보라적 이동 3 (오른쪽)
        tmp.append([770, 330, 840, 400]) # 보라적 이동 4 (오른쪽)
        tmp.append([510, 330, 580, 400]) # 보라적 공격1 (왼쪽)
        tmp.append([20, 480, 90, 550]) # 보라적 공격1 (오른쪽)
        tmp.append([210, 480, 280, 550]) # 줄무니적 이동 1 (왼쪽)
        tmp.append([360, 480, 430, 550]) # 줄무니적 이동 2 (왼쪽)
        tmp.append([620, 480, 690, 550]) # 줄무니적 이동 3  (오른쪽)
        tmp.append([770, 480, 840, 550]) # 줄무니적 이동 4  (오른쪽)
        tmp.append([510, 480, 580, 550]) # 줄무늬적 공격 1 (왼쪽)
        tmp.append([20, 630, 90, 700]) # 줄무늬적 공격 1 (오른쪽)
        self.imgXY.append(tmp)
        
        for a in self.imgXY:  #임시 이미지 스프라이트에서 리스트 만들어주기

            newList = []
            for b in a:
                dst = PhotoImage()
                dst.tk.call(dst, 'copy', self.spritesheet, '-from', b[0], b[1], b[2], b[3], '-to', 0, 0)
                newList.append(dst)
            self.img.append(newList)

        self.update(state)
        
    def update(self, state):    #화면 표기를 위한 업데이트
        self.main.update()
        self.canvas.delete("all")   #이전 그린것을 모두 삭제
        self.canvas.create_image(0, 0, anchor=NW, image=self.bg)    #배경 넣고
        for a in state: # 화면에 업데이트 된것 표기(몬스터와 플레이어 캐릭터)
            self.canvas.create_image(a.x - (self.imgXY[a.code][a.img][2] - self.imgXY[a.code][a.img][0]) / 2, a.y - (self.imgXY[a.code][a.img][3] - self.imgXY[a.code][a.img][1]) / 2, anchor=NW, image=self.img[a.code][a.img])
        self.canvas.create_text(50, 50, text="HP: " + str(playerHP)) #HP표기


entitySize = 7
summon = [0, 0, 0, 0, 0, 0, 0]
death = [0, 0, 0, 0, 0, 0, 0]
def summon1(e):
    summon[1] += 1 #보라적 소환
def summon2(e):
    summon[2] += 0 #미구현
def summon3(e):
    summon[3] += 0 #미구현
def summon4(e):
    summon[4] += 0 #미구현
def summon5(e):
    summon[5] += 0 #미구현
def summon6(e):
    summon[6] += 0 #미구현

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
        ret.direction = 0 #보는 방향을 선택하는것, 1이면 오른쪽 0이면 왼쪽
        ret.walkFrame = 0
        ret.stopFrame = 0
    if code == 1:
        ret.type = random.randrange(0, 2)
        ret.direction = 0
        ret.walkFrame = 0
        ret.attackFrame = 0
        ret.hp = 1
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
        global keyL
        global keyR
        global keyU
        global keyD

        self.coolDown -= 1
        if random.random() < 0.02 and self.coolDown <= 0:
            summon[random.randrange(1, 2)] += 1
            self.coolDown = 20

        # 소환
        for i in range(1, 7):
            while summon[i] > 0:
                summon[i] -= 1
                
                y = random.randrange(20, 620)
                x = random.randrange(20, 620)

                r = random.random()
                if r < 0.25:
                    y = 20
                elif r < 0.5:
                    y = 620
                elif r < 0.75:
                    x = 20
                else:
                    x = 620
                self.state.append(createEntity(i, 0, x, y))
        
        for a in self.state:
            if a.code == 0: # 플레이어인 경우

                if a.stopFrame > 0: # 움직일 수 없음
                    if a.stopFrame == 1:
                        a.walkFrame = 0
                        if a.direction == 0:
                            a.img = 1
                        if a.direction == 1:
                            a.img = 3
                    a.stopFrame -= 1
                    continue
                
                if keyZ > 0:
                    keyZ = 0
                    sound_punch.play() #공격 효과음 추가
                    if keyR == True and keyL == False:
                        a.direction = 1
                    if keyL == True and keyR == False:
                        a.direction = 0
                        
                    if a.direction == 0:
                        a.img = 4
                        for b in self.state: # 모든 적에게
                            if b.code == 0:
                                continue
                            dist = (self.state[0].x - b.x) * (self.state[0].x - b.x) + (self.state[0].y - b.y) * (self.state[0].y - b.y) # 거리의 제곱
                            if dist < 4000 and b.x - 5 <= self.state[0].x:
                                b.hp -= 1
                                break
                    else:
                        a.img = 5
                        for b in self.state: # 모든 적에게
                            if b.code == 0:
                                continue
                            dist = (self.state[0].x - b.x) * (self.state[0].x - b.x) + (self.state[0].y - b.y) * (self.state[0].y - b.y) # 거리의 제곱
                            if dist < 4000 and b.x + 5 >= self.state[0].x:
                                b.hp -= 1
                                break
                    a.stopFrame = 3
                    continue

                walk = False
                if keyR == True and keyL == False:
                    walk = True
                    a.direction = 1
                    a.x += 5
                    if a.x > 610:
                        a.x = 610
                    
                if keyL == True and keyR == False:
                    walk = True
                    a.direction = 0
                    a.x -= 5
                    if a.x < 30:
                        a.x = 30

                if keyU == True and keyD == False:
                    walk = True
                    a.y -= 5
                    if a.y < 30:
                        a.y = 30

                if keyD == True and keyU == False:
                    walk = True
                    a.y += 5
                    if a.y > 610:
                        a.y = 610

                if walk:
                    a.walkFrame += 1
                else :
                    a.walkFrame = 0

                if a.direction == 0:
                    if a.walkFrame % 6 < 3:
                        a.img = 0
                    else:
                        a.img = 1
                else:
                    if a.walkFrame % 6 < 3:
                        a.img = 2
                    else:
                        a.img = 3
                    
                    
            if a.code == 1: # 근접공격 entity

                # 죽음
                if a.hp <= 0:
                    self.state.remove(a)
                    death[a.code] += 1
                    continue

                dist = (self.state[0].x - a.x) * (self.state[0].x - a.x) + (self.state[0].y - a.y) * (self.state[0].y - a.y) # 거리의 제곱
                if dist < 1600:
                    # 플레이어와 닿음
                    a.walkFrame = 0
                    a.attackFrame += 1
                   # sound_monster1.play()# 추가 효과음 호출
                   # clock.tick(120)# 추가 효과음 호출
                    if a.direction == 0:
                        if a.attackFrame % 8 < 4:
                            a.img = 4 + a.type * 6
                        else:
                            a.img = 1 + a.type * 6
                    if a.direction == 1:
                        if a.attackFrame % 8 < 4:
                            a.img = 5 + a.type * 6
                        else:
                            a.img = 3 + a.type * 6
                    playerHP -= 1

                else:
                     # 플레이어로 이동
                    a.attackFrame = 0
                    a.walkFrame += 1
                    if self.state[0].x < a.x:
                        a.direction = 0
                        if a.walkFrame % 6 < 3:
                            a.img = 0 + a.type * 6
                        else:
                            a.img = 1 + a.type * 6
                    if self.state[0].x > a.x:
                        a.direction = 1
                        if a.walkFrame % 6 < 3:
                            a.img = 2 + a.type * 6
                        else:
                            a.img = 3 + a.type * 6

                    dx = float(self.state[0].x - a.x)
                    dx /= math.sqrt(dist)
                    dx = int(dx * 4)
                    
                    dy = float(self.state[0].y - a.y)
                    dy /= math.sqrt(dist)
                    dy = int(dy * 4)

                    a.x += dx
                    a.y += dy


            if a.code == 2: # 원거리공격 entity

                # 죽음
                if a.hp <= 0:
                    self.state.remove(a)
                    death[a.code] += 1
                    continue

                dist = (self.state[0].x - a.x) * (self.state[0].x - a.x) + (self.state[0].y - a.y) * (self.state[0].y - a.y) # 거리의 제곱
                if dist < 1600:
                    # 플레이어와 닿음
                    a.walkFrame = 0
                    a.attackFrame += 1
                    # sound_monster1.play()  # 추가 효과음 호출

                    if a.direction == 0:
                        if a.attackFrame % 8 < 4:
                            a.img = 4
                        else:
                            a.img = 0
                    if a.direction == 1:
                        if a.attackFrame % 8 < 4:
                            a.img = 5
                        else:
                            a.img = 2
                    playerHP -= 1
                else:
                    # 플레이어로 이동
                    a.attackFrame = 0
                    a.walkFrame += 1
                    if self.state[0].x < a.x:
                        a.direction = 0
                        if a.walkFrame % 6 < 3:
                            a.img = 0
                        else:
                            a.img = 1
                    if self.state[0].x > a.x:
                        a.direction = 1
                        if a.walkFrame % 6 < 3:
                            a.img = 2
                        else:
                            a.img = 3

                    dx = float(self.state[0].x - a.x)
                    dx /= math.sqrt(dist)
                    dx = int(dx * 4)
                    
                    dy = float(self.state[0].y - a.y)
                    dy /= math.sqrt(dist)
                    dy = int(dy * 4)

                    a.x += dx
                    a.y += dy

        keyZ -= 1
        keyX -= 1

    # 게임 상태 처음으로 초기화
    def clearState(self):
        global playerHP
        playerHP = 100
        self.state = []
        self.state.append(createEntity(0, 0, 320, 320)) # player의 경우 = [entity code, img code, x, y]

        for i in range(entitySize):
            summon[i] = 0
            death[0] = 0
        summon[1] = 1
        
    # state 반환
    def getState(self):
        ret = []
        
        ret.append(self.state[0].x / 800.0)
        ret.append(self.state[0].y / 800.0)

        #ret.append(float(self.state[0].direction)) # 방향 입력으로 넣는가

        obs = [800.0, 800.0, 800.0, 800.0, 800.0, 800.0]
        #obs = [800.0, 800.0]
        
        for a in self.state:
            cy = a.y
            cx = a.x
            if a.code == 1 and a.hp > 0:
                for i in range(0, 6, 2):
                    distNow = (self.state[0].x - cx) * (self.state[0].x - cx) + (self.state[0].y - cy) * (self.state[0].y - cy)
                    distPrev = (self.state[0].x - obs[i]) * (self.state[0].x - obs[i]) + (self.state[0].y - obs[i + 1]) * (self.state[0].y - obs[i + 1])
                    if distNow < distPrev:
                        tx = obs[i]
                        ty = obs[i+1]
                        obs[i] = cx
                        obs[i+1] = cy
                        cx = tx
                        cy = ty

        for i in range(0, 6):
            ret.append(obs[i] / 800.0)

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
        global keyU
        global keyD
        global playerHP

        if action >= 3:
            action += 2

        keyL = False
        keyR = False
        keyU = False
        keyD = False
        keyZ = 0
        if action == 0: # stop
            pass
        if action == 1: # left
            keyL = True
        if action == 2: # right
            keyR = True
        if action == 3: # left attack
            keyL = True
            keyZ = 1
        if action == 4: # right attack
            keyR = True
            keyZ = 1
        if action == 5:
            keyU = True
        if action == 6:
            keyD = True

        cHP = playerHP
        self.update()

        if self.state[0].stopFrame > 0:
            action = 0

        reward = 0

        if playerHP < cHP:
            reward -= 1
        if action == 3:
            reward -= 3
        if action == 4:
            reward -= 3
        for i in range(entitySize):
            reward += death[i] * 50
            death[i] = 0

        return self.getState(), reward, False, []
    
        '''
        if playerHP <= 0:
            return self.getState(), reward, True, []
        else :
            return self.getState(), reward, False, []
        '''
    
if __name__ == '__main__':
    Env(True)
