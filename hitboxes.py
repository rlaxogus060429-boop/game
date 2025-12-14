## 히트박스 클래스 및 함수들

from tkinter import *
from container import *

class Hitbox:
    def __init__(self, x, y, width, height):
        self.x = x  # 좌상단 x
        self.y = y  # 좌상단 y

        self.width = width
        self.height = height

        self.hitbox_rect = None  # 캔버스에 그려진 히트박스 객체 ID(시각적효과)

    def get_rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def coords(self, x, y):
        self.x = x
        self.y = y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw_hitbox(self, color='blue'): # 디버그용 함수
        # 기존 히트박스 사각형이 있으면 삭제
        if self.hitbox_rect is not None:
            canvas.delete(self.hitbox_rect)
        # 히트박스 좌표 계산
        x1 = self.x; y1 = self.y; x2 = self.x + self.width; y2 = self.y + self.height
        # 히트박스 사각형 그리기 (빨간색, 투명도 없음)
        self.hitbox_rect = canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=2)

class Atk_Hitbox(Hitbox): 
    def __init__(self, x, y, width, height, damage=1):
        super().__init__(x, y, width, height)
        self.damage = damage