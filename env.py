import os
from copy import deepcopy
import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from tkinter import *
from time import *
import math
import random
from hyperparameters import *
import pygame  # sound
pygame.init()
#mySound = pygame.mixer.Sound("charselect.ogg")
mySound = pygame.mixer.Sound("Project 2 marioish.mp3")
mySound.set_volume(0.7)
mySound.play(-1)
# mySound.fadeout(1000)
# FPS를 위한 Clock 생성
# player attack
clock = pygame.time.Clock()
sound_punch = pygame.mixer.Sound('jump.mp3')

# monster attack
# clock = pygame.time.Clock()
sound_monster1 = pygame.mixer.Sound('monster.mp3')






class Renderer:
    def __init__(self, state):
        self.main = Tk()
        self.main.title("Escape Ocean")  # title
        self.main.configure(bg='black') # 배경화면 검정색
        self.canvas = Canvas(self.main, width=640, height=480, bd = 0, highlightthickness = 0, bg="black")
        #self.canvas = Canvas(self.main, width=self.w, height=self.h)

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
        self.bg = PhotoImage(file="back.png")
        self.spritesheet = PhotoImage(file="sprite4.png")
        self.main.iconphoto(False, PhotoImage(file="balpanicon.png")) #icon 추가
        #self.main.iconphoto(False, PhotoImage(file="backicon.png")) #icon 추가

        self.fullScreenState = False #전체화면 만들기
        self.main.attributes("-fullscreen", self.fullScreenState)

        self.w, self.h = self.main.winfo_screenwidth(), self.main.winfo_screenheight()
        self.main.geometry("%dx%d" % (self.w, self.h))
        self.main.bind("<F11>", self.toggleFullScreen)
        self.main.bind("<Escape>", self.quitFullScreen)
        button = Button(text="Quit", command=self.main.destroy, bg = "red", fg = "black")
        #button = Button(text="Jump". command)
        button.pack()




        self.img = []  # 스프라이트에서 이미지 뽑아서 저장
        self.imgXY = []
        tmp = []
        tmp.append([35, 50, 140, 100])  # 왼쪽 걷기1
        tmp.append([185, 50, 290, 100])  # 왼쪽 걷기2
        tmp.append([160, 200, 265, 250])  # 오른쪽 걷기1
        tmp.append([310, 200, 415, 250])  # 오른쪽 걷기2
        tmp.append([35, 200, 140, 250])  # 왼쪽 공격1
        tmp.append([10, 350, 115, 400])  # 오른쪽 공격1
        self.imgXY.append(tmp)

        tmp = []
        tmp.append([350, 980, 400, 1030])  # 성게
        self.imgXY.append(tmp)

        tmp = []
        tmp.append([695,885,787,940])  # 0
        tmp.append([661,955,737,1021])  # 1
        tmp.append([754,959,827,1013])  # 2

        self.imgXY.append(tmp)


        for a in self.imgXY:

            newList = []
            for b in a:
                dst = PhotoImage()
                dst.tk.call(dst, 'copy', self.spritesheet, '-from', b[0], b[1], b[2], b[3], '-to', 0, 0)
                newList.append(dst)
            self.img.append(newList)

        self.update(state)

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.main.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.main.attributes("-fullscreen", self.fullScreenState)

    def update(self, state):
        self.main.update()
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=NW, image=self.bg)
        for a in state:  # 표시
            if a.code != 0:
                self.canvas.create_image(a.x - (self.imgXY[a.code][a.img][2] - self.imgXY[a.code][a.img][0]) / 2,
                                         a.y - (self.imgXY[a.code][a.img][3] - self.imgXY[a.code][a.img][1]) / 2,
                                         anchor=NW, image=self.img[a.code][a.img])
        for a in state:
            if a.code == 0:
                self.canvas.create_image(a.x - (self.imgXY[a.code][a.img][2] - self.imgXY[a.code][a.img][0]) / 2,
                                         a.y - (self.imgXY[a.code][a.img][3] - self.imgXY[a.code][a.img][1]) / 2,
                                         anchor=NW, image=self.img[a.code][a.img])



