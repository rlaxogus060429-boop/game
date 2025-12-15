## 메인 
# hasattr(오브젝트, '속성명') -> 객체에 해당 속성이 있는지 확인

# 파이썬 내장 라이브러리 임포트
import os
import sys
import ctypes
from random import randint

# tkinter 임포트
from tkinter import *
import music

# PIL 임포트
import PIL.Image
import PIL.ImageTk

# 개인 모듈 임포트
# 플레이어 체력, 돈, 대쉬 등 UI임포트
from gameUI import *

# 행동 객체 임포트
from player import *
from enemy import *
from spawnEnemy import *

# 히트박스 및 충돌 임포트
from hitboxes import *
from collision import *

# 맵 임포트
from makeMap import *
from map_container import *

from func_recall import func_recall
# 기타 
from container import *


def install_font(font_path):
    # 폰트 경로 절대 경로로 변환
    abs_path = os.path.abspath(font_path)

    # 경로 확인
    if not os.path.exists(abs_path):
        print("X 폰트 파일이 존재하지 않습니다:", abs_path) # 디버그용 출력문
        return False
    
    # 폰트 이름이 한글 <<< 유니코드 버전 함수 사용
    addfont = ctypes.windll.gdi32.AddFontResourceW
    result = addfont(abs_path)
    
    # 시스템에 폰트 변경 알림
    if result != 0:
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x001D, 0, 0)
        print("O 폰트 설치 성공:", abs_path) # 디버그용 출력문
        return True
    else:
        print("X 폰트 설치 실패:", abs_path) # 디버그용 출력문
        return False

def on_key_press(event):
    # 키가 눌렸을 때 상태를 True로 변경

    k = event.keysym.lower()
    c = event.char.lower()
    if k in key_states:
        key_states[k] = True
        # 공격 입력 처리
        if k == 'j' and player.can_air_atk:
            if player.atk_cd > 0:
                return

            if player.unlock[2] == 1:
                player.state[6] = 0

            if player.state[5] == 0 and player.combo_cd <= 0:
                player.state[5] = 1

            elif player.state[5] == 0 and player.combo_cd > 0:
                player.state[5] = player.state[7]

            elif player.combo_cd > 0 and 1 <= player.state[5] < 3:
                player.state[5] += 1
            
            player.frame_count = 0
            player.atk_cd = player.atk_timer
            player.combo_cd = player.combo_ok

        if k == 'space':
            if player.unlock[1] == 1 and player.state[3] == -1:
                player.state[3] = -2
                
            if player.unlock[2] == 1:
                if player.unlock[1] == 0 and player.state[3] == 3 and player.state[6] == 0:
                    player.dy = 0
                    player.state[6] = 1 # 점프 남은거 없음


                elif player.unlock[1] == 1 and player.state[3] == 3 and player.state[6] == 0:
                    player.dy = 0
                    player.state[6] = 1

        
    elif c in key_states:
        key_states[c] = True


def on_key_release(event):
    # 키가 떼졌을 때 상태를 False로 변경 및 정지 상태로 변경
    k = event.keysym.lower()
    c = event.char.lower()
    if k in key_states:
        key_states[k] = False
        if k not in ['j'] and k not in ['shift_l']:
            player.state[0] = 0
        
    elif c in key_states:
        key_states[c] = False
        if k not in ['j']:
            player.state[0] = 0

def start_game(event):
    lobby_canvas.destroy()
    canvas.pack()
    music.music_play('main')

    # 맵 및 적 스폰 설정
    go_map = 'stage1_2'
    spawn_enemy(go_map)
    makeMap(show_map, go_map)
    Worldbox.update_map(show_map)

    #키보드 이벤트 바인딩
    root.bind_all('<KeyPress>', on_key_press)
    root.bind_all('<KeyRelease>', on_key_release, player)

    # 플레이어 함수 호출
    func_recall()
    
    game_ui.update_ui()


