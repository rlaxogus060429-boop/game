from container import *
from map_container import *
from tkinter import *
import PIL.Image
import PIL.ImageTk
from hitboxes import Hitbox

import gc

def makeMap(show_map, load_map):

    if load_map == 'stage0_0':
        load_map_list = stage0_0
    elif load_map == 'stage0_1':
        load_map_list = stage0_1
    elif load_map == 'stage0_2':
        load_map_list = stage0_2
    elif load_map == 'stage0_3':
        load_map_list = stage0_3

    elif load_map == 'stage1_0':
        load_map_list = stage1_0
    elif load_map == 'stage1_1':
        load_map_list = stage1_1
    elif load_map == 'stage1_2':
        load_map_list = stage1_2
    elif load_map == 'stage1_3':
        load_map_list = stage1_3

    elif load_map == 'stage1_boss':
        load_map_list = stage1_boss
    
    if load_map_list[0][0] == 'theme1':
        fileName = 'theme1'
    elif load_map_list[0][0] == 'theme2':
        fileName = 'theme2'
    elif load_map_list[0][0] == 'theme3':
        fileName = 'theme3'
    elif load_map_list[0][0] == 'theme4':
        fileName = 'theme4'
    elif load_map_list[0][0] == 'theme5':
        fileName = 'theme5'
    else:
        fileName = 'theme0'

    for row_nb, row in enumerate(load_map_list):
        for col_nb, tile in enumerate(row):
            if tile == 00:
                show_map[row_nb][col_nb] = 00
            else:
                if col_nb == 0 and row_nb == 0:
                    show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName)
                else:
                    if tile == 'entry':
                        if load_map == 'stage0_0':
                            show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName, 'stage0_1') # '이어지는 맵'
                        elif load_map == 'stage0_1':
                            show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName, 'stage0_2')
                        elif load_map == 'stage0_2':
                            show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName, 'stage0_3')
                        elif load_map == 'stage0_3':
                            show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName, 'stage1_0')

                        elif load_map == 'stage1_0':
                            show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName, 'stage1_1')
                        elif load_map == 'stage1_1':
                            show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName, 'stage1_2')
                        elif load_map == 'stage1_2':
                            show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName, 'stage1_3')
                        elif load_map == 'stage1_3':
                            show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName, 'stage1_boss')
                    else:
                        show_map[row_nb][col_nb] = Worldbox((col_nb-1)*40, row_nb*40, tile, fileName)
                        

class Worldbox:
    box_list = []
    tk_image_refs = []  # 모든 PhotoImage 참조를 저장

    def __init__(self, x, y, name, theme, wto_go=None):
        self.x = x
        self.y = y
        self.name = name
        self.file = theme
        self.wto_go = wto_go
        self.tk_image = None

    @staticmethod
    def update_map(maps):
        # 기존 이미지 및 히트박스 삭제
        if len(Worldbox.box_list) >= 1:
            for old_m in Worldbox.box_list:
                canvas.delete(old_m.image)
                if hasattr(old_m, 'hitbox'):
                    if old_m.hitbox.hitbox_rect is not None:
                        canvas.delete(old_m.hitbox.hitbox_rect)
                        old_m.hitbox.hitbox_rect = None
            Worldbox.box_list.clear()

        # 기존 PhotoImage 객체 참조 해제
        for img in Worldbox.tk_image_refs:
            del img
        Worldbox.tk_image_refs = []

        gc.collect()

        # 새 맵 생성
        
        for row_nb, row in enumerate(maps):
            for col_nb, m in enumerate(row):
                if m == 00:
                    continue
                if m.name not in ['theme0', 'theme1', 'theme2', 'theme3', 'theme4', 'theme5']:
                    raw_image = PIL.Image.open(f"{img_path}tile/{m.file}/{m.name}.png")
                else:
                    raw_image = PIL.Image.open(f"{img_path}tile/{m.file}/wall_l.png")
                resize_image = raw_image.resize((40,40), PIL.Image.NEAREST)
                m.tk_image = PIL.ImageTk.PhotoImage(resize_image)
                Worldbox.tk_image_refs.append(m.tk_image)  # 참조 유지
                m.image = canvas.create_image(m.x, m.y, image=m.tk_image, anchor=NW, tags="box")

                if m.name == 'spike':
                    m.hitbox = Hitbox(m.x, m.y+10, 40, 30)
                else:
                    if m.name in ['un_wall_l', 'un_wall_r', 'un_middle', 'decoration1', 'decoration2', 'decoration3']:
                        continue
                    m.hitbox = Hitbox(m.x, m.y, 40, 40)

                if hasattr(m, 'hitbox'):
                    pass
                    #m.hitbox.draw_hitbox() # 디버그용

                Worldbox.box_list.append(m)