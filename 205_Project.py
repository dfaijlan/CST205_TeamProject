import pygame
from pygame import mixer
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('Track01.mp3')
pygame.mixer.music.set_endevent(pygame.USEREVENT)
pygame.event.set_allowed(pygame.USEREVENT)
pygame.mixer.music.play()
pygame.event.wait()