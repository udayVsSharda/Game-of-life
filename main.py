import pygame  
import sys
import numpy as np
 
pygame.init()
 
#Screen Res setup
videoInfo = pygame.display.Info()
res_x = videoInfo.current_w  
res_y = videoInfo.current_h
 
#Color
WHITE = (255, 255, 255)
BG_COLOR = (247, 213, 239)
MINT_GREEN = (250, 249, 246)
 
#Misc Global Variables
blockSize = 40
currentState = "mainmenu"
 
 
 
#main() called at the end
def main() -> None:
    #font setup
    pygame.font.init() 

    #error handling implemented after finding out that you can't upload .ttf files on moodle. so backup 
    error = False
    try:
        monogram = pygame.font.Font("assets/monogram-extended.ttf",40)
    except FileNotFoundError:
        monogram = pygame.font.SysFont("arial",40)
        error = True

    #Game state setup
    display = pygame.display.set_mode((res_x,res_y))    
    clock = pygame.time.Clock()
    pygame.display.set_caption('Game of Life')
   
    #visual asset loading
    background = pygame.image.load("assets/Background.png")
    background = pygame.transform.scale(background, (res_x,res_y))
 
    background_blank =  pygame.image.load("assets/Interface.png")
    background_blank = pygame.transform.scale(background_blank, (res_x,res_y))
   
    background_help = pygame.image.load("assets/Rules interface.png")
    background_help = pygame.transform.scale(background_help,(res_x,res_y))
 
    exit = monogram.render("Exit",False,WHITE)
    exit_rect = exit.get_rect(center= (res_x*0.85, res_y*0.85))
 
    #non-visual asset create
    grid = np.array([[0]*(int(res_y*0.8)//blockSize)]*(int(res_x*0.8)//blockSize),dtype=int)
    new_grid = np.copy(grid)
    
    currentState = "mainMenu"  
    is_running = False  
   
 
    #Game Loop    
    while True:
        #gameplay/menu fps
        if is_running:
            clock.tick(10)
        else:
            clock.tick(144)
 
       #Game state - Visual  
        if currentState == "mainMenu":          
            display.blit(background,(0,0))            
            mainoptions = mainOptions(display,monogram)
            display.blit(exit,exit_rect)    

            if error:
                error_txt = monogram.render("!!!!!ERROR!!!!!!\n ADD THE FONT FILE\n Check mail",False,(255,0,0))
                error_rect = error_txt.get_rect(center= (res_x*0.5, res_y*0.75))
                display.blit(error_txt,error_rect) 
       
        elif currentState == "play":
            
            display.blit(background_blank,(0,0))  
            if is_running:
                for i in range(0,grid.shape[0]):
                    for j in range(0,grid.shape[1]):
                        new_grid[i,j] = 1 if check_alive( grid, (i,j)) else 0
 
                draw_grid( display, new_grid)
                grid = np.copy(new_grid)
            else:
                draw_grid(display, grid)  
           
        elif currentState == "credits":
            currentState = creditsRun(display,monogram,background_blank)
           
        elif currentState == "help":
            display.blit(background_help,(0,0))                
     
 
        pygame.display.update()    
 
 
        #inputs
        for event in pygame.event.get():
            #common events
            if event.type == pygame.QUIT:                    
                pygame.quit()
                sys.exit()          
           
            #Game state - Control
            if currentState == "mainMenu":
 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()      
                    if mainoptions["Play"].collidepoint(mouse_pos):
                        currentState = "play"
                    elif mainoptions["Credits"].collidepoint(mouse_pos):
                        currentState = "credits"
                    elif mainoptions["Help"].collidepoint(mouse_pos):
                        currentState = "help"
                    elif exit_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
 
            elif currentState == "play" :
 
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        is_running = not is_running                
                    elif event.key == pygame.K_ESCAPE:
                        currentState = "mainMenu"
                        is_running = False
                        grid = np.zeros(grid.shape)
 
                elif not is_running:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                     
                        if(res_x*0.89 > int(mouse_pos[0]) >= res_x*0.1) and (res_y*0.89 > int(mouse_pos[1]) >= res_y*0.1):
                           
                            grid_x = int(mouse_pos[0] - (res_x*0.1))// blockSize
                            grid_y = int(mouse_pos[1] - (res_y*0.1))// blockSize
 
                            grid[grid_x,grid_y] =  1 - grid[grid_x,grid_y]
           
            elif currentState == "help":
 
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        currentState = "mainMenu"
           
def mainOptions(screen: pygame.Surface ,font : pygame.font.Font) -> dict:
 
    mainoptions_txt = ["Play","Credits","Help"]
    mainoptions = {}
    i=0
 
    for txt in mainoptions_txt:
        text = font.render(txt,False,WHITE)
        text_rect = text.get_rect(center=(int(res_x/2), (int(res_y/2)-10) + (30*i) ))
        mainoptions[txt] = text_rect
        screen.blit(text, text_rect)
        i += 1
             
    return mainoptions
 
def creditsetup(screen: pygame.Surface ,font : pygame.font.Font) -> list:
    
    
    credit_txt = [  "          ",
                    "Theophile",
                    "          ",
                    "Uday",
                    "          ",
                    "Maya",
                    "          ",          
                    "Leo-Paul",
                    "          ",
                    "Erwane",
                   "          ",
                    "Max"
            ]
 
    screen_rect = screen.get_rect()
    credits = []
 
    i=0
   
    for credit in credit_txt:
       
        text = font.render(credit,False,WHITE)
        text_rect = text.get_rect(center= (res_x/2, screen_rect.bottom + (30*i) ))
        credits.append((text,text_rect))
        i += 1
   
    return credits    
 
def creditsRun(screen: pygame.Surface ,font : pygame.font.Font,bg: pygame.Surface):
 
    credits = creditsetup(screen,font)
    pygame.mixer.init()
    gol_sfx = pygame.mixer.Sound("assets/golsong.mp3")
    gol_sfx.play()

    while True:
 
        screen.blit(bg,(0,0))
        con = False
 
        for event in pygame.event.get():
           
           if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    gol_sfx.stop()
                    pygame.mixer.quit()
                    return "mainMenu"                
        for credit in credits:
            credit[1].move_ip(0,-1)
            screen.blit(credit[0],credit[1])
 
        pygame.display.flip()

    
 
   
def check_alive(grid: np.array, index: tuple) -> bool:
 
    alive_neighbour = 0
 
    for i in grid[index[0]-1:index[0]+2]:
        for j in i[index[1]-1:index[1]+2]:
            alive_neighbour += j
 
    self_alive = grid[index[0],index[1]]
    alive_neighbour -= self_alive
   
    if alive_neighbour < 2 or alive_neighbour > 3:
        return False
    elif 2 <= alive_neighbour <= 3:
        if self_alive == 1:
            return True
        elif self_alive == 0 and alive_neighbour == 3:
            return True
        else:
            return False
           
def draw_grid(display: pygame.surface, grid: np.array) -> None:
    # Draw squares
    for i in range(0,grid.shape[0]):
        for j in range(0,grid.shape[1]):
 
            if  grid[i,j] == 1:
                rect = pygame.Rect((res_x*0.1)+i*blockSize,(res_y*0.1)+j*blockSize,blockSize-1,blockSize-1)
                pygame.draw.rect(display,(213, 247, 221),rect)
               
            elif grid[i,j] == 0:
                rect = pygame.Rect((res_x*0.1)+blockSize*20,(res_y*0.1)+blockSize*20,blockSize-1,blockSize-1)
                pygame.draw.rect(display,BG_COLOR,rect)        
 
 
 
main()