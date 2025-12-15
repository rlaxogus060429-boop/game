from tkinter import *
import PIL.Image
import PIL.ImageTk
from container import img_path, canvas
from hitboxes import Atk_Hitbox
import math

class Bullet:
    bullet_list = []
    def __init__(self, x, y, size, name="bullet", owner=None, target=None, target_x=0, target_y=0, damage=1, speed=1, istracking=False):
        self.x = x
        self.y = y
        self.img_size = size

        self.name = name

        self.owner = owner
        self.target = target
        if self.target is None:
            self.target = [target_x, target_y]
        self.damage = damage
        self.speed = speed
        self.istracking = istracking

        self.destroy = False

        self.raw_image = PIL.Image.open(f"{img_path}/bullet/{self.name}.png")
        self.resize_image = self.raw_image.resize((self.img_size, self.img_size), PIL.Image.NEAREST)
        self.tk_image = PIL.ImageTk.PhotoImage(self.resize_image)

        self.image = canvas.create_image(self.x, self.y, image=self.tk_image, anchor=NW, tags = "bullet")

        self.hitbox = Atk_Hitbox(self.x, self.y, self.img_size, self.img_size, damage=self.damage)

        Bullet.bullet_list.append(self)
        if target is not None:
            self.vx = (self.target.x + 35) - (self.x + self.img_size//2)
            self.vy = (self.target.y + 35) - (self.y + self.img_size//2)
        else:
            self.vx = (self.target[0]) - (self.x + self.img_size//2)
            self.vy = (self.target[1]) - (self.y + self.img_size//2)

        self.vect = math.hypot(self.vx, self.vy)
        self.dist = math.sqrt(self.vx**2 + self.vy**2)
        if self.vect > 1e-6:
            self.dx = self.vx / self.vect
            self.dy = self.vy / self.vect

        self.alpha = 0.1

    def tracking(self):
        if self.istracking:
            self.vx = (self.target.x + 35) - (self.x + self.img_size//2)
            self.vy = (self.target.y + 35) - (self.y + self.img_size//2)

            self.vect = math.hypot(self.vx, self.vy)
            if self.vect > 1e-6:
                self.new_dx = self.vx / self.vect
                self.new_dy = self.vy / self.vect
                self.dx = (1 - self.alpha) * self.dx + self.alpha * self.new_dx
                self.dy = (1 - self.alpha) * self.dy + self.alpha * self.new_dy

            self.dist = math.sqrt(self.vx**2 + self.vy**2)
            if self.dist <= min(self.img_size * 3, 140):
                self.istracking = False

    def move(self):
        self.x += self.dx*self.speed
        self.y += self.dy*self.speed
        canvas.move(self.image, self.dx*self.speed, self.dy*self.speed)
        self.hitbox.move(self.dx*self.speed, self.dy*self.speed)

        #self.hitbox.draw_hitbox() # 디버그용

    def destroy_self(self):
        if self.hitbox.hitbox_rect is not None:
            canvas.delete(self.hitbox.hitbox_rect)
            self.hitbox.hitbox_rect = None
            # 리스트에서 제거
        if self in Bullet.bullet_list:
            Bullet.bullet_list.remove(self)
        canvas.delete(self.image)

    def layer_up(self):
        canvas.tag_raise(self.image)