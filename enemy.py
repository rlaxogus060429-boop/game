## 적 클래스 및 함수들
from tkinter import *
import PIL.Image
import PIL.ImageTk
from math import radians, cos, sin
from hitboxes import Hitbox, Atk_Hitbox
from container import *
from collision import Collision
from random import random
from bullet import Bullet
import bossHPUI
import gameUI

class Enemy:
    enemy_list = []
    def __init__(self, name, x, y, target):
        self.trace = False # 추적 상태 유무
        self.target = target

        self.atk_hitboxes = []
        self.atk_hitbox = None
     
        self.name = name # 적 아이디
        self.x = x
        self.y = y
        self.dx = self.dy = 0

        self.damaged = False # 피격 상태
        self.image = canvas.create_image(self.x, self.y, image=None, anchor=NW, tags = "enemy")

        self.frame_count = 0

        self.state = [0,0,0,1,0]
        ''' 
            [0] == 정지유무(0-정지, 1-움직임), [1] = 왼오(0-왼, 1-오), [2] == 공격(0-안함, 1-공격함)
            [3] == 공중(0-공중아님, 1-공중임), [4] == 공격이미지 보정(0-보정 전, 1-보정 후)
        '''

        Enemy.enemy_list.append(self)

    def enemy_img_update(self):
        pass

    def update_enemy_position(self):
        pass
    def set_position(self, set_x, set_y):
        self.x = set_x
        self.y = set_y
        canvas.coords(self.image, set_x, set_y)
        try:
            self.hitbox.coords(self.x + (self.img_size/2 - self.hitsize_x/2), self.y + (self.img_size - self.hitsize_y) - self.up_y)
                    
            if self.type == 'A':
                self.trackbox.coords((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2), self.y + (self.img_size - self.hitsize_y) - (self.tsize_y - self.hitsize_y) - self.up_y)
                self.atk_range.coords(self.x + (self.img_size/2 - (self.hitsize_x * 1.5)/2), self.y + (self.img_size - self.hitsize_y*1.2) - self.up_y)
            elif self.type == 'B':
                self.trackbox.coords((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2), (self.y + (self.img_size/2 - self.hitsize_y/2)) - (self.tsize_y/2 - self.hitsize_y/2))
                self.atk_range.coords(self.x + (self.img_size/2 - (self.hitsize_x*12)/2), self.y + (self.hitsize_y - (self.hitsize_y*12)/2))
        except:
            pass

    def reset_damaged_state(self):
        if self.FC == self.OUCH_FC:
            self.FC = self.backFC
        self.damaged = False

    def take_damage(self, attacker):
        if self.damaged==False:
            self.damaged = True # 피격 됨
            self.health -= attacker.damage
            root.after(100, self.reset_damaged_state)  # 피격 상태 초기화

            if self.target.state[1] == 0: # 피격 시 넉백
                self.x += -self.hitsize_x * 0.6
            elif self.target.state[1] == 1:
                self.x += self.hitsize_x * 0.6

    def layer_up(self):
         canvas.tag_raise(self.image)

    def isDead(self):
        if self.health <= 0:
            canvas.delete(self.image)
            # 히트박스 사각형이 있으면 삭제
            try:
                if self.hitbox.hitbox_rect is not None:
                    canvas.delete(self.hitbox.hitbox_rect)
                    self.hitbox.hitbox_rect = None
                if self.trackbox.hitbox_rect is not None:
                    canvas.delete(self.trackbox.hitbox_rect)
                    self.trackbox.hitbox_rect = None
                if self.atk_range.hitbox_rect is not None:
                    canvas.delete(self.atk_range.hitbox_rect)
                    self.atk_range.hitbox_rect = None
            except:
                pass

            # 리스트에서 제거
            if self in Enemy.enemy_list:
                Enemy.enemy_list.remove(self)


