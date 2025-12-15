import pygame

def music_play(music):
    bgm_path = "./bgm/"
    pygame.init()
    pygame.mixer.music.load(f"{bgm_path}{music}.mp3") #Loading File Into Mixer
    pygame.mixer.music.play(-1) #Playing It In The Whole Device