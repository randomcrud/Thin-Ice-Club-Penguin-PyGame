import pygame
import time

import math
import gym
from gym import spaces, logger
import numpy as np


# Structure to be followed by the custom environment class: (i think this is called a wrapper?)
# class thin_ice_custom(gym.Env):
#   def __init__(self):
#     # Initialize the environment class
#     self.action_space = ...
#     self.observation_space = ...

#   def step(self, action):
#     # Take an action in the environment and return the next state, reward, done, info

#   def reset(self):
#     # Reset the environment to an initial state

#   def render(self):
#     # visualization

#   def close(self):

UNIT = 40 # PIXELS
HEIGHT = 15 # GRID HEIGHT
WIDTH = 18 # GRID WIDTH
SQUARE_SIZE = 20


player = pygame.image.load("thin_ice_rl/thin_ice_rl/envs/Textures/Player.png")
water = pygame.image.load("thin_ice_rl/thin_ice_rl/envs/Textures/Water.png")
empty_square = pygame.image.load("thin_ice_rl/thin_ice_rl/envs/Textures/EmptySquare.png")
finish_square = pygame.image.load("thin_ice_rl/thin_ice_rl/envs/Textures/FinishSquare.png")
wall = pygame.image.load("thin_ice_rl/thin_ice_rl/envs/Textures/Wall.png")
double_ice = pygame.image.load("thin_ice_rl/thin_ice_rl/envs/Textures/DoubleIce.png")
score_screen = pygame.image.load("thin_ice_rl/thin_ice_rl/envs/Textures/score_screen.png")
ice = pygame.image.load("thin_ice_rl/thin_ice_rl/envs/Textures/ice.png")


class ThinIceCustom(gym.Env):
    def __init__(self):
        super(ThinIceCustom, self).__init__()
        self.action_space = spaces.Discrete(4) # up, down, left and right
        
        self.observation_space = spaces.Box(low = 0, high = 1, shape = (HEIGHT, WIDTH), dtype = np.int32)
        
        self.reset()
        
    def load_level(self):
        level_names = ["level1", "level2", "level3", "level4", "level5", "level6", "level7", "level8", "level9"]
        m = list(map(lambda x: list(x), open("thin_ice_rl/thin_ice_rl/envs/Levels/" + level_names[self.level_i] + ".txt", "r").read().splitlines()))
        self.grid = m
        val_xy = open("thin_ice_rl/thin_ice_rl/envs/Levels/" + level_names[self.level_i] + ".txt", "r").read().splitlines()[15].split(" ")
        self.start_pos = (int(val_xy[0]) * SQUARE_SIZE, int(val_xy[1]) * SQUARE_SIZE)

    def reset(self):
        self.level_i = 0
        self.load_level()
        self.pos_x , self.pos_y = self.start_pos
        return self.get_observation()
    
    def get_observation(self):
        max_length = max(len(row) for row in self.grid)
        uniform_grid = [row + [0] * (max_length - len(row)) for row in self.grid]  # Pad shorter rows with zeros
        return np.array(uniform_grid)
    
    def step(self, action):
        if action == 0:  # up
            new_pos = (self.pos_x, self.pos_y - SQUARE_SIZE)
        elif action == 1:  # down
            new_pos = (self.pos_x, self.pos_y + SQUARE_SIZE)
        elif action == 2:  # left
            new_pos = (self.pos_x - SQUARE_SIZE, self.pos_y)
        elif action == 3:  # right
            new_pos = (self.pos_x + SQUARE_SIZE, self.pos_y)

        # Check for collisions and update the position
        if self.is_valid_move(new_pos):
            self.pos_x, self.pos_y = new_pos

        # Check for rewards or penalties
        reward, done = self.check_reward()
        return self.get_observation(), reward, done, {}
    
    def is_valid_move(self, pos):
        x, y = pos
        if 0 <= x < WIDTH * SQUARE_SIZE and 0 <= y < HEIGHT * SQUARE_SIZE:
            grid_x = x // SQUARE_SIZE
            grid_y = y // SQUARE_SIZE
            return self.grid[grid_y][grid_x] != "4"  # Not a wall
        return False
    
    def check_reward(self):
        grid_x = self.pos_x // SQUARE_SIZE
        grid_y = self.pos_y // SQUARE_SIZE
        if self.grid[grid_y][grid_x] == "1":  # Water
            return -1, True  # Penalty and done
        elif self.grid[grid_y][grid_x] == "3":  # Finish
            return 1, True  # Reward and done
        return 0, False  # No reward and not done


    def render(self, mode='human'):
        fundo.fill((230, 253, 255))  # Background color
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.grid[y][x] == "0":
                    fundo.blit(empty_square, (x * SQUARE_SIZE, y * SQUARE_SIZE))
                elif self.grid[y][x] == "1":
                    fundo.blit(water, (x * SQUARE_SIZE, y * SQUARE_SIZE))
                elif self.grid[y][x] == "2":
                    fundo.blit(ice, (x * SQUARE_SIZE, y * SQUARE_SIZE))
                elif self.grid[y][x] == "3":
                    fundo.blit(finish_square, (x * SQUARE_SIZE, y * SQUARE_SIZE))
                elif self.grid[y][x] == "4":
                    fundo.blit(wall, (x * SQUARE_SIZE, y * SQUARE_SIZE))
                elif self.grid[y][x] == "5":
                    fundo.blit(double_ice, (x * SQUARE_SIZE, y * SQUARE_SIZE))

        # Draw the player
        fundo.blit(player, (self.pos_x, self.pos_y))
        pygame.display.flip()  # Update the display


        