# 메인 루프
if __name__ == "__main__":
    # 폰트 설치 후 진행
    if install_font(font_path):
        
        root.geometry("1280x720")
        root.resizable(False, False)
        root.title("Project E")

        lobby_canvas.pack()
        raw_alpha = PIL.Image.open(f"{img_path}ui/alpha.png").convert("RGBA")
        alpha_resize = raw_alpha.resize((500, 250), PIL.Image.BILINEAR)
        alpha_tk = PIL.ImageTk.PhotoImage(alpha_resize)

        start_text = lobby_canvas.create_text(640, 500, text="게 임  시 작", font=("온글잎 의연체", 40), fill="black")
        info_text = lobby_canvas.create_text(640, 570, text="설 명", font=("온글잎 의연체", 30), fill="black")
        exit_text = lobby_canvas.create_text(640, 630, text="나 가 기", font=("온글잎 의연체", 35), fill="black")

    
        def no_bind(): # 바인딩 해제
            lobby_canvas.tag_unbind(start_text, "<Button-1>")
            lobby_canvas.tag_unbind(start_text, "<Enter>")
            lobby_canvas.tag_unbind(start_text, "<Leave>")

            lobby_canvas.itemconfig(info_text, fill="black")
            lobby_canvas.tag_unbind(info_text, "<Button-1>")
            lobby_canvas.tag_unbind(info_text, "<Enter>")
            lobby_canvas.tag_unbind(info_text, "<Leave>")

            lobby_canvas.itemconfig(exit_text, fill="black")
            lobby_canvas.tag_unbind(exit_text, "<Button-1>")
            lobby_canvas.tag_unbind(exit_text, "<Enter>")
            lobby_canvas.tag_unbind(exit_text, "<Leave>")


        def yes_bind(): # 바인딩 (재)설정
            lobby_canvas.tag_bind(start_text, "<Button-1>", start_game)
            lobby_canvas.tag_bind(start_text, "<Enter>", lambda e: lobby_canvas.itemconfig(start_text, fill="white"))
            lobby_canvas.tag_bind(start_text, "<Leave>", lambda e: lobby_canvas.itemconfig(start_text, fill="black"))

            lobby_canvas.tag_bind(info_text, "<Button-1>", info)
            lobby_canvas.tag_bind(info_text, "<Enter>", lambda e: lobby_canvas.itemconfig(info_text, fill="white"))
            lobby_canvas.tag_bind(info_text, "<Leave>", lambda e: lobby_canvas.itemconfig(info_text, fill="black"))

            lobby_canvas.tag_bind(exit_text, "<Button-1>", exit_game)
            lobby_canvas.tag_bind(exit_text, "<Enter>", lambda e: lobby_canvas.itemconfig(exit_text, fill="white"))
            lobby_canvas.tag_bind(exit_text, "<Leave>", lambda e: lobby_canvas.itemconfig(exit_text, fill="black"))

        def info(event):
            no_bind()
            bg_img = lobby_canvas.create_image(400, 200, image=alpha_tk, anchor=NW)
            info_text_title = lobby_canvas.create_text(650, 240, text="게임 설명", font=("온글잎 의연체", 40), fill="white")
            info_text1 = lobby_canvas.create_text(520, 350, text="    A (좌) D (우)\n SPACE_BAR (점프) \n   SHIFT_L (대시) \n       J (공격)", font=("온글잎 의연체", 28), fill="white")
            info_text2 = lobby_canvas.create_text(750, 350, text="    적을 무찌르고\n       앞으로\n     나아가세요    ", font=("온글잎 의연체", 28), fill="white")
            x_text = lobby_canvas.create_text(860, 240, text="X", font=("온글잎 의연체", 30), fill="white")

            lobby_canvas.tag_bind(x_text, "<Button-1>", lambda x: yes_bind() or lobby_canvas.delete(bg_img) or lobby_canvas.delete(info_text_title) or lobby_canvas.delete(info_text1) or lobby_canvas.delete(info_text2) or lobby_canvas.delete(x_text))        
            lobby_canvas.tag_bind(x_text, "<Enter>", lambda e: lobby_canvas.itemconfig(x_text, fill="red"))
            lobby_canvas.tag_bind(x_text, "<Leave>", lambda e: lobby_canvas.itemconfig(x_text, fill="white"))

        def exit_game(event): # 게임 종료 확인
            no_bind()
            bg_img = lobby_canvas.create_image(400, 200, image=alpha_tk, anchor=NW)
            real_exit_text = lobby_canvas.create_text(650, 300, text="정말로 종료하시겠습니까?", font=("온글잎 의연체", 40), fill="white")
            yes_text = lobby_canvas.create_text(550, 400, text="예", font=("온글잎 의연체", 30), fill="white")
            no_text = lobby_canvas.create_text(750, 400, text="아니오", font=("온글잎 의연체", 30), fill="white")

            lobby_canvas.tag_bind(yes_text, "<Button-1>", lambda yes: sys.exit())
            lobby_canvas.tag_bind(yes_text, "<Enter>", lambda e: lobby_canvas.itemconfig(yes_text, fill="black"))
            lobby_canvas.tag_bind(yes_text, "<Leave>", lambda e: lobby_canvas.itemconfig(yes_text, fill="white"))
        
            lobby_canvas.tag_bind(no_text, "<Button-1>", lambda no: yes_bind() or lobby_canvas.delete(bg_img) or lobby_canvas.delete(real_exit_text) or lobby_canvas.delete(yes_text) or lobby_canvas.delete(no_text))        
            lobby_canvas.tag_bind(no_text, "<Enter>", lambda e: lobby_canvas.itemconfig(no_text, fill="black"))
            lobby_canvas.tag_bind(no_text, "<Leave>", lambda e: lobby_canvas.itemconfig(no_text, fill="white"))

        # 바인딩 설정
        yes_bind()

        def on_Close():
            canvas.destroy()
            root.destroy()
            ctypes.windll.gdi32.RemoveFontResourceW(os.path.abspath(font_path))
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001D, 0, 0)
            sys.exit()
            

        # 메인 루프 시작
        root.protocol("WM_DELETE_WINDOW", on_Close)
        root.mainloop()

    else: # 폰트 설치 실패 시 종료
        sys.exit()
        os._exit()