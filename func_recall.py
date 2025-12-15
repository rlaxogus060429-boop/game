from player import player
from enemy import Enemy, Boss
from collision import *
from bullet import Bullet
from gameUI import show_gameclear

after_ids = None

def func_recall():
    global after_ids
    if Enemy.enemy_list != []:
        player.can_go = False
    else:
        player.can_go = True

    for enemy in Enemy.enemy_list:
        enemy.enemy_img_update()
        enemy.update_enemy_position()
        enemy.layer_up()
        enemy.isDead()
        Collision.map_collision(enemy)
        Collision.hitbox_collision(player, enemy)
        if enemy.__class__.__name__ == 'Boss':
            enemy.attack_cycle()
        if enemy.x < -(enemy.img_size/2 - enemy.hitsize_x/2): 
            enemy.set_position(-(enemy.img_size/2 - enemy.hitsize_x/2), enemy.y)
        if enemy.x > 1280 - (enemy.img_size/2 - enemy.hitsize_x/2) - enemy.hitsize_x:
            enemy.set_position(1280 - (enemy.img_size/2 - enemy.hitsize_x/2) - enemy.hitsize_x, enemy.y)
        if enemy.y < -enemy.hitsize_y//2:
            enemy.set_position(enemy.x, -enemy.hitsize_y//2)
        if enemy.name == "FlyingSprout" and enemy.y > 720 - enemy.hitsize_y:
            enemy.set_postion(enemy.x, 720 - enemy.hitsize_y)
        if enemy.y > 720 + enemy.hitsize_y*5:
            enemy.health = -1 # 화면 아래로 떨어지면 즉시 처치
            if enemy.__class__.__name__ == 'Boss':
                if Boss.boss_health <= 0:
                    Boss.boss_health = -10
                    show_gameclear()

    for bullet in Bullet.bullet_list:
        bullet.tracking()
        bullet.move()
        bullet.layer_up()
        Collision.hitbox_collision(player, bullet)
        if bullet.destroy:
            bullet.destroy_self()
    if player.health > 0:
        player.create_dash_trail()
        player.update_cd()
        player.player_img_update()
        player.layer_up()
        player.update_player_position()
        Collision.map_collision(player)
    else:
        player.isDead()
    
    if player.x < -17: # 0 - player.size//4
        player.set_position(-17, player.y)
    if player.x > 1228: # 1280 - (player.size//4 + player.size//2)
        player.set_position(1228, player.y)
    if player.y < -35: # 0 - player.size//2
         player.set_position(player.x, -35)
    if player.y > 860: # 720 + player.size * 2
        if player.where == 'stage0_0':
            player.set_position(x0_0, y0_0)
        if player.where == 'stage0_1':
            player.set_position(x0_1, y0_1)
        if player.where == 'stage0_2':
            player.set_position(x0_2, y0_2)
        if player.where == 'stage0_3':
            player.set_position(x0_3, y0_3)

        if player.where == 'stage1_0':
            player.set_position(x1_0, y1_0)
        if player.where == 'stage1_1':
            player.set_position(x1_1, y1_1)
        if player.where == 'stage1_2':
            player.set_position(x1_2, y1_2)
        if player.where == 'stage1_3':
            player.set_position(x1_3, y1_3)
        if player.where == 'stage1_boss':
            player.set_position(x1_b, y1_b)

    canvas.tag_raise("UI")

    if after_ids is not None:
        canvas.after_cancel(after_ids)
    after_ids = canvas.after(20, func_recall)