class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self):
        return self.action_space.sample()  # Randomly select an action     
    
    
if __name__ == "__main__":
    pygame.init()
    fundo = pygame.display.set_mode((WIDTH * SQUARE_SIZE, HEIGHT * SQUARE_SIZE))
    pygame.display.set_caption("Thin Ice Game")

    env = ThinIceCustom()
    agent = RandomAgent(env.action_space)

    done = False
    state = env.reset()

    while not done:
        action = agent.act()  # Get action from the agent
        next_state, reward, done, _ = env.step(action)  # Take action in the environment
        env.render()  # Render the environment

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.quit()  
    
        
        
"""
level_names = ["level1","level2","level3","level4","level5","level6","level7","level8","level9"]
level_i = 0
m = list(map(lambda x:list(x),open("Levels/"+level_names[level_i]+".txt","r").read().splitlines()))


SQUARE_SIZE = 20
VALUES_XY = open("Levels/"+level_names[level_i]+".txt","r").read().splitlines()[15].split(" ")
X_BEGIN = int(VALUES_XY[0])*SQUARE_SIZE
Y_BEGIN = int(VALUES_XY[1])*SQUARE_SIZE


branco=(230,253,255)
preto=(0,0,0)
vermelho=(255,0,0)
verde=(0,255,0)
azul=(0,0,255)
azulesp = (155, 244, 249)

pygame.init()

largura=380
altura=330
tamanho = 20
pos_x= X_BEGIN
pos_y= Y_BEGIN

pygame.mixer.music.load("Sounds/GameMusic.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.65)

fundo = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Gelo Fino")

player = pygame.image.load("Textures/Player.png")
water = pygame.image.load("Textures/Water.png")
empty_square = pygame.image.load("Textures/EmptySquare.png")
finish_square = pygame.image.load("Textures/FinishSquare.png")
wall = pygame.image.load("Textures/Wall.png")
double_ice = pygame.image.load("Textures/DoubleIce.png")
score_screen = pygame.image.load("Textures/score_screen.png")

ice = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
ice.fill(branco)

pygame.font.init()
font = pygame.font.Font("Fonts/Pixeled.ttf",9)

score = 0
score_aux = 0
lifes = 3


sair = False
while not sair:
    for event in pygame.event.get():
        
        if event.type==pygame.QUIT:
            sair = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                
                if m[int(pos_y/SQUARE_SIZE)][int((pos_x-SQUARE_SIZE)/SQUARE_SIZE)]!="4":
                    
                    if m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]=="2": 
                        m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)] = "1"
                        score_aux+=1
                        score+=1
                    else:
                        m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]="2"
                        
                    pos_x-=SQUARE_SIZE
                    
            elif event.key == pygame.K_RIGHT:
                
                if m[int(pos_y/SQUARE_SIZE)][int((pos_x+SQUARE_SIZE)/SQUARE_SIZE)]!="4":
                    
                    if m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]=="2": 
                        m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)] = "1"
                        score_aux+=1
                        score+=1
                    else:
                        m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]="2"
                        
                    pos_x+=SQUARE_SIZE
                    
            elif event.key == pygame.K_UP:
                
                if m[int((pos_y-SQUARE_SIZE)/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]!="4":
                    
                    if m[int((pos_y)/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]=="2": 
                        m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)] = "1"
                        score_aux+=1
                        score+=1
                    else:
                        m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]="2"
                        
                    pos_y-=SQUARE_SIZE
                    
            elif event.key == pygame.K_DOWN:
                
                if m[int((pos_y+SQUARE_SIZE)/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]!="4":
                    
                    if m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]=="2": 
                        m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)] = "1"
                        score_aux+=1
                        score+=1
                    else:
                        m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]="2"
                        
                    pos_y+=SQUARE_SIZE

            elif event.key == pygame.K_ESCAPE:
                sair=True

    
    for y in range(0,15):
        for x in range(0,19):
            if m[y][x]=="0":
                fundo.blit(empty_square,(x*SQUARE_SIZE,y*SQUARE_SIZE))
            elif m[y][x]=="1":
                fundo.blit(water,(x*SQUARE_SIZE,y*SQUARE_SIZE))
            elif m[y][x]=="2":
                fundo.blit(ice,(x*SQUARE_SIZE,y*SQUARE_SIZE))
            elif m[y][x]=="3":
                fundo.blit(finish_square,(x*SQUARE_SIZE,y*SQUARE_SIZE))
            elif m[y][x]=="4":
                fundo.blit(wall,(x*SQUARE_SIZE,y*SQUARE_SIZE))
            elif m[y][x]=="5":
                fundo.blit(double_ice,(x*SQUARE_SIZE,y*SQUARE_SIZE))
                
    fundo.blit(score_screen,(0,300))
    fundo.blit(font.render( "SCORE: "+str(score) ,1,azul ),(285,300))
    fundo.blit(font.render( "x"+str(lifes) ,1,preto ),(32,300))

    if m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)] in ["1","3"]:
        
        if m[int(pos_y/SQUARE_SIZE)][int(pos_x/SQUARE_SIZE)]=="1":

            lifes-=1
            score -= score_aux
            score_aux = 0

            if lifes==-1:

                pygame.mixer.music.play(-1)
                
                lifes=3
                level_i = 0
                
                VALUES_XY = open("Levels/"+level_names[level_i]+".txt","r").read().splitlines()[15].split(" ")
                m = list(map(lambda x:list(x),open("Levels/"+level_names[level_i]+".txt","r").read().splitlines()))
                
                X_BEGIN = int(VALUES_XY[0])*SQUARE_SIZE
                Y_BEGIN = int(VALUES_XY[1])*SQUARE_SIZE
                
                pos_x= X_BEGIN
                pos_y= Y_BEGIN
    
            else:
                
                m = list(map(lambda x:list(x),open("Levels/"+level_names[level_i]+".txt","r").read().splitlines()))
                pos_x= X_BEGIN
                pos_y= Y_BEGIN
            
        else:

            score_aux = 0
            level_i+=1
            m = list(map(lambda x:list(x),open("Levels/"+level_names[level_i]+".txt","r").read().splitlines()))
            
            VALUES_XY = open("Levels/"+level_names[level_i]+".txt","r").read().splitlines()[15].split(" ")
            X_BEGIN = int(VALUES_XY[0])*SQUARE_SIZE
            Y_BEGIN = int(VALUES_XY[1])*SQUARE_SIZE
            pos_x= X_BEGIN
            pos_y= Y_BEGIN
            
        
                
    else:
        fundo.blit(player,(pos_x,pos_y))
        pygame.display.update()

    

pygame.quit()
"""