class Monster(Enemy):
    def __init__(self, name, x, y, target):
        super().__init__(name, x, y, target)

        self.FC = 0
        self.backFC = 0
        self.OUCH_FC = 4

        if self.name=="WalkingSprout":
            self.fc1 = 6 # idle 프레임 수 - 1
            self.fc2 = 7 # walk 프레임 수 - 1
            self.fc3 = 4 # attack 프레임 수 - 1
            self.velocity = 3  # 적 이동 속도
            self.health = 5 # 적 체력
            self.atk_timer = 20 # 적 재공격에 필요한 시간
            self.atk_cd = self.atk_timer

            self.hastrace_ani = None # 추적 상태 전용 애니메이션 소지 판별용

            self.type = 'A' # A: 근접, B: 원거리
            self.img_size = 85
            self.hitsize_x = 45
            self.hitsize_y = 45
            self.up_y = 0 # 이미지 y축 보정용 변수

        if self.name=="FlyingSprout":
            self.fc1 = 6
            self.fc2 = 6
            self.fc3 = 6
            self.velocity = 2
            self.health = 4
            self.atk_timer = 30
            self.atk_cd = self.atk_timer

            self.type = 'B'
            self.img_size = 85
            self.hitsize_x = 45
            self.hitsize_y = 45
            self.up_y = 12
        
        # 트랙박스, 공격 가능 범위: 근거리 형
        if self.type == 'A':
            self.tsize_x = self.hitsize_x * 7
            self.tsize_y = self.hitsize_y * 1.5
            self.trackbox = Hitbox((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2), self.y + (self.img_size - self.hitsize_y) - (self.tsize_y - self.hitsize_y) - self.up_y, self.tsize_x, self.tsize_y)
            self.atk_range = Hitbox(self.x + (self.img_size/2 - (self.hitsize_x*1.5)/2), self.y + (self.img_size - self.hitsize_y*1.2) - self.up_y, self.hitsize_x * 1.5, self.hitsize_y*1.2)

        # 트랙박스, 공격 가능 범위: 원거리 형
        elif self.type == 'B':
            self.tsize_x = self.hitsize_x * 10
            self.tsize_y = self.hitsize_y * 10
            self.trackbox = Hitbox((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2), (self.y + (self.img_size/2 - self.hitsize_y/2)) - (self.tsize_y/2 - self.hitsize_y/2), self.tsize_x, self.tsize_y)
            self.atk_range = Hitbox(self.x + (self.img_size/2 - (self.hitsize_x*12)/2), self.y + (self.hitsize_y - (self.hitsize_y*12)/2), self.hitsize_x * 12, self.hitsize_y*12)

        # 히트박스
        self.hitbox = Hitbox(self.x + (self.img_size/2 - self.hitsize_x/2), self.y + (self.img_size - self.hitsize_y) - self.up_y, self.hitsize_x, self.hitsize_y)
        
        # 랜덤 행동용 카운트 초기화
        self.move_count = 0
        self.ratios = [random() for _ in range(2)]
        self.s = sum(self.ratios)
        self.numbers_1 = [int(200 * r / self.s) for r in self.ratios] # 멈춤 비율
        self.ratios = [random() for _ in range(2)]
        self.s = sum(self.ratios)
        self.numbers_2 = [int(400 * r / self.s) for r in self.ratios] # 이동 비율
        if sum(self.numbers_1) != 200:
            self.numbers_1[1] = 200 - self.numbers_1[0]
        if sum(self.numbers_2) != 400:
            self.numbers_2[1] = 400 - self.numbers_2[0]
        
        if self.type == 'B':
            self.ratios = [random() for _ in range(2)]
            self.s = sum(self.ratios)
            self.numbers_3 = [int(100 * r / self.s) for r in self.ratios] # 상하 이동 비율

        
        # 이미지 저장용 배열
        self.tk_image_list_R = [[],[],[],[],[]]
        self.tk_image_list_L = [[],[],[],[],[]]

        for i in range(self.fc1): # idle 이미지 로드
            self.raw_image = PIL.Image.open(f"{img_path}enemy_Monster/{self.name}/idle_{i}.png")
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
            self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_R[0].append(self.tk_image)
            self.tk_image_list_L[0].append(self.tk_image_flip)

        for i in range(self.fc2): # walk 이미지 로드
            self.raw_image = PIL.Image.open(f"{img_path}enemy_Monster/{self.name}/walk_{i}.png")
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
            self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_R[1].append(self.tk_image)
            self.tk_image_list_L[1].append(self.tk_image_flip)

            try: # trace 이미지 로드 시도
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Monster/{self.name}/trace_{i}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[2].append(self.tk_image)
                self.tk_image_list_L[2].append(self.tk_image_flip)
            except:
                continue

        for i in range(self.fc3): # attack 이미지 로드
            self.raw_image = PIL.Image.open(f"{img_path}enemy_Monster/{self.name}/atk_{i}.png")
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
            self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_R[3].append(self.tk_image)
            self.tk_image_list_L[3].append(self.tk_image_flip)

        # attacked 이미지 로드
        self.raw_image = PIL.Image.open(f"{img_path}enemy_Monster/{self.name}/atked.png")
        self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
        self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
        self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
        self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
        self.tk_image_list_R[4].append(self.tk_image)
        self.tk_image_list_L[4].append(self.tk_image_flip)


    def enemy_img_update(self):
        if self.health > 0:
            if self.damaged == False:
                if self.state[0] == 0:# idle 애니메이션
                    self.FC = 0
                    self.fc = int(self.frame_count % self.fc1)

                else:
                    if self.state[2] == 0: # 걷기
                        self.FC = 1
                        self.fc = int(self.frame_count % self.fc2)
                        if hasattr(self,'hastrace_ani'): # 추적 애니메이션 소지 확인
                            if self.trace == True:
                                self.FC = 2                        
                            
                    if self.state[2] == 1: # 공격
                        if self.state[4] == 0: # 공격시 애니메이션 프레임 보정용 스위치
                            self.frame_count = 0
                            self.state[4] = 1

                        self.FC = 3
                        self.fc = int(self.frame_count % self.fc3)
                        if self.name == 'WalkingSprout': # enemy 종 마다 공격 타이밍
                            if 1<= self.fc <=2: # 1 ~ 2 프레임에 공격 박스 생성
                                self.atk_cd = 0
                                self.do_atk()
                            if self.fc > 2: # 3 프레임에 공격 종료
                                self.state[2] = 0 # 공격 상태 해제
                                self.state[0] = 0 # 정지 상태 설정
                                self.state[4] = 0 # 공격시 애니메이션 프레임 보정용 스위치 해제

                        elif self.name == 'FlyingSprout':
                            if self.fc == 5:
                                self.atk_cd = 0
                                self.do_atk()
                            if self.fc > 4:
                                self.state[2] = 0
                                self.state[4] = 0

            else: # 피격시 애니메이션
                if self.backFC != self.OUCH_FC:
                    self.backFC = self.FC
                self.FC = 4
                self.fc = 0
        if self.backFC == self.OUCH_FC:
            if self.state[0] == 0:# idle 애니메이션
                self.backFC = 0
            if self.state[0] == 1 and self.state[2] == 0:
                self.backFC = 1
                if hasattr(self,'hastrace_ani'): # 추적 애니메이션 소지 확인
                    if self.trace == True:
                        self.backFC = 2
            if self.state[0] == 1 and self.state[2] == 1:
                self.backFC = 3
           
        # 캔버스에 있는 이미지를 새로운 이미지로 업데이트
        if self.state[1] == 0:
            canvas.itemconfig(self.image, image=self.tk_image_list_L[self.FC][self.fc])
        elif self.state[1] == 1:
            canvas.itemconfig(self.image, image=self.tk_image_list_R[self.FC][self.fc])

        self.frame_count += 0.3
        if self.state[2] == 0:
            self.atk_cd += 0.3

    def update_enemy_position(self):
        if self.state[0] == 0 and self.state[2] == 1:
            self.state[2] = 0

        if self.state[2] == 0:
            # 추적 시 행동방식
            if self.trace == True:

                self.state[0] = 1

                if self.type == 'A' and self.atk_cd > self.atk_timer:
                    if self.x > self.target.x:
                        self.state[1] = 0
                        self.dx = -self.velocity * 1.3
                    elif self.x < self.target.x:
                        self.state[1] = 1
                        self.dx = self.velocity * 1.3
                    else:
                        self.dx = 0
                elif self.type =='A' and self.atk_cd <= self.atk_timer:
                    self.state[0] = 0

                if self.type == 'B':
                    if ((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2)) - 1 > self.target.x + self.target.size//2:
                        self.state[1] = 0
                        self.dx = -self.velocity
                    elif ((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2) + self.tsize_x) + 1 < self.target.x + self.target.size//2:
                        self.state[1] = 1
                        self.dx = self.velocity
                    elif ((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2)) < self.target.x + self.target.size//2 < ((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2) + self.tsize_x//2) + 1:
                        self.state[1] = 0
                        self.dx = self.velocity * 0.9
                    elif ((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2) + self.tsize_x//2) < self.target.x + self.target.size//2 < ((self.x + (self.img_size/2 - self.hitsize_x/2)) - (self.tsize_x/2 - self.hitsize_x/2) + self.tsize_x) - 1:
                        self.state[1] = 1
                        self.dx = - self.velocity * 0.9
                    else:
                        self.dx = 0
                        
                    if ((self.y + (self.img_size/2 - self.hitsize_y/2)) - (self.tsize_y/2 - self.hitsize_y/2)) - 1 > self.target.y + self.target.size:
                        self.dy = -self.velocity
                    elif ((self.y + (self.img_size/2 - self.hitsize_y/2)) - (self.tsize_y/2 - self.hitsize_y/2) + self.tsize_y) + 1 < self.target.y + self.target.size:
                        self.dy = self.velocity
                    elif ((self.y + (self.img_size/2 - self.hitsize_y/2)) - (self.tsize_y/2 - self.hitsize_y/2)) < self.target.y + self.target.size < ((self.y + (self.img_size/2 - self.hitsize_y/2)) - (self.tsize_y/2 - self.hitsize_y/2) + self.tsize_y//2) + 1:
                        self.dy = self.velocity * 0.9
                    elif ((self.y + (self.img_size/2 - self.hitsize_y/2)) - (self.tsize_y/2 - self.hitsize_y/2) + self.tsize_y//2) < self.target.y + self.target.size < ((self.y + (self.img_size/2 - self.hitsize_y/2)) - (self.tsize_y/2 - self.hitsize_y/2) + self.tsize_y) - 1:
                        self.dy = -self.velocity * 0.9
                    else:
                        self.dy = 0

            # 비추적 시 행동방식
            elif self.trace == False:
                self.move_count+=1
            
                if self.move_count <= self.numbers_1[0]:
                    self.state[0] = 0
                    self.dx = 0
                    if self.type == 'B':
                        self.dy = 0

                elif self.move_count <= self.numbers_1[0] + self.numbers_2[0]:
                    self.state[0] = 1
                    self.state[1] = 0 
                    self.dx = -self.velocity
                    if self.type == 'B':
                        if self.numbers_3[0] <= 45:
                            self.dy = -self.velocity * 0.8
                        elif self.numbers_3[0] <= 85:
                            self.dy = (0 if (self.y > 720 - self.hitsize_y*3) else self.velocity * 0.8)
                        else:
                            self.dy = 0

                elif self.move_count <= self.numbers_1[0] + self.numbers_2[0] + self.numbers_1[1]:
                    self.state[0] = 0
                    self.dx = 0
                    if self.type == 'B':
                        self.dy = 0

                elif self.move_count <= self.numbers_1[0] + self.numbers_2[0] + self.numbers_1[1] + self.numbers_2[1]:
                    self.state[0] = 1
                    self.state[1] = 1
                    self.dx = self.velocity
                    if self.type == 'B':
                        if self.numbers_3[1] <= 45:
                            self.dy = -self.velocity * 0.8
                        elif self.numbers_3[1] <= 85:
                            self.dy = (0 if (self.y > 720 - self.hitsize_y*3) else self.velocity * 0.8)
                        else:
                            self.dy = 0

                else: # 랜덤 행동용 카운트
                    self.move_count = 0
                    self.ratios = [random() for _ in range(2)]
                    self.s = sum(self.ratios)
                    self.numbers_1 = [int(200 * r / self.s) for r in self.ratios]
                    self.ratios = [random() for _ in range(2)]
                    self.s = sum(self.ratios)
                    self.numbers_2 = [int(400 * r / self.s) for r in self.ratios]
                    if sum(self.numbers_1) != 200:
                        self.numbers_1[1] = 200 - self.numbers_1[0]
                    if sum(self.numbers_2) != 400:
                        self.numbers_2[1] = 400 - self.numbers_2[0]

                    if self.type == 'B':
                        self.ratios = [random() for _ in range(2)]
                        self.s = sum(self.ratios)
                        self.numbers_3 = [int(100 * r / self.s) for r in self.ratios]
        else:
            self.dx = 0
        
        # 중력 적용
        if self.type == 'A':
            if self.state[3] == 1:
                self.dy += g
            else:
                self.dy = 0

        self.x += self.dx
        self.y += self.dy

        canvas.move(self.image, self.dx, self.dy)
        self.hitbox.move(self.dx, self.dy)
        self.trackbox.move(self.dx, self.dy)
        self.atk_range.move(self.dx, self.dy)

        
        if self.health > 0 : # 디버그용
            #self.hitbox.draw_hitbox(color="blue")
            #self.trackbox.draw_hitbox(color="yellow")
            #self.atk_range.draw_hitbox(color="red")
            pass

    def do_atk(self):
        if self.type == 'A':
            if 1 < self.fc < 3:
                Collision.attack_hitbox_collision(5, self.atk_hitboxes, self.target)
                if self.state[2] == 1 and self.fc >= 2:
                    self.atk_hitbox = Atk_Hitbox(self.x + (self.img_size/2 - (self.hitsize_x*1.5)/2), self.y + (self.img_size - self.hitsize_y*1.2), self.hitsize_x * 1.5, self.hitsize_y*1.2, damage=1)
                    self.atk_hitboxes.append(self.atk_hitbox)
                    
                    #self.atk_hitbox.draw_hitbox() # 디버그용

        if self.type == 'B':
            if self.fc > 4:
                self.bullet = Bullet(self.x+(self.img_size//2 - self.hitsize_x//2), self.y+self.hitsize_y, 32, owner=self, target=self.target, damage=1, speed=4, istracking=True)

        def remove_atk_box(): # 공격 히트박스 제거
            if self.atk_hitbox is not None:
                canvas.delete(self.atk_hitbox.hitbox_rect)
                self.atk_hitbox.hitbox_rect = None
            if self.atk_hitboxes is not None and self.atk_hitbox in self.atk_hitboxes:
                self.atk_hitboxes.remove(self.atk_hitbox)

        root.after(20, remove_atk_box)


class Boss(Enemy):
    boss_health = 0
    boss1_main_xy = [1280//2,720] ###
    fight_start = False
    hp_bar_created = False
    def __init__(self, name, x, y, target):
        super().__init__(name, x, y, target)

        self.AC = 0
        self.FC = 0
        self.backFC = 0
        self.OUCH_FC = 5

        # 개별 설정
        if self.name == 'Boss1_main':

            self.y_to_start = y

            self.type = 'Boss1'
            self.health = 25
            self.velocity = 2

            self.img_size = 265
            self.hitsize_x = 165
            self.hitsize_y = 165
            self.up_y = 48
            self.radius = self.img_size

            self.atk_timer = 50
            self.atk_cd = 0

            self.fc1 = 16
            self.fc2 = 16
            self.fc_a1 = 11
            self.fc_a2 = 12
            self.fc_a3 = 62

            self.check = -1
            self.circle = 20

        elif self.name == 'Boss1_hand_R':
            self.type = 'Boss1'
            self.health = 15
            self.velocity = 3

            self.img_size = 250
            self.hitsize_x = 180
            self.hitsize_y = 180
            self.up_y = 0
            self.radius = self.img_size

            self.atk_timer = 60
            self.atk_cd = 0

            self.fc1 = 1
            self.fc2 = 1
            self.fc_a1 = 36
            self.fc_a2 = 1
            self.fc_a3 = 1

        elif self.name == 'Boss1_hand_L':
            self.type = 'Boss1'
            self.health = 15
            self.velocity = 3

            self.img_size = 250
            self.hitsize_x = 180
            self.hitsize_y = 180
            self.up_y = 0
            self.radius = self.img_size

            self.atk_timer = 90
            self.atk_cd = 0

            self.fc1 = 1
            self.fc2 = 1
            self.fc_a1 = 36
            self.fc_a2 = 1
            self.fc_a3 = 1

        Boss.boss_health += self.health # 보스 토탈 체력 설정

        # 박스 생성
        if self.type == 'A':
            self.atk_range = Hitbox(self.x + (self.img_size/2 - (self.hitsize_x*1.5)/2), self.y + (self.img_size - self.hitsize_y*1.2) - self.up_y, self.hitsize_x * 1.5, self.hitsize_y*1.2)

        elif self.type == 'B':
            self.atk_range = Hitbox(self.x + (self.img_size/2 - (self.hitsize_x*15)/2), self.y + (self.hitsize_y - (self.hitsize_y*10)/2), self.hitsize_x * 15, self.hitsize_y*10)

        self.hitbox = Hitbox(self.x + (self.img_size/2 - self.hitsize_x/2), self.y + (self.img_size - self.hitsize_y) - self.up_y, self.hitsize_x, self.hitsize_y)
       
        # 이미지
        self.tk_image_list_R = [[],[],[],[],[],[],[]]
        self.tk_image_list_L = [[],[],[],[],[],[],[]]

        for i in range(self.fc1): # idle 이미지 로드 FC = 0
            if self.name == 'Boss1_hand_R':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/idle_{i}.png")
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_list_R[0].append(self.tk_image)
                self.tk_image_list_L[0].append(self.tk_image)
            elif self.name == 'Boss1_hand_L':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/idle_{i}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[0].append(self.tk_image)
                self.tk_image_list_L[0].append(self.tk_image)
            else:
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_{self.name}/idle_{i}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[0].append(self.tk_image)
                self.tk_image_list_L[0].append(self.tk_image_flip)

        for i in range(self.fc2): # walk 이미지 로드 FC = 1
            if self.name == 'Boss1_hand_R':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/walk_{i}.png")
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_list_R[1].append(self.tk_image)
                self.tk_image_list_L[1].append(self.tk_image)
            elif self.name == 'Boss1_hand_L':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/walk_{i}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[1].append(self.tk_image)
                self.tk_image_list_L[1].append(self.tk_image)
            else:
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_{self.name}/walk_{i}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[1].append(self.tk_image)
                self.tk_image_list_L[1].append(self.tk_image_flip)

        for i in range(self.fc_a1): # attack 이미지 로드1 FC = 2
            if self.name == 'Boss1_hand_R':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/atk1_{i}.png")
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_list_R[2].append(self.tk_image)
                self.tk_image_list_L[2].append(self.tk_image)
            elif self.name == 'Boss1_hand_L':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/atk1_{i}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[2].append(self.tk_image)
                self.tk_image_list_L[2].append(self.tk_image)
            else:
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_{self.name}/atk1_{i}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[2].append(self.tk_image)
                self.tk_image_list_L[2].append(self.tk_image_flip)
        
        for i in range(self.fc_a2): # attack 이미지 로드2 FC = 3
            if self.name == 'Boss1_main':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_{self.name}/atk2_{i}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[3].append(self.tk_image)
                self.tk_image_list_L[3].append(self.tk_image_flip)
        self.j = 0
        for i in range(self.fc_a3): # attack 이미지 로드3 FC = 4
            if self.name == 'Boss1_main':
                if 5 <= i <= 9:
                    self.j = 5
                elif 18<= i <= 19:
                    self.j = 18
                elif 20 <= i <=28:
                    self.j = 20
                elif 29<= i <=37:
                    self.j = 29
                elif 38<= i <=46:
                    self.j = 38
                elif 47<= i <=55:
                    self.j = 47
                else:
                    self.j = i
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_{self.name}/atk3_{self.j}.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[4].append(self.tk_image)
                self.tk_image_list_L[4].append(self.tk_image_flip)
        # attacked 이미지 로드 FC = 5
        try:
            if self.name == 'Boss1_hand_R':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/atked.png")
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_list_R[5].append(self.tk_image)
                self.tk_image_list_L[5].append(self.tk_image)
            elif self.name == 'Boss1_hand_L':
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/atked.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[5].append(self.tk_image)
                self.tk_image_list_L[5].append(self.tk_image)
            else:
                self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_{self.name}/atked.png")
                self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                self.tk_image_list_R[5].append(self.tk_image)
                self.tk_image_list_L[5].append(self.tk_image_flip)
        except:
            pass

        for i in range(11):
            try:
                if self.name == 'Boss1_main':
                    self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_{self.name}/dead_{i}.png")
                    self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                    self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                    self.tk_image_list_R[6].append(self.tk_image)
                    self.tk_image_list_L[6].append(self.tk_image)
                if self.name == 'Boss1_hand_R':
                    self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/dead_{i}.png")
                    self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                    self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
                    self.tk_image_list_R[6].append(self.tk_image)
                    self.tk_image_list_L[6].append(self.tk_image)
                elif self.name == 'Boss1_hand_L':
                    self.raw_image = PIL.Image.open(f"{img_path}enemy_Boss_Boss1_hand/dead_{i}.png")
                    self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                    self.resize_image_flip = self.raw_image_flip.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
                    self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image_flip)
                    self.tk_image_list_R[6].append(self.tk_image)
                    self.tk_image_list_L[6].append(self.tk_image)
            except:
                break

        canvas.itemconfig(self.image, image=self.tk_image_list_L[0][0])

    def enemy_img_update(self):
        if Boss.boss_health > 0:
            if self.damaged == False:
                if self.state[0] == 0:# idle 애니메이션
                    self.FC = 0
                    self.fc = int(self.frame_count % self.fc1)

                else:
                    if self.state[2] == 0: # 이동
                        self.FC = 1
                        self.fc = int(self.frame_count % self.fc2)
                        if hasattr(self,'hastrace_ani'): # 추적 애니메이션 소지 확인
                            if self.trace == True:
                                self.FC = 2                        
                            
                    if self.state[2] == 1: # 공격
                        if self.state[4] == 0: # 공격시 애니메이션 프레임 보정용 스위치
                            self.frame_count = 0
                            self.state[4] = 1

                        if self.name == 'Boss1_main':
                            if self.FC == 2: # 패턴 1
                                self.fc = int(self.frame_count % self.fc_a1)
                                self.do_atk()

                                if self.fc >= 10:
                                    self.state[2] = 0
                                    self.state[0] = 0
                                    self.state[4] = 0

                            if self.FC == 3: # 패턴 2
                                self.fc = int(self.frame_count % self.fc_a2)
                                if self.fc == 9:
                                    self.do_atk()

                                if self.fc >= 11:
                                    self.state[2] = 0
                                    self.state[0] = 0
                                    self.state[4] = 0

                            if self.FC == 4: # 패턴 3
                                self.fc = int(self.frame_count % self.fc_a3)
                                self.do_atk()

                                if self.fc >= 61:
                                    self.state[2] = 0
                                    self.state[0] = 0
                                    self.state[4] = 0

                        elif self.name == 'Boss1_hand_R':
                            if self.FC == 2:
                                self.fc = int(self.frame_count % self.fc_a1)
                                self.do_atk()

                                if self.fc >= 35:
                                    self.state[2] = 0
                                    self.state[0] = 0
                                    self.state[4] = 0
                            else:
                                self.state[2] = 0
                                self.state[0] = 0
                                self.state[4] = 0

                        elif self.name == 'Boss1_hand_L':
                            if self.FC == 2:
                                self.fc = int(self.frame_count % self.fc_a1)
                                self.do_atk()

                                if self.fc >= 35:
                                    self.state[2] = 0
                                    self.state[0] = 0
                                    self.state[4] = 0
                            else:
                                self.state[2] = 0
                                self.state[0] = 0
                                self.state[4] = 0

            else: # 피격시 애니메이션
                if self.backFC != self.OUCH_FC:
                    self.backFC = self.FC
                self.FC = 5
                self.fc = 0

        else:
            self.FC = 6
            if self.fc < 10:
                self.fc = int(self.frame_count % 11) # 이미지 고정을 위한 1추가
            else:
                self.fc = 10
            if self.name == 'Boss1_hand_L' or self.name == 'Boss1_hand_R':
                self.fc = 0
            

        if self.backFC == self.OUCH_FC:
            if self.state[0] == 0:# idle 애니메이션
                self.backFC = 0
            if self.state[0] == 1 and self.state[2] == 0:
                self.backFC = 1
            if self.state[0] == 1 and self.state[2] == 1:
                if self.AC <= 1:
                    self.FC = 2
                if self.AC == 2:
                    self.FC = 3
                if self.AC == 3:
                    self.FC = 4
           
        # 캔버스에 있는 이미지를 새로운 이미지로 업데이트
        if self.state[1] == 0:
            canvas.itemconfig(self.image, image=self.tk_image_list_L[self.FC][self.fc])
        elif self.state[1] == 1:
            canvas.itemconfig(self.image, image=self.tk_image_list_R[self.FC][self.fc])


        self.frame_count += 0.3
        if self.state[2] == 0 and Boss.fight_start == True:
            self.atk_cd += 0.3

    def update_enemy_position(self):
        if Boss.fight_start == True:
            
            if Boss.boss_health > 0:
                if self.type == 'Boss1':
                    if self.name == 'Boss1_main':
                        Boss.boss1_main_xy = [self.x, self.y]
                        if self.state[2] == 0:
                            if (self.x + (self.img_size/2 - self.hitsize_x/2) + (self.hitsize_x/2)) > self.target.x + self.target.size//2:
                                self.state[1] = 0
                            else:
                                self.state[1] = 1
                            if (self.x + (self.img_size/2 - self.hitsize_x/2) + (self.hitsize_x/2)) - self.radius > self.target.x + self.target.size//2:
                                self.state[0] = 1
                                self.dx = -self.velocity
                            elif (self.x + (self.img_size/2 - self.hitsize_x/2) + (self.hitsize_x/2)) + self.radius < self.target.x + self.target.size//2:
                                self.state[0] = 1
                                self.dx = self.velocity
                            else:
                                self.state[0] = 0
                                self.dx = 0

                            if (self.y + (self.img_size - self.hitsize_y/2) - self.up_y) + self.radius - self.velocity > self.target.y + self.target.size//2:
                                self.dy = -self.velocity * 0.9
                            elif (self.y + (self.img_size - self.hitsize_y/2) - self.up_y) + self.radius < self.target.y + self.target.size//2:
                                self.dy = self.velocity * 0.9
                            else:
                                self.dy = 0
                        elif self.state[2] == 1:
                            self.dx = self.dy = 0
                            if self.AC == 3 and self.fc > 5:
                                self.set_position(1280//2-(self.img_size/2 + self.hitsize_x/2) + (self.hitsize_x/2), 720//2 - (self.img_size - self.hitsize_y/2))

                    if self.name == 'Boss1_hand_R':
                        if self.state[2] == 0:
                            self.state[1] = 1
                            self.dx = self.dy = 0
                            self.set_position(Boss.boss1_main_xy[0]-self.img_size//2 - 70, Boss.boss1_main_xy[1] + self.hitsize_y//2)

                        elif self.state[2] == 1:
                            if self.AC == 1:
                                if self.fc < 5:self.dx = 0
                                if self.fc < 11:self.dy = 0
                                if 5 <= self.fc < 6:
                                    self.set_position(self.target.x-(self.target.size/2), self.hitsize_y)
                                if 18 <= self.fc < 22:
                                    self.dy = self.velocity * 5
                                if 22 <= self.fc:
                                    self.set_position(self.x, 720-40-self.img_size)
                                

                    elif self.name == 'Boss1_hand_L':
                        self.state[0] = 1
                        if self.state[2] == 0:
                            self.state[1] = 0
                            self.dx = self.dy = 0
                            self.set_position(Boss.boss1_main_xy[0]+(self.img_size - self.hitsize_x)*3, Boss.boss1_main_xy[1] + self.hitsize_y//2)
                        
                        elif self.state[2] == 1:
                            if self.AC == 1:
                                if self.fc < 5:self.dx = 0
                                if self.fc < 11:self.dy = 0
                                if 5 <= self.fc < 6:
                                    self.set_position(self.target.x-(self.target.size/2), self.hitsize_y)
                                if 18 <= self.fc < 22:
                                    self.dy = self.velocity * 5
                                if 22 <= self.fc:
                                    self.set_position(self.x, 720-40-self.img_size)
            else:
                self.dx = 0
                self.dy = 3
            self.x += self.dx
            self.y += self.dy

            canvas.move(self.image, self.dx, self.dy)
            self.hitbox.move(self.dx, self.dy)

        else:
            if self.name == 'Boss1_main':
                x = 1280//2-(self.img_size/2 + self.hitsize_x/2) + (self.hitsize_x/2)
                self.y_to_start -= 4
                
                self.set_position(x, self.y_to_start) # 720//2 - (self.img_size - self.hitsize_y/2))
                Boss.boss1_main_xy = [self.x,self.y]

            if self.name == 'Boss1_hand_R':
                self.state[1] = 1
                self.dx = self.dy = 0
                hand_r_x = Boss.boss1_main_xy[0] - self.img_size//2 - 70
                hand_r_y = Boss.boss1_main_xy[1] + self.hitsize_y//2
                self.set_position(hand_r_x, hand_r_y)
            if self.name == 'Boss1_hand_L':
                self.state[1] = 0
                self.dx = self.dy = 0
                hand_l_x = Boss.boss1_main_xy[0] + (self.img_size - self.hitsize_x)*3
                hand_l_y = Boss.boss1_main_xy[1] + self.hitsize_y//2
                self.set_position(hand_l_x, hand_l_y)

            if Boss.boss1_main_xy[1] < 200:
                Boss.fight_start = True
                bossHPUI.set_boss_hp_bar(canvas, 60)
                bossHPUI.boss_hp_anim_state = "full"

            if Boss.boss1_main_xy[1] < 800 and not Boss.fight_start and not Boss.hp_bar_created:
                bossHPUI.create_boss_hp_bar(canvas)
                Boss.hp_bar_created = True
                
        #self.hitbox.draw_hitbox() # 디버그용

    
    def attack_cycle(self):

        if Boss.fight_start == True:
            if self.atk_cd > self.atk_timer:
                self.state[0] = 1
                self.state[2] = 1
                if self.AC < 1 or self.AC >= 3: # 첫 번째 패턴 ( HEAD: bullet 3개 순차적 발사 / HAND_R: 플레이어 머리 위로 이동 후 내려찍기 / HAND_L: 플레이어 머리 위로 이동 후 내려찍기)
                    self.AC = 1
                    self.atk_cd = 0
                    if self.name == 'Boss1_hand_L':
                            self.atk_cd = 30
            
                elif self.AC == 1:
                    if self.name == 'Boss1_main': # 두 번째 패턴 ( HEAD: 큰 유도 bullet 1개 발사 )
                        self.AC = 2
                        self.atk_cd = -(self.atk_timer//2)
                    else:
                        self.AC = 0
                        self.atk_cd = 0
                        if self.name == 'Boss1_hand_L':
                            self.atk_cd = 30
                    
                elif self.AC == 2: # 세 번째 패턴 ( HEAD: 맵 중앙 이동, bullet 여러개 360도로 순차적으로 발사)
                    self.AC = 3
                    self.atk_cd = -(self.atk_timer//1.5)

                self.FC = self.AC + 1
    
    def do_atk(self):
        if self.name == 'Boss1_main':
            x = self.x+(self.img_size//2)
            y = self.y+(self.img_size//2)
            if self.AC == 1:
                if self.check == -1:
                    self.check = 0
                if self.fc == 3 and self.check == 0:
                    if self.state[1] == 0:
                        self.bullet = Bullet(x-24-22.5, y+45, 45, owner=self, target=self.target, damage=1, speed=8)
                    else:
                        self.bullet = Bullet(x, y+45, 45, owner=self, target=self.target, damage=1, speed=6)
                    self.check = 1
                if self.fc == 5 and self.check == 1:
                    if self.state[1] == 0:
                        self.bullet = Bullet(x-24-22.5, y+45, 45, owner=self, target=self.target, damage=1, speed=8)
                    else:
                        self.bullet = Bullet(x, y+45, 45, owner=self, target=self.target, damage=1, speed=6)
                    self.check = 2
                if self.fc == 7 and self.check == 2:
                    if self.state[1] == 0:
                        self.bullet = Bullet(x-24-22.5, y+45, 45, owner=self, target=self.target, damage=1, speed=8)
                    else:
                        self.bullet = Bullet(x, y+45, 45, owner=self, target=self.target, damage=1, speed=6)
                    self.check = -1
            if self.AC == 2:
                if self.check == -1:
                    self.check = 0
                if self.check == 0:
                    self.bullet = Bullet(x-64, y+32, 128, name="Super_bullet", owner=self, target=self.target, damage=1, speed=3, istracking=True)
                    self.check = -2

            if self.AC == 3:
                if self.check == -2:
                    self.check = 0
                if self.fc == self.circle and self.check <= 12:
                    angle = radians(self.check * 30)
                    self.bullet = Bullet(x-32, y-32, 64, owner=self, damage=1, speed=6, target_x=x + 100 * cos(angle), target_y=y + 100 * sin(angle))
                    self.circle += 3
                    self.check += 1
                    if self.check >= 11:
                        self.check = -1
                        self.circle = 20

        elif self.name == 'Boss1_hand_R' or self.name=='Boss1_hand_L':
            if self.AC == 1:
                Collision.attack_hitbox_collision(5, self.atk_hitboxes, self.target)
                if 23 <= self.fc < 25:
                    self.atk_hitbox = Atk_Hitbox(self.x + (self.img_size/2 - self.hitsize_x/2), self.y + ((self.img_size - self.hitsize_y//2) - self.up_y), self.hitsize_x, self.hitsize_y//2, damage=1)
                    self.atk_hitboxes.append(self.atk_hitbox)

                    #self.atk_hitbox.draw_hitbox(color='red') # 디버그용

        def remove_atk_box(): # 공격 히트박스 제거
            if self.atk_hitbox is not None:
                canvas.delete(self.atk_hitbox.hitbox_rect)
                self.atk_hitbox.hitbox_rect = None
            if self.atk_hitboxes is not None and self.atk_hitbox in self.atk_hitboxes:
                self.atk_hitboxes.remove(self.atk_hitbox)

        root.after(20, remove_atk_box)


    def take_damage(self, attacker):
        if self.fight_start:
            if self.damaged==False:
                self.damaged = True # 피격 됨
                Boss.boss_health -= attacker.damage
                bossHPUI.set_boss_hp_bar(canvas, Boss.boss_health)
                root.after(100, self.reset_damaged_state)  # 피격 상태 초기화

    def isDead(self):
        if Boss.boss_health <= 0:
            self.state[0] = 0
            self.state[2] = 0
            self.state[3] = 0
            self.state[4] = 0
            self.damaged = True
            bossHPUI.hide_boss_hp_bar(canvas, 1)
            if Boss.boss_health <= -10:
                canvas.delete(self.image)
                bossHPUI.hide_boss_hp_bar(canvas, 0)
                bossHPUI.animate_boss_hp_bar(canvas)
                # 히트박스 사각형이 있으면 삭제
                try:
                    if self.hitbox.hitbox_rect is not None:
                        canvas.delete(self.hitbox.hitbox_rect)
                        self.hitbox.hitbox_rect = None
                    if self.trackbox.hitbox_rect is not None:
                        canvas.delete(self.trackbox.hitbox_rect)
                        self.trackbox.hitbox_rect = None
                    if self.atk_range.hitbox_rect is not None:
                        canvas.delete(self.atk_range.hitbox_rect)
                        self.atk_range.hitbox_rect = None
                except:
                    pass
                # 리스트에서 제거
                if self in Enemy.enemy_list:
                    Enemy.enemy_list.remove(self)

                
