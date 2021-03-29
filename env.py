from tkinter import *
from time import *

class Renderer:
    def __init__(self, state):
        self.main = Tk()
        self.canvas = Canvas(self.main, width=500, height=400)
        self.canvas.pack()
        self.main.bind('<Left>', keyLDown)
        self.main.bind('<KeyRelease-Left>', keyLUp)
        self.main.bind('<Right>', keyRDown)
        self.main.bind('<KeyRelease-Right>', keyRUp)
        self.spritesheet = PhotoImage(file="spritesheet.gif")

        self.playerImage = [] # 플레이어의 여러 모습(이미지)를 담음
        self.playerImageXY = []
        self.playerImageXY.append([112, 4, 136, 50]) # left, up, right, down
        # todo: 여기에 플레이어 스프라이트들 좌표 찍기

        for a in self.playerImageXY:
            dst = PhotoImage()
            dst.tk.call(dst, 'copy', self.spritesheet, '-from', a[0], a[1], a[2], a[3], '-to', 0, 0)
            self.playerImage.append(dst)

        self.display(state)
        
    def update(self):
        self.main.update()

    def display(self, state):
        self.canvas.delete("all")
        for a in state:
            if a[0] == 0: # player의 경우
                self.canvas.create_image(a[2], a[3] - (self.playerImageXY[a[1]][3] - self.playerImageXY[a[1]][1]) / 2, anchor=NW, image=self.playerImage[a[1]])

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

class Env:
    def __init__(self, manual=False):

        self.render = False
        self.clearState() # 상태 초기화
        
        if manual:
            self.render = Renderer(self.state)

            while True:
                if keyL == True: # 왼쪽 키가 눌려짐
                    self.state[0][2] += -4 # 플레이어 좌표 왼쪽으로
                if keyR == True:
                    self.state[0][2] += 4
                self.display()
                sleep(0.03)

    # 화면 표시
    def display(self):
        if self.render == False:
            self.render = Renderer(self.state)
        self.render.display(self.state)
        self.render.update()

    # 게임 상태 처음으로 초기화
    def clearState(self):
        self.state = []
        self.state.append([0, 0, 250, 350]) # player의 경우

    # 한 단계 진행할 때
    def step(self, action):
        pass
    
if __name__ == '__main__':
    Env(True)
