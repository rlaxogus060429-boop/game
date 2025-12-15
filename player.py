## 플레이어 클래스 및 관련 함수들
from tkinter import *
import PIL.Image
import PIL.ImageTk
from math import e
from hitboxes import Hitbox, Atk_Hitbox
from container import *
from collision import Collision
from enemy import *
import gameUI
from map_container import x0_0, y0_0

class Player: # 플레이어 클래스
    def __init__(self, x, y, v, h, mh, d, aspeed, where):
        self.health = h # 현재 체력
        self.maxhealth = mh # 최대 체력

        self.can_go = False

        self.where = where  # 현재 위치한 스테이지

        self.after_ids = {}

        self.x = x 
        self.y = y
        self.size = 70  # 플레이어 크기
        self.atk_size = 150  # 공격 이펙트 크기

        self.velocity = v  # 이동 속도
        self.damage = d  # 공격력
        
        self.dash_cd = 0
        self.dash_timer = 0

        self.atk_cd = 0
        self.atk_timer = aspeed  # 공격 속도(공격 간의 텀)

        self.combo_ok = self.atk_timer + 10    # 콤보 입력 허용 시간(공격 가능 후 10 동안)
        self.combo_cd = 0

        ###########

        self.dx = self.dy = 0 # 가로축 및 세로축 속도 초기화
        self.jump_count = 0 # 점프력 적용용 카운트

        ###########

        self.atk_hitboxes = []

        self.damaged = False # 피격 상태
        self.re_atk = False
        self.can_air_atk = True

        self.unlock = [1, 1, 1]
        '''
        [0] == 대쉬, [1] == 이단점프, [2] == 활강 (0 잠금, 1 해금)
        '''

        self.state = [0, 0, 0, 0, 1, 0, 0, 0, 0]
        ''' 
            [0] == 정지유무(0-정지, 1-움직임), [1] = 왼오(0-왼, 1-오), [2] == 대쉬(0-대쉬안함, 1-대쉬함), [3] == 점프(0-점프안함, 1-점프함, 2-이단점프함), 
            [4] == 공중(0-공중아님, 1-공중임),
            [5] == 공격(0-안함, 1-1공격함, 2-2공격함, 3-3공격함, state[3] != 0 and state[5] != 0 공중공격함), [6] == 활강(0-안함, 1-함)
            [7] == 연격 테스트
        '''


        self.frame_count = 0 # 애니메이션 프레임 카운트
        self.frame_count = 0 # 애니메이션 프레임 카운트
        
        self.image = canvas.create_image(self.x, self.y, image=None, anchor=NW, tags = "player") # 캔버스에 플레이어 이미지 추가

        self.hitbox = Hitbox(x+self.size//4, y+self.size//2, self.size//2, self.size//2)  # 히트박스 생성
        self.hit_r = False
        self.hit_l = False
        self.hit_u = False
        self.hit_d = False
        
        self.tk_image_list_r = [[],[],[],[],[],[],[],[],[]]  # 모든 PhotoImage 참조를 저장
        self.tk_image_list_l = [[],[],[],[],[],[],[],[],[]]

        for i in range(6): # idle
            self.raw_image= PIL.Image.open(f"{img_path}player/idle_{i}.png")
            self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_list_r[0].append(self.tk_image)
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_l[0].append(self.tk_image_flip)

        for i in range(8): # walk
            self.raw_image= PIL.Image.open(f"{img_path}player/walk_{i}.png")
            self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_list_r[1].append(self.tk_image)
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_l[1].append(self.tk_image_flip)
        # dash
        self.raw_image= PIL.Image.open(f"{img_path}player/dash_0.png")
        self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
        self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
        self.tk_image_list_r[2].append(self.tk_image) # dash 중
        self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
        self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
        self.tk_image_list_l[2].append(self.tk_image_flip)

        self.raw_image= PIL.Image.open(f"{img_path}player/walk_6.png")
        self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
        self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
        self.tk_image_list_r[2].append(self.tk_image) # dash 종료 후 방향키를 누르고 있을 때
        self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
        self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
        self.tk_image_list_l[2].append(self.tk_image_flip)

        self.raw_image= PIL.Image.open(f"{img_path}player/walk_6.png")
        self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
        self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
        self.tk_image_list_r[2].append(self.tk_image) # dash 종료 후 방향키를 누르고 있지 않을 때
        self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
        self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
        self.tk_image_list_l[2].append(self.tk_image_flip)


        for i in range(4): #atk
            self.raw_image= PIL.Image.open(f"{img_path}player/atk1_{i}.png")
            self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_list_r[3].append(self.tk_image) # 1공격
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_l[3].append(self.tk_image_flip)

            self.raw_image= PIL.Image.open(f"{img_path}player/atk2_{i}.png")
            self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_list_r[4].append(self.tk_image) # 2공격
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_l[4].append(self.tk_image_flip)

            self.raw_image= PIL.Image.open(f"{img_path}player/atk3_{i}.png")
            self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_list_r[5].append(self.tk_image) # 3공격
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_l[5].append(self.tk_image_flip)

            self.raw_image= PIL.Image.open(f"{img_path}player/airatk_{i}.png")
            self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_list_r[6].append(self.tk_image) # 공중공격
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_l[6].append(self.tk_image_flip)

        for i in range(2):
            self.raw_image= PIL.Image.open(f"{img_path}player/jump_{i}.png")
            self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
            self.tk_image_list_r[7].append(self.tk_image) # 점프
            self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
            self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
            self.tk_image_list_l[7].append(self.tk_image_flip)

        self.raw_image= PIL.Image.open(f"{img_path}player/hover_0.png")
        self.resize_image = self.raw_image.resize((self.size, self.size), PIL.Image.NEAREST)
        self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)
        self.tk_image_list_r[8].append(self.tk_image) # 활강
        self.raw_image_flip = self.raw_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        self.resize_image_flip = self.raw_image_flip.resize((self.size, self.size), PIL.Image.NEAREST)
        self.tk_image_flip = PIL.ImageTk.PhotoImage(self.resize_image_flip)
        self.tk_image_list_l[8].append(self.tk_image_flip)
    
    def create_dash_trail(self): # 대쉬 할때 잔상 생성
        def remove_trail(): # 잔상 제거
            canvas.delete(trail_img)
            self.trail_refs = [t for t in self.trail_refs if t[0] != trail_img]

        if self.state[2] == 1:
            trail_raw = PIL.Image.open(f"{img_path}player/dash_1.png")
            if self.state[1] == 0:
                trail_raw = trail_raw.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            trail_resize = trail_raw.resize((self.size, self.size), PIL.Image.NEAREST)
            trail_tk = PIL.ImageTk.PhotoImage(trail_resize)
            trail_img = canvas.create_image(self.x, self.y, image=trail_tk, anchor=NW)

            if not hasattr(self, 'trail_refs'):
                self.trail_refs = []
            self.trail_refs.append((trail_img, trail_tk))

            root.after(100, remove_trail)

    def update_effect(self): # 대쉬 시 잔상 생성 2
        if self.state[2] == 1:
            self.create_dash_trail()

    def update_cd(self):
        if self.atk_cd > 0: # 공격 쿨타임 감소
            self.atk_cd -= 1
        if self.atk_cd <= 0:
            self.atk_cd = 0

        if self.combo_cd > 0: # 콤보 입력 가능 시간 감소
            self.combo_cd -= 1
        if self.combo_cd <= 0:
            self.combo_cd = 0
            self.state[7] = 0

    def create_atk_effect(self): # 공격 이펙트 생성
        atk_hitbox = None
        if self.state[3] == 0: # 지상 공격 이펙트
            atkef_raw = PIL.Image.open(f"{img_path}effect/atk{self.state[5]}_{self.fc}.png")
            # 히트박스 생성
            if 0 < self.fc < 2:
                ###
                Collision.attack_hitbox_collision(8, self.atk_hitboxes, Enemy.enemy_list)
                ###
                if self.state[1] == 0:
                    atk_hitbox = Atk_Hitbox(self.x+(self.size//1.5-self.atk_size//2), self.y+self.size//2-self.atk_size//3.7, self.atk_size//2, self.atk_size//1.8, damage=self.damage)

                    #atk_hitbox.draw_hitbox() # 디버그용

                    self.atk_hitboxes.append(atk_hitbox)
                else:
                    atk_hitbox = Atk_Hitbox(self.x+self.size//3, self.y+self.size//2-self.atk_size//3.7, self.atk_size//2, self.atk_size//1.8, damage=self.damage)

                    #atk_hitbox.draw_hitbox() # 디버그용

                    self.atk_hitboxes.append(atk_hitbox)

        elif self.state[3] != 0: # 공중 공격 이펙트
            ###
            Collision.attack_hitbox_collision(8, self.atk_hitboxes, Enemy.enemy_list)
            ###
            atkef_raw = PIL.Image.open(f"{img_path}effect/airatk_{self.fc}.png")
            if 0 < self.fc < 2:
                atk_hitbox = Atk_Hitbox(self.x+(self.size//2-self.atk_size//2), self.y+(self.size//2-self.atk_size//2), self.atk_size, self.atk_size, damage=self.damage + 2)
                
                #atk_hitbox.draw_hitbox() # 디버그용

                self.atk_hitboxes.append(atk_hitbox)

        atkef_resize = atkef_raw.resize((self.atk_size, self.atk_size), PIL.Image.NEAREST) # 170 170
        if self.state[1] == 0:
            #atkef_raw = atkef_raw.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            atkef_resize = atkef_resize.transpose(PIL.Image.FLIP_LEFT_RIGHT)

        
        atkef_tk = PIL.ImageTk.PhotoImage(atkef_resize)
        atkef_img = canvas.create_image(self.x+(self.size//2-self.atk_size//2), self.y+(self.size//2-self.atk_size//2), image=atkef_tk, anchor=NW)

        if not hasattr(self, 'atkef_refs'):
            self.atkef_refs = []
        self.atkef_refs.append((atkef_img, atkef_tk))

        def remove_atkef(): # 공격 이펙트 제거
            canvas.delete(atkef_img)

            if atk_hitbox is not None:
                canvas.delete(atk_hitbox.hitbox_rect)
                atk_hitbox.hitbox_rect = None
                self.atk_hitboxes.remove(atk_hitbox)

            self.atkef_refs = [t for t in self.atkef_refs if t[0] != atkef_img]

        root.after(40, remove_atkef)
        
    def player_img_update(self):
        if self.state[5] == 0:
            if self.state[0] == 0 and self.state[2] != 1:
                # idle 애니메이션
                self.FC = 0
                self.fc = min(int(self.frame_count % 6),5)
            
            elif self.state[0] == 1 and self.state[2] != 1:
                # walk 애니메이션
                self.FC = 1
                self.fc = min(int(self.frame_count % 8),7)
            
        if self.state[2] == 1:
            self.state[5] = 0
            # dash 애니메이션
            self.FC = 2
            self.fc = min(int(self.frame_count % 2),1)
            if self.fc >= 1:
                if self.state[0]==1:
                    self.fc = 1
                    
                else:
                    self.fc = 2
                    
            else:
                self.fc = 0
                
        # 공격 애니메이션
        if self.state[5] != 0:
            if self.state[5] >= 1 and self.combo_cd > 0:
                self.state[7] = self.state[5] + 1
                if self.state[7] > 3:
                    self.state[7] = 1
            
            #self.FC = self.state[5] + 2 if self.state[3] == 0 else 6
            self.fc = min(int(self.frame_count % 100),3)

            if self.state[3] == 0: # 지상 공격 애니메이션
                self.FC = self.state[5] + 2
                
            if self.state[3] != 0: # 공중 공격 애니메이션
                if self.can_air_atk:
                    self.FC = 6
                    
                   
            if 0 < self.fc < 3:
                if self.state[3] == 0:
                    self.create_atk_effect()
                elif self.state[3] != 0 and self.can_air_atk == True:
                    self.create_atk_effect()

            if self.fc >= 3:
                self.state[5] = 0
                self.can_air_atk = False

        # 점프 및 활공 애니메이션
        if self.state[3] != 0 and self.state[5] == 0 and self.state[2] == 0:
            if self.state[6] == 1:
                self.FC = 8
                self.fc = 0
                
            elif self.dy < -6:
                self.FC = 7
                self.fc = 0

            elif -6 <= self.dy:
                self.FC = 7
                self.fc = 1
      
        # 캔버스에 있는 이미지를 새로운 이미지로 업데이트
        if self.state[1] == 0:
            canvas.itemconfig("player", image=self.tk_image_list_l[self.FC][self.fc])
        if self.state[1] == 1:
            canvas.itemconfig("player", image=self.tk_image_list_r[self.FC][self.fc])

        self.frame_count += 0.3

    
    def update_player_position(self):
        self.jump_count += 1

        if self.state[0] == 0 and self.state[2] == 0:
            self.dx = 0

        # 위아래
        if key_states['w']:
            pass
        
        if key_states['s']:
            if self.unlock[2] == 1 and self.state[6] == 1: # 활강 해제
                self.state[6] = 0

        # 좌우 이동
        if key_states['a']:
            self.state[0] = 1
            if self.state[1] == 1 and not(self.state[5] and self.fc < 3):
                self.state[1] = 0
            if self.state[1] == 0:
                self.dx = -self.velocity
            

        if key_states['d']:
            self.state[0] = 1
            if self.state[1] == 0 and not(self.state[5] and self.fc < 3):
                self.state[1] = 1
            if self.state[1] == 1:
                self.dx = self.velocity

        if self.state[2] == 1:
            
            if self.hit_r == True or self.hit_l == True:
                self.dx = 0
                self.dash_timer -= 1000
            else:
                if self.state[1] == 1:
                    self.dx = self.velocity * 6  # 대시 중일 때 속도 증가
                else:
                    self.dx = -self.velocity * 6

            self.dy = 0
        
        if self.unlock[0] == 1:
            if self.state[2] == 0:
                self.dash_cd += 1
            # 대시: 이동 중에만 가능
            
            if key_states['shift_l'] and self.state[0] == 1 and self.state[2] == 0 and self.dash_cd >= 50:
                self.dash_cd = 0
                self.frame_count = 0
                self.state[2] = 1
                self.dash_timer = 50 # 대쉬 지속 시간(ms)
                self.state[6] = 0

            if self.state[2] == 1:
                self.dash_timer -= 10
                if self.dash_timer <= 0:
                    self.state[2] = 0
                    self.dash_timer = 0

        # 점프
        if key_states['space']:
            if self.state[5] == 0:
                if self.state[3] == 0:
                    self.frame_count = 0
                    self.atk_cd = 0
                    self.jump_count = 0
                    self.state[3] = 1
                    self.state[4] = 1
                    self.dy = 0
                    self.can_air_atk = True
                    self.hit_d = False  # 점프 시작 시 바닥 충돌 해제
            
                elif self.unlock[1] == 1 and self.state[3] == -2 and self.state[4] == 1:
                    self.frame_count = 0
                    self.atk_cd = 0
                    self.jump_count = 0
                    self.dy = 0
                    self.atk_cd = 0
                    self.can_air_atk = True
                    self.state[3] = 2
            
            # 점프력 적용
        if self.state[3] == 1 or self.state[3] == 2:
            if self.jump_count >= 3:
                self.state[4] = 1
                if self.unlock[1] == 1 and self.state[3] == 1: # 이단점프 해금 상태 1
                    self.state[3] = -1
                elif self.unlock[1] == 1 and self.state[3] == 2: # 이단점프 해금 상태 2
                    self.state[3] = 3 # 점프 소진
                else:
                    self.state[3] = 3 # 점프 소진
                
            else:
                self.dy -= 6 / (e ** (0.2 * self.jump_count)) # 지수함수로 점프력 감소
                

        elif self.hit_d == False and self.state[4] == 1: # 중력 적용 및 활강시 중력 적용
            if self.unlock[2] == 1 and self.state[6] == 1:
                    self.dy = g * 1.8 # 활강시 중력 적용
                    self.dx *= 0.8 # 활강시 이속저하
            else:
                self.dy += g  # 중력 가속도 적용

            if self.can_air_atk == True and self.state[3] != 0 and self.state[5] != 0: # 공중 공격시 잠시 채공
                self.dy = 0
                self.dx = 0

        if self.state[2] == 0 and self.state[5] != 0:# 공격시 이속 저하
            self.dx *= 0.5

        # 이동 적용
        self.dy = min(self.dy, 30)

        if self.state[5] != 0:
            canvas.move("player", self.dx, self.dy)
        else:
            canvas.move("player", self.dx, self.dy)

         # 히트박스 이동
        self.x += self.dx
        self.y += self.dy
        self.hitbox.move(self.dx, self.dy)
        

        #self.hitbox.draw_hitbox() # 디버그용

    def set_position(self, set_x, set_y):
        self.x = set_x
        self.y = set_y
        canvas.coords(self.image, set_x, set_y)
        self.hitbox.coords(self.x + (self.size//4), self.y+(self.size//2))

       
    def reset_damaged_state(self):
        self.damaged = False

    def take_damage(self):
        if self.damaged == False:
            self.damaged = True # 피격 됨
            self.health -= 1
            root.after(1000, self.reset_damaged_state)  # 무적 시간 이후 피격 상태 초기화
            if self.health < 0:
                self.isDead()

            if self.state[1] == 0 and self.hit_l == False: # 피격 시 넉백
                self.x += 35 * 0.7
                self.y -= 10
            elif self.state[1] == 1 and self.hit_r == False:
                self.x += -35 * 0.7
                self.y -= 10

    def layer_up(self):
         canvas.tag_raise("player") # 플레이어 이미지를 맵 타일 위로 올리기


    def isDead(self):
        # 캔버스에서 이미지와 히트박스 삭제
        #canvas.delete(self.image)
        canvas.itemconfig(self.image, state="hidden")

        # 히트박스 사각형이 있으면 삭제
        if self.hitbox.hitbox_rect is not None:
            canvas.delete(self.hitbox.hitbox_rect)
            self.hitbox.hitbox_rect = None

        gameUI.show_gameover()



player = Player(x0_0, y0_0, 6, 10, 10, 1, 15, 'stage0_0') # Player(x, y, 이동속도, 현재체력, 최대체력, 공격력, 공격 텀, 위치)