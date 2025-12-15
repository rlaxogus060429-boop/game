from tkinter import *

root=Tk()
lobby_canvas=Canvas(root, width = "1280", height = "720", bg="gray")
canvas = Canvas(root, width= "1280", height= "720", bg="#8ec9de")

global can_go
can_go = False

g = 1.5

# 키 입력 상태
'''
    이동:
        w매달리기/올라가기, s않기/내려가기, a왼쪽이동, d오른쪽이동, space점프, shift_l대시

    공격:
        j근접공격, k원거리공격, i스킬1사용, o스킬2사용, l스킬3사용

    특수:(활성화 시 사용 가능)
        공중+j원베기, 공중+space활강, 공중+k흩뿌리기, s+j포효, s+k뿌리 창 던지기, shift_l+j대쉬찌르기,

    시스템:
        m지도, tab지도, e상호작용, b가방, u아이템사용, escape메뉴

'''


key_states = {
            'w': False, 's': False, 'a': False, 'd': False, 'space': False, 'shift_l': False,
            'j': False, 'k': False, 'i': False, 'o': False, 'l': False,
            'm': False, 'tab': False, 'e': False, 'b': False,'u': False, 'escape': False
        }

img_path = "./"

font_path = r"./font/온글잎 의연체.ttf"
