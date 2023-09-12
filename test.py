import pygame
import math
import pymunk
from pygame import mixer
import random
pygame.init()
import sys
from math import atan2, degrees, pi
# Constants
WIDTH, HEIGHT = 800, 600
MENU_FONT = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the main window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Start Menu")

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def start_menu(End):
    running = True

    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        # Start button clicked, you can start your game here
                        running = False
                    elif exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
        except:pass
                        
                            


        # Clear the screen
        screen.fill(WHITE)
        if End:
            font = pygame.font.Font('freesansbold.ttf', 70)
            text = font.render( f'GAME OVER ' , True, (255, 0, 0))
            screen.blit(text, (200, 0))
            
        
        # Draw start button
        start_button_rect = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(screen, BLACK, start_button_rect)
        draw_text("Start Game", MENU_FONT, WHITE, screen, 400, 225)

        # Draw exit button
        exit_button_rect = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(screen, BLACK, exit_button_rect)
        draw_text("Exit", MENU_FONT, WHITE, screen, 400, 325)

        pygame.display.update()

# Run the start menu
#


def main():
    space=pymunk.Space()
    for shapes in space.shapes:
        space.remove(shapes)
    for bodies in space.bodies:
        space.remove(bodies)
    
    
    space.gravity=(100,00)
    static_lines = [
            pymunk.Segment(space.static_body, (00, 780.0), (780, 780), 0.0),
            pymunk.Segment(space.static_body, (780, 780), (780, 0), 0.0),
            pymunk.Segment(space.static_body, (780, 0), (0, 0), 0.0),
            pymunk.Segment(space.static_body, (0, 0), (0, 780), 0.0)
        ]
    for l in static_lines:
            l.friction = 0.5
            l.color = pygame.color.THECOLORS['blue']
            
    space.add(*static_lines)
    





    # Set up the display
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Rotating and Moving Player")

    # Initialize variables
    Player_rotation = 0.0  # Initial angle of rotation (in radians)
    speed = 0  # Speed of movement

    # Load player image
    Player_image = pygame.image.load("myplayer.png") # Replace "player.png" with your image path

    Player_image=pygame.transform.scale(Player_image, (722/2.5, 400/2.5))  # Adjust player size as needed
    Player_image=pygame.transform.rotate(Player_image,-0)
    PLAYER = pymunk.Body(mass=100, moment=100, body_type=pymunk.Body.DYNAMIC)
    player_shape = pymunk.Circle(radius=30,body=PLAYER)  # Reduced radius value for better visualization
    player_shape.friction = 1  # Adjusted friction value
    player_shape.elasticity = 1  # Adjusted elasticity value
    player_shape.position = 200,200
    player_shape.body = PLAYER
    space.add(PLAYER, player_shape)


    BulletImage=pygame.image.load("bullet.png")
    EnemyImage=pygame.image.load("MY ENEMY.png")

    EnemyImage=pygame.transform.scale(EnemyImage , (722/4, 400/4)) 

    def collisionfinder(enemy_pos,bullet_pos,distance=30):
        if abs(enemy_pos[0]-bullet_pos[0])<distance and abs(enemy_pos[1]-bullet_pos[1])<distance:
            return True
        return False


    class Bullet:
        
        def __init__(self,position,rotation,space) -> None:
            self.speed=4
            self.body=pymunk.Body(mass=1, moment=1, body_type=pymunk.Body.DYNAMIC)
            self.shape = pymunk.Circle(radius=10,body=self.body)  # Reduced radius value for better visualization    
            self.shape.friction = 1  # Adjusted friction value
            self.shape.elasticity = 1  # Adjusted elasticity value
            self.shape.position = position
            self.shape.body = self.body
            self.body.velocity=self.speed*math.cos(rotation),self.speed*math.sin(rotation)
            self.rotation=rotation
            space.add(self.body,self.shape)



        def draw_bullet(self,screen):
            
            rotated_image = pygame.transform.rotate(BulletImage, math.degrees(self.rotation) + 90)
            rotated_rect = rotated_image.get_rect(center=player_shape.position)
            screen.blit(rotated_image, rotated_rect.topleft)



    class Enemy:
            def __init__(self,position,rotation,space) -> None:
                self.player_pos=position
                self.speed=4
                self.body=pymunk.Body(mass=10, moment=0, body_type=pymunk.Body.DYNAMIC)
                self.shape = pymunk.Circle(radius=30,body=self.body)  # Reduced radius value for better visualization    
                self.shape.friction = 1  # Adjusted friction value
                self.shape.elasticity = 1  # Adjusted elasticity value
                self.shape.position = random.randint(0,800),random.randint(0,800)
                self.shape.body = self.body
                #self.angle=rotation
                space.add(self.body,self.shape)
                
                
            def find_angle(self):
                dx = self.player_pos[0]- self.shape.position[0]
                dy = self.player_pos[1] - self.shape.position[1]
                rads = atan2(-dy,dx)
                rads %= 2*pi
                self.degs = degrees(rads)

            def find_velocity(self,player_shape):
                
                self.player_pos = player_shape.position
                self.find_angle()
                
                #self.angle=math.atan2(player_shape.position[1]-self.shape.position[1],player_shape.position[0]-self.shape.position[0])
                self.body.velocity=self.speed*math.cos(self.degs),self.speed*math.sin(self.degs)
                
                
            
            def draw_enemy(self,screen):
                rotated_image = pygame.transform.rotate(EnemyImage, math.degrees(self.degs/100) + 0*90+0*180)
                rotated_rect = rotated_image.get_rect(center=self.shape.position)
                screen.blit(rotated_image, rotated_rect.topleft)
                
        
    
        #Bullet_objects.append([Bullet,Bullet_shape])
        #Bullets.append([Bullet_shape.position,Bullet.velocity,rotation])
        #screen.blit(rotated_image, rotated_rect.topleft)

    
        #Bullet.velocity=speed*math.cos(rotation),speed*math.sin(rotation)
        #rotated_image = pygame.transform.rotate(BulletImage, math.degrees(rotation) + 90)
        #rotated_rect = rotated_image.get_rect(center=player_shape.position)
        

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    keys_pressed = {}


    #OBJECT HOLDERS and parameters 
    Bullets=[]
    Bullet_objects=[]

    Enemies_objects=[]

    number_of_enemies=3

    Score=0
    Lives=40

    while running:
        End=False

        
        
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys_pressed[event.key] = True

            
            if event.type == pygame.KEYUP:
                keys_pressed[event.key] = False
        
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                Bullet_objects.append(Bullet(position=player_shape.position,rotation=Player_rotation,space=space))
                mixer.music.load("9mm-pistol-shoot-short-reverb-7152.mp3")
                mixer.music.play(loops=0)            
        
        
        

        speed=   -(keys_pressed.get(pygame.K_s, False) - keys_pressed.get(pygame.K_w, False))*10
        keys = pygame.key.get_pressed()
        
        # Rotate the player
        if keys[pygame.K_a]:
            Player_rotation += 0.1  # Adjust the rotation speed as needed
        if keys[pygame.K_d]:
            Player_rotation -= 0.1  # Adjust the rotation speed as needed

        # Calculate velocity components
        velocityX = -speed * math.cos(Player_rotation)
        velocityY = speed * math.sin(Player_rotation)

        # Update the position of the player
        
        
        
        
            
        for line in static_lines:
                body = line.body

                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = round(pv1.x), round((pv1.y))
                p2 = round(pv2.x), round((pv2.y))
                pygame.draw.lines(screen, pygame.Color("lightgray"), False, [p1, p2], 2)

        
         
        
         
         
            
        if player_shape.position[0]+velocityX>780 or player_shape.position[0]+velocityX<0:
            velocityX=0
        if player_shape.position[1]+velocityY>780 or player_shape.position[1]+velocityY<0:
            velocityY=0
        
        #if player_shape.position[0] < 500 or player_shape.position[0]==player_shape.position[1] :
        player_shape.position= player_shape.position[0]+ velocityX,player_shape.position[1] + velocityY

        #if player_shape.position[1] < 500 or player_shape.position[0]==player_shape.position[1]:
        


        # Draw the player
        for bullet in Bullet_objects:
            #print((bullet.shape.position),(bullet.body.velocity[0]))
            bullet.shape.position=bullet.shape.position[0]-bullet.body.velocity[0],bullet.shape.position[1]+bullet.body.velocity[1]
            #print(bullet.shape.position)#,player_shape.position)
            #bullet.draw_bullet(screen)
            #screen.blit(BulletImage, bullet.shape.position)
            rotated_image = pygame.transform.rotate(BulletImage, math.degrees(bullet.rotation) + 90)
            rotated_rect = rotated_image.get_rect(center=bullet.shape.position)
            
            
            
            screen.blit(rotated_image, rotated_rect.topleft)
        
        while len(Enemies_objects)<number_of_enemies:
            Enemies_objects.append(Enemy(player_shape.position,Player_rotation,space))
        
        
        for enemy in Enemies_objects:
            enemy.find_velocity(player_shape)
            enemy.shape.position=enemy.shape.position[0]-enemy.body.velocity[0],enemy.shape.position[1]+enemy.body.velocity[1]
            for bullet in Bullet_objects:
                if collisionfinder(bullet.shape.position,enemy.shape.position):
                    space.remove(bullet.body,bullet.shape)
                    Bullet_objects.remove(bullet)
                    Enemies_objects.remove(enemy)
                    space.remove(enemy.body,enemy.shape)
                    Score+=1
                    break
            
            if collisionfinder(enemy.shape.position,player_shape.position):
                try:
                    space.remove(enemy.body,enemy.shape)
                    Enemies_objects.remove(enemy)
                    Lives-=1
                    mixer.music.load("male_hurt7-48124.mp3")
                    mixer.music.play(loops=0)
                    
                    if Lives==0:
                        mixer.music.load("male-scream-in-fear-123079.mp3")
                        mixer.music.play(loops=0)
                        
                        return True
                        running=False
                    break
                except:pass
            
            enemy.draw_enemy(screen)
            
        #SCORE TEXt    
            
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render( f'Lives = {Lives}  , Score={Score}' , True, (255, 255, 255))
        screen.blit(text, (00, 0))
        
        #DRAW BOX AROUND SCORE
        pygame.draw.lines(screen, pygame.Color("lightgray"), False, [(0,0),(400,0),(400,50),(0,50)], 2)
        
        
        
        
        
        
        rotated_image = pygame.transform.rotate(Player_image, math.degrees(Player_rotation) + 90)
        rotated_rect = rotated_image.get_rect(center=player_shape.position)
        screen.blit(rotated_image, rotated_rect.topleft)
        pygame.display.flip()

        #print(player_shape.position[0],player_shape.position[0])
        #player_shape.position = player_shape.position[0], player_shape.w
        clock.tick(60)



start_menu(End=False)
while True: 
    start_menu(End=main())
    #print(End)
pygame.quit()