entitySize = 7
summon = [0, 0, 0, 0, 0, 0, 0]
death = [0, 0, 0, 0, 0, 0, 0]


def summon1(e):
    summon[1] += 1


def summon2(e):
    summon[2] += 0


def summon3(e):
    summon[3] += 0


def summon4(e):
    summon[4] += 0


def summon5(e):
    summon[5] += 0


def summon6(e):
    summon[6] += 0


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


class Entity:
    def __init__(self, code, img, x, y):
        self.code = code
        self.img = img
        self.x = x
        self.y = y


def createEntity(code, img, x, y):
    ret = Entity(code, img, x, y)
    if code == 0:
        ret.walkFrame = 0
        ret.jumpFrame = 0
        ret.ySpeed = 0
        ret.jumpLeft = 1
    if code == 1:  # enemy
        ret.hp = 1
    if code == 2:  # platform
        ret.chain = 1
    return ret


class Env:
    def __init__(self, manual=False, option=""):

        self.model = False
        self.actionSize = 2
        self.state = []
        self.renderer = False
        self.option = option
        self.stage = []
        self.x = 0
        self.nextIndex = 0

        if option == "stageBuilder":
            env = Env(False, False)
            inputDim = len(env.reset())
            self.inputDim = inputDim
            outputDim = self.actionSize
            self.outputDim = outputDim

            self.model = Sequential()
            self.model.add(Dense(layerNode, input_dim=inputDim, activation='relu'))
            self.model.add(Dense(layerNode, activation='relu'))
            self.model.add(Dense(layerNode, activation='relu'))
            self.model.add(Dense(outputDim))

            if os.path.isfile("save.h5"):
                print("save.h5 파일이 환경에 로드되었습니다. 스테이지 생성시 agent를 사용합니다.")
                self.model.load_weights("save.h5")
            else:
                print("save.h5 파일이 존재하지 않습니다. 스테이지를 무작위로 생성합니다.")
                self.model = False
        else:
            print("스테이지를 무작위로 생성합니다.")
            self.model = False

        if manual:
            self.buildStage()
            self.renderer = Renderer(self.state)
            while True:
                self.update()
                self.render()
                sleep(0.03)

    def setStage(self, newStage):
        self.stage = deepcopy(newStage)

    # 맵 생성
    def buildStage(self):
        self.stage = []
        playerSpawn = False
        nextPosition = 90

        stageLength = 5000
        process = 0

        tryCount = 1000
        indexArray = []
        positionArray = []
        failLimit = 2
        failCount = []
        unit = 500
        depth = 0

        indexArray.append(0)
        positionArray.append(90)
        failCount.append(0)

        # stage build with model
        if self.model != False:
            while positionArray[depth] < stageLength and tryCount > 0:
                tryCount -= 1

                if depth == 0:
                    positionArray[depth] = 90
                else:
                    positionArray[depth] = positionArray[depth - 1]
                self.stage = self.stage[0:indexArray[depth]]
                # build unit
                while positionArray[depth] < (depth + 1) * unit:
                    dx = int(random.uniform(10, 200))  # * (1.0 - random.random() * random.random()))
                    y = random.randrange(100, 380)
                    n = random.randrange(2, 5)
                    self.stage.append([2, positionArray[depth], y, n])
                    positionArray[depth] += dx + n * 54
                    # positionArray[depth] += dx

                self.state = []
                self.nextIndex = 0
                # 첫 발판 위에 플레이어를 생성
                for a in self.stage:
                    if a[0] == 2:  # code == platform
                        self.state.append(
                            createEntity(0, 2, a[1], a[2] - 48))  # player의 경우 = [entity code, img code, x, y]
                        a[3] = 5  # 첫 발판의 길이는 항상 5
                        break
                self.x = 0

                # print("depth=", depth, len(failCount), len(positionArray), len(indexArray), len(self.state), len(self.stage))
                agentSuccess = 1
                while self.x < positionArray[depth]:

                    '''
                    if self.renderer == False:
                        self.renderer = Renderer(self.state)
                    self.render()
                    sleep(0.03)
                    '''

                    cState = self.getState()
                    cState = np.reshape(cState, [1, self.inputDim])
                    action = np.argmax(self.model(cState)[0])
                    _a, _b, done, _c = self.step(action)
                    if done == True:
                        agentSuccess = 0
                        break

                if agentSuccess == 1:
                    # print("success agent")
                    # agent가 통과
                    depth += 1
                    indexArray.append(len(self.stage))
                    positionArray.append(positionArray[depth - 1])
                    failCount.append(0)
                else:
                    failCount[depth] += 1
                    if failCount[depth] >= failLimit:
                        depth -= 1
                        if depth < 0:
                            depth = 0
                            indexArray[0] = 0
                            positionArray[0] = 90
                        else:
                            indexArray.pop()
                            positionArray.pop()
                            failCount.pop()
                    else:
                        if depth == 0:
                            indexArray[0] = 0
                            positionArray[0] = 90
                        else:
                            positionArray[depth] = positionArray[depth - 1]

                while positionArray[depth] / 500 > process:
                    if process < 10:
                        print("스테이지 생성:", process, "/", stageLength // 500)
                    process += 1

        if positionArray[depth] / 500 > 10:
            print("스테이지 생성: 10 / 10")
        elif process > 0:
            print("agent를 이용한 스테이지 생성에 실패하였습니다. 랜덤 배치를 사용합니다.")

        nextPosition = positionArray[depth]
        # 자동 생성이 실패했다면, 그 이후의 작업은 랜덤으로 생성
        while nextPosition < stageLength:
            dx = int(random.uniform(10, 200) * (1.0 - random.random() * random.random()))
            y = random.randrange(100, 380)
            n = random.randrange(2, 5)
            self.stage.append([2, nextPosition, y, n])
            nextPosition += dx + n * 54

        self.nextIndex = 0  # 다음으로 읽을 Entity
        self.state = []
        self.x = 0

        # 첫 발판 위에 플레이어를 생성
        for a in self.stage:
            if a[0] == 2:  # code == platform
                self.state.append(createEntity(0, 2, a[1], a[2] - 48))  # player의 경우 = [entity code, img code, x, y]
                a[3] = 5  # 첫 발판의 길이는 항상 5
                break

    # 1프레임 마다
    def update(self):
        global keyZ
        global keyX
        global keyL
        global keyR
        global keyU
        global keyD

        self.x += 8
        while self.nextIndex < len(self.stage):
            item = self.stage[self.nextIndex]
            if item[1] < self.x + 640 + 54:  # x위치 고려, 화면 안에 들어온 경우
                if item[0] == 2:  # code == "platform"
                    self.state.append(createEntity(2, 0, item[1] - self.x, item[2]))
                    for i in range(1, item[3] - 1):  # item[3] = platform 길이
                        self.state.append(createEntity(2, 1, item[1] - self.x + i * 54, item[2]))
                    self.state.append(createEntity(2, 2, item[1] - self.x + item[3] * 54 - 54, item[2]))
                self.nextIndex += 1
            else:
                break

        for a in self.state:
            if a.code == 0:  # 플레이어인 경우

                # a.x = 90
                a.jumpLeft = min(a.jumpLeft, 1)

                a.jumpFrame += 1
                a.ySpeed += 0.8
                if a.ySpeed > 0:
                    for b in self.state:
                        if b.code == 2:  # 플랫폼
                            if b.x - 27 <= a.x and a.x <= b.x + 27 and a.y + 48 <= b.y and a.y + 48 + a.ySpeed > b.y:  # 충돌체크
                                # 착지한 경우
                                a.y = b.y - 48
                                a.jumpFrame = 0
                                a.jumpLeft = 2
                                a.ySpeed = 0
                                break

                a.y += a.ySpeed

                if keyU == True:
                    keyU = False
                    if a.jumpLeft > 0:
                        a.ySpeed = -12.0
                        a.jumpLeft -= 1
                        sound_punch.play()  # sound 효과음 호출
                        print("jump.mp3")  # sound 잘 돌아가는지 확인하려고 콘솔에 출력하는 메세지
                clock.tick(60)  # sound 1초에 60번 빈도로 순환

                a.walkFrame += 1
                if a.walkFrame % 8 < 4:
                    a.img = 2
                else:
                    a.img = 3

                # 성게랑
                for b in self.state:
                    if b.code == 1:
                        if abs(a.x - b.x) < 30 and abs(a.y - b.y) < 20:
                            pass

            if a.code == 1:  # 성게
                a.x -= 10
                if a.x < -10:
                    self.state.remove(a)

            if a.code == 2:  # platform
                a.x -= 8
                if a.x < -50:
                    self.state.remove(a)

        keyZ -= 1
        keyX -= 1

    # state 반환
    def getState(self):
        ret = []

        # 점프 잔여 횟수
        ret.append(self.state[0].jumpLeft / 2.0)

        # y, ySpeed
        # -30~480
        y = self.state[0].y + 30
        if y < 0.0:
            y = 0.0
        if y > 510.0:
            y = 510.0
        ret.append(y / 510.0)

        # -16~16
        y = self.state[0].ySpeed + 16.0
        if y < 0.0:
            y = 0.0
        if y > 32.0:
            y = 32.0
        ret.append(y / 32.0)

        '''
        obsLeft = 10
        for a in self.state:
            if a.code == 2:
                if 0.0 < a.x and a.x < 640.0:
                    ret.append(a.x/640.0)
                    ret.append(a.y/480.0)
                    obsLeft -= 1
                    if obsLeft <= 0:
                        break

        while obsLeft > 0:
            ret.append(1.0)
            ret.append(1.0)
            obsLeft -= 1
        '''
        platformLeft = 5
        platformStart = False
        platformX1 = 0
        platformX2 = 0
        platformY = 0
        platformPrev = 0
        for a in self.state:
            if a.code == 2 and a.x > 0:
                if platformStart == True:
                    if platformPrev + 54 == a.x:  # 이어짐
                        platformPrev += 54
                        platformX2 = a.x
                    else:  # 끊김
                        x = platformX1 - 27
                        if x < 0.0:
                            x = 0.0
                        if x > 640.0:
                            x = 640.0
                        ret.append(x / 640.0)
                        x = platformX2 - 27
                        if x < 0.0:
                            x = 0.0
                        if x > 640.0:
                            x = 640.0
                        ret.append(x / 640.0)
                        y = platformY - 48
                        if y < 0.0:
                            y = 0.0
                        if y > 480.0:
                            y = 480.0
                        ret.append(y / 480.0)
                        platformLeft -= 1
                        if platformLeft <= 0:
                            break

                        platformX1 = a.x
                        platformY = a.y
                        platformPrev = a.x
                else:
                    platformStart = True
                    platformX1 = a.x
                    platformY = a.y
                    platformPrev = a.x
            else:
                if platformStart == True:
                    platformStart = False

        # 마지막 platform
        if platformLeft > 0 and platformStart == True:
            x = platformX1 - 27
            if x < 0.0:
                x = 0.0
            if x > 640.0:
                x = 640.0
            ret.append(x / 640.0)
            x = platformX2 - 27
            if x < 0.0:
                x = 0.0
            if x > 640.0:
                x = 640.0
            ret.append(x / 640.0)
            y = platformY - 48
            if y < 0.0:
                y = 0.0
            if y > 480.0:
                y = 480.0
            ret.append(y / 480.0)
            platformLeft -= 1

        while platformLeft > 0:
            ret.append(1.0)
            ret.append(1.0)
            ret.append(1.0)
            platformLeft -= 1

        return ret

    # 게임 초기화 후 state 반환
    def reset(self):
        self.buildStage()
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

        keyL = False
        keyR = False
        keyU = False
        keyD = False
        keyZ = 0

        if action == 0:  # stop
            pass
        if action == 1:  # jump
            keyU = True

        if self.state[0].jumpFrame != 0:
            action = 0

        self.update()
        reward = 1

        if self.state[0].y >= 450:
            return self.getState(), reward, True, []
        else:
            return self.getState(), reward, False, []


if __name__ == '__main__':
    Env(True, "stageBuilder")


