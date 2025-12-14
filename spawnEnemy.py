from enemy import *
from bullet import Bullet
from player import player
from random import randint

def spawn_enemy(load_map):
    for e in Enemy.enemy_list:
        e.health = -10
        if e.__class__.__name__ == "Boss":
            Boss.boss_health = -10
    for b in Bullet.bullet_list:
        b.destroy_self()

    if load_map == 'stage0_0':
        # Enemy(id, x, y, target)
        enemy=Monster("WalkingSprout", 540, 520, player)
        enemy=Monster("WalkingSprout", 960, 600, player)
        enemy=Monster("WalkingSprout", 760, 600, player)

    elif load_map == 'stage0_1':
        for _ in range(3): # Enemy(id, x, y, target)
            x = randint(320, 1000)
            enemy=Monster("WalkingSprout", x, 300, player)

    elif load_map == 'stage0_3':
        for _ in range(2):
            x = randint(200, 800)
            enemy=Monster("WalkingSprout", x, 200, player)
        for _ in range(3):
            x=randint(200, 900)
            y=randint(300, 450)
            enemy=Monster("FlyingSprout",x, y, player)



    if load_map == 'stage1_0':
        enemy=Monster("WalkingSprout", 80, 280, player)
        for _ in range(2):
            x = randint(600, 800)
            enemy=Monster("WalkingSprout", x, 280, player)
        for _ in range(4):
            x = randint(800, 1000)
            enemy=Monster("WalkingSprout", x, 320, player)

    elif load_map == 'stage1_1':
        for _ in range(5):
            x = randint(400, 800)
            enemy=Monster("WalkingSprout", x, 300, player)

    elif load_map == 'stage1_2':
        for _ in range(5):
            x = randint(400, 800)
            enemy=Monster("FlyingSprout", x, 500, player)

    elif load_map == 'stage1_3':
        pass

    elif load_map == 'stage1_boss':
        boss1_0 = Boss("Boss1_main", 1280//2, 1500, player)
        boss1_1 = Boss("Boss1_hand_R", 1280//2, 1500, player)
        boss1_2 = Boss("Boss1_hand_L", 1280//2, 1500, player)