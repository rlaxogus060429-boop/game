from tkinter import *
from container import *
from makeMap import *
from map_container import *
from gameUI import *
import music

class Collision:
    not_Collision = ['entry', 'un_wall_l', 'un_wall_r', 'un_middle', 'decoration1', 'decoration2', 'decoration3']

    @staticmethod
    def hitbox_collision(box1, box2):
        
        # box1과 box2의 사각형(히트박스) 정보
        x1, y1, x2, y2 = box1.hitbox.get_rect()

        if box1.__class__.__name__ == 'Player' and box2.__class__.__name__ == 'Bullet':
            p1, q1, p2, q2 = box2.hitbox.get_rect()
            if x2 > p1 and x1 < p2 and y2 > q1 and y1 < q2:
                if box1.state[2] == 0:
                    box2.destroy_self()
                    box2.destroy = True
                    box1.take_damage()
                

        if box1.__class__.__name__ == 'Player' and box2.__class__.__name__ == 'Monster':
            p1, q1, p2, q2 = box2.trackbox.get_rect()
            a1, b1, a2, b2 = box2.atk_range.get_rect()
    
            if x2 > p1 and x1 < p2 and y2 > q1 and y1 < q2:
                if box2.trace == False:
                    box2.trace = True
            if box2.trace == True:
                if x2 > a1 and x1 < a2 and y2 > b1 and y1 < b2:
                    if box2.atk_cd > box2.atk_timer:
                        box2.state[2] = 1           
     

        if box2 in Worldbox.box_list: # 맵 타일과의 box1 충돌 확인
            if hasattr(box2, 'hitbox'):
                p1, q1, p2, q2 = box2.hitbox.get_rect()

                over_l = over_t = over_r = over_b = 0
    
                # 충돌 여부 확인
                if x2 > p1 and x1 < p2 and y2 > q1 and y1 < q2:
                    # 각 방향의 겹친 거리 계산
                    over_r = x2 - p1
                    over_l = p2 - x1
                    over_b = y2 - q1
                    over_t = q2 - y1

                # 겹친 거리 중 가장 작은 값이 충돌 방향
                    over_where = min(over_l, over_r, over_t, over_b)

                    if box2.name not in Collision.not_Collision:
                        # 충돌 방향별로 위치 보정
                        if over_where == over_r:
                            # 오른쪽(박스1의 오른편이 박스2의 왼편과 충돌)
                            box1.x -= over_r
                            box1.dx = 0
                            if box1.__class__.__name__ == "Player":
                                box1.hit_r = True
                                box1.state[2] = 0
            
                        elif over_where == over_l:
                            # 왼쪽(박스1의 왼편이 박스2의 오른편과 충돌)
                            box1.x += over_l
                            box1.dx = 0
                            if box1.__class__.__name__ == "Player":
                                box1.hit_l = True
                                box1.state[2] = 0

                        if over_where == over_t and (box2.name != "ground_l" and box2.name != "ground_r" and box2.name != "wall_l" and box2.name != "wall_r"):
                            # 위(박스1의 윗부분이 박스2의 아래와 충돌)
                            box1.y += over_t
                            box1.dy = 0

                        elif over_where == over_b:
                            # 아래(박스1의 아래가 박스2의 윗부분과 충돌)
                            box1.y -= over_b
                            box1.dy = 0
                            if box1.__class__.__name__ == 'Player':
                                box1.hit_d = True
                                box1.can_air_atk = True
                                box1.state[4] = 0   # 착지 상태로 전환
                                box1.state[3] = 0
                                box1.state[6] = 0
                                if box2.name == 'spike': # 함정 착지 시 데미지
                                    box1.take_damage()

                            if box1.__class__.__name__ == 'Monster':
                                box1.state[3] = 0   # 착지 상태로 전환

                    elif box2.name == "entry" and box1.__class__.__name__ == 'Player': # box1 이 플레이어 캐릭터일 경우에만 실행
                        if box2.wto_go is not None and box1.can_go == True:
                            # 출입구 충돌 시 맵 전환 로직
                            if box2.wto_go == 'stage0_1':
                                box1.set_position(x0_1, y0_1)
                                canvas.config(bg="#8ec9de")
                            elif box2.wto_go == 'stage0_2':
                                box1.set_position(x0_2, y0_2)
                                canvas.config(bg="#8ec9de")
                            elif box2.wto_go == 'stage0_3':
                                box1.set_position(x0_3, y0_3)
                                canvas.config(bg="#8ec9de")

                            if box2.wto_go == 'stage1_0':
                                box1.set_position(x1_0, y1_0)
                                canvas.config(bg="#575757")
                            elif box2.wto_go == 'stage1_1':
                                box1.set_position(x1_1, y1_1)
                                canvas.config(bg="#575757")
                            elif box2.wto_go == 'stage1_2':
                                box1.set_position(x1_2, y1_2)
                                canvas.config(bg="#575757")
                            elif box2.wto_go == 'stage1_3':
                                box1.set_position(x1_3, y1_3)
                                canvas.config(bg="#575757")
                            elif box2.wto_go == 'stage1_boss':
                                music.music_play('Boss')
                                box1.set_position(box1.x - 9*40, 0)
                                canvas.config(bg="#404040")

                            import spawnEnemy
                            spawnEnemy.spawn_enemy(box2.wto_go)
                            makeMap(show_map, box2.wto_go) # 맵 타일 재배치
                            Worldbox.update_map(show_map) # 맵 타일 재배치
                            box1.can_go = False
                        
                else:
                    if box1.__class__.__name__ == 'Player':
                        box1.hit_r = box1.hit_l = box1.hit_d = box1.hit_u = False
                        box1.state[4] = 1   # 공중 상태로 전환

                    else:
                        box1.state[3] = 1   # 공중 상태로 전환

                # 위치 보정 후 이미지/히트박스 동기화
                if box1.__class__.__name__ == 'Player':
                    canvas.coords(box1.image, box1.x, box1.y)
                    box1.hitbox.coords(box1.x + (box1.size//4), box1.y+(box1.size//2)) # 히트박스 이동

                elif box1.__class__.__name__ == 'Monster':
                    canvas.coords(box1.image, box1.x, box1.y)
                    box1.hitbox.coords(box1.x + (box1.img_size/2 - box1.hitsize_x/2), box1.y + (box1.img_size - box1.hitsize_y) - box1.up_y)
                    
                    if box1.type == 'A':
                        box1.trackbox.coords((box1.x + (box1.img_size/2 - box1.hitsize_x/2)) - (box1.tsize_x/2 - box1.hitsize_x/2), box1.y + (box1.img_size - box1.hitsize_y) - (box1.tsize_y - box1.hitsize_y) - box1.up_y)
                        box1.atk_range.coords(box1.x + (box1.img_size/2 - (box1.hitsize_x * 1.5)/2), box1.y + (box1.img_size - box1.hitsize_y*1.2) - box1.up_y)
                    elif box1.type == 'B':
                        box1.trackbox.coords((box1.x + (box1.img_size/2 - box1.hitsize_x/2)) - (box1.tsize_x/2 - box1.hitsize_x/2), (box1.y + (box1.img_size/2 - box1.hitsize_y/2)) - (box1.tsize_y/2 - box1.hitsize_y/2))
                        box1.atk_range.coords(box1.x + (box1.img_size/2 - (box1.hitsize_x*12)/2), box1.y + (box1.hitsize_y - (box1.hitsize_y*12)/2))


    # 공격자의 공격용 히트박스 리스트와 타겟 객체 리스트를 받아 충돌 체크
    def attack_hitbox_collision(max_count, attack_hitboxes, targets): # max_count 공격 범위 내에 들어왔는지 확인용 히트박스 유지 시간
        count = 0
        after_id = None
        def collision_main(attack_hitboxes, targets):
            nonlocal after_id
            nonlocal count

            for atk in attack_hitboxes:

                ax1, ay1, ax2, ay2 = atk.get_rect()
                if type(targets) == list:# 타겟이 플레이어면 player.hitbox, 적이면 enemy.hitbox 사용
                    for target in targets:
                        if hasattr(target, 'hitbox'):
                            tx1, ty1, tx2, ty2 = target.hitbox.get_rect()

                            if ax2 > tx1 and ax1 < tx2 and ay2 > ty1 and ay1 < ty2:
                                target.take_damage(atk)
                else:
                    if hasattr(targets, 'hitbox'):
                        tx1, ty1, tx2, ty2 = targets.hitbox.get_rect()

                        if ax2 > tx1 and ax1 < tx2 and ay2 > ty1 and ay1 < ty2:
                                targets.take_damage()
                        
            count += 1
            if count < max_count: #공격용 히트박스 유지
                if after_id is not None:
                    root.after_cancel(after_id)
                after_id = root.after(10, collision_main, attack_hitboxes, targets)


        collision_main(attack_hitboxes, targets)

    def map_collision(obj):
        for box in Worldbox.box_list:
            if box == 00:
                continue
            if abs(box.x - obj.x) > 300 or abs(box.y - obj.y) > 300:
                continue
            Collision.hitbox_collision(obj,box)


        