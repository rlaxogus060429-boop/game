from tkinter import *
from container import canvas

boss_hp_bar = None
boss_hp_bar_bg = None
boss_hp_bar_width = 400
boss_hp_bar_height = 30
boss_hp_bar_x = 440
boss_hp_bar_y = 30
boss_hp_anim_val = 0
boss_hp_anim_max = 60
boss_hp_anim_state = "idle"  # "idle", "fill", "full", "drain", "hide"
boss_hp_target_val = 0

def create_boss_hp_bar(canvas):
    global boss_hp_bar, boss_hp_bar_bg, boss_hp_anim_val, boss_hp_anim_state, boss_hp_target_val
    boss_hp_anim_val = 0
    boss_hp_target_val = 0
    boss_hp_anim_state = "fill"
    if boss_hp_bar_bg is None:
        boss_hp_bar_bg = canvas.create_rectangle(
            boss_hp_bar_x, boss_hp_bar_y,
            boss_hp_bar_x + boss_hp_bar_width, boss_hp_bar_y + boss_hp_bar_height,
            fill='#242424', outline='black'
        )
    if boss_hp_bar is None:
        boss_hp_bar = canvas.create_rectangle(
            boss_hp_bar_x, boss_hp_bar_y,
            boss_hp_bar_x, boss_hp_bar_y + boss_hp_bar_height,
            fill='red', outline=''
        )
    animate_boss_hp_bar(canvas)

def animate_boss_hp_bar(canvas):
        global boss_hp_anim_val, boss_hp_anim_state, boss_hp_target_val
        if boss_hp_anim_state == "fill":
            if boss_hp_anim_val < boss_hp_anim_max:
                boss_hp_anim_val += 0.5
                update_boss_hp_bar(canvas, boss_hp_anim_val)
                canvas.after(16, animate_boss_hp_bar, canvas)
            else:
                boss_hp_anim_val = boss_hp_anim_max
                boss_hp_target_val = boss_hp_anim_max
                boss_hp_anim_state = "full"
                update_boss_hp_bar(canvas, boss_hp_anim_val)
        elif boss_hp_anim_state == "full" or boss_hp_anim_state == "idle":
            # 체력바가 목표 체력까지 부드럽게 이동
            if boss_hp_anim_val > boss_hp_target_val:
                boss_hp_anim_val -= max(1, int((boss_hp_anim_val - boss_hp_target_val) * 0.1))
                if boss_hp_anim_val < boss_hp_target_val:
                    boss_hp_anim_val = boss_hp_target_val
                update_boss_hp_bar(canvas, boss_hp_anim_val)
                canvas.after(16, animate_boss_hp_bar, canvas)
            elif boss_hp_anim_val < boss_hp_target_val:
                boss_hp_anim_val += max(1, int((boss_hp_target_val - boss_hp_anim_val) * 0.1))
                if boss_hp_anim_val > boss_hp_target_val:
                    boss_hp_anim_val = boss_hp_target_val
                update_boss_hp_bar(canvas, boss_hp_anim_val)
                canvas.after(16, animate_boss_hp_bar, canvas)

def update_boss_hp_bar(canvas, hp):
    fill_width = int(boss_hp_bar_width * (hp / boss_hp_anim_max))
    canvas.coords(
        boss_hp_bar,
        boss_hp_bar_x, boss_hp_bar_y,
        boss_hp_bar_x + fill_width, boss_hp_bar_y + boss_hp_bar_height
    )

def set_boss_hp_bar(canvas, hp):
    global boss_hp_target_val, boss_hp_anim_state
    hp = max(0, min(hp, boss_hp_anim_max))
    boss_hp_target_val = hp
    if boss_hp_anim_state in ("full", "idle"):
        animate_boss_hp_bar(canvas)

def hide_boss_hp_bar(canvas, what):
    global boss_hp_bar, boss_hp_bar_bg
    if what == 1:
        if boss_hp_bar is not None:
            canvas.delete(boss_hp_bar)
            boss_hp_bar = None
    elif what == 0:
        if boss_hp_bar_bg is not None:
            canvas.delete(boss_hp_bar_bg)
            boss_hp_bar_bg = None