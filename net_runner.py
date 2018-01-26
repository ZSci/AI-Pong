
import pygame
from pygame.locals import *
from sys import exit
import random
import time
import win32api as wapi
import win32con as wcon
import math
import numpy as np

from neu_net_v2 import model

model.load('model_v4.tfl')
dir_map = {0 : 0x26, 1 : 0x28, 2 : None}

pygame.init()

screen=pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption("Pong Pong!")

#Creating 2 bars, a ball and background. 
back = pygame.Surface((640,480))
background = back.convert()
background.fill((0,0,0))

bar = pygame.Surface((10,50))

bar1 = bar.convert()
bar1.fill((0,0,255))

bar2 = bar.convert()
bar2.fill((255,0,0))

circ_sur = pygame.Surface((15,15))
circ = pygame.draw.circle(circ_sur,(0,255,0),(7,7),7)
circle = circ_sur.convert()

circle.set_colorkey((0,0,0))

# some definitions
bar1_x, bar2_x = 10. , 620.
bar1_y, bar2_y = 215. , 215.

circle_x, circle_y = 307.5, 232.5

bar1_move, bar2_move = 0. , 0.

speed_x = random.randrange(230, 270)
speed_y = math.sqrt(125000 - math.pow(speed_x, 2))
speed_circ = 250.

bar1_score, bar2_score = 0,0

#clock and font objects
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri",40)

mod_out = [[0, 0, 0]]
t2 = time.time()

while True:
	

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

		if event.type == KEYDOWN:
			if event.key == K_UP:
				bar1_move = -ai_speed

			elif event.key == K_DOWN:
				bar1_move = ai_speed

		elif event.type == KEYUP:
			if event.key == K_UP:
				bar1_move = 0.

			elif event.key == K_DOWN:
				bar1_move = 0.

	if np.argmax(mod_out[0]) != 2:
		wapi.keybd_event(dir_map[np.argmax(mod_out[0])], 0, wcon.KEYEVENTF_KEYUP)


	mod_out = model.predict([[bar1_y, circle_x, circle_y, speed_x, speed_y]])

	print(dir_map[np.argmax(mod_out[0])], '\n')
	print(time.time()-t2)
	t2=time.time()

	if np.argmax(mod_out[0]) != 2:
		wapi.keybd_event(dir_map[np.argmax(mod_out[0])], 0)

	print(time.time()-t2, '\n')

	score1 = font.render(str(bar1_score), True,(255,255,255))
	score2 = font.render(str(bar2_score), True,(255,255,255))

	screen.blit(background,(0,0))
	frame = pygame.draw.rect(screen,(255,255,255),Rect((5,5),(630,470)),2)
	middle_line = pygame.draw.aaline(screen,(255,255,255),(330,5),(330,475))
	screen.blit(bar1,(bar1_x,bar1_y))
	screen.blit(bar2,(bar2_x,bar2_y))
	screen.blit(circle,(circle_x,circle_y))
	screen.blit(score1,(250.,210.))
	screen.blit(score2,(380.,210.))

	bar1_y += bar1_move
	
# movement of circle
	time_passed = clock.tick(30)
	time_sec = time_passed / 1000.0
	
	circle_x += speed_x * time_sec
	circle_y += speed_y * time_sec
	ai_speed = speed_circ * time_sec
#AI of the computer.
	if circle_x >= 250.:
		if not bar2_y == circle_y + 7.5:
			if bar2_y < circle_y + 7.5:
				bar2_y += ai_speed
			if  bar2_y > circle_y - 42.5:
				bar2_y -= ai_speed
		else:
			bar2_y == circle_y + 7.5
	
	if bar1_y >= 420.: bar1_y = 420.
	elif bar1_y <= 10. : bar1_y = 10.
	if bar2_y >= 420.: bar2_y = 420.
	elif bar2_y <= 10.: bar2_y = 10.


#since i don't know anything about collision, ball hitting bars goes like this.
	if circle_x <= bar1_x + 10.:
		if circle_y >= bar1_y - 7.5 and circle_y <= bar1_y + 42.5:
			circle_x = 20.
			speed_x = -speed_x

	if circle_x >= bar2_x - 15.:
		if circle_y >= bar2_y - 7.5 and circle_y <= bar2_y + 42.5:
			circle_x = 605.
			speed_x = -speed_x

	if circle_x < 5.:
		bar2_score += 1
		circle_x = random.randrange(300, 340)
		circle_y = random.randrange(210, 260)
		speed_x = random.randrange(230, 270) * random.choice([1, -1])
		speed_y = math.sqrt(125000 - math.pow(speed_x, 2)) * random.choice([1, -1])

	elif circle_x > 620.:
		bar1_score += 1
		circle_x = random.randrange(300, 340)
		circle_y = random.randrange(210, 260)
		speed_x = random.randrange(230, 270) * random.choice([1, -1])
		speed_y = math.sqrt(125000 - math.pow(speed_x, 2)) * random.choice([1, -1])

	if circle_y <= 10.:
		speed_y = -speed_y
		circle_y = 10.
	elif circle_y >= 457.5:
		speed_y = -speed_y
		circle_y = 457.5

	print(bar1_score, bar2_score)
	pygame.display.update()
