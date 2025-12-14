## UI 클래스 및 함수들
from tkinter import *
import PIL.Image
import PIL.ImageTk
from container import *
from player import player
from container import canvas
from enemy import *

gameover_text = None
PILgameover_img = PIL.Image.open(f"{img_path}/ui/gameover.png")
PILgameover_img = PILgameover_img.resize((1280, 720), PIL.Image.NEAREST)
PILgameover_img = PIL.ImageTk.PhotoImage(PILgameover_img)

def show_gameover():
    global gameover_text, gameover_img
    if gameover_text is None:
        gameover_text = canvas.create_text(
            640, 360,  # 화면 중앙 (해상도에 맞게 조정)
            text="G A M E   O V E R",
            font=("온글잎 의연체", 80, "bold"),
            fill="red"
        )
        gameover_img = canvas.create_image(0, 0, image=PILgameover_img, anchor=NW)
        canvas.tag_raise(gameover_img)
        canvas.tag_raise(gameover_text)

        for e in Enemy.enemy_list:
            e.health = -1
            if e.__class__.__name__ == "Boss":
                Boss.boss_health = -10

        for b in Bullet.bullet_list:
            b.destroy_self()


gameclear_text = None
PILgameclear_img = PIL.Image.open(f"{img_path}/ui/gameover.png")

def show_gameclear():
    global gameclear_text, gameclear_img
    if gameclear_text is None:
        gameclear_text = canvas.create_text(
            640, 360,  # 화면 중앙 (해상도에 맞게 조정)
            text="G A M E   C L E A R",
            font=("온글잎 의연체", 80, "bold"),
            fill="Yellow"
        )

        canvas.tag_raise(gameclear_text)




class GameUI():
    HP_container = None
    text_M = None
    def __init__(self, player):
        self.dash_cd = player.dash_cd

        # UI 이미지 로드 및 초기화
        '''H:체력, EH:빈체력, D:대쉬 쿨 타임, M:돈(자금우 열매)'''
        
        self.raw_H1 = PIL.Image.open(f"{img_path}ui/life1.png")
        self.re_H1 = self.raw_H1.resize((38,38), PIL.Image.BILINEAR)
        self.tk_H1 = PIL.ImageTk.PhotoImage(self.re_H1)
        self.raw_H2 = PIL.Image.open(f"{img_path}ui/life2.png")
        self.re_H2 = self.raw_H2.resize((38,38), PIL.Image.BILINEAR)
        self.tk_H2 = PIL.ImageTk.PhotoImage(self.re_H2)

        self.raw_EH1 = PIL.Image.open(f"{img_path}ui/nolife1.png")
        self.re_EH1 = self.raw_EH1.resize((38,38), PIL.Image.BILINEAR)
        self.tk_EH1 = PIL.ImageTk.PhotoImage(self.re_EH1)
        self.raw_EH2 = PIL.Image.open(f"{img_path}ui/nolife2.png")
        self.re_EH2 = self.raw_EH2.resize((38,38), PIL.Image.BILINEAR)
        self.tk_EH2 = PIL.ImageTk.PhotoImage(self.re_EH2)


        GameUI.HP_container = []
        for i in range(player.maxhealth): # 최대 체력만큼 빈 이미지 칸 생성
            if i < 5:
                HP_img = canvas.create_image(20 + i * 50, 25, image=None, anchor=NW, tag = "UI")
            else:
                i -= 5
                HP_img = canvas.create_image(20 + i * 50, 70 , image=None, anchor=NW, tag = "UI")
            GameUI.HP_container.append(HP_img)

    def update_ui(self): # UI 이미지 업데이트

        for i in range(player.maxhealth):
            if i < 5:
                canvas.itemconfig(GameUI.HP_container[i], image=self.tk_EH1)
            else:
                canvas.itemconfig(GameUI.HP_container[i], image=self.tk_EH2)

        for i in range(player.health):
            if i < 5:
                canvas.itemconfig(GameUI.HP_container[i], image=self.tk_H1)
            else:
                canvas.itemconfig(GameUI.HP_container[i], image=self.tk_H2)

       
        root.after(100, self.update_ui)


game_ui = GameUI(player